import ipaddress

a = ipaddress.ip_network("192.168.10.70/26", strict=False)
b = ipaddress.ip_network("192.168.10.120/26", strict=False)
c = ipaddress.ip_network("192.168.10.130/26", strict=False)
print(a, b, c)

# 1. a 와 b 가 같은 망인지(a == b) 를 「70과 120: True」 꼴로 출력하세요
print("70과 120:", a == b)                        # 둘 다 64~127
# 2. a 와 c 가 같은 망인지를 같은 꼴로 출력하세요
print("70과 130:", a == c)                        # 130 은 128~191
