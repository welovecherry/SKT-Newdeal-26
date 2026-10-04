def show_tree(name):                              # 이름을 위층부터 한 층씩 보여 주는 함수
    parts = name.split(".")                       # ['www', 'example', 'com']
    print("루트 (.)")
    current = ""                                  # 지금까지 만든 이름
    for label in reversed(parts):                 # com → example → www 차례로
        # 1. current 가 비어 있으면 current 에 label 을, 아니면 label + "." + current 를 담으세요
        if current == "":                         # 첫 층(TLD)
            current = label
        else:                                     # 그 아래 층은 왼쪽에 붙인다
            current = label + "." + current
        print("  →", current)


show_tree("www.example.com")
show_tree("mail.google.co.kr")
