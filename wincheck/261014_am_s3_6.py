queries = [                                       # 하루 동안 물어본 이름이라고 가정합니다
    "www.naver.com", "mail.google.com", "example.com", "www.daum.net",
    "kxq3vz9a.top", "update.microsoft.com", "p0w8rk2m.top", "news.example.co.kr",
]
# 1. 이름마다 맨 끝 조각(TLD)을 꺼내 사전으로 세고, 「com 4」 꼴로 출력하세요
count = {}                                        # TLD → 횟수
for name in queries:                              # 이름을 하나씩
    tld = name.split(".")[-1]                     # 맨 끝 조각
    count[tld] = count.get(tld, 0) + 1            # 처음 보면 0 에서 시작
for tld in count:
    print(tld, count[tld])
