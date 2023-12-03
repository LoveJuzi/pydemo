# myscript.ps1

# 获取脚本所在目录的绝对路径
$scriptPath = Get-Item -Path $MyInvocation.MyCommand.Path | Resolve-Path
$scriptDirectory = Split-Path -Path $scriptPath -Parent

$resolvePath = $(Resolve-Path -Path $scriptDirectory)

$scriptDirectory = $resolvePath.Path.Replace('Microsoft.PowerShell.Core\FileSystem::', '')
echo $scriptDirectory

Push-Location

# 进入脚本所在目录
Set-Location -Path $scriptDirectory

# 设置 PYTHONPATH 环境变量
$env:PYTHONPATH = "$scriptDirectory\utils;$scriptDirectory\resource"

# 返回到之前的工作目录
Pop-Location

