import ipaddress

devices = {
    "PC0": {"vlan": 10, "ip": "192.168.10.10/26", "gateway": "192.168.10.1"},
    "PC1": {"vlan": 10, "ip": "192.168.10.20/26", "gateway": "192.168.10.1"},
    "PC2": {"vlan": 20, "ip": "192.168.10.70/26", "gateway": "192.168.10.65"},
}
checks = [("PC0", "PC1", True), ("PC0", "PC2", True), ("PC0", "PC2", False)]   # (출발, 도착, 라우터 있음)
# 1. checks 를 하나씩 꺼내 판정하고 「PC0 -> PC1 스위치 직접 전달」 꼴로 출력하세요
for src, dst, has_router in checks:               # 검사를 하나씩
    a = devices[src]                              # 출발 장비
    b = devices[dst]                              # 도착 장비
    same_net = ipaddress.ip_network(a["ip"], strict=False) == ipaddress.ip_network(b["ip"], strict=False)
    if a["vlan"] == b["vlan"] and same_net:       # VLAN 도 망도 같으면
        print(f"{src} -> {dst} 스위치 직접 전달")
    elif has_router:                              # 다르지만 라우터가 있으면
        print(f"{src} -> {dst} 게이트웨이 {a['gateway']}로 전달")
    else:                                         # 다르고 라우터도 없으면
        print(f"{src} -> {dst} 통신 불가")
