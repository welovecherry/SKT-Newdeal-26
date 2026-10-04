import ipaddress                                  # 파이썬에 들어 있는 IP 계산 도구

for prefix in range(24, 29):                      # 24, 25, 26, 27, 28
    # 1. net 이라는 변수에 ipaddress.ip_network(f"192.168.10.0/{prefix}") 를 담으세요
    net = ipaddress.ip_network(f"192.168.10.0/{prefix}")   # 그 크기의 망
    # 2. prefix, net.netmask, net.num_addresses 를 한 줄에 출력하세요
    print(prefix, net.netmask, net.num_addresses)
