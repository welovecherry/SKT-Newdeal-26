SERVER = "203.0.113.10"                           # 살펴볼 서버
packets = [                                       # 캡처한 패킷이라고 가정합니다
    {"no": 12, "src": "192.168.0.15", "dst": "203.0.113.10", "flags": ["SYN"]},
    {"no": 13, "src": "203.0.113.10", "dst": "192.168.0.15", "flags": ["SYN", "ACK"]},
    {"no": 14, "src": "192.168.0.15", "dst": "203.0.113.10", "flags": ["ACK"]},
    {"no": 15, "src": "192.168.0.15", "dst": "198.51.100.7", "flags": ["ACK"]},
    {"no": 16, "src": "192.168.0.15", "dst": "203.0.113.10", "flags": ["FIN", "ACK"]},
]

print("[SYN 필터]")
for p in packets:                                 # 패킷을 하나씩
    # 1. p["flags"] 안에 "SYN" 이 있으면 f"{p['no']} {p['src']} → {p['dst']} {p['flags']}" 를 출력하세요
    if "SYN" in p["flags"]:                       # 플래그 리스트 안에 SYN 이 있으면
        print(f"{p['no']} {p['src']} → {p['dst']} {p['flags']}")

print("[서버 대화 필터]")
for p in packets:
    # 2. p["src"] 가 SERVER 이거나 p["dst"] 가 SERVER 이면 같은 모양으로 출력하세요
    if p["src"] == SERVER or p["dst"] == SERVER:  # 보낸 쪽이든 받은 쪽이든 그 서버면
        print(f"{p['no']} {p['src']} → {p['dst']} {p['flags']}")
