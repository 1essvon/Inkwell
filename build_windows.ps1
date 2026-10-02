param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

$RepositoryRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$SpecPath = Join-Path $RepositoryRoot "TheInkwell.spec"
$BuildRequirements = Join-Path $RepositoryRoot "requirements-build-windows.txt"
$WorkPath = Join-Path $RepositoryRoot "build\windows"
$DistPath = Join-Path $RepositoryRoot "dist\windows"
$ApplicationPath = Join-Path $DistPath "TheInkwell\TheInkwell.exe"

if ($env:OS -ne "Windows_NT") {
    throw "Windows build must run on Windows; PyInstaller does not cross-compile."
}

if (-not (Test-Path -LiteralPath $SpecPath -PathType Leaf)) {
    throw "PyInstaller spec was not found: $SpecPath"
}
if (-not (Test-Path -LiteralPath $BuildRequirements -PathType Leaf)) {
    throw "Build dependency file was not found: $BuildRequirements"
}

Push-Location $RepositoryRoot
try {
    $VersionCheck = "from importlib.metadata import version; assert version('PyInstaller') == '6.22.3'; assert version('pyinstaller-hooks-contrib') == '2026.7'"
    & $Python -c $VersionCheck
    if ($LASTEXITCODE -ne 0) {
        throw "Required build tools are missing or have the wrong versions. Install requirements.txt and requirements-build-windows.txt first."
    }

    & $Python -m PyInstaller --noconfirm --clean `
        --distpath $DistPath `
        --workpath $WorkPath `
        $SpecPath
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller failed with exit code $LASTEXITCODE."
    }

    if (-not (Test-Path -LiteralPath $ApplicationPath -PathType Leaf)) {
        throw "Build completed without the expected executable: $ApplicationPath"
    }

    Write-Host "Windows application bundle created: $ApplicationPath"
}
catch {
    [Console]::Error.WriteLine("Windows build failed: {0}", $_.Exception.Message)
    exit 1
}
finally {
    Pop-Location
}
