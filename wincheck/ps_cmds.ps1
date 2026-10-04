"### cd network_zt"; try { cd network_zt 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### ping 8.8.8.8          # 4번 보내고 끝난다"; try { ping 8.8.8.8          # 4번 보내고 끝난다 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### ping -n 10 8.8.8.8    # 10번 보낸다"; try { ping -n 10 8.8.8.8    # 10번 보낸다 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### ping abc.nowhere-not-exist"; try { ping abc.nowhere-not-exist 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### ping 192.0.2.1"; try { ping 192.0.2.1 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### ping 8.8.8.8"; try { ping 8.8.8.8 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### ping google.com"; try { ping google.com 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### ping -n 10 8.8.8.8"; try { ping -n 10 8.8.8.8 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### ipconfig"; try { ipconfig 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### ipconfig /all"; try { ipconfig /all 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### ping 192.168.0.1"; try { ping 192.168.0.1 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### arp -a"; try { arp -a 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### netstat -n"; try { netstat -n 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### netstat -ano"; try { netstat -ano 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### netstat -an | findstr LISTENING"; try { netstat -an | findstr LISTENING 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### curl.exe "http://example.com/?q=network_day1""; try { curl.exe "http://example.com/?q=network_day1" 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### curl.exe "https://example.com/?q=network_day1""; try { curl.exe "https://example.com/?q=network_day1" 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### curl.exe https://api.ipify.org"; try { curl.exe https://api.ipify.org 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### ping -n 1 8.8.8.8"; try { ping -n 1 8.8.8.8 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### route print -4"; try { route print -4 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### tracert -d -h 5 8.8.8.8"; try { tracert -d -h 5 8.8.8.8 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### nslookup example.com"; try { nslookup example.com 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### nslookup example.com 8.8.8.8"; try { nslookup example.com 8.8.8.8 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### nslookup abc.nowhere-not-exist.com"; try { nslookup abc.nowhere-not-exist.com 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### nslookup -type=ns example.com"; try { nslookup -type=ns example.com 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### nslookup -type=ns kr"; try { nslookup -type=ns kr 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### nslookup example.com hera.ns.cloudflare.com"; try { nslookup example.com hera.ns.cloudflare.com 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### nslookup -type=mx google.com"; try { nslookup -type=mx google.com 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### nslookup -type=cname www.naver.com"; try { nslookup -type=cname www.naver.com 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### nslookup www.naver.com"; try { nslookup www.naver.com 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### ipconfig /displaydns"; try { ipconfig /displaydns 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### nslookup e6030.a.akamaiedge.net"; try { nslookup e6030.a.akamaiedge.net 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
"### nslookup qzkx7wp2v.example.com"; try { nslookup qzkx7wp2v.example.com 2>&1 | Select-Object -First 25 | Out-String -Width 200 } catch { "!!" + $_ }
exit 0
