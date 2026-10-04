PUBLIC_IP = "203.0.113.7"                         # 공유기의 공인 IP
nat_table = {                                     # 바깥 포트 → 안의 주소 · 포트
    40001: {"ip": "192.168.10.10", "port": 51001},
    40002: {"ip": "192.168.10.25", "port": 51234},
    40003: {"ip": "192.168.10.31", "port": 50999},
}
reply_port = 40002                                # 답이 돌아온 바깥 포트

# 1. inside 라는 변수에 nat_table 에서 reply_port 로 꺼낸 값을 담으세요
inside = nat_table[reply_port]                    # 표에서 원래 주인을 찾는다
print(f"밖: {PUBLIC_IP}:{reply_port}")
# 2. f"안: {inside['ip']}:{inside['port']}" 를 출력하세요
print(f"안: {inside['ip']}:{inside['port']}")
