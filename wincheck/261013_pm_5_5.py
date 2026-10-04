import ipaddress

pcs = [                                           # (이름, IP/CIDR, 기본 게이트웨이)
    ("PC0", "192.168.10.10/26", "192.168.10.1"),
    ("PC1", "192.168.10.20/26", "192.168.10.65"),
    ("PC2", "192.168.10.70/26", "192.168.10.65"),
]

for name, cidr, gw in pcs:                        # PC 를 하나씩
    net = ipaddress.ip_network(cidr, strict=False)   # 그 PC 가 속한 망
    # 1. gw 가 net 안에 있으면 「PC0 정상」, 아니면 「PC1 게이트웨이 192.168.10.65 가 망 밖 — 밖으로 못 나감」 을 출력하세요
    if ipaddress.ip_address(gw) in net:           # 게이트웨이가 같은 망에 있으면
        print(name, "정상")
    else:                                         # 망 밖이면
        print(name, "게이트웨이", gw, "가 망 밖 — 밖으로 못 나감")
