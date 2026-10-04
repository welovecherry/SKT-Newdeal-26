conns = [                                         # netstat -n 의 상태 칸을 옮겨 왔다고 가정합니다
    {"peer": "203.0.113.10:443", "state": "ESTABLISHED"},
    {"peer": "198.51.100.7:443", "state": "ESTABLISHED"},
    {"peer": "203.0.113.10:443", "state": "TIME_WAIT"},
    {"peer": "192.0.2.53:53", "state": "TIME_WAIT"},
    {"peer": "198.51.100.20:443", "state": "SYN_SENT"},
]
count = {}                                        # 상태마다 센 수를 담을 빈 사전

for c in conns:                                   # 연결을 하나씩 꺼낸다
    # 1. count 의 c["state"] 키에 지금까지 센 수 + 1 을 담으세요 (.get 을 씁니다)
    count[c["state"]] = count.get(c["state"], 0) + 1   # 처음 보는 상태면 0 에서 시작

for state in count:                               # 센 상태를 하나씩
    print(state, count[state])                    # 상태와 개수
