echo "### cd network_zt"; timeout 90 cd network_zt 2>&1 | head -25
echo "### ping 8.8.8.8          # 4번 보내고 끝난다"; timeout 90 ping 8.8.8.8          # 4번 보내고 끝난다 2>&1 | head -25
echo "### ping -n 10 8.8.8.8    # 10번 보낸다"; timeout 90 ping -n 10 8.8.8.8    # 10번 보낸다 2>&1 | head -25
echo "### ping abc.nowhere-not-exist"; timeout 90 ping abc.nowhere-not-exist 2>&1 | head -25
echo "### ping 192.0.2.1"; timeout 90 ping 192.0.2.1 2>&1 | head -25
echo "### ping 8.8.8.8"; timeout 90 ping 8.8.8.8 2>&1 | head -25
echo "### ping google.com"; timeout 90 ping google.com 2>&1 | head -25
echo "### ping -n 10 8.8.8.8"; timeout 90 ping -n 10 8.8.8.8 2>&1 | head -25
echo "### ipconfig"; timeout 90 ipconfig 2>&1 | head -25
echo "### ipconfig //all"; timeout 90 ipconfig //all 2>&1 | head -25
echo "### ping 192.168.0.1"; timeout 90 ping 192.168.0.1 2>&1 | head -25
echo "### arp -a"; timeout 90 arp -a 2>&1 | head -25
echo "### netstat -n"; timeout 90 netstat -n 2>&1 | head -25
echo "### netstat -ano"; timeout 90 netstat -ano 2>&1 | head -25
echo "### netstat -an | findstr LISTENING"; timeout 90 netstat -an | findstr LISTENING 2>&1 | head -25
echo "### curl.exe "http://example.com/?q=network_day1""; timeout 90 curl.exe "http://example.com/?q=network_day1" 2>&1 | head -25
echo "### curl.exe "https://example.com/?q=network_day1""; timeout 90 curl.exe "https://example.com/?q=network_day1" 2>&1 | head -25
echo "### curl.exe https://api.ipify.org"; timeout 90 curl.exe https://api.ipify.org 2>&1 | head -25
echo "### ping -n 1 8.8.8.8"; timeout 90 ping -n 1 8.8.8.8 2>&1 | head -25
echo "### route print -4"; timeout 90 route print -4 2>&1 | head -25
echo "### tracert -d -h 5 8.8.8.8"; timeout 90 tracert -d -h 5 8.8.8.8 2>&1 | head -25
echo "### nslookup example.com"; timeout 90 nslookup example.com 2>&1 | head -25
echo "### nslookup example.com 8.8.8.8"; timeout 90 nslookup example.com 8.8.8.8 2>&1 | head -25
echo "### nslookup abc.nowhere-not-exist.com"; timeout 90 nslookup abc.nowhere-not-exist.com 2>&1 | head -25
echo "### nslookup -type=ns example.com"; timeout 90 nslookup -type=ns example.com 2>&1 | head -25
echo "### nslookup -type=ns kr"; timeout 90 nslookup -type=ns kr 2>&1 | head -25
echo "### nslookup example.com hera.ns.cloudflare.com"; timeout 90 nslookup example.com hera.ns.cloudflare.com 2>&1 | head -25
echo "### nslookup -type=mx google.com"; timeout 90 nslookup -type=mx google.com 2>&1 | head -25
echo "### nslookup -type=cname www.naver.com"; timeout 90 nslookup -type=cname www.naver.com 2>&1 | head -25
echo "### nslookup www.naver.com"; timeout 90 nslookup www.naver.com 2>&1 | head -25
echo "### ipconfig //displaydns"; timeout 90 ipconfig //displaydns 2>&1 | head -25
echo "### nslookup e6030.a.akamaiedge.net"; timeout 90 nslookup e6030.a.akamaiedge.net 2>&1 | head -25
echo "### nslookup qzkx7wp2v.example.com"; timeout 90 nslookup qzkx7wp2v.example.com 2>&1 | head -25
