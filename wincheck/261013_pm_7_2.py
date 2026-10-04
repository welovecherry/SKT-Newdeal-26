import ipaddress

plan = [                                          # (부서, CIDR, VLAN)
    ("개발팀", "10.20.0.0/26", 10),
    ("운영팀", "10.20.0.64/27", 20),
    ("보안팀", "10.20.0.96/28", 30),
]
print("| 부서 | VLAN | CIDR | 게이트웨이 | 장비에 줄 범위 |")
print("|---|---|---|---|---|")

for name, cidr, vlan in plan:                     # 부서를 하나씩
    net = ipaddress.ip_network(cidr)              # 그 부서의 망
    # 1. gateway 에 net.network_address + 1 을 담으세요
    gateway = net.network_address + 1             # 첫 호스트를 게이트웨이로
    # 2. first 에 gateway + 1, last 에 net.broadcast_address - 1 을 담으세요
    first = gateway + 1                           # PC 에 줄 첫 주소
    last = net.broadcast_address - 1              # PC 에 줄 마지막 주소
    print(f"| {name} | {vlan} | {cidr} | {gateway} | {first} ~ {last} |")
