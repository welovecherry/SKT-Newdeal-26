import ipaddress

plan = [                                          # (부서, CIDR, 필요한 장비 수)
    ("개발팀", "192.168.50.0/26", 50),
    ("운영팀", "192.168.50.64/27", 25),
    ("보안팀", "192.168.50.96/28", 10),
]
networks = []                                     # 겹침 검사용으로 망을 모을 리스트

for name, cidr, required in plan:                 # 부서를 하나씩
    net = ipaddress.ip_network(cidr)              # CIDR 을 망으로
    # 1. ok 라는 변수에 「쓸 수 있는 수가 required 이상인지」 를 담으세요
    ok = net.num_addresses - 2 >= required        # 장비를 다 담을 수 있나
    print(name, cidr, "충분:", ok)
    networks.append(net)                          # 겹침 검사용으로 모은다

# 2. overlap 에 「앞 둘(networks[0], networks[1])이 겹치거나 networks[1] 과 networks[2] 가 겹치거나 networks[0] 과 networks[2] 가 겹치는지」 를 담으세요
overlap = networks[0].overlaps(networks[1]) or networks[1].overlaps(networks[2]) or networks[0].overlaps(networks[2])
print("겹침 있음:", overlap)
