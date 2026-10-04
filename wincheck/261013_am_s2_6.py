def is_private(ip):                               # 2-3 에서 만든 함수
    parts = ip.split(".")
    first = int(parts[0])
    second = int(parts[1])
    if first == 10:
        return True
    if first == 172 and 16 <= second <= 31:
        return True
    if first == 192 and second == 168:
        return True
    return False


logs = [                                          # 로그라고 가정합니다
    "09:01 FAIL admin from 192.168.10.31",
    "09:02 FAIL admin from 203.0.113.50",
    "09:05 OK kim01 from 192.168.10.25",
    "09:07 FAIL root from 198.51.100.9",
    "09:09 FAIL guest from 172.20.5.6",
]
# 1. 로그를 하나씩 꺼내, "FAIL" 이 들었고 맨 끝 주소가 공인 IP 인 줄만 「[바깥 실패] 줄」 꼴로 출력하세요
for line in logs:                                 # 로그를 한 줄씩
    address = line.split()[-1]                    # 맨 끝 칸이 주소
    if "FAIL" in line and not is_private(address):   # 실패이고 바깥 주소면
        print("[바깥 실패]", line)
