def to_bits(ip):                                  # IP 주소를 2진수 32칸 글자로 바꾸는 함수
    bits = ""                                     # 이어 붙일 빈 글자
    for part in ip.split("."):                    # 점으로 나눈 마디를 하나씩
        # 1. bits 뒤에 format(int(part), "08b") 를 이어 붙이세요
        bits = bits + format(int(part), "08b")    # 마디 하나를 여덟 칸으로 바꿔 붙인다
    return bits                                   # 32칸 글자를 돌려준다


ip = "192.168.10.25"                              # 내 IPv4 주소로 바꿔 봅니다
print(ip)
print(to_bits(ip))
print("길이:", len(to_bits(ip)))
