param(
    [string]$SourceRoot = (Join-Path $PSScriptRoot '..\source\id-ID'),
    [Parameter(Mandatory = $true)]
    [string]$FullBuildRoot,
    [Parameter(Mandatory = $true)]
    [string]$OutputRoot
)

$ErrorActionPreference = 'Stop'
$source = [IO.Path]::GetFullPath($SourceRoot)
$fullBuild = [IO.Path]::GetFullPath($FullBuildRoot)
$output = [IO.Path]::GetFullPath($OutputRoot)

foreach ($required in @(
    (Join-Path $source 'hints.tex'),
    (Join-Path $source 'lectures.sty'),
    (Join-Path $source 'locale-id.tex'),
    (Join-Path $fullBuild 'all-lectures.aux')
)) {
    if (-not (Test-Path -LiteralPath $required -PathType Leaf)) {
        throw "Missing required input: $required"
    }
}
if (Test-Path -LiteralPath $output) {
    throw "OutputRoot must not already exist: $output"
}

New-Item -ItemType Directory -Path $output | Out-Null
Copy-Item -LiteralPath (Join-Path $source 'lectures.sty') -Destination $output
Copy-Item -LiteralPath (Join-Path $source 'locale-id.tex') -Destination $output
Copy-Item -LiteralPath (Join-Path $fullBuild 'all-lectures.aux') -Destination $output

$hints = [IO.File]::ReadAllText((Join-Path $source 'hints.tex'), [Text.Encoding]::UTF8)
$boundary = '%\subsection*{Chapter~\ref{chap:axioms}}'
$index = $hints.IndexOf($boundary, [StringComparison]::Ordinal)
if ($index -lt 0) {
    throw 'Chapter 2 hint boundary is missing.'
}
$body = $hints.Substring(0, $index) + "\spell{\end{multicols}}{}`n"
[IO.File]::WriteAllText(
    (Join-Path $output 'unit001-hints-body.tex'),
    $body,
    [Text.UTF8Encoding]::new($false)
)

$driver = @'
\documentclass[twoside]{book}
\usepackage{geometry}
\usepackage{lectures}
\input{locale-id.tex}
\usepackage{xr-hyper}
\externaldocument{all-lectures}
\hypersetup{
breaklinks=true,
pdftitle={Bidang Euklides dan Kerabatnya — Petunjuk Bab 1},
pdfauthor={Anton Petrunin}
}
\newcommand{\arxiv}[2]{#1}
\newcommand{\spell}[2]{#1}
\geometry{top=0.9in, bottom=0.9in,inner=0.55in, outer=0.45in, paperwidth=6in, paperheight=9in}
\begin{document}
{\footnotesize
\input{unit001-hints-body.tex}
}
\end{document}
'@
[IO.File]::WriteAllText(
    (Join-Path $output 'unit001-hints.tex'),
    $driver,
    [Text.UTF8Encoding]::new($false)
)

$env:SOURCE_DATE_EPOCH = '1766112130'
$env:FORCE_SOURCE_DATE = '1'

Push-Location $output
try {
    foreach ($pass in 1..2) {
        $console = Join-Path $output ("pdflatex-$pass.console.txt")
        & pdflatex -interaction=nonstopmode -halt-on-error unit001-hints.tex *> $console
        if ($LASTEXITCODE -ne 0) {
            throw "Hint build pass $pass failed with exit code $LASTEXITCODE"
        }
    }
}
finally {
    Pop-Location
}

$pdf = Get-Item -LiteralPath (Join-Path $output 'unit001-hints.pdf')
$hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $pdf.FullName).Hash.ToLowerInvariant()
[ordered]@{
    schema = 'o004-unit001-hints-build-v0'
    source_root = $source
    full_build_root = $fullBuild
    output_root = $output
    source_date_epoch = 1766112130
    chapter_2_suffix_excluded = $true
    pdf_bytes = $pdf.Length
    pdf_sha256 = $hash
} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $output 'BUILD_RECEIPT.json') -Encoding utf8NoBOM

Write-Output "PDF=$($pdf.FullName)"
Write-Output "BYTES=$($pdf.Length)"
Write-Output "SHA256=$hash"
