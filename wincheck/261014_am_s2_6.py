import socket

names = ["example.com", "google.com", "www.naver.com", "abc.nowhere-not-exist.com"]
# 1. 이름을 하나씩 꺼내 socket.gethostbyname 으로 묻고 「example.com → 104.20.23.154」 꼴로 출력하세요. 못 찾으면 「… → 찾지 못함」
for name in names:                                # 이름을 하나씩
    try:
        ip = socket.gethostbyname(name)           # 내 PC 의 DNS 설정으로 묻는다
        print(name, "→", ip)
    except socket.gaierror:                       # 이름이 없으면
        print(name, "→ 찾지 못함")
