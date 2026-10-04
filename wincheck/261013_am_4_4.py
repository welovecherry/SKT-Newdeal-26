import ipaddress

addresses = ["192.168.50.20", "192.168.50.70", "192.168.50.90", "192.168.50.130"]
for address in addresses:                         # 주소를 하나씩
    # 1. net 에 ipaddress.ip_network(f"{address}/27", strict=False) 를 담으세요
    net = ipaddress.ip_network(f"{address}/27", strict=False)   # 그 주소가 속한 /27 망
    # 2. f"{address} -> {net}" 을 출력하세요
    print(f"{address} -> {net}")
