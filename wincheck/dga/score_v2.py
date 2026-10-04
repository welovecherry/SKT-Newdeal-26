CHEAP_TLD = ["top", "xyz", "tk"]                  # 값싼 TLD


def score(name, rcode):                           # 이름과 답을 받아 점수 · 이유를 돌려준다
    parts = name.split(".")
    label = parts[-2]                             # TLD 앞 조각
    if label.startswith("xn--"):                  # 한글 도메인을 영문으로 바꾼 모양이면
        return {"points": 0, "why": ["한글 도메인 예외"]}
    tld = parts[-1]                               # TLD
    points = 0                                    # 합계 점수
    why = []                                      # 걸린 규칙 이름
    if len(label) >= 10:                          # 규칙 ① 길이
        points = points + 1
        why.append("길이")
    digits = 0
    vowels = 0
    for ch in label:                              # 한 자씩 센다
        if ch in "0123456789":
            digits = digits + 1
        if ch in "aeiou":
            vowels = vowels + 1
    if digits >= 2:                               # 규칙 ② 숫자
        points = points + 1
        why.append("숫자")
    if vowels / len(label) < 0.25:                # 규칙 ③ 모음 적음
        points = points + 1
        why.append("모음")
    if tld in CHEAP_TLD:                          # 규칙 ④ 값싼 TLD
        points = points + 1
        why.append("TLD")
    if rcode == "NXDOMAIN":                       # 규칙 ⑤ 없는 이름
        points = points + 2
        why.append("NXDOMAIN")
    return {"points": points, "why": why}


if __name__ == "__main__":                        # 직접 실행할 때만 시험한다
    print(score("www.naver.com", "NOERROR"))
    print(score("kxq3vz9a.top", "NXDOMAIN"))
