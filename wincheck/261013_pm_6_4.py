port_vlan = {1: 10, 2: 10, 3: 20, 4: 20, 5: 10}   # 포트 → VLAN 번호


def flood_ports(in_port):                         # in_port 로 들어온 브로드캐스트가 퍼질 포트들
    vlan = port_vlan[in_port]                     # 들어온 포트의 VLAN
    out = []
    for port in port_vlan:                        # 포트를 하나씩
        # 1. port 의 VLAN 이 vlan 과 같고 port 가 in_port 가 아니면 out 에 더하세요
        if port_vlan[port] == vlan and port != in_port:   # 같은 VLAN 이고 들어온 포트가 아니면
            out.append(port)
    return out


print("1번에서:", flood_ports(1))
print("3번에서:", flood_ports(3))
