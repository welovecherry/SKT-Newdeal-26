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

def judge(src, dst, port):                   # 요청 하나를 규칙표 위에서부터 판정하는 함수이다
    for rule in RULES:                       # 규칙을 위에서부터 하나씩 꺼낸다
        if match_rule(rule, src, dst, port): # 이 규칙이 요청과 맞으면
            return rule[4], rule[0]          # 규칙의 동작과 규칙 번호를 함께 리턴하고 함수를 끝낸다
    return default_policy(src, dst), 0       # 맞는 규칙이 없으면 기본 정책의 동작과 번호 0 을 리턴한다

def allowed_ports(src, dst, ports):          # ports 중 허용(permit) 되는 포트만 모아 리스트로 리턴하는 함수이다. 이 함수를 직접 만든다
    # 여기를 직접 씁니다 (4줄 이하): 빈 리스트 만들기 → for 로 포트 하나씩 꺼내기 → judge 로 판정 → permit 이면 append → 리스트 리턴
    return []                                # ← 이 줄을 지우고 위 내용을 코드로 쓴다

PORTS = [22, 80, 443, 445, 3389]             # 시험할 포트 다섯 개이다
print(allowed_ports("outside", "DMZ", PORTS))      # 인터넷 → DMZ 에서 허용되는 포트 목록을 출력한다
print(allowed_ports("DMZ", "inside", PORTS))       # DMZ → 내부망에서 허용되는 포트 목록을 출력한다
print(allowed_ports("inside", "DMZ", PORTS))       # 내부망 → DMZ 에서 허용되는 포트 목록을 출력한다
print(allowed_ports("outside", "inside", PORTS))   # 인터넷 → 내부망에서 허용되는 포트 목록을 출력한다
