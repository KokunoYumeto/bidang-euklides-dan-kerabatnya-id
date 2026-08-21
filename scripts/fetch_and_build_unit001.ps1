param(
    [Parameter(Mandatory = $true)]
    [string]$WorkRoot,
    [Parameter(Mandatory = $true)]
    [string]$OutputRoot
)

$ErrorActionPreference = 'Stop'
$commit = '0b0858e1e985f4c8dadbb6075ae9e095cd4a8981'
$archiveSha256 = 'ef6142598854078fe3d9777005b5aff49ee0d5c70b17acebce876398c8b71081'
$archiveUrl = "https://github.com/anton-petrunin/birkhoff/archive/$commit.zip"
$work = [IO.Path]::GetFullPath($WorkRoot)
$output = [IO.Path]::GetFullPath($OutputRoot)

if (Test-Path -LiteralPath $work) {
    throw "WorkRoot must not already exist: $work"
}
if (Test-Path -LiteralPath $output) {
    throw "OutputRoot must not already exist: $output"
}

New-Item -ItemType Directory -Path $work | Out-Null
$archive = Join-Path $work 'authority.zip'
Invoke-WebRequest -Uri $archiveUrl -OutFile $archive -MaximumRedirection 5
$observed = (Get-FileHash -Algorithm SHA256 -LiteralPath $archive).Hash.ToLowerInvariant()
if ($observed -ne $archiveSha256) {
    throw "Authority archive mismatch: $observed"
}

$expanded = Join-Path $work 'expanded'
Expand-Archive -LiteralPath $archive -DestinationPath $expanded
$source = Join-Path $expanded "birkhoff-$commit"
if (-not (Test-Path -LiteralPath (Join-Path $source 'all-lectures.tex') -PathType Leaf)) {
    throw "Expanded authority root is invalid: $source"
}

$cover = [IO.Path]::GetFullPath((Join-Path $source 'cover'))
$sourcePrefix = [IO.Path]::GetFullPath($source).TrimEnd('\') + '\'
if (-not $cover.StartsWith($sourcePrefix, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing unsafe cover path: $cover"
}
if (Test-Path -LiteralPath $cover) {
    Remove-Item -LiteralPath $cover -Recurse -Force
}

$overlay = Join-Path $PSScriptRoot '..\source\id-ID'
foreach ($name in @(
    'all-lectures.tex',
    'locale-id.tex',
    'title.tex',
    'intro.tex',
    'metric.tex',
    'hints.tex'
)) {
    $candidate = [IO.Path]::GetFullPath((Join-Path $overlay $name))
    if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) {
        throw "Missing overlay file: $candidate"
    }
    Copy-Item -LiteralPath $candidate -Destination (Join-Path $source $name)
}

& (Join-Path $PSScriptRoot 'build_reader_id.ps1') -SourceRoot $source -OutputRoot $output
if ($LASTEXITCODE -ne 0) {
    throw "Reader build failed with exit code $LASTEXITCODE"
}
