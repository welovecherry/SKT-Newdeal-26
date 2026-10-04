"### PS nslookup -type=ns kr."; nslookup -type=ns kr. 2>&1 | Select-Object -First 12 | Out-String
"### PS nslookup qzkx7wp2v.invalid"; nslookup qzkx7wp2v.invalid 2>&1 | Out-String
exit 0
