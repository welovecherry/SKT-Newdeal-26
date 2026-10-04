PORTS = [1, 2, 3, 4]                              # 스위치의 포트 네 개
mac_table = {}                                    # 처음엔 아무것도 모른다


def receive(in_port, src, dest):                  # 프레임 하나가 in_port 로 들어왔다
    # 1. mac_table 의 src 키에 in_port 를 담으세요 (출발지를 배운다)
    mac_table[src] = in_port                      # 이 MAC 은 이 포트에 있다
    # 2. dest 가 mac_table 에 있으면 [mac_table[dest]] 를 return 하세요
    if dest in mac_table:                         # 목적지를 안다면
        return [mac_table[dest]]                  # 그 포트 하나로만
    out = []                                      # 모르면 플러딩할 포트들
    for port in PORTS:
        # 3. port 가 in_port 가 아니면 out 에 더하세요
        if port != in_port:                       # 들어온 포트는 빼고
            out.append(port)
    return out


print("AA → BB :", receive(1, "AA", "BB"))       # BB 를 아직 모른다
print("BB → AA :", receive(3, "BB", "AA"))       # AA 는 1번에서 배웠다
print("AA → BB :", receive(1, "AA", "BB"))       # 이제 BB 도 안다
print("표:", mac_table)
