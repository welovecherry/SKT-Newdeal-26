from dga_score import score

LOG = [
    ("www.naver.com", "NOERROR", "정상"), ("mail.google.com", "NOERROR", "정상"),
    ("update.microsoft.com", "NOERROR", "정상"), ("e6030.a.akamaiedge.net", "NOERROR", "정상"),
    ("cdn.jsdelivr.net", "NOERROR", "정상"), ("xn--3e0b707e.kr", "NOERROR", "정상"),
    ("kxq3vz9a.top", "NXDOMAIN", "의심"), ("p0w8rk2mzq.xyz", "NXDOMAIN", "의심"),
    ("qwrtpzkx7v.com", "NOERROR", "의심"), ("zzx9q2lk.top", "NXDOMAIN", "의심"),
    ("bnk-secure-login.xyz", "NOERROR", "의심"), ("www.example.com", "NOERROR", "정상"),
]
print("| 문턱값 | 맞힘 | 오탐 | 미탐 |")
print("|---|---|---|---|")
# 1. 문턱값 2, 3, 4 를 하나씩 꺼내 6-4 처럼 세고, 한 줄씩 표로 출력하세요
for threshold in [2, 3, 4]:                       # 문턱값을 하나씩
    hit = 0
    false_alarm = 0
    missed = 0
    for name, rcode, truth in LOG:
        if score(name, rcode)["points"] >= threshold:
            judged = "의심"
        else:
            judged = "정상"
        if judged == "의심" and truth == "의심":
            hit = hit + 1
        if judged == "의심" and truth == "정상":
            false_alarm = false_alarm + 1
        if judged == "정상" and truth == "의심":
            missed = missed + 1
    print(f"| {threshold} | {hit} | {false_alarm} | {missed} |")
