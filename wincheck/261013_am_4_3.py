import ipaddress

parent = ipaddress.ip_network("192.168.50.0/24")  # 회사가 받은 전체 주소
for sub in parent.subnets(new_prefix=26):         # /26 네 개를 하나씩
    # 1. sub 와 「사용 가능 62」 처럼 쓸 수 있는 수를 한 줄에 출력하세요
    print(sub, "사용 가능", sub.num_addresses - 2)
