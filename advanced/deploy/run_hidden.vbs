' Launches ../../deploy/run_watcher.ps1 with zero visible window,
' forwarding any arguments given. This is one of advanced's concrete
' engineering-quality improvements over baseline (see
' advanced/deploy/README.md): baseline's scheduled task runs with a
' plain, visible console window on every poll; advanced's runs silently.
'
' Unlike PowerShell's own -WindowStyle Hidden (which still briefly
' allocates a console before hiding it -- causing a visible flash that
' can steal foreground focus), WScript.Shell.Run with style 0 never
' creates a console window at all.
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")
scriptDir = objFSO.GetParentFolderName(WScript.ScriptFullName)
repoRoot = objFSO.GetParentFolderName(objFSO.GetParentFolderName(scriptDir))
runWatcher = repoRoot & "\deploy\run_watcher.ps1"

forwardedArgs = ""
For i = 0 To WScript.Arguments.Count - 1
    forwardedArgs = forwardedArgs & " " & WScript.Arguments(i)
Next

cmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File """ & runWatcher & """" & forwardedArgs

' 0 = hidden window, True = wait for completion and relay its exit code
exitCode = objShell.Run(cmd, 0, True)
WScript.Quit exitCode
