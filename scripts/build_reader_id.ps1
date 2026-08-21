param(
    [string]$SourceRoot,
    [Parameter(Mandatory = $true)]
    [string]$OutputRoot
)

$ErrorActionPreference = 'Stop'
if ([string]::IsNullOrWhiteSpace($SourceRoot)) {
    # Windows PowerShell can evaluate a param-block default before
    # $PSScriptRoot is populated when this script is launched with -File.
    $SourceRoot = Join-Path $PSScriptRoot '..\source\id-ID'
}
$source = [IO.Path]::GetFullPath($SourceRoot)
$output = [IO.Path]::GetFullPath($OutputRoot)

if (-not (Test-Path -LiteralPath (Join-Path $source 'all-lectures.tex') -PathType Leaf)) {
    throw "Missing source driver: $source"
}
if (Test-Path -LiteralPath $output) {
    throw "OutputRoot must not already exist: $output"
}
if (Test-Path -LiteralPath (Join-Path $source 'cover')) {
    throw 'The id-ID source closure must not contain the excluded cover directory.'
}

New-Item -ItemType Directory -Path $output | Out-Null
New-Item -ItemType Directory -Path (Join-Path $output 'mppics') | Out-Null
New-Item -ItemType Directory -Path (Join-Path $output 'pics') | Out-Null

Get-ChildItem -LiteralPath $source -File |
    Where-Object { $_.Extension -in @('.tex', '.sty', '.bib', '.md', '.txt') } |
    ForEach-Object { Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $output $_.Name) }
Get-ChildItem -LiteralPath (Join-Path $source 'mppics') -File -Filter '*.mp' |
    ForEach-Object { Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $output ('mppics\' + $_.Name)) }
Get-ChildItem -LiteralPath (Join-Path $source 'pics') -File -Filter '*.eps' |
    ForEach-Object { Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $output ('pics\' + $_.Name)) }

# The upstream wood-texture macro uses uniformdeviate for figures 287--289.
# MetaPost otherwise chooses a time-dependent seed, so independent builds can
# differ even when every source byte is identical.  Seed each driver explicitly
# in the disposable build closure; the upstream source overlay remains intact.
$metaPostRandomSeed = 2718
foreach ($driverName in @('pic.mp', 'pic-hints.mp')) {
    $driverPath = Join-Path $output ('mppics\' + $driverName)
    $driverText = [IO.File]::ReadAllText($driverPath, [Text.Encoding]::UTF8)
    [IO.File]::WriteAllText(
        $driverPath,
        "randomseed := $metaPostRandomSeed;`n" + $driverText,
        [Text.UTF8Encoding]::new($false)
    )
}

$env:SOURCE_DATE_EPOCH = '1766112130'
$env:FORCE_SOURCE_DATE = '1'

function Invoke-BuildCommand {
    param([string]$Name, [string]$WorkingDirectory, [scriptblock]$Command)
    Push-Location $WorkingDirectory
    try {
        & $Command *> (Join-Path $output ($Name + '.console.txt'))
        if ($LASTEXITCODE -ne 0) {
            throw "$Name failed with exit code $LASTEXITCODE"
        }
    }
    finally {
        Pop-Location
    }
}

Invoke-BuildCommand '01-mpost-pic' (Join-Path $output 'mppics') {
    mpost -interaction=nonstopmode -tex=latex pic.mp
}
Invoke-BuildCommand '02-mpost-hints' (Join-Path $output 'mppics') {
    mpost -interaction=nonstopmode -tex=latex pic-hints.mp
}

$epsNormalizer = Join-Path $PSScriptRoot 'normalize_eps_pdf.py'
if (-not (Test-Path -LiteralPath $epsNormalizer -PathType Leaf)) {
    throw "Missing EPS-PDF normalizer: $epsNormalizer"
}
$normalizedEps = @()
foreach ($epsFile in Get-ChildItem -LiteralPath (Join-Path $output 'pics') -File -Filter '*.eps') {
    $stem = [IO.Path]::GetFileNameWithoutExtension($epsFile.Name)
    $livePdf = Join-Path $output ('pics\' + $stem + '-live-conversion.pdf')
    $normalizedPdf = Join-Path $output ('pics\' + $stem + '-eps-converted-to.pdf')
    Invoke-BuildCommand ('03-epstopdf-' + $stem) $output {
        epstopdf "--outfile=$livePdf" $epsFile.FullName
    }
    Invoke-BuildCommand ('04-normalize-eps-pdf-' + $stem) $output {
        python $epsNormalizer --source-eps $epsFile.FullName --input-pdf $livePdf --output-pdf $normalizedPdf
    }
    Remove-Item -LiteralPath $livePdf
    $normalizedFile = Get-Item -LiteralPath $normalizedPdf
    $normalizedEps += [ordered]@{
        source = $epsFile.Name
        output = $normalizedFile.Name
        bytes = $normalizedFile.Length
        sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $normalizedPdf).Hash.ToLowerInvariant()
    }
}

# The driver inputs the index unconditionally.  Seed an empty generated index
# for the first pass; MakeIndex replaces it immediately afterward.
[IO.File]::WriteAllBytes((Join-Path $output 'all-lectures.ind'), [byte[]]@())

Invoke-BuildCommand '05-pdflatex-initial' $output {
    pdflatex -interaction=nonstopmode -halt-on-error all-lectures.tex
}
Invoke-BuildCommand '06-makeindex' $output { makeindex all-lectures }
Invoke-BuildCommand '07-biber' $output { biber all-lectures }
Invoke-BuildCommand '08-pdflatex' $output {
    pdflatex -interaction=nonstopmode -halt-on-error all-lectures.tex
}
Invoke-BuildCommand '09-makeindex' $output { makeindex all-lectures }
Invoke-BuildCommand '10-pdflatex' $output {
    pdflatex -interaction=nonstopmode -halt-on-error all-lectures.tex
}

$first = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $output 'all-lectures.pdf')).Hash.ToLowerInvariant()
Invoke-BuildCommand '11-pdflatex-reproducibility' $output {
    pdflatex -interaction=nonstopmode -halt-on-error all-lectures.tex
}
$second = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $output 'all-lectures.pdf')).Hash.ToLowerInvariant()
if ($first -ne $second) {
    throw "Non-reproducible final PDF: $first != $second"
}

$pdf = Get-Item -LiteralPath (Join-Path $output 'all-lectures.pdf')
[ordered]@{
    source_root = $source
    output_root = $output
    source_date_epoch = 1766112130
    metapost_random_seed = $metaPostRandomSeed
    normalized_eps_pdfs = $normalizedEps
    pdf_bytes = $pdf.Length
    pdf_sha256 = $second
} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $output 'BUILD_RECEIPT.json') -Encoding utf8NoBOM

Write-Output "PDF=$($pdf.FullName)"
Write-Output "BYTES=$($pdf.Length)"
Write-Output "SHA256=$second"
