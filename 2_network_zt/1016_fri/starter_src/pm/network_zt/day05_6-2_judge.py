# 3 개 회선의 ping 결과 10 번씩 (단위: ms). None 은 응답이 없었던 것(손실)이다
LINES = {
    "회선 A": [22, 21, 23, 22, 21, 22, 23, 22, 21, 22],
    "회선 B": [18, 19, 95, 17, 18, 110, 19, 18, 92, 17],
    "회선 C": [40, 41, None, 42, 40, None, 41, 43, None, 40],
}

# 화상회의에 쓸 수 있는 기준 (이 수업에서 정한 값)
MAX_DELAY = 150    # 평균 지연 150 ms 이하
MAX_JITTER = 30    # 지터 30 ms 이하
MAX_LOSS = 1       # 손실률 1 % 이하

def measure(data):
    # 1. 응답을 받은 값만 got 리스트에 모은다
    got = []
    for v in data:
        if v != None:
            got.append(v)
    # 2. 평균 지연
    delay = sum(got) / len(got)
    # 3. 지터 = 이웃한 두 값의 차이의 평균
    total = 0
    for i in range(1, len(got)):
        total = total + abs(got[i] - got[i - 1])
    jitter = total / (len(got) - 1)
    # 4. 손실률
    loss = (len(data) - len(got)) / len(data) * 100
    return delay, jitter, loss

for name in LINES:
    delay, jitter, loss = measure(LINES[name])

    # 5. 세 기준을 모두 지켰는지 ok 에 담는다. 여기를 직접 씁니다
    ok = False   # 이 줄의 False 를 「세 기준을 모두 지키면 True」가 되는 식으로 바꾼다
    # 6. 어느 기준에 걸렸는지 모은다 (이미 채워져 있음)
    reasons = []
    if delay > MAX_DELAY:
        reasons.append("지연")
    if jitter > MAX_JITTER:
        reasons.append("지터")
    if loss > MAX_LOSS:
        reasons.append("손실")

    # 7. 결과를 출력한다
    if ok:
        print(name, "→ 적합")
    else:
        print(name, "→ 부적합 (걸린 기준:", ", ".join(reasons) + ")")
