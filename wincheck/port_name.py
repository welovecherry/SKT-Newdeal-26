PORTS = {22: "SSH", 53: "DNS", 80: "HTTP", 443: "HTTPS", 3389: "RDP", 135: "RPC", 445: "SMB"}
seen = [443, 445, 3389, 51234]                    # netstat 에서 본 포트라고 가정합니다

for port in seen:                                 # 포트를 하나씩 꺼낸다
    # 1. name 이라는 변수에 PORTS 에서 port 의 이름을 꺼내 담으세요. 없으면 "모름" 입니다
    name = PORTS.get(port, "모름")                 # 없는 포트는 "모름"
    # 2. f"{port} → {name}" 을 출력하세요
    print(f"{port} → {name}")
