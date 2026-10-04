def is_private(ip):                               # 사설 IP 면 True 를 돌려주는 함수
    parts = ip.split(".")                         # 점으로 나눈 마디 네 개
    first = int(parts[0])                         # 첫 마디(숫자)
    second = int(parts[1])                        # 둘째 마디(숫자)
    # 1. first 가 10 이면 True 를 return 하세요
    if first == 10:                               # 10.x.x.x
        return True
    # 2. first 가 172 이고 second 가 16 이상 31 이하이면 True 를 return 하세요
    if first == 172 and 16 <= second <= 31:       # 172.16 ~ 172.31 만
        return True
    # 3. first 가 192 이고 second 가 168 이면 True 를 return 하세요
    if first == 192 and second == 168:            # 192.168.x.x
        return True
    return False                                  # 셋 다 아니면 공인


for ip in ["10.0.0.8", "172.20.5.6", "172.32.5.6", "192.168.10.25", "8.8.8.8", "203.0.113.7"]:
    if is_private(ip):
        print("[사설]", ip)
    else:
        print("[공인]", ip)
