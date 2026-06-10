; HuSuiBot - Inno Setup Installer Script
; 使用 Inno Setup Compiler 编译: https://jrsoftware.org/isdl.php

#define MyAppName "花碎机器人"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "花碎"
#define MyAppURL "https://github.com/242605129/HuSuiBot"
#define MyAppExeName "start_bot.bat"

[Setup]
AppId={{8E7E3F2A-1B2C-4D5E-9F0A-1B2C3D4E5F6G}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName=C:\HuSuiBot
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=Output
OutputBaseFilename=HuSuiBot_Setup_v{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
DisableProgramGroupPage=yes

[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "创建桌面快捷方式"; GroupDescription: "快捷方式："; Flags: checkedonce

[Files]
Source: "..\bot.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\pyproject.toml"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\check_plugins.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\.env.example"; DestDir: "{app}"; DestName: ".env.example"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\src\plugins\*"; DestDir: "{app}\src\plugins"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\data\poke\*"; DestDir: "{app}\data\poke"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\scripts\*"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\installer\readme_install.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\启动机器人"; Filename: "{app}\start_bot.bat"; WorkingDir: "{app}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\start_bot.bat"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{cmd}"; Parameters: "/c cd /d ""{app}"" && python -m venv venv && venv\Scripts\pip install -r requirements.txt"; Flags: runhidden; StatusMsg: "正在安装 Python 依赖（首次安装需要下载，请耐心等待）..."
Filename: "{app}\start_bot.bat"; Description: "启动花碎机器人"; Flags: postinstall nowait skipifsilent unchecked; WorkingDir: "{app}"

[UninstallRun]
Filename: "{cmd}"; Parameters: "/c taskkill /f /im python.exe"; Flags: runhidden

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    if not FileExists(ExpandConstant('{app}\.env')) then
    begin
      if FileCopy(ExpandConstant('{app}\.env.example'), ExpandConstant('{app}\.env'), False) then
      begin
        Log('.env 文件已从 .env.example 创建，请编辑后使用。');
      end;
    end;
  end;
end;
