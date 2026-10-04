"### authoritative NS lookup"; $ns=(nslookup -type=ns example.com 2>$null | Select-String "nameserver" | Select-Object -First 1).ToString().Split("=")[-1].Trim(); $ns; nslookup example.com $ns
"### Resolve-DnsName"; Resolve-DnsName example.com | Format-Table -AutoSize | Out-String -Width 200
exit 0
