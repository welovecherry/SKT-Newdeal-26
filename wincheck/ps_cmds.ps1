"### curl.exe http (PowerShell)"; curl.exe -s "http://example.com/?q=network_day1" | Select-String "<title>"
"### curl alias in PowerShell 5.1"; (Get-Command curl).CommandType; (Get-Command curl).Definition
"### netstat -n | findstr 443"; netstat -n | findstr 443 | Select-Object -First 3
exit 0
