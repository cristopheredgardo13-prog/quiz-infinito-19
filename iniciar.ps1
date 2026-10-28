$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot
$runtime = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (Test-Path -LiteralPath $runtime) { $pythonApp = $runtime }
else {
    $pythonApp = (Get-Command python -ErrorAction SilentlyContinue).Source
    if (-not $pythonApp) { throw 'Instala Python 3.13 desde python.org, marca Add Python to PATH y vuelve a abrir este archivo.' }
}
$dep = Join-Path $PSScriptRoot '.dependencias'
$tmp = Join-Path $PSScriptRoot '.temporal'
New-Item -ItemType Directory -Force $dep,$tmp | Out-Null
$env:TEMP=$tmp
$env:TMP=$tmp
$env:PYTHONPATH=$dep
$marcaDependencias = Join-Path $dep 'requirements.sha256'
$hashRequisitos = (Get-FileHash -LiteralPath requirements.txt -Algorithm SHA256).Hash
$hashInstalado = if (Test-Path -LiteralPath $marcaDependencias) { (Get-Content -LiteralPath $marcaDependencias -Raw).Trim() } else { '' }
if ($hashInstalado -ne $hashRequisitos) {
    & $pythonApp -m pip install --upgrade --no-cache-dir --target $dep -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw 'No se pudieron instalar las dependencias. Revisa la conexión y vuelve a abrir INICIAR.cmd.' }
    Set-Content -LiteralPath $marcaDependencias -Value $hashRequisitos -Encoding ascii
}
if (-not $env:PORT) { $env:PORT = '7860' }
Write-Host "Abre http://localhost:$($env:PORT). Para salir pulsa Ctrl+C."
& $pythonApp main.py




