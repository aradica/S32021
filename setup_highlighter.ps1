$extensions = $HOME + "\.vscode\extensions\"
Copy-Item "s3" -Destination $extensions -Recurse
Write-Output "Restart Visual Studio Code for changes to take effect!"