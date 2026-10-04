from dga_score import score

LOG = [
    ("www.naver.com", "NOERROR", "정상"), ("mail.google.com", "NOERROR", "정상"),
    ("update.microsoft.com", "NOERROR", "정상"), ("e6030.a.akamaiedge.net", "NOERROR", "정상"),
    ("cdn.jsdelivr.net", "NOERROR", "정상"), ("xn--3e0b707e.kr", "NOERROR", "정상"),
    ("kxq3vz9a.top", "NXDOMAIN", "의심"), ("p0w8rk2mzq.xyz", "NXDOMAIN", "의심"),
    ("qwrtpzkx7v.com", "NOERROR", "의심"), ("zzx9q2lk.top", "NXDOMAIN", "의심"),
    ("bnk-secure-login.xyz", "NOERROR", "의심"), ("www.example.com", "NOERROR", "정상"),
]
THRESHOLD = 3
hit = 0                                           # 맞힘 — 의심을 의심으로
false_alarm = 0                                   # 오탐 — 정상을 의심으로
missed = 0                                        # 미탐 — 의심을 정상으로

for name, rcode, truth in LOG:
    if score(name, rcode)["points"] >= THRESHOLD:   # 기준을 넘으면 의심
        judged = "의심"
    else:
        judged = "정상"
    # 1. judged 가 "의심" 이고 truth 가 "의심" 이면 hit 에 1 을 더하세요
    if judged == "의심" and truth == "의심":
        hit = hit + 1
    # 2. judged 가 "의심" 이고 truth 가 "정상" 이면 false_alarm 에 1 을 더하세요
    if judged == "의심" and truth == "정상":
        false_alarm = false_alarm + 1
    # 3. judged 가 "정상" 이고 truth 가 "의심" 이면 missed 에 1 을 더하세요
    if judged == "정상" and truth == "의심":
        missed = missed + 1

print("맞힘", hit, "· 오탐", false_alarm, "· 미탐", missed)
