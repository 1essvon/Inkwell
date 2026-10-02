param(
    [string]$Python = "python",
    [switch]$CreateInstaller,
    [string]$InnoSetupCompiler = "ISCC.exe"
)

$ErrorActionPreference = "Stop"

$RepositoryRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$SpecPath = Join-Path $RepositoryRoot "TheInkwell.spec"
$BuildRequirements = Join-Path $RepositoryRoot "requirements-build-windows.txt"
$WorkPath = Join-Path $RepositoryRoot "build\windows"
$DistPath = Join-Path $RepositoryRoot "dist\windows"
$ApplicationPath = Join-Path $DistPath "TheInkwell\TheInkwell.exe"
$InstallerScript = Join-Path $RepositoryRoot "packaging\windows\TheInkwell.iss"
$InstallerPath = Join-Path $DistPath "TheInkwellSetup.exe"

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

    if ($CreateInstaller) {
        if (-not (Test-Path -LiteralPath $InstallerScript -PathType Leaf)) {
            throw "Inno Setup script was not found: $InstallerScript"
        }

        $CompilerCommand = Get-Command -Name $InnoSetupCompiler `
            -CommandType Application `
            -ErrorAction SilentlyContinue
        if (-not $CompilerCommand) {
            throw "Inno Setup compiler was not found. Install Inno Setup 6 or pass its ISCC.exe path with -InnoSetupCompiler."
        }

        & $CompilerCommand.Source "/DRepoRoot=$RepositoryRoot" $InstallerScript
        if ($LASTEXITCODE -ne 0) {
            throw "Inno Setup failed with exit code $LASTEXITCODE."
        }

        if (-not (Test-Path -LiteralPath $InstallerPath -PathType Leaf)) {
            throw "Installer build completed without the expected executable: $InstallerPath"
        }

        Write-Host "Windows installer created: $InstallerPath"
    }
}
catch {
    [Console]::Error.WriteLine("Windows build failed: {0}", $_.Exception.Message)
    exit 1
}
finally {
    Pop-Location
}
