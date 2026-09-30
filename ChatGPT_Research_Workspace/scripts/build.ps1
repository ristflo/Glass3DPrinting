$ErrorActionPreference = 'Stop'
$researchRoot = Split-Path -Parent $PSScriptRoot
$env:TEMP = Join-Path $researchRoot 'scripts/tmp'
$env:TMP = $env:TEMP
$env:TECTONIC_CACHE_DIR = Join-Path $env:TEMP 'tectonic-cache'
$env:XDG_CACHE_HOME = $env:TECTONIC_CACHE_DIR
$env:LOCALAPPDATA = Join-Path $env:TEMP 'local-appdata'
$env:APPDATA = Join-Path $env:TEMP 'appdata'
$env:TEXMFVAR = Join-Path $env:TEMP 'texmf-var'
$env:TEXMFCONFIG = Join-Path $env:TEMP 'texmf-config'
$env:PYTHONIOENCODING = 'utf-8'
$env:FONTCONFIG_FILE = Join-Path $env:TEMP 'fonts.conf'
$fontCache = (Join-Path $env:TEMP 'fontconfig-cache').Replace('\','/')
"<?xml version='1.0'?><!DOCTYPE fontconfig SYSTEM 'fonts.dtd'><fontconfig><cachedir>$fontCache</cachedir></fontconfig>" | Set-Content -LiteralPath $env:FONTCONFIG_FILE -Encoding utf8
foreach ($p in @($env:TEMP,$env:TECTONIC_CACHE_DIR,$env:LOCALAPPDATA,$env:APPDATA,$env:TEXMFVAR,$env:TEXMFCONFIG)) {
    New-Item -ItemType Directory -Force -Path $p | Out-Null
}
$compiler = Join-Path $researchRoot 'scripts/tmp/tectonic/tectonic.exe'
Push-Location -LiteralPath (Join-Path $researchRoot 'latex')
try {
    if (Test-Path -LiteralPath $compiler) {
        & $compiler --outdir build --keep-logs --keep-intermediates main.tex 2>&1 | Tee-Object -FilePath (Join-Path $researchRoot 'artifacts/compile_output.txt')
    } elseif (Get-Command latexmk -ErrorAction SilentlyContinue) {
        latexmk -xelatex -outdir=build -halt-on-error main.tex 2>&1 | Tee-Object -FilePath (Join-Path $researchRoot 'artifacts/compile_output.txt')
    } else { throw 'Install Tectonic into scripts/tmp/tectonic or make latexmk with XeLaTeX available.' }
    if ($LASTEXITCODE -ne 0) { throw 'LaTeX compilation failed.' }
    Copy-Item -LiteralPath 'build/main.pdf' -Destination (Join-Path $researchRoot 'output/glass_3d_printing_sota_monograph.pdf')
} finally { Pop-Location }
