cache = {}                                        # 이름 → {"ip": 주소, "expire": 만료 시각}
TTL = 300                                         # 답을 300초 동안 쓴다
answers = {"example.com": "104.20.23.154"}        # 담당자에게 물었다고 가정한 답


def resolve(name, now):                           # now 초에 name 을 묻는다
    # 1. name 이 cache 에 있고 now 가 cache[name]["expire"] 보다 작으면 "캐시 " + 그 IP 를 return 하세요
    if name in cache and now < cache[name]["expire"]:   # 저장해 둔 답이 아직 유효하면
        return "캐시 " + cache[name]["ip"]
    ip = answers[name]                            # 새로 묻는다
    cache[name] = {"ip": ip, "expire": now + TTL}   # 만료 시각과 함께 저장
    return "새로 물음 " + ip


for t in [0, 100, 299, 300, 450]:
    print(t, "초:", resolve("example.com", t))
