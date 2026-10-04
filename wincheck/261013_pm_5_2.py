import ipaddress

my_net = ipaddress.ip_network("10.20.0.10/26", strict=False)   # 내 PC 가 속한 망
destinations = ["10.20.0.40", "10.20.0.63", "10.20.0.70"]

for dest in destinations:                         # 목적지를 하나씩
    # 1. dest 가 my_net 안에 있으면 「10.20.0.40 스위치로 직접」, 아니면 「… 게이트웨이로」 를 출력하세요
    if ipaddress.ip_address(dest) in my_net:      # 같은 망이면
        print(dest, "스위치로 직접")
    else:                                         # 다른 망이면
        print(dest, "게이트웨이로")
