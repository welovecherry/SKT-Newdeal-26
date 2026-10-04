import ipaddress

my_ip = "192.168.10.25"
prefix = 24
gateway = "192.168.10.1"

# 1. net 에 내 망을 담으세요 (3-4 와 같은 줄)
net = ipaddress.ip_network(f"{my_ip}/{prefix}", strict=False)   # 내 망
# 2. 게이트웨이가 net 안에 있는지를 「게이트웨이 192.168.10.1 이 내 망 안에 있나: True」 꼴로 출력하세요
inside = ipaddress.ip_address(gateway) in net     # 주소 하나가 망 안에 있나
print(f"게이트웨이 {gateway} 이 내 망 안에 있나: {inside}")
