#define MyAppName "ULTRA FORCE"
#define MyAppPublisher "ULTRA FORCE"
#define MyAppExeName "ULTRA_FORCE.exe"
#define MyAppVersion GetEnv("RELEASE_VERSION")
#if MyAppVersion == ""
  #define MyAppVersion "dev"
#endif

[Setup]
AppId={{6D39D5B3-B3C4-4F15-BB63-8F4A7A2A1E25}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=dist
OutputBaseFilename=ULTRA_FORCE-windows-{#MyAppVersion}-setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible

[Files]
Source: "dist\ULTRA_FORCE\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
