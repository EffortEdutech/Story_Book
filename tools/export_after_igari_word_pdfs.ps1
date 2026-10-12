$ErrorActionPreference = "Stop"

$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$manuscript = Join-Path $root "02_After_Igari\Manuscript"
$out = Join-Path $root "02_After_Igari\Gate\rendered_after_remediation"
New-Item -ItemType Directory -Force -Path $out | Out-Null

$files = @(
  "AFTER_IGARI_Chapter_01_The_Message.docx",
  "AFTER_IGARI_Chapter_04_Before_the_Door_Closes_REISSUED.docx",
  "AFTER_IGARI_Chapter_05_Takeoff.docx",
  "AFTER_IGARI_Chapter_06_Cruise.docx",
  "AFTER_IGARI_Chapter_07_Thirty_Five_Thousand_Feet.docx",
  "AFTER_IGARI_Chapter_08_Good_Night.docx",
  "AFTER_IGARI_Chapter_09_IGARI.docx"
)

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

try {
  foreach ($name in $files) {
    $src = Join-Path $manuscript $name
    $stem = [System.IO.Path]::GetFileNameWithoutExtension($name)
    $dir = Join-Path $out $stem
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    $pdf = Join-Path $dir "$stem.pdf"
    Write-Host "Exporting $name"
    $doc = $word.Documents.Open($src, $false, $true)
    try {
      $doc.ExportAsFixedFormat($pdf, 17)
    } finally {
      $doc.Close($false)
    }
  }
} finally {
  $word.Quit()
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
