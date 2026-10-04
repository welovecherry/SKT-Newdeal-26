import ipaddress

my_ip = "192.168.10.25"                           # 내 IPv4 주소 (ipconfig)
prefix = 24                                       # 3-2 에서 바꾼 CIDR 숫자

# 1. net 이라는 변수에 ipaddress.ip_network(f"{my_ip}/{prefix}", strict=False) 를 담으세요
net = ipaddress.ip_network(f"{my_ip}/{prefix}", strict=False)   # 내 주소가 속한 망
# 2. "네트워크 주소:", "브로드캐스트 주소:", "사용 가능 주소 수:" 를 각각의 값과 함께 한 줄씩 출력하세요
print("네트워크 주소:", net.network_address)
print("브로드캐스트 주소:", net.broadcast_address)
print("사용 가능 주소 수:", net.num_addresses - 2)
