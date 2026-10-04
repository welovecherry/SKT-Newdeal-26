from dga_score import score

LOG = [
    ("www.naver.com", "NOERROR"), ("mail.google.com", "NOERROR"), ("update.microsoft.com", "NOERROR"),
    ("e6030.a.akamaiedge.net", "NOERROR"), ("cdn.jsdelivr.net", "NOERROR"), ("xn--3e0b707e.kr", "NOERROR"),
    ("kxq3vz9a.top", "NXDOMAIN"), ("p0w8rk2mzq.xyz", "NXDOMAIN"), ("qwrtpzkx7v.com", "NOERROR"),
    ("zzx9q2lk.top", "NXDOMAIN"), ("bnk-secure-login.xyz", "NOERROR"), ("www.example.com", "NOERROR"),
]
print("| 이름 | 답 | 점수 | 판정 | 근거 |")
print("|---|---|---|---|---|")

for name, rcode in LOG:
    result = score(name, rcode)
    if result["points"] >= 3:                     # 문턱값 3
        judged = "의심"
    else:
        judged = "정상"
    # 1. reason 에 result["why"] 를 ", " 로 이은 글자를 담고, 비어 있으면 "-" 를 담으세요
    reason = ", ".join(result["why"])             # 걸린 규칙을 이어 붙인다
    if reason == "":                              # 아무 규칙에도 안 걸렸으면
        reason = "-"
    print(f"| {name} | {rcode} | {result['points']} | {judged} | {reason} |")
