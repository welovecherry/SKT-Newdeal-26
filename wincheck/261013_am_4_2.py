def smallest_prefix(required):                    # 장비 수를 받아 CIDR 숫자를 돌려준다
    for host_bits in range(2, 33):                # 호스트 칸을 2칸부터 하나씩 늘려 본다
        # 1. 2 ** host_bits - 2 가 required 이상이면 32 - host_bits 를 return 하세요
        if 2 ** host_bits - 2 >= required:        # 이 칸 수로 충분하면
            return 32 - host_bits                 # 나머지가 네트워크 칸 = CIDR 숫자


for name, count in [("보안팀", 10), ("운영팀", 25), ("개발팀", 50)]:
    print(name, count, f"/{smallest_prefix(count)}")
