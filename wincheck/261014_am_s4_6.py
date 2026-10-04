records = {
    "www.shop.test": {"type": "CNAME", "value": "shop.cdn.test"},
    "shop.cdn.test": {"type": "CNAME", "value": "edge7.cdn.test"},
    "edge7.cdn.test": {"type": "A", "value": "192.0.2.77"},
}
# 1. "www.shop.test" 에서 시작해, CNAME 이면 다음 이름으로 옮기기를 되풀이하고, 거쳐 간 이름을 「 → 」 로 이어 출력한 뒤 마지막 IP 를 출력하세요
name = "www.shop.test"                            # 시작 이름
chain = [name]                                    # 거쳐 간 이름들
while records[name]["type"] == "CNAME":           # 별명인 동안
    name = records[name]["value"]                 # 진짜 이름으로 옮긴다
    chain.append(name)
print(" → ".join(chain))
print("IP:", records[name]["value"])
