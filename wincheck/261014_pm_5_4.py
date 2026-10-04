TRUSTED = ["naver.com", "google.com", "kbstar.com"]   # 우리 회사가 쓰는 진짜 도메인
seen = ["nav3r.com", "google.com", "g00gle.com", "kbstar.com", "kb5tar.com"]

for name in seen:                                 # 로그에 나온 이름을 하나씩
    # 1. plain 에 name 의 0 을 o 로, 1 을 l 로, 3 을 e 로 바꾼 글자를 담으세요
    plain = name.replace("0", "o").replace("1", "l").replace("3", "e")   # 숫자를 닮은 글자로
    if name in TRUSTED:
        print("[정상]", name)
    # 2. 아니고 plain 이 TRUSTED 안에 있으면 「[사칭 의심] nav3r.com → naver.com 흉내」 를 출력하세요
    elif plain in TRUSTED:                        # 바꾸니 진짜와 같아지면
        print("[사칭 의심]", name, "→", plain, "흉내")
    else:
        print("[모름]", name)
