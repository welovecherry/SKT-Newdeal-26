# 9월 28일 (월) · 정답 모음

실습 중에 막혔을 때 보는 문서입니다. **먼저 스스로 해 보고** 펼쳐 보세요.
들여쓰기는 **네 칸**입니다. 코드는 회색 칸을 통째로 복사하면 그대로 들어갑니다.

## 오전 · 2~4교시 — 예외처리와 로깅

### 정답 2-1

`['09:01', 'kim01', 'LOGIN_OK']`

### 정답 2-2

`IndexError: list index out of range`

### 정답 2-3

```python
line = "09:05,admin,LOGIN_FAIL,10.0.9.8"
parts = line.split(",")

print(parts)
```

### 정답 2-4

```python
line = "09:05,admin,LOGIN_FAIL,10.0.9.8"
parts = line.split(",")

print(parts[1])
```

### 정답 2-5

```python
line = "09:05,admin,LOGIN_FAIL,10.0.9.8"
parts = line.split(",")

print(parts[0], parts[3])
```

### 정답 2-6

`숫자가 아닙니다 · 프로그램은 계속 돌아갑니다`

### 정답 2-7

`kim01 LOGIN_OK · 깨진 줄 건너뜀: 03:22,hacker · lee02 LOGIN_FAIL · 끝까지 읽었습니다`

### 정답 2-8

```python
line = "09:41,guest"
parts = line.split(",")

try:
    print(parts[3])
except IndexError:
    print("칸이 모자랍니다")

print("확인 끝")
```

### 정답 2-9

```python
with open("sample_logs_broken.csv", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(",")
        try:
            print(parts[1], parts[3])
        except IndexError:
            pass
```

### 정답 2-10

```python
broken_count = 0

with open("sample_logs_broken.csv", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(",")
        try:
            parts[3]
        except IndexError:
            broken_count = broken_count + 1

print(f"깨진 줄 {broken_count}건")
```

### 정답 ⭐2-1

```python
line = "09:05,admin,LOGIN_FAIL,10.0.9.8"
parts = line.split(",")

print(f"{parts[1]} 의 접속 IP 는 {parts[3]} 입니다")
```

### 정답 ⭐2-2

```python
line = "09:05,admin,LOGIN_FAIL,10.0.9.8"
parts = line.split(",")
time_parts = parts[0].split(":")

print(time_parts[0])
print(time_parts[1])
```

### 정답 ⭐2-3

```python
broken_lines = []

with open("sample_logs_broken.csv", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(",")
        try:
            parts[3]
        except IndexError:
            broken_lines.append(line.strip())

print(broken_lines)
```

### 정답 ⭐2-4

```python
logs = []

with open("sample_logs_broken.csv", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(",")
        try:
            logs.append({"time": parts[0], "user": parts[1], "event": parts[2], "ip": parts[3]})
        except IndexError:
            pass

print(f"정상 로그 {len(logs)}건")
```

### 정답 ⭐2-5

```python
def parse_line(line):
    parts = line.strip().split(",")
    return {"time": parts[0], "user": parts[1], "event": parts[2], "ip": parts[3]}

logs = []

with open("sample_logs_broken.csv", encoding="utf-8") as f:
    for line in f:
        try:
            logs.append(parse_line(line))
        except IndexError:
            pass

print(f"정상 로그 {len(logs)}건")
```

### 정답 3-1

`ValueError: invalid literal for int() with base 10: '??'`

### 정답 3-2

`시각을 읽을 수 없습니다`

### 정답 3-3

```python
time = "21:30"

print(int(time.split(":")[0]))
```

### 정답 3-4

```python
line = "03:22,hacker,LOGIN_FAIL,10.0.9.9"
parts = line.split(",")

print(int(parts[0].split(":")[0]))
```

### 정답 3-5

```python
line = "03:22,hacker,LOGIN_FAIL,10.0.9.9"
parts = line.split(",")
hour = int(parts[0].split(":")[0])

if hour >= 0 and hour <= 6:
    print("야간")
```

### 정답 3-6

`9 10.0.3.21 · 시각이 깨진 줄: ??:??,unknown,LOGIN_FAIL · 칸이 모자란 줄: 09:41,guest`

### 정답 3-7

`9 · --- 한 줄 확인 끝 · 읽을 수 없음 · --- 한 줄 확인 끝`

### 정답 3-8

```python
with open("sample_logs_broken.csv", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(",")
        try:
            hour = int(parts[0].split(":")[0])
            if hour >= 0 and hour <= 6:
                print(parts[1])
        except ValueError:
            pass
        except IndexError:
            pass
```

### 정답 3-9

```python
bad_time = 0
bad_column = 0

with open("sample_logs_broken.csv", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(",")
        try:
            int(parts[0].split(":")[0])
            parts[3]
        except ValueError:
            bad_time = bad_time + 1
        except IndexError:
            bad_column = bad_column + 1

print(f"시각이 깨진 줄 {bad_time}건")
print(f"칸이 모자란 줄 {bad_column}건")
```

### 정답 3-10

```python
try:
    with open("sample_logs_2025.csv", encoding="utf-8") as f:
        print(f.readline())
except FileNotFoundError:
    print("파일이 없습니다")
finally:
    print("확인 끝")
```

### 정답 ⭐3-1

```python
times = ["09:01", "03:22", "21:30"]

for time in times:
    print(int(time.split(":")[0]))
```

### 정답 ⭐3-2

```python
times = ["09:01", "03:22", "21:30"]

for time in times:
    hour = int(time.split(":")[0])
    if hour >= 0 and hour <= 6:
        print(hour, "야간")
    else:
        print(hour, "주간")
```

### 정답 ⭐3-3

```python
bad_time = []
bad_column = []

with open("sample_logs_broken.csv", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(",")
        try:
            int(parts[0].split(":")[0])
            parts[3]
        except ValueError:
            bad_time.append(line.strip())
        except IndexError:
            bad_column.append(line.strip())

print(bad_time)
print(bad_column)
```

### 정답 ⭐3-4

```python
def parse_line(line):
    parts = line.strip().split(",")
    return {
        "time": parts[0],
        "user": parts[1],
        "event": parts[2],
        "ip": parts[3],
        "hour": int(parts[0].split(":")[0]),
    }

logs = []

with open("sample_logs_broken.csv", encoding="utf-8") as f:
    for line in f:
        try:
            logs.append(parse_line(line))
        except ValueError:
            pass
        except IndexError:
            pass

print(f"정상 로그 {len(logs)}건")
```

### 정답 ⭐3-5

```python
tried = 0
logs = []

with open("sample_logs_broken.csv", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(",")
        try:
            int(parts[0].split(":")[0])
            parts[3]
            logs.append(parts[1])
        except ValueError:
            pass
        except IndexError:
            pass
        finally:
            tried = tried + 1

print(f"시도한 줄 {tried}건")
print(f"정상 로그 {len(logs)}건")
```

### 정답 4-1

`화면에는 이 줄만 보입니다`

### 정답 4-2

`WARNING 이 줄은 남을까요 — 한 줄만`

### 정답 4-3

새 셀에 그대로 붙여 넣고 실행합니다.

```python
%%writefile my_log.py
import logging

logging.basicConfig(
    filename="my.log",
    format="%(asctime)s %(levelname)s %(message)s",
    encoding="utf-8",
)

logging.warning("첫 기록")
```

### 정답 4-4

새 셀에 그대로 붙여 넣고 실행합니다.

```python
%%writefile my_log.py
import logging

logging.basicConfig(
    filename="my.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    encoding="utf-8",
)

logging.info("시작")
logging.warning("주의")
logging.error("오류")
```

### 정답 4-5

```python
print("!python my_log.py 를 한 번 더 실행한 뒤 !cat my.log 로 봅니다.")
print("logging 은 언제나 파일 끝에 덧붙입니다. 세 줄이 여섯 줄이 됩니다.")
```

### 정답 4-6

`정상 로그 17건`

### 정답 4-7

`파서 시작 · 깨진 줄 건너뜀 5줄 · 정상 로그 17건 처리 완료`

### 정답 4-8

```python
code = """import logging

logging.basicConfig(
    filename="agent.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    encoding="utf-8",
)

logging.info("집계 시작")

count = 0
with open("sample_logs.csv", encoding="utf-8") as f:
    for line in f:
        count = count + 1

logging.info(f"집계 완료 {count}건")
print(count)
"""

with open("count_logs.py", "w", encoding="utf-8") as f:
    f.write(code)

print("count_logs.py 를 만들었습니다. 아래 두 줄을 각각 새 셀에서 실행하세요.")
print("!python count_logs.py")
print("!cat agent.log")
```

### 정답 4-9

```python
code = """import logging
from collections import Counter

logging.basicConfig(
    filename="agent.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    encoding="utf-8",
)


def parse_line(line):
    parts = line.strip().split(",")
    return {"time": parts[0], "user": parts[1], "event": parts[2], "ip": parts[3]}


logging.info("파서 시작: sample_logs_broken.csv")

logs = []
with open("sample_logs_broken.csv", encoding="utf-8") as f:
    for line in f:
        try:
            logs.append(parse_line(line))
        except IndexError:
            logging.warning(f"깨진 줄 건너뜀: {line.strip()}")

logging.info(f"정상 로그 {len(logs)}건 처리 완료")

failed_users = []
for log in logs:
    if log["event"] == "LOGIN_FAIL":
        failed_users.append(log["user"])

counted = Counter(failed_users)
for user in counted:
    if counted[user] >= 3:
        print(f"확인 필요: {user} — 실패 {counted[user]}회")
"""

with open("log_parser.py", "w", encoding="utf-8") as f:
    f.write(code)

print("log_parser.py 를 만들었습니다. 새 셀에서 !python log_parser.py 를 실행하세요.")
```

### 정답 4-10

새 셀에 그대로 붙여 넣고 실행합니다.

```python
맨 앞 준비 셀을 실행했다면 이미 드라이브에 저장돼 있습니다.

확인
   !ls
   !python log_parser.py   → 정상 로그 17건

안 보이면
   준비 셀(%cd /content/drive/MyDrive/agent_core)을 실행하지 않은 것입니다.
   그 셀을 실행한 뒤 데이터 셀과 %%writefile log_parser.py 셀을 다시 실행합니다.
```

### 정답 ⭐4-1

새 셀에 그대로 붙여 넣고 실행합니다.

```python
%%writefile only_error.py
import logging

logging.basicConfig(
    filename="only_error.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s",
    encoding="utf-8",
)

logging.info("시작")
logging.warning("주의")
logging.error("오류")
```

### 정답 ⭐4-2

새 셀에 그대로 붙여 넣고 실행합니다.

```python
%%writefile short_format.py
import logging

logging.basicConfig(
    filename="short.log",
    format="%(asctime)s %(message)s",
    encoding="utf-8",
)

logging.warning("깨진 줄 건너뜀")
```

### 정답 ⭐4-3

새 셀에 그대로 붙여 넣고 실행합니다.

```python
parse_line 안에 hour 를 추가하고, 부르는 쪽 except 를 둘로 나눕니다.

def parse_line(line):
    parts = line.strip().split(",")
    return {"time": parts[0], "user": parts[1], "event": parts[2],
            "ip": parts[3], "hour": int(parts[0].split(":")[0])}

        try:
            logs.append(parse_line(line))
        except ValueError:
            logging.warning(f"시각이 깨진 줄: {line.strip()}")
        except IndexError:
            logging.warning(f"칸이 모자란 줄: {line.strip()}")
```

### 정답 ⭐4-4

새 셀에 그대로 붙여 넣고 실행합니다.

```python
logging.info("파서 시작")

try:
    with open("sample_logs_2025.csv", encoding="utf-8") as f:
        for line in f:
            pass
except FileNotFoundError:
    logging.error("로그 파일을 찾을 수 없음")
```

### 정답 ⭐4-5

```python
warning_count = 0

with open("agent.log", encoding="utf-8") as f:
    for line in f:
        if "WARNING" in line:
            warning_count = warning_count + 1

print(f"경고 {warning_count}건")
```


## 오후 · 5~8교시 — 중첩 자료구조와 JSON

### 정답 5-1

`{'time': '09:01', 'user': 'kim01', 'event': 'LOGIN_OK', 'ip': '10.0.3.21'}`

### 정답 5-2

`admin`

### 정답 5-3

```python
logs = [
    {"time": "09:01", "user": "kim01", "event": "LOGIN_OK", "ip": "10.0.3.21"},
    {"time": "09:05", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
]

print(logs[1]["event"])
```

### 정답 5-4

```python
logs = [
    {"time": "09:01", "user": "kim01", "event": "LOGIN_OK", "ip": "10.0.3.21"},
    {"time": "09:05", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
    {"time": "09:12", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
    {"time": "09:18", "user": "lee02", "event": "LOGIN_FAIL", "ip": "10.0.7.5"},
    {"time": "09:21", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
]

for log in logs:
    print(log["user"])
```

### 정답 5-5

```python
logs = [
    {"time": "09:01", "user": "kim01", "event": "LOGIN_OK", "ip": "10.0.3.21"},
    {"time": "09:05", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
    {"time": "09:12", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
    {"time": "09:18", "user": "lee02", "event": "LOGIN_FAIL", "ip": "10.0.7.5"},
    {"time": "09:21", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
]

for log in logs:
    if log["event"] == "LOGIN_FAIL":
        print(log["user"], log["ip"])
```

### 정답 5-6

```python
logs = [
    {"time": "09:01", "user": "kim01", "event": "LOGIN_OK", "ip": "10.0.3.21"},
    {"time": "09:05", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
    {"time": "09:12", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
    {"time": "09:18", "user": "lee02", "event": "LOGIN_FAIL", "ip": "10.0.7.5"},
    {"time": "09:21", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
]

fail_count = 0

for log in logs:
    if log["event"] == "LOGIN_FAIL":
        fail_count = fail_count + 1

print(f"실패 {fail_count}건")
```

### 정답 5-7

`{'fail': 3, 'ip': '10.0.9.8'}`

### 정답 5-8

`3`

### 정답 5-9

```python
report = {
    "admin": {"fail": 3, "ip": "10.0.9.8"},
    "lee02": {"fail": 1, "ip": "10.0.7.5"},
}

print(report["lee02"]["ip"])
```

### 정답 5-10

```python
report = {
    "admin": {"fail": 3, "ip": "10.0.9.8"},
    "lee02": {"fail": 1, "ip": "10.0.7.5"},
}

for user in report:
    print(user, report[user]["fail"])
```

### 정답 5-11

```python
report = {
    "admin": {"fail": 3, "ip": "10.0.9.8"},
    "lee02": {"fail": 1, "ip": "10.0.7.5"},
}

for user in report:
    if report[user]["fail"] >= 2:
        print(f"확인 필요: {user}")
```

### 정답 5-12

```python
report = {
    "admin": {"fail": 3, "ip": "10.0.9.8"},
    "lee02": {"fail": 1, "ip": "10.0.7.5"},
}

report["park03"] = {"fail": 0, "ip": "10.0.4.11"}

print(report)
```

### 정답 ⭐5-1

```python
logs = [
    {"time": "09:01", "user": "kim01", "event": "LOGIN_OK", "ip": "10.0.3.21"},
    {"time": "09:05", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
    {"time": "09:12", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
    {"time": "09:18", "user": "lee02", "event": "LOGIN_FAIL", "ip": "10.0.7.5"},
    {"time": "09:21", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
]

failed_users = []

for log in logs:
    if log["event"] == "LOGIN_FAIL":
        failed_users.append(log["user"])

print(failed_users)
```

### 정답 ⭐5-2

```python
logs = [
    {"time": "09:01", "user": "kim01", "event": "LOGIN_OK", "ip": "10.0.3.21"},
    {"time": "09:05", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
    {"time": "09:12", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
    {"time": "09:18", "user": "lee02", "event": "LOGIN_FAIL", "ip": "10.0.7.5"},
    {"time": "09:21", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
]

report = {}

for log in logs:
    if log["event"] == "LOGIN_FAIL":
        user = log["user"]
        if user in report:
            report[user]["fail"] = report[user]["fail"] + 1
        else:
            report[user] = {"fail": 1}

print(report)
```

### 정답 6-1

`{"user": "admin", "fail": 3}`

### 정답 6-2

`{"user": "admin", "note": "\uc57c\uac04 \uc811\uc18d"}`

### 정답 6-3

```python
import json

log = {"user": "lee02", "fail": 1}

print(json.dumps(log))
```

### 정답 6-4

```python
import json

log = {"user": "lee02", "note": "야간 접속"}

print(json.dumps(log, ensure_ascii=False))
```

### 정답 6-5

```python
import json

log = {"user": "lee02", "note": "야간 접속"}

print(json.dumps(log, ensure_ascii=False, indent=2))
```

### 정답 6-6

```python
import json

text = '{"user": "admin", "fail": 3}'

back = json.loads(text)

print(back["fail"])
```

### 정답 6-7

`{"admin": 3}`

### 정답 6-8

`3`

### 정답 6-9

```python
import json

summary = {"date": "9/28", "note": "야간 실패 많음", "fail": 4}

with open("summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print("저장했습니다")
```

### 정답 6-10

```python
import json

summary = {"date": "9/28", "note": "야간 실패 많음", "fail": 4}
with open("summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

with open("summary.json", encoding="utf-8") as f:
    back = json.load(f)

print(back["note"])
```

### 정답 6-11

```python
import json

logs = [
    {"time": "09:01", "user": "kim01", "event": "LOGIN_OK", "ip": "10.0.3.21"},
    {"time": "09:05", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
    {"time": "09:12", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
    {"time": "09:18", "user": "lee02", "event": "LOGIN_FAIL", "ip": "10.0.7.5"},
    {"time": "09:21", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
]

with open("logs.json", "w", encoding="utf-8") as f:
    json.dump(logs, f, ensure_ascii=False, indent=2)

print("저장했습니다")
```

### 정답 6-12

```python
import json

logs = [
    {"time": "09:01", "user": "kim01", "event": "LOGIN_OK", "ip": "10.0.3.21"},
    {"time": "09:05", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
    {"time": "09:12", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
    {"time": "09:18", "user": "lee02", "event": "LOGIN_FAIL", "ip": "10.0.7.5"},
    {"time": "09:21", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
]
with open("logs.json", "w", encoding="utf-8") as f:
    json.dump(logs, f, ensure_ascii=False, indent=2)

with open("logs.json", encoding="utf-8") as f:
    back = json.load(f)

print(f"로그 {len(back)}건")
```

### 정답 ⭐6-1

```python
import json

logs = [
    {"time": "09:01", "user": "kim01", "event": "LOGIN_OK", "ip": "10.0.3.21"},
    {"time": "09:05", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
    {"time": "09:12", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
    {"time": "09:18", "user": "lee02", "event": "LOGIN_FAIL", "ip": "10.0.7.5"},
    {"time": "09:21", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
]

print(json.dumps(logs, ensure_ascii=False, indent=2))
```

### 정답 ⭐6-2

```python
import json

logs = [
    {"time": "09:01", "user": "kim01", "event": "LOGIN_OK", "ip": "10.0.3.21"},
    {"time": "09:05", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
    {"time": "09:12", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
    {"time": "09:18", "user": "lee02", "event": "LOGIN_FAIL", "ip": "10.0.7.5"},
    {"time": "09:21", "user": "admin", "event": "LOGIN_FAIL", "ip": "10.0.9.8"},
]
with open("logs.json", "w", encoding="utf-8") as f:
    json.dump(logs, f, ensure_ascii=False, indent=2)

with open("logs.json", encoding="utf-8") as f:
    back = json.load(f)

fail_count = 0
for log in back:
    if log["event"] == "LOGIN_FAIL":
        fail_count = fail_count + 1

print(f"실패 {fail_count}건")
```

### 정답 7-1

`LOGIN_FAIL`

### 정답 7-2

`2`

### 정답 7-3

```python
line = "09:12,admin,login_fail,10.0.9.8"
parts = line.split(",")

print(parts[2].upper())
```

### 정답 7-4

```python
line = "09:12,admin,login_fail,10.0.9.8"
parts = line.split(",")

log = {
    "time": parts[0],
    "user": parts[1],
    "event": parts[2].upper(),
    "ip": parts[3],
    "hour": int(parts[0].split(":")[0]),
}

print(log)
```

### 정답 7-5

```python
line = "09:41,guest"
parts = line.split(",")

if len(parts) >= 4:
    ip = parts[3]
else:
    ip = "unknown"

print(ip)
```

### 정답 7-6

```python
logs = []
skipped = 0

with open("sample_logs_raw.csv", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(",")
        if len(parts) < 3:
            skipped = skipped + 1
        else:
            if len(parts) >= 4:
                ip = parts[3]
            else:
                ip = "unknown"
            try:
                logs.append({
                    "time": parts[0],
                    "user": parts[1],
                    "event": parts[2].upper(),
                    "ip": ip,
                    "hour": int(parts[0].split(":")[0]),
                })
            except ValueError:
                skipped = skipped + 1

print(f"정규화 {len(logs)}건 · 버린 줄 {skipped}건")
```

### 정답 7-7

```python
REQUIRED = ["time", "user", "event", "ip"]

row = {"time": "09:41", "user": "guest", "event": "UNKNOWN"}

missing = []
for key in REQUIRED:
    if key not in row:
        missing.append(key)

print("빠진 항목:", missing)
```

### 정답 7-8

`저장 완료`

### 정답 7-9

`{ "city": "seoul", "count": 3 } — 두 칸 들여쓴 여러 줄`

### 정답 7-10

```python
code = """import json

logs = []

with open("sample_logs_raw.csv", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(",")
        if len(parts) >= 3:
            if len(parts) >= 4:
                ip = parts[3]
            else:
                ip = "unknown"
            try:
                logs.append({
                    "time": parts[0],
                    "user": parts[1],
                    "event": parts[2].upper(),
                    "ip": ip,
                    "hour": int(parts[0].split(":")[0]),
                })
            except ValueError:
                pass

with open("normalized_logs.json", "w", encoding="utf-8") as f:
    json.dump(logs, f, ensure_ascii=False, indent=2)

print(f"정규화 {len(logs)}건")
"""

with open("normalize_logs.py", "w", encoding="utf-8") as f:
    f.write(code)

print("normalize_logs.py 를 만들었습니다. 새 셀에서 !python normalize_logs.py 를 실행하세요.")
```

### 정답 7-11

새 셀에 그대로 붙여 넣고 실행합니다.

```python
아래 두 줄을 각각 새 셀에서 실행합니다.
!python normalize_logs.py
!cat normalized_logs.json
```

### 정답 7-12

새 셀에 그대로 붙여 넣고 실행합니다.

```python
맨 앞 준비 셀을 실행했다면 이미 드라이브에 저장돼 있습니다.

확인
   !ls
   !python normalize_logs.py

안 보이면
   준비 셀(%cd /content/drive/MyDrive/agent_core)을 실행하지 않은 것입니다.
   그 셀을 실행한 뒤 데이터 셀과 %%writefile 셀을 다시 실행합니다.
```

### 정답 ⭐7-1

```python
logs = []
with open("sample_logs_raw.csv", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(",")
        if len(parts) >= 3:
            if len(parts) >= 4:
                ip = parts[3]
            else:
                ip = "unknown"
            try:
                logs.append({"time": parts[0], "user": parts[1],
                             "event": parts[2].upper(), "ip": ip,
                             "hour": int(parts[0].split(":")[0])})
            except ValueError:
                pass

for log in logs:
    if log["event"] == "LOGIN_FAIL" and log["hour"] >= 0 and log["hour"] <= 6:
        print(log["user"], log["time"])
```

### 정답 ⭐7-2

```python
import json

logs = []
with open("sample_logs_raw.csv", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(",")
        if len(parts) >= 3:
            if len(parts) >= 4:
                ip = parts[3]
            else:
                ip = "unknown"
            try:
                logs.append({"time": parts[0], "user": parts[1],
                             "event": parts[2].upper(), "ip": ip,
                             "hour": int(parts[0].split(":")[0])})
            except ValueError:
                pass

report = {}
for log in logs:
    if log["event"] == "LOGIN_FAIL":
        user = log["user"]
        if user in report:
            report[user] = report[user] + 1
        else:
            report[user] = 1

with open("report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(report)
```

