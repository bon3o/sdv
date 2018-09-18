#include <Date.au3>
#RequireAdmin
$FindString = IniRead("HostMonChecker.ini", "Strings", "Connected", "none")
$Host = IniRead("HostMonChecker.ini", "Zabbix", "Host", "none")
$Key = IniRead("HostMonChecker.ini", "Zabbix", "Key", "none")
$ZBX = IniRead("HostMonChecker.ini", "Zabbix", "Proxy", "none")



$CMD1 = "taskkill -f -im rcc.exe"
$CMD2 = "taskkill /S STA-C3MGMT-001 /f /im rcc.exe"


RunWait(@ComSpec & " /c " & $CMD1)
RunWait(@ComSpec & " /c " & $CMD2)


Run('C:\Program Files (x86)\HostMonitor8\rcc.exe')


Local $rcc = WinWaitActive('Remote Control Console','When connection established', 10)


ControlClick($rcc, "", "[Class:TButton;Instance:3]")


Local $instance = WinWaitActive($FindString,'', 10)
WinClose($FindString, '')

If $instance Then
	$Result = 1
Else
	$Result = 0
EndIf

$run = "C:\zabbix\zabbix_sender.exe -z " & $ZBX & " " & "-p 10051 " & '-s "' & $Host & '" -k "' & $Key & '" -o "' & $Result & '"'
FileWrite("c:\hostmonchecker\log.log", "Script executed: " &  _NowTime() & @CRLF)


Run($run)





