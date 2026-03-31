[Setup]
AppName=InventarioJC
AppVersion=1.0
DefaultDirName={autopf}\InventarioJC
DefaultGroupName=InventarioJC
OutputDir=installer_output
OutputBaseFilename=Instalar_InventarioJC
SetupIconFile=assets\inventario_converted.ico
Compression=lzma
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin

[Tasks]
Name: "desktopicon"; Description: "Crear un acceso directo en el Escritorio"; GroupDescription: "Iconos adicionales:"; Flags: unchecked

[Dirs]
; Necesitamos otorgar permisos de escritura en el directorio de la app para que la base de datos se pueda modificar
Name: "{app}"; Permissions: users-modify

[Files]
Source: "dist\InventarioJC\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\InventarioJC"; Filename: "{app}\InventarioJC.exe"; IconFilename: "{app}\InventarioJC.exe"
Name: "{autodesktop}\InventarioJC"; Filename: "{app}\InventarioJC.exe"; Tasks: desktopicon; IconFilename: "{app}\InventarioJC.exe"

[Run]
Filename: "{app}\InventarioJC.exe"; Description: "Lanzar InventarioJC"; Flags: nowait postinstall skipifsilent
