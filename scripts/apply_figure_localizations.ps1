param(
    [Parameter(Mandatory = $true)]
    [string]$SourceRoot
)

$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath($SourceRoot)
$pic = Join-Path $root 'mppics\pic.mp'
if (-not (Test-Path -LiteralPath $pic -PathType Leaf)) {
    throw "Missing MetaPost source: $pic"
}

$english = @'
label (btex bisector etex rotated angle(z.P), z.P+(0,6));
label (btex external etex rotated angle(-z.Q), z.Q+(6,0));
label (btex bisector etex rotated angle(-z.Q), z.Q-(5,0));
'@
$indonesian = @'
label (btex garis bagi etex rotated angle(z.P), z.P+(0,6));
label (btex luar etex rotated angle(-z.Q), z.Q+(6,0));
label (btex garis bagi etex rotated angle(-z.Q), z.Q-(5,0));
'@

$text = [IO.File]::ReadAllText($pic, [Text.Encoding]::UTF8)
$englishCount = ([regex]::Matches($text, [regex]::Escape($english))).Count
$indonesianCount = ([regex]::Matches($text, [regex]::Escape($indonesian))).Count

if ($englishCount -eq 1 -and $indonesianCount -eq 0) {
    $text = $text.Replace($english, $indonesian)
    [IO.File]::WriteAllText($pic, $text, [Text.UTF8Encoding]::new($false))
}
elseif ($englishCount -eq 0 -and $indonesianCount -eq 1) {
    # The live id-ID closure already carries the exact overlay.
}
else {
    throw "Unexpected pic-108 label surface: English=$englishCount Indonesian=$indonesianCount"
}

$hash = (Get-FileHash -LiteralPath $pic -Algorithm SHA256).Hash.ToLowerInvariant()
if ($hash -ne '567a0e33c5addabb995ce0d283984cba768606b0819a92a3ead5b83dc596cef1') {
    throw "Localized pic.mp hash mismatch: $hash"
}

Write-Output "FIGURE_LOCALIZATION=pic-108"
Write-Output "PIC_MP_SHA256=$hash"
