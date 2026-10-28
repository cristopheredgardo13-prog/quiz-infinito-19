$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
Write-Host 'Conectar Quiz infinito con Gemini'
Write-Host 'Pega la clave de Google AI Studio. No se mostrara ni se guardara en archivos.'
$claveSegura = Read-Host 'Clave Gemini (pega y pulsa Enter)' -AsSecureString
$punteroClave = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($claveSegura)
try {
    $env:GEMINI_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($punteroClave)
    if ([string]::IsNullOrWhiteSpace($env:GEMINI_API_KEY)) { throw 'No pegaste una clave. Abre CONECTAR_IA.cmd para intentarlo otra vez.' }
    $env:GEMINI_API_KEY = $env:GEMINI_API_KEY.Trim()
    $env:PORT = '7861'
    Write-Host 'Abre http://localhost:7861. Esta ventana debe permanecer abierta.'
    & (Join-Path $PSScriptRoot 'iniciar.ps1')
} finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($punteroClave)
    Remove-Item Env:GEMINI_API_KEY -ErrorAction SilentlyContinue
    $claveSegura.Dispose()
}
