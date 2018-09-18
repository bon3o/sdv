Param (
[Parameter(Mandatory=$True)]
$path
) 

$folders = ls -dir $path
$n = $folders.count-1
$f = 0

write-host "{"
write-host " `"data`":[`n"

    

    if ($n -gt 0)
    {
    do 
        {
        $str= "{`"{#SHARE.FOLDER.NAME}`" : `"" + $folders[$f] + "`" },"
        write-host $str
        ++$f
        }
        while ($f -lt $n)
    }
    
    if ($f -eq $n) 
    {
    $str= "{`"{#SHARE.FOLDER.NAME}`" : `"" + $folders[$f] + "`" }"
    write-host $str
    }

write-host
write-host " ]"
write-host "}"