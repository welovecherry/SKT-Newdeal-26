names = ["www.naver.com", "e6030.a.akamaiedge.net", "kxq3vz9a.top", "bnk-secure-login.xyz"]

for name in names:                                # 이름을 하나씩
    parts = name.split(".")                       # 점으로 나눈 조각들
    # 1. label 에 parts 의 끝에서 둘째(-2)를, tld 에 맨 끝(-1)을 담으세요
    label = parts[-2]                             # TLD 앞 조각
    tld = parts[-1]                               # TLD
    print(name, "조각:", label, "TLD:", tld)
