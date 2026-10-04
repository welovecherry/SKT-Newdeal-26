import ipaddress

routes = [                                        # (목적지 망, 다음 홉)
    ("0.0.0.0/0", "인터넷 게이트웨이"),
    ("192.168.10.0/26", "직접 연결 G0/0"),        # G0/0 · G0/1 은 라우터의 포트 이름
    ("192.168.10.64/26", "직접 연결 G0/1"),
]


def lookup(dest):                                 # 목적지 주소의 다음 홉을 돌려준다
    dest = ipaddress.ip_address(dest)
    best = None                                   # 지금까지 고른 줄
    for cidr, hop in routes:                      # 표를 한 줄씩
        net = ipaddress.ip_network(cidr)
        # 1. dest 가 net 안에 있고, best 가 None 이거나 net.prefixlen 이 best 의 prefixlen 보다 크면 best 에 (net, hop) 을 담으세요
        if dest in net and (best is None or net.prefixlen > best[0].prefixlen):   # 맞고 더 좁으면
            best = (net, hop)
    return best[1]                                # 고른 줄의 다음 홉


for d in ["192.168.10.20", "192.168.10.70", "8.8.8.8"]:
    print(d, "→", lookup(d))
