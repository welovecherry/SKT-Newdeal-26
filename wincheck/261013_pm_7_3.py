import ipaddress

used = [                                          # 이미 쓰는 세 부서의 망
    ipaddress.ip_network("10.20.0.0/26"),
    ipaddress.ip_network("10.20.0.64/27"),
    ipaddress.ip_network("10.20.0.96/28"),
]
parent = ipaddress.ip_network("10.20.0.0/24")

server = None
for candidate in parent.subnets(new_prefix=28):   # /28 후보를 앞에서부터
    # 1. candidate 가 used 의 어느 것과도 겹치지 않으면 server 에 담고 반복을 끝내세요(break)
    hits = 0                                      # 겹치는 부서 수
    for net in used:
        if candidate.overlaps(net):
            hits = hits + 1
    if hits == 0:                                 # 아무와도 안 겹치면
        server = candidate
        break                                     # 처음 빈 자리를 찾았으니 끝

print("서버망:", server)
overlap = False
for net in used:                                  # 기존 부서와 하나씩 비교
    # 2. server 가 net 과 겹치면 overlap 을 True 로 바꾸세요
    if server.overlaps(net):
        overlap = True
print("겹침 있음:", overlap)
