param(
    [string]$Python = "python",
    [switch]$CreateInstaller,
    [string]$InnoSetupCompiler = "ISCC.exe"
)

$ErrorActionPreference = "Stop"

$RepositoryRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$VersionFile = Join-Path $RepositoryRoot "VERSION"
$VersionInfoFile = Join-Path ([System.IO.Path]::GetTempPath()) "TheInkwell-version-info-$PID.txt"
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
if (-not (Test-Path -LiteralPath $VersionFile -PathType Leaf)) {
    throw "Release version file was not found: $VersionFile"
}

$ReleaseVersion = (Get-Content -LiteralPath $VersionFile -Raw).Trim()
if ($ReleaseVersion -notmatch '^\d+\.\d+\.\d+$') {
    throw "Release version must use MAJOR.MINOR.PATCH format: $ReleaseVersion"
}
$VersionComponents = @($ReleaseVersion.Split('.') | ForEach-Object { [int]::Parse($_) })
if ($VersionComponents | Where-Object { $_ -gt 65535 }) {
    throw "Each release version component must be between 0 and 65535: $ReleaseVersion"
}

Push-Location $RepositoryRoot
$PreviousVersionInfoFile = $env:INKWELL_VERSION_INFO
try {
    $VersionCheck = "from importlib.metadata import version; assert version('PyInstaller') == '6.22.3'; assert version('pyinstaller-hooks-contrib') == '2026.7'"
    & $Python -c $VersionCheck
    if ($LASTEXITCODE -ne 0) {
        throw "Required build tools are missing or have the wrong versions. Install requirements.txt and requirements-build-windows.txt first."
    }

    $VersionTuple = "($($VersionComponents[0]), $($VersionComponents[1]), $($VersionComponents[2]), 0)"
    $VersionInfo = @'
VSVersionInfo(
  ffi=FixedFileInfo(filevers=__VERSION_TUPLE__, prodvers=__VERSION_TUPLE__),
  kids=[
    StringFileInfo([
      StringTable('040904B0', [
        StringStruct('CompanyName', 'The Inkwell'),
        StringStruct('FileDescription', 'The Inkwell'),
        StringStruct('FileVersion', '__VERSION__'),
        StringStruct('InternalName', 'TheInkwell'),
        StringStruct('OriginalFilename', 'TheInkwell.exe'),
        StringStruct('ProductName', 'The Inkwell'),
        StringStruct('ProductVersion', '__VERSION__'),
      ])
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
'@
    $VersionInfo = $VersionInfo.Replace("__VERSION_TUPLE__", $VersionTuple)
    $VersionInfo = $VersionInfo.Replace("__VERSION__", $ReleaseVersion)
    [System.IO.File]::WriteAllText(
        $VersionInfoFile,
        $VersionInfo,
        [System.Text.UTF8Encoding]::new($false)
    )
    $env:INKWELL_VERSION_INFO = $VersionInfoFile

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

        & $CompilerCommand.Source `
            "/DRepoRoot=$RepositoryRoot" `
            "/DAppVersion=$ReleaseVersion" `
            $InstallerScript
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
    if (Test-Path -LiteralPath $VersionInfoFile -PathType Leaf) {
        Remove-Item -LiteralPath $VersionInfoFile -Force
    }
    if ($null -eq $PreviousVersionInfoFile) {
        Remove-Item Env:INKWELL_VERSION_INFO -ErrorAction SilentlyContinue
    }
    else {
        $env:INKWELL_VERSION_INFO = $PreviousVersionInfoFile
    }
    Pop-Location
}
