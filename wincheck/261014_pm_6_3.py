from dga_score import score                       # 6-2 의 함수를 꺼내 쓴다

LOG = [                                           # (이름, 답, 실제)
    ("www.naver.com", "NOERROR", "정상"), ("mail.google.com", "NOERROR", "정상"),
    ("update.microsoft.com", "NOERROR", "정상"), ("e6030.a.akamaiedge.net", "NOERROR", "정상"),
    ("cdn.jsdelivr.net", "NOERROR", "정상"), ("xn--3e0b707e.kr", "NOERROR", "정상"),
    ("kxq3vz9a.top", "NXDOMAIN", "의심"), ("p0w8rk2mzq.xyz", "NXDOMAIN", "의심"),
    ("qwrtpzkx7v.com", "NOERROR", "의심"), ("zzx9q2lk.top", "NXDOMAIN", "의심"),
    ("bnk-secure-login.xyz", "NOERROR", "의심"), ("www.example.com", "NOERROR", "정상"),
]
THRESHOLD = 3                                     # 문턱값

for name, rcode, truth in LOG:                    # 로그를 한 줄씩
    result = score(name, rcode)
    # 1. judged 에 result["points"] 가 THRESHOLD 이상이면 "의심", 아니면 "정상" 을 담으세요
    if result["points"] >= THRESHOLD:             # 기준을 넘으면
        judged = "의심"
    else:
        judged = "정상"
    print(name, f"{result['points']}점", judged, f"(실제 {truth})")
