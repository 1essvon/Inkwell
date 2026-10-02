#ifndef RepoRoot
  #define RepoRoot "."
#endif

[Setup]
AppId={{38C5F10C-49F6-481B-9C5A-27FA198D9A4A}
AppName=The Inkwell
AppVersion=1.0
DefaultDirName={autopf}\The Inkwell
DefaultGroupName=The Inkwell
UninstallDisplayName=The Inkwell
UninstallDisplayIcon={app}\TheInkwell.exe
OutputDir={#RepoRoot}\dist\windows
OutputBaseFilename=TheInkwellSetup
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
CloseApplications=yes
RestartApplications=no

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "{#RepoRoot}\dist\windows\TheInkwell\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\The Inkwell"; Filename: "{app}\TheInkwell.exe"; WorkingDir: "{app}"
Name: "{autodesktop}\The Inkwell"; Filename: "{app}\TheInkwell.exe"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\TheInkwell.exe"; Description: "Launch The Inkwell"; WorkingDir: "{app}"; Flags: postinstall nowait skipifsilent
