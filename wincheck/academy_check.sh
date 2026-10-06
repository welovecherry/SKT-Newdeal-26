#!/usr/bin/env bash
# 학원 PC 실측 — 10/12~10/14 실습 문서의 명령을 학원망 · 한국어 Windows 에서 한 번에 돌려 결과를 파일로 남긴다
# 쓰는 법 (Git Bash): bash academy_check.sh
# 결과: 이 파일과 같은 폴더의 academy_check_결과.txt — 통째로 Claude 에게 붙여 넣는다
# 학생 PC 를 바꾸지 않는다. 설치 · 설정 변경 · 삭제를 하지 않고, 보기만 한다.

OUT="academy_check_결과.txt"
exec > >(tee "$OUT") 2>&1

run() {                                   # 명령 하나를 제목과 함께 실행한다
  echo
  echo "=================================================================="
  echo "### $1"
  echo "=================================================================="
  shift
  eval "$@"
}

run "0 · 환경"                 'date; uname -a; git --version; python --version; chcp.com'

# ── 10/12(월) 오전 · ping · ipconfig · arp · netstat
run "10/12 AM · ipconfig"      'ipconfig'
GW=$(ipconfig | grep -a "기본 게이트웨이\|Default Gateway" | grep -aoE "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" | head -1)
echo "찾은 기본 게이트웨이: $GW"
run "10/12 AM · ping 8.8.8.8"  'ping -n 4 8.8.8.8'
run "10/12 AM · ping 게이트웨이" "ping -n 4 $GW"
run "10/12 AM · ping google.com" 'ping -n 2 google.com'
run "10/12 AM · ping 없는 이름" 'ping -n 2 abc.nowhere-not-exist'
run "10/12 AM · ping 답 없는 주소" 'ping -n 2 192.0.2.1'
run "10/12 AM · ping -n 10"    'ping -n 10 8.8.8.8'
run "10/12 AM · ipconfig //all" 'ipconfig //all'
run "10/12 AM · arp -a"        'arp -a'
run "10/12 AM · netstat -n (앞 20줄)"   'netstat -n | head -20'
run "10/12 AM · netstat -ano (앞 20줄)" 'netstat -ano | head -20'
run "10/12 AM · LISTENING (findstr)"    'netstat -an | findstr LISTENING'
run "10/12 AM · LISTENING (grep)"       'netstat -an | grep LISTENING'

# ── 10/12(월) 오후 · Wireshark 의 명령줄 판 tshark 로 같은 캡처를 해 본다
TS="/c/Program Files/Wireshark/tshark.exe"
if [ -x "$TS" ]; then
  run "10/12 PM · tshark 통로 목록" '"$TS" -D'
  IF=$("$TS" -D 2>/dev/null | grep -aiv "bluetooth\|loopback\|etw\|usbpcap" | grep -ai "이더넷\|ethernet" | head -1 | cut -d. -f1)
  [ -z "$IF" ] && IF=1
  echo "고른 통로 번호: $IF"
  run "10/12 PM · 캡처 tcp port 80 + curl http" \
    '("$TS" -i "$IF" -f "tcp port 80" -a duration:8 -w cap80.pcapng >/dev/null 2>&1 &) ; sleep 2; curl -s "http://example.com/?q=network_day1" | head -c 120; echo; sleep 7; "$TS" -r cap80.pcapng | head -20'
  run "10/12 PM · 표시 필터 http"          '"$TS" -r cap80.pcapng -Y http'
  run "10/12 PM · 표시 필터 SYN"           '"$TS" -r cap80.pcapng -Y "tcp.flags.syn == 1"'
  run "10/12 PM · 표시 필터 FIN"           '"$TS" -r cap80.pcapng -Y "tcp.flags.fin == 1"'
  run "10/12 PM · 캡처 tcp port 443 + curl https" \
    '("$TS" -i "$IF" -f "tcp port 443" -a duration:8 -w cap443.pcapng >/dev/null 2>&1 &) ; sleep 2; curl -s "https://example.com/?q=network_day1" >/dev/null; sleep 7; "$TS" -r cap443.pcapng | head -15'
  run "10/12 PM · 443 에서 검색어가 보이나" '"$TS" -r cap443.pcapng -Y "frame contains \"network_day1\"" | wc -l'
else
  echo "tshark 없음 — Wireshark 가 설치되지 않았거나 다른 위치"
fi

# ── 10/13(화) · 공인 IP · 서브넷 · 라우팅
run "10/13 AM · 공인 IP"        'curl -s https://api.ipify.org; echo'
run "10/13 PM · route print -4" 'route print -4'
run "10/13 PM · tracert"        'tracert -d -h 5 8.8.8.8'
run "10/13 PM · ping 뒤 arp"    'ping -n 1 8.8.8.8 >/dev/null; arp -a'

# ── 10/14(수) · DNS
run "10/14 AM · nslookup example.com"            'nslookup example.com'
run "10/14 AM · nslookup example.com 8.8.8.8"    'nslookup example.com 8.8.8.8'
run "10/14 AM · nslookup 없는 이름"              'nslookup abc.nowhere-not-exist.com'
run "10/14 AM · NS example.com"                  'nslookup -type=ns example.com'
run "10/14 AM · NS kr."                          'nslookup -type=ns kr.'
run "10/14 AM · 권한 있는 서버에 직접"           'nslookup example.com hera.ns.cloudflare.com'
run "10/14 AM · MX google.com"                   'nslookup -type=mx google.com'
run "10/14 AM · CNAME www.naver.com"             'nslookup -type=cname www.naver.com'
run "10/14 AM · nslookup www.naver.com"          'nslookup www.naver.com'
run "10/14 AM · DNS 캐시 (앞 40줄)"              'ipconfig //displaydns | head -40'
run "10/14 AM · 파이썬 socket"                   'python -c "import socket; print(socket.gethostbyname(\"example.com\"))"'
run "10/14 PM · CDN 이름"                        'nslookup e6030.a.akamaiedge.net'
run "10/14 PM · 없는 이름 .invalid"              'nslookup qzkx7wp2v.invalid'

echo
echo "끝 — $OUT 를 통째로 붙여 넣어 주세요."
