LIMIT = 100                                       # 이 값(ms)을 넘으면 느리다고 본다

results = [                                       # 문제 2-2 ~ 2-4 에서 본 결과라고 가정합니다
    {"target": "8.8.8.8", "ms": 34},
    {"target": "1.1.1.1", "ms": 120},
    {"target": "192.0.2.1", "ms": None},          # None = 답이 오지 않았다
]

for r in results:                                 # 결과를 하나씩 꺼낸다
    # 1. r["ms"] 가 None 이면 f"[실패] {r['target']} 응답 없음" 을 출력하세요
    if r["ms"] is None:                           # 답이 없었으면 — 맨 먼저 본다
        print(f"[실패] {r['target']} 응답 없음")
    # 2. 아니고 r["ms"] 가 LIMIT 보다 크면 f"[느림] {r['target']} {r['ms']}ms" 를 출력하세요
    elif r["ms"] > LIMIT:                         # 기준보다 오래 걸렸으면
        print(f"[느림] {r['target']} {r['ms']}ms")
    # 3. 그 밖에는 f"[정상] {r['target']} {r['ms']}ms" 를 출력하세요
    else:                                         # 그 밖은 정상
        print(f"[정상] {r['target']} {r['ms']}ms")
