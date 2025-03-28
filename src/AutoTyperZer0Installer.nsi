; AutoTyperZer0 Installer Script

; Include Modern UI and necessary plugins
!include "MUI2.nsh"
!include "LogicLib.nsh"
!include "nsDialogs.nsh"

; General Installer Information
Name "AutoTyperZer0"
OutFile "AutoTyperZer0-Windows_Installer.exe"
InstallDir "$PROGRAMFILES64\AutoTyperZer0"
RequestExecutionLevel admin

; Compressor
SetCompressor lzma

; Modern UI Configuration
!define MUI_WELCOMEPAGE_TITLE "AutoTyperZer0 V1.2 Installer"
!define MUI_WELCOMEPAGE_TEXT ""

; Python Installer Download URL (latest stable version)


; Variables
Var PythonInstallCheckbox


; Custom Pages
Page custom ReadmePage ReadmePageLeave
Page custom PythonInstallPage PythonInstallPageLeave

; Additional Pages
!define MUI_FINISHPAGE_SHOWREADME ""
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES

; Shortcut Creation on Finish Page
!define MUI_FINISHPAGE_SHOWREADME_CHECKED
!define MUI_FINISHPAGE_SHOWREADME_TEXT "Create Desktop Shortcut"
!define MUI_FINISHPAGE_SHOWREADME_FUNCTION finishpageaction

; Thank You Page
Page custom ThankYouPage

!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

; Python Installation Page
Function PythonInstallPage
    !insertmacro MUI_HEADER_TEXT "Python Installation" "Prepare for AutoTyperZer0"
    
    nsDialogs::Create 1018
    Pop $0
    ${If} $0 == error
        Abort
    ${EndIf}

    ; Description Text
    ${NSD_CreateLabel} 0 0 100% 40u "AutoTyperZer0 works better with Python 3.12 or newer. Wish to update your Python?"
    Pop $1

    ${NSD_CreateButton} 10u 50u 120u 24u "Update Python"
    Pop $2
    ${NSD_OnClick} $2 PythonUpdate

    nsDialogs::Show
FunctionEnd

Function PythonInstallPageLeave
    ; Check if Python installation is selected
    ${NSD_GetState} $PythonInstallCheckbox $0
    ${If} $0 == ${BST_CHECKED}
        ; Download Python Installer
        NSISdl::download "${PYTHON_DOWNLOAD_URL}" "$TEMP\${PYTHON_INSTALLER}"
        Pop $R0
        ${If} $R0 == "success"
            ; Silent install of Python
            ExecWait '"$TEMP\${PYTHON_INSTALLER}" /quiet InstallAllUsers=1 PrependPath=1'
            ; Clean up installer
            Delete "$TEMP\${PYTHON_INSTALLER}"
        ${Else}
            MessageBox MB_OK "Failed to download Python installer. Error: $R0$\nPlease download manually from python.org"
        ${EndIf}
    ${EndIf}
FunctionEnd

; README Display Function
Function ReadmePage
    !insertmacro MUI_HEADER_TEXT "About AutoTyperZer0" "Learn about the application features"
    
    ; Create a README display dialog
    nsDialogs::Create 1018
    Pop $0
    ${If} $0 == error
        Abort
    ${EndIf}

    ; README Text
    ${NSD_CreateLabel} 10u 20u 100% 120u "Auto Typer Zer0, Not just your regular Auto Typer.$\n$\nFeatures:$\n - Perfect for Coding assignments with coding language selections and Perfect Indentation.$\n - Supports customizable typing speed and Super Speed mode.$\n - Always on Top toggle for the emergency stops.$\n$\nClick Next to continue."
    Pop $0
    SetCtlColors $0 0x000000 0xFFFFFF

    nsDialogs::Show
FunctionEnd

Function ReadmePageLeave
    ; Any additional processing if needed
FunctionEnd

; Thank You Page
Function ThankYouPage
    !insertmacro MUI_HEADER_TEXT "Thank You for Installing AutoTyperZer0" "What's Next?"
    
    nsDialogs::Create 1018
    Pop $0
    ${If} $0 == error
        Abort
    ${EndIf}

    ; Thank You Text with Future Features and GitHub Link
    ${NSD_CreateLabel} 10u 10u 100% 100u "Thank you for installing AutoTyperZer0!$\n$\nUpcoming Features:$\n - Special Typing modes (Remote typing, Obfuscated Typing, and Humanized Typing)$\n - More Customization Options$\n - Better UI$\n$\nCheck out my GitHub for the latest updates and to address any doubts:"
    Pop $1

    ; Manually set the Y-position of the button (text label height + margin)
    ${NSD_CreateButton} 10u 120u 120u 24u "Visit GitHub"
    Pop $2
    ${NSD_OnClick} $2 OpenGitHubLink

    nsDialogs::Show
FunctionEnd



Function OpenGitHubLink
    ExecShell "open" "https://github.com/RBLakshya/Auto-Typer-Zer0"
FunctionEnd

Function PythonUpdate
    ExecShell "open" "https://www.python.org/downloads/"
FunctionEnd

; Shortcut Creation Function for Finish Page
Function finishpageaction
    CreateShortcut "$DESKTOP\AutoTyperZer0.lnk" "$INSTDIR\AutoTyperZer0.exe"
FunctionEnd

; Detect and Uninstall Previous Version
Function .onInit
    ; Check if already installed
    ReadRegStr $R0 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AutoTyperZer0" "UninstallString"
    ${If} $R0 != ""
        ; Silent uninstall of previous version
        ClearErrors
        ExecWait '$R0 /S' ;Run uninstaller silently
        
        ; Remove desktop shortcut from previous installation
        Delete "$DESKTOP\AutoTyperZer0.lnk"
    ${EndIf}
FunctionEnd

Section "Install"
    ; Set output path to the installation directory
    SetOutPath $INSTDIR

    ; Add files to install
    File "C:\Users\MSI-1\Desktop\AutoTyperZer0-Win\AutoTyperZer0.exe"
    ; Add any additional files or dependencies here

    ; Store installation folder in registry
    WriteRegStr HKLM "Software\AutoTyperZer0" "InstallPath" $INSTDIR

    ; Create uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"

    ; Add registry keys for Windows Add/Remove Programs
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AutoTyperZer0" "DisplayName" "AutoTyperZer0"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AutoTyperZer0" "UninstallString" "$INSTDIR\Uninstall.exe"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AutoTyperZer0" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AutoTyperZer0" "NoRepair" 1
SectionEnd

; Uninstaller Section
Section "Uninstall"
    ; Remove files
    Delete "$INSTDIR\AutoTyperZer0.exe"
    Delete "$INSTDIR\Uninstall.exe"
    Delete "$DESKTOP\AutoTyperZer0.lnk"
    Delete "$DESKTOP\AutoTyperZer0.exe"

    ; Remove installation directory
    RMDir "$INSTDIR"

    ; Remove registry keys
    DeleteRegKey HKLM "Software\AutoTyperZer0"
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AutoTyperZer0"
SectionEnd