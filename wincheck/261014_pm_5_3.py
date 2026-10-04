def features(name):                               # 이름 하나의 특징을 사전으로 돌려준다
    label = name.split(".")[-2]                   # TLD 앞 조각
    digits = 0
    vowels = 0
    for ch in label:                              # 한 자씩
        # 1. ch 가 숫자면 digits 에 1 을 더하세요
        if ch in "0123456789":
            digits = digits + 1
        # 2. ch 가 모음(aeiou)이면 vowels 에 1 을 더하세요
        if ch in "aeiou":
            vowels = vowels + 1
    return {"label": label, "len": len(label), "digits": digits, "vowel_ratio": round(vowels / len(label), 2)}


for name in ["www.naver.com", "kxq3vz9a.top", "xn--3e0b707e.kr"]:
    print(features(name))
