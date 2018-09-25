Param (
[Parameter(Mandatory=$True)]
$path
)

$folders = ls -dir $path

$data = @()

foreach ($folder in $folders)
		{
			$data_tmp = @(@{'{#SHARE.FOLDER.NAME}' = $folder.Name})
			$data += $data_tmp
		}
		

$js = @{"data"  = $data} | ConvertTo-Json

Write-Host $js 
