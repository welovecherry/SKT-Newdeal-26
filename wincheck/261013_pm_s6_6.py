import ipaddress

vlan_subnet = {                                   # VLAN 번호 → 서브넷
    10: "192.168.10.0/26",
    20: "192.168.10.0/26",
    30: "192.168.10.64/27",
}
# 1. VLAN 을 둘씩 짝지어(10-20, 10-30, 20-30) 서브넷이 겹치면 「VLAN 10 과 20 이 같은 주소를 씀 — 라우터가 있어도 통신 안 됨」 을 출력하세요
for a, b in [(10, 20), (10, 30), (20, 30)]:       # 짝을 하나씩
    net_a = ipaddress.ip_network(vlan_subnet[a])
    net_b = ipaddress.ip_network(vlan_subnet[b])
    if net_a.overlaps(net_b):                     # 주소가 겹치면
        print(f"VLAN {a} 과 {b} 이 같은 주소를 씀 — 라우터가 있어도 통신 안 됨")
