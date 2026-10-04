echo "### curl.exe http (Git Bash)"; curl.exe -s "http://example.com/?q=network_day1" | grep -i "<title>" || true
echo "### curl http (Git Bash)"; curl -s "http://example.com/?q=network_day1" | grep -i "<title>" || true
echo "### curl.exe https"; curl.exe -s "https://example.com/?q=network_day1" | grep -i "<title>" || true
echo "### netstat -n | findstr 443"; netstat -n | findstr 443 | head -3 || true
echo "### which curl.exe"; which curl.exe; which curl
