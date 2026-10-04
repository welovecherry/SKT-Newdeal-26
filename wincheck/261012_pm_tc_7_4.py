packets = [                                       # 7-2 의 3-way 세 줄
    {"src": "192.168.0.15", "dst": "203.0.113.10", "info": "[SYN]"},
    {"src": "203.0.113.10", "dst": "192.168.0.15", "info": "[SYN, ACK]"},
    {"src": "192.168.0.15", "dst": "203.0.113.10", "info": "[ACK]"},
]
headers = [                                       # 6-4 · 7-2 에서 읽은 헤더 값
    {"item": "출발지 IP", "value": "192.168.0.15", "where": "IP 헤더 (3층)"},
    {"item": "목적지 IP", "value": "203.0.113.10", "where": "IP 헤더 (3층)"},
    {"item": "TTL", "value": "128", "where": "IP 헤더 (3층)"},
    {"item": "출발지 포트", "value": "51234", "where": "TCP 헤더 (4층)"},
    {"item": "목적지 포트", "value": "80", "where": "TCP 헤더 (4층)"},
]

print("| 순서 | Source | Destination | Info |")
print("|---|---|---|---|")
i = 0                                             # 순서 번호
for p in packets:                                 # 3-way 세 줄을 하나씩
    # 1. i 에 1 을 더하고, f"| {i} | {p['src']} | {p['dst']} | {p['info']} |" 를 출력하세요
    i = i + 1                                     # 번호를 하나 늘린다
    print(f"| {i} | {p['src']} | {p['dst']} | {p['info']} |")

print()
print("| 항목 | 값 | 어느 헤더 |")
print("|---|---|---|")
for h in headers:                                 # 헤더 값을 하나씩
    # 2. f"| {h['item']} | {h['value']} | {h['where']} |" 를 출력하세요
    print(f"| {h['item']} | {h['value']} | {h['where']} |")
