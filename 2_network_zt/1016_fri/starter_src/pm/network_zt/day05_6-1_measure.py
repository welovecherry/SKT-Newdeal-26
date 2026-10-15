# 3 개 회선의 ping 결과 10 번씩 (단위: ms). None 은 응답이 없었던 것(손실)이다
LINES = {
    "회선 A": [22, 21, 23, 22, 21, 22, 23, 22, 21, 22],
    "회선 B": [18, 19, 95, 17, 18, 110, 19, 18, 92, 17],
    "회선 C": [40, 41, None, 42, 40, None, 41, 43, None, 40],
}

def jitter(got):                          # 받은 값 리스트 got 로 지터를 구해 리턴하는 함수이다. 이 함수를 직접 만든다
    """
    한 줄: 이 함수가 하는 일을 여기에 씁니다
    입력: 이 함수가 받는 값을 여기에 씁니다
    리턴: 이 함수가 리턴하는 값을 여기에 씁니다
    """
    # 1. total 을 0 으로 시작한다
    # 2. for 와 range(1, len(got)) 로 위치 i 를 꺼내, i 번째 값과 바로 앞 값의 차이의 절댓값을 total 에 더한다
    # 3. total 을 (got 의 개수 - 1) 로 나눈 값을 리턴한다
    return 0                              # ← 계산을 만들기 전에 넣어 둔 임시 값이다. 이 줄을 지우고 위 1 ~ 3 을 코드로 쓴다 (4줄 이하)

def measure(name, data):                  # 회선 하나의 지연 · 지터 · 손실을 구해 출력하는 함수이다
    got = []                              # 응답을 받은 값만 모을 빈 리스트이다
    for v in data:                        # 응답 10 개를 하나씩 꺼낸다
        if v != None:                     # 응답이 있으면 (None 이 아니면)
            got.append(v)                 # got 에 담는다

    delay = sum(got) / len(got)           # 평균 지연 = 받은 값의 합 ÷ 받은 개수
    jitter_value = jitter(got)            # 위에서 만든 jitter 함수에 got 을 넘겨 지터를 받는다
    loss = (len(data) - len(got)) / len(data) * 100   # 손실률 = 못 받은 개수 ÷ 보낸 개수 × 100

    print(name, "| 지연", round(delay, 1), "ms | 지터", round(jitter_value, 1), "ms | 손실", round(loss), "%")   # 한 줄로 출력한다

for name in LINES:                        # 회선 이름을 하나씩 꺼낸다
    measure(name, LINES[name])            # 그 회선의 값을 measure 에 넘긴다
