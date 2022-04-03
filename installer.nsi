!include MUI2.nsh

;--------------------------------
; Basic values definitions.

!define VERSION "@APP_VERSION@"
!define APP_VERSION "@APP_VERSION@"
!define APP_NAME "@APP_NAME@"
!define EXE_NAME "@EXE_NAME@"
!define README_FILE "README"
!define LICENSE_FILE "@PWD@\resources\text\COPYING_GNU_GPL"
!define MUI_ICON "@PWD@\resources\graphics\@APP_LOW_NAME@.ico"
!define MUI_UNICON "@PWD@\resources\graphics\@APP_LOW_NAME@.ico"
!define PATCH  "0"
!define OUTPUT_FILE "@OUT_PWD@\@APP_LOW_NAME@-@APP_VERSION@-win32.exe"
!define BINARY_TREE "@OUT_PWD@\app"

; Name and file.
Name "${APP_NAME} portable"
OutFile "${OUTPUT_FILE}"

; Set custom branding text.
BrandingText "${APP_NAME}"

; Set compression.
SetCompressor /SOLID /FINAL lzma

; Default installation folder.
InstallDir "$PROGRAMFILES\${APP_NAME}"
InstallDirRegKey HKCU "Software\${APP_NAME}" "Install Directory"

; Require administrator access.
RequestExecutionLevel admin

;--------------------------------
; Interface Settings

; Show "are you sure" dialog when cancelling installation.
!define MUI_ABORTWARNING

;--------------------------------
; Pages

; Pages for installator.
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "${LICENSE_FILE}"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_COMPONENTS

; Start menu folder page configuration.
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU" 
!define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\${APP_NAME}" 
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"

!insertmacro MUI_PAGE_INSTFILES

; Offer user to launch the application right when it is installed.
!define MUI_FINISHPAGE_RUN "$INSTDIR\${EXE_NAME}"

!insertmacro MUI_PAGE_FINISH

; Pages for uninstallator.
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

;--------------------------------
; Languages.

!insertmacro MUI_LANGUAGE "English"

;--------------------------------
; Helper macros.

!macro ExecWaitJob _exec
StrCpy $9 0
System::Call 'kernel32::CreateIoCompletionPort(i -1,i0,i0,i0)i.r1'
${IfThen} $1 != 0 ${|} IntOp $9 $9 + 1 ${|}
System::Call 'kernel32::CreateJobObject(i0,i0)i.r2'
${IfThen} $2 != 0 ${|} IntOp $9 $9 + 1 ${|}
System::Call '*(i 0,i $1)i.r0'
System::Call 'kernel32::SetInformationJobObject(i $2,i 7,i $0,i 8)i.r3'
${IfThen} $3 != 0 ${|} IntOp $9 $9 + 1 ${|}
System::Free $0
System::Call '*(i,i,i,i)i.r0'
System::Alloc 72
pop $4
System::Call "*$4(i 72)"
System::Call 'kernel32::CreateProcess(i0,t ${_exec},i0,i0,i0,i 0x01000004,i0,i0,i $4,i $0)i.r3'
${IfThen} $3 != 0 ${|} IntOp $9 $9 + 1 ${|}
System::Free $4
System::Call "*$0(i.r3,i.r4,i,i)"
System::Free $0
System::Call 'kernel32::AssignProcessToJobObject(i $2,i $3)i.r0'
${IfThen} $0 != 0 ${|} IntOp $9 $9 + 1 ${|}
System::Call 'kernel32::ResumeThread(i $4)i.r0'
${IfThen} $0 != -1 ${|} IntOp $9 $9 + 1 ${|}
System::Call 'kernel32::CloseHandle(i $3)'
System::Call 'kernel32::CloseHandle(i $4)'
!define __ExecWaitJob__ ExecWaitJob${__LINE__}
${__ExecWaitJob__}ioportwait:
System::Call 'kernel32::GetQueuedCompletionStatus(i $1,*i.r3,*i,*i.r4,i -1)i.r0'
${IfThen} $0 = 0 ${|} StrCpy $9 0 ${|}
${IfThen} $3 != 4 ${|} goto ${__ExecWaitJob__}ioportwait ${|}
System::Call 'kernel32::CloseHandle(i $2)'
System::Call 'kernel32::CloseHandle(i $1)'
!undef __ExecWaitJob__
${IfThen} $9 < 6 ${|} MessageBox mb_iconstop `ExecWaitJob "${_exec}" failed!` ${|}
!macroend
  
; If you are using solid compression, files that are required before
; the actual installation should be stored first in the data block,
; because this will make your installer start faster.
!insertmacro MUI_RESERVEFILE_LANGDLL

;--------------------------------
; Sections.

; Installer sections.
Section "!Core" Core
  IfFileExists $INSTDIR\Uninstall.exe +1 NotInstalled
  MessageBox MB_OK|MB_ICONEXCLAMATION "${APP_NAME} is already installed. $\n$\nClick 'OK' to automatically uninstall it, installer will then automatically continue with current installation." IDOK Uninstall
  
Uninstall:  
  !insertmacro ExecWaitJob '"$INSTDIR\Uninstall.exe /S"'

NotInstalled:
  SetOutPath "$INSTDIR"
  
  ; Install core application files.
  File /r "${BINARY_TREE}\"
  
  ; Store installation folder.
  WriteRegStr HKCU "Software\${APP_NAME}" "Install Directory" $INSTDIR
  
  ; Create uninstaller.
  WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Desktop Icon" DesktopIcon
  CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${EXE_NAME}"
SectionEnd

Section "Start Menu Shortcuts" StartMenuShortcuts
  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${EXE_NAME}"
  CreateShortCut "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
SectionEnd

LangString DESC_Core ${LANG_ENGLISH} "Core installation files for ${APP_NAME}."
LangString DESC_DesktopIcon ${LANG_ENGLISH} "Desktop icon for ${APP_NAME}."
LangString DESC_StartMenuShortcuts ${LANG_ENGLISH} "Start Menu Shortcuts for ${APP_NAME}."

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${Core} $(DESC_Core)
  !insertmacro MUI_DESCRIPTION_TEXT ${DesktopIcon} $(DESC_DesktopIcon)
  !insertmacro MUI_DESCRIPTION_TEXT ${StartMenuShortcuts} $(DESC_StartMenuShortcuts)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; Uninstaller section.
Section "Uninstall"
  ; Here remove all files, but skip "data" folder.
  Push "$INSTDIR"
  Push "data"
  Call un.RmDirsButOne
  
  ; Remove uninstaller.
  Delete "$INSTDIR\*"
   
  ; Remove rest of installed files.
  ; Custom files are left intact.
  RMDir "$INSTDIR"
    
  Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"
  RMDir "$SMPROGRAMS\${APP_NAME}"
  
  Delete "$DESKTOP\${APP_NAME}.lnk"

  DeleteRegKey /ifempty HKCU "Software\${APP_NAME}"
SectionEnd

;--------------------------------
; Custom functions.

Function un.RmDirsButOne
  Exch $R0 ; exclude dir
  Exch
  Exch $R1 ; route dir
  Push $R2
  Push $R3

  ClearErrors
  FindFirst $R3 $R2 "$R1\*.*"
  IfErrors Exit

  Top:
    StrCmp $R2 "." Next
    StrCmp $R2 ".." Next
    StrCmp $R2 $R0 Next
    IfFileExists "$R1\$R2\*.*" 0 Next
    RmDir /r "$R1\$R2"

    #Goto Exit ;uncomment this to stop it being recursive (delete only one dir)

  Next:
    ClearErrors
    FindNext $R3 $R2
    IfErrors Exit
    Goto Top

  Exit:
    FindClose $R3

  Pop $R3
  Pop $R2
  Pop $R1
  Pop $R0
FunctionEnd

; Executed when installer starts.
Function .onInit
  IntOp $0 ${SF_SELECTED} | ${SF_RO}
  SectionSetFlags ${Core} $0
FunctionEnd