echo "### nslookup example.com"; nslookup example.com 2>&1
echo "### nslookup -type=ns example.com"; nslookup -type=ns example.com 2>&1
echo "### nslookup -type=mx google.com"; nslookup -type=mx google.com 2>&1
echo "### nslookup -type=cname www.naver.com"; nslookup -type=cname www.naver.com 2>&1
echo "### nslookup www.naver.com"; nslookup www.naver.com 2>&1
echo "### nslookup nowhere"; nslookup abc.nowhere-not-exist.com 2>&1
echo "### ipconfig //displaydns | head"; ipconfig //displaydns 2>&1 | head -30
echo "### ipconfig //flushdns"; ipconfig //flushdns 2>&1
