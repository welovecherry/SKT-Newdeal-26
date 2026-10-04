logs = [                                          # (PC 주소, 물어본 이름, 답)
    ("10.20.0.15", "www.naver.com", "NOERROR"),
    ("10.20.0.42", "kxq3vz9a.top", "NXDOMAIN"),
    ("10.20.0.42", "p0w8rk2mzq.xyz", "NXDOMAIN"),
    ("10.20.0.15", "mail.google.com", "NOERROR"),
    ("10.20.0.42", "zzx9q2lk.top", "NXDOMAIN"),
    ("10.20.0.33", "typo-nevar.com", "NXDOMAIN"),
    ("10.20.0.42", "qwrtpzkx7v.com", "NOERROR"),
]
nx = {}                                           # PC 주소 → NXDOMAIN 횟수

for pc, name, rcode in logs:                      # 로그를 한 줄씩
    # 1. rcode 가 "NXDOMAIN" 이면 nx 의 pc 키를 1 늘리세요 (.get)
    if rcode == "NXDOMAIN":
        nx[pc] = nx.get(pc, 0) + 1                # 처음 보는 PC 면 0 에서

for pc in nx:
    # 2. 횟수가 3 이상이면 「[확인 필요] 10.20.0.42 NXDOMAIN 3번」 을 출력하세요
    if nx[pc] >= 3:
        print(f"[확인 필요] {pc} NXDOMAIN {nx[pc]}번")
