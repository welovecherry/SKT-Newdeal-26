# 방화벽 규칙표: (번호, 출발 구역, 도착 구역, 포트, 동작) 튜플을 모은 리스트이다
RULES = [
    (1, "outside", "DMZ", 443, "permit"),    # 규칙 1: 인터넷에서 DMZ 의 443 번을 허용한다
    (2, "DMZ", "inside", 445, "permit"),     # 규칙 2: DMZ 에서 내부망의 445 번을 허용한다
]

def default_policy(src, dst):                # 규칙에 맞는 것이 없을 때의 기본 정책 함수이다
    if src == dst:                           # 출발 구역과 도착 구역이 같으면
        return "permit"                      # 허용한다
    if src == "inside":                      # 내부망에서 출발하면
        return "permit"                      # 허용한다
    if dst == "outside":                     # 인터넷으로 나가는 통신이면
        return "permit"                      # 허용한다
    return "deny"                            # 나머지는 모두 차단한다

def match_rule(rule, src, dst, port):        # 규칙 하나가 요청과 맞는지 알아보는 함수이다
    no, r_src, r_dst, r_port, action = rule  # 튜플 다섯 값을 각각 이름으로 꺼낸다
    return r_src == src and r_dst == dst and r_port == port   # 셋 다 같으면 True, 아니면 False 를 리턴한다

def judge(src, dst, port):                   # ← 이 함수가 하는 일을 여기에 주석으로 씁니다
    for rule in RULES:                       # 규칙을 위에서부터 하나씩 꺼낸다
        if match_rule(rule, src, dst, port): # 이 규칙이 요청과 맞으면
            return rule[4], rule[0]          # ← 이 줄이 리턴하는 값 두 개를 여기에 주석으로 씁니다
    return default_policy(src, dst), 0       # ← 맞는 규칙이 없을 때 리턴하는 값을 여기에 주석으로 씁니다

TESTS = [                                    # 시험 요청 여섯 개: (출발, 도착, 포트)
    ("outside", "DMZ", 443),
    ("outside", "DMZ", 80),
    ("inside", "DMZ", 443),
    ("DMZ", "inside", 445),
    ("DMZ", "inside", 3389),
    ("outside", "inside", 445),
]

for src, dst, port in TESTS:                 # 시험 요청을 하나씩 꺼내 출발 · 도착 · 포트 로 나눈다
    action, no = judge(src, dst, port)       # judge 가 리턴한 두 값을 action 과 no 에 나눠 담는다
    print(src, "→", dst, port, ":", action, "(규칙 " + str(no) + ")")   # 판정 결과를 한 줄로 출력한다
