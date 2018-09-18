Param (
[Parameter(Mandatory=$True)]
$path
)
$n = 1

$folders = ls -dir $path

write-host "{"
write-host " `"data`":[`n"


foreach ($folder in $folders)
{
    
    if ($n -lt $folders.Count)
        {
        $line= "{`"{#SHARE.FOLDER.NAME}`" : `"" + $folder.name + "`" },"
        write-host $line
        $n++;
        }
    

    elseif ($n -ge $folders.Count)
        {
        $line= "{`"{#SHARE.FOLDER.NAME}`" : `"" + $folder.name + "`" }"
        write-host $line
        }
                
}

write-host
write-host " ]"
write-host "}"
