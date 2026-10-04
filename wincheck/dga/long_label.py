names = [
    "www.naver.com",
    "aGVsbG8gd29ybGQgdGhpcyBpcyBzZWNyZXQ.t1.example.com",
    "update.microsoft.com",
    "c2VjcmV0X3Bhc3N3b3JkX2Zvcl9hZG1pbl91c2Vy.t1.example.com",
]
# 1. 이름마다 맨 앞 조각의 길이를 재서 30 이상이면 「[터널링 의심] 길이 35 : 이름」 꼴로 출력하세요
for name in names:                                # 이름을 하나씩
    first = name.split(".")[0]                    # 맨 앞 조각
    if len(first) >= 30:                          # 비정상적으로 길면
        print("[터널링 의심] 길이", len(first), ":", name)
