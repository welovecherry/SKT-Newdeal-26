import ipaddress

assignments = [                                   # (부서, CIDR, 필요한 장비 수)
    ("개발팀", "10.20.0.0/26", 50),
    ("운영팀", "10.20.0.64/27", 25),
    ("보안팀", "10.20.0.96/28", 10),
]
print("| 부서 | CIDR | 첫 호스트 | 마지막 호스트 | 사용 가능 | 필요 |")
print("|---|---|---|---|---|---|")
# 1. 부서를 하나씩 꺼내 망을 만들고, 첫 호스트(네트워크 주소 + 1)와 마지막 호스트(브로드캐스트 주소 - 1)를 구해 한 줄씩 출력하세요
for name, cidr, required in assignments:          # 부서를 하나씩
    net = ipaddress.ip_network(cidr)              # CIDR 을 망으로
    first = net.network_address + 1              # 첫 호스트
    last = net.broadcast_address - 1              # 마지막 호스트
    print(f"| {name} | {cidr} | {first} | {last} | {net.num_addresses - 2} | {required} |")
