# 10/12(월) 오후 · TCP 와 3-way handshake · Wireshark 첫 캡처 · 1일 차 보고서 — 실습

> **강사용 · 학생에게 나눠 주지 않습니다.** 모든 문제 바로 아래에 「정답」과 해설이 있습니다. 찾아 쓰기 표는 채워 두었습니다.
>
> **수업 전에 확인할 것**
> 1. Wireshark 가 설치돼 있는지(학원 PC 10/6 실측 — 통로 이름은 `이더넷 2`)
> 2. `curl http://example.com` 이 되는지(학원망에서 HTTP 차단 없음 — 10/6 실측)
> 3. 사진 저장(`Win + Shift + S`) 위치 — `network_zt` 폴더

오전에는 `netstat`(넷스탯 · 지금의 연결을 보여 주는 명령)에서 `ESTABLISHED`(이스태블리시드 · 연결된 상태)라는 글자를 봤습니다. 오후에는 그 연결이 **어떻게 맺어지고 어떻게 끝나는지**를 배우고, **Wireshark**(와이어샤크 · 오가는 패킷을 붙잡아 보여 주는 프로그램)로 실제 패킷을 눈으로 봅니다.

| 교시 | 무엇 | 쓰는 것 |
|---|---|---|
| 5교시 | TCP 와 UDP · 연결을 맺는 세 번의 신호(3-way handshake) · 끝내는 네 번 | 파이썬 · `netstat` |
| 6교시 | Wireshark 실행 · 첫 캡처 · 화면 읽기 · 필터 | Wireshark (아침 과제 8 에서 설치) |
| 7교시 | 내 연결을 직접 잡아 보고서로 남기기 | Wireshark · `curl` · 파이썬 |

**오늘 남기는 것:** `network_zt/day01_packet_analysis.md` 완성본(오전의 1번 표 + 오후의 캡처 사진 · 표) — 강의계획서의 1일 차 산출물입니다.

---

## 시작하기

### 이 파일을 여는 법

이 파일은 **카톡으로 받은 실습 안내**입니다. 노트북이 아니라 읽으면서 따라 하는 문서입니다.

1. 카톡에서 받은 이 파일(`261012_pm_tcp_wireshark.md`)을 `security-agent-toolkit` 안의 **`network_zt` 폴더**로 옮깁니다.
2. VS Code 왼쪽 목록에서 이 파일을 누르고, **`Ctrl + Shift + V`** 를 눌러 **미리보기**로 엽니다. 표 · 굵은 글씨 · 「답 보기」가 읽기 좋게 보입니다. (화면을 둘로 나눠 보려면 `Ctrl + K` 를 누른 뒤 `V`.)
3. 이 파일은 **읽기만** 합니다. 내가 적는 것은 그날 **보고서 파일**과 **`.py` 파일**입니다.
4. 코드나 명령을 복사할 때는 미리보기의 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 를 누릅니다.

### 오늘 시작할 때

0. 오늘 적는 것은 모두 **오전에 만든 `day01_packet_analysis.md` 하나에** 이어서 적습니다 — 문제 답은 `## 실습 기록`, 찾아 쓰기는 `## 찾아본 것`, 새 절은 `## 실습 기록` **위에** 붙입니다. 문제마다 「**적는 곳**」 줄을 봅니다.
1. 오전과 같은 터미널(Git Bash)을 씁니다. 줄 앞에 `$` 가 보이면 됩니다.
2. `network_zt` 폴더에서 시작합니다 — `cd network_zt`(이미 들어와 있으면 생략).
3. 이 문서의 화면 예시는 **모양을 보여 주는 예시**입니다. 주소 · 숫자는 내 화면의 값을 읽습니다.
4. 문제 앞의 **상자**를 먼저 읽습니다 — 🐍 문법 상자(파이썬) · 명령 상자(터미널) · Wireshark 상자 · 개념 상자. 문제 제목 아래 **어디서** 줄이 실습하는 곳입니다. `→` 는 하는 순서입니다. 막히면 **💡 힌트** → 맨 아래 **「정답」** 순서로 봅니다. ⭐도전은 선택입니다.

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">5교시 (14:00–14:50) · TCP 와 UDP · 3-way handshake</mark>

### 왜 필요한가

1. 오전에 본 4층(전송 계층)에는 데이터를 보내는 방식이 **두 가지** 있습니다 — TCP 와 UDP.
2. 웹 · 파일 · 1과목의 `requests.post` 는 TCP 입니다. TCP 는 보내기 전에 **세 번 신호를 주고받아 연결을 맺습니다.** 이것이 3-way handshake 입니다.
3. 관제 화면에 「연결을 시도만 하고 끝까지 안 맺는 패킷」이 쏟아지면 공격(포트 스캔 · 열린 포트를 차례로 두드려 찾는 공격 등)일 수 있습니다. 정상적인 세 번을 알아야 이상한 것이 보입니다.

### 5.1 TCP 와 UDP

| | TCP(티시피 · Transmission Control Protocol) | UDP(유디피 · User Datagram Protocol) |
|---|---|---|
| 연결 | 보내기 **전에 연결을 맺는다** | 연결 없이 **바로 보낸다** |
| 받았는지 확인 | 한다 — 안 왔으면 **다시 보낸다** | 안 한다 |
| 순서 | 번호로 **순서를 맞춘다** | 맞추지 않는다 |
| 속도 | 확인하느라 조금 느리다 | 빠르다 |
| 쓰는 곳 | 웹(HTTP 에이치티티피 · HTTPS 에이치티티피에스) · 파일 · 메일 · SSH(에스에스에이치 · 서버 원격 접속) | DNS(디엔에스 · 이름을 IP 로 바꾸는 조회) 조회 · 실시간 영상 · 게임 · 음성 통화 |

`ping`(핑) 은 둘 다 아닙니다. 오전에 본 **ICMP**(아이시엠피 · 「살아 있나」만 묻는 방식)라는 별도 방식입니다.

### 5.2 연결을 맺는 세 번, 끝내는 네 번

```
   내 PC                                서버
     │ ──── ① SYN ───────────────────▶ │   「연결하자」
     │ ◀─── ② SYN, ACK ────────────── │   「알았다. 나도 연결하자」
     │ ──── ③ ACK ───────────────────▶ │   「알았다」        → 이제 ESTABLISHED
     │          ( 데이터를 주고받는다 )          │
     │ ──── FIN ─────────────────────▶ │   「나는 다 보냈다」
     │ ◀─── ACK ───────────────────── │   「알았다」
     │ ◀─── FIN ───────────────────── │   「나도 다 보냈다」
     │ ──── ACK ─────────────────────▶ │   「알았다」        → 연결 끝
```

> 학생 문서에서는 아래 표의 일부 칸이 **[찾아 쓰기]** 로 비어 있습니다. 강사용에는 채운 표를 둡니다.

| 이름 | 읽는 법 · 원래 말 | 뜻 |
|---|---|---|
| SYN | 신 · synchronize | 연결하자 (번호를 맞추자) |
| ACK | 액 · acknowledge | 받았다 |
| FIN | 핀 · finish | 나는 다 보냈다 |
| RST | 리셋 · reset | 인사 없이 **바로 끊는다** — 닫힌 포트에 접속하거나 방화벽이 끊을 때 |

- **왜 맺을 때는 세 번인가:** 서버의 「알았다(ACK)」와 「나도 연결하자(SYN)」는 그 순간 둘 다 참이라 **한 신호에 같이 실을 수 있습니다** → ②번 하나.
- **왜 끝낼 때는 네 번인가:** 서버는 「알았다」는 바로 답하지만, 아직 보낼 데이터가 남아 있을 수 있어 「나도 다 보냈다(FIN)」는 **나중에 따로** 보냅니다.
- 끝난 연결은 바로 사라지지 않고 잠시 **`TIME_WAIT`**(타임 웨이트) 상태로 남습니다. `netstat` 에서 자주 보입니다 — 이상한 것이 아닙니다.

### 5.3 연결 하나를 가리키는 네 값

| 값 | 어디에 적혀 있나 | 예 |
|---|---|---|
| 출발지 IP | IP 헤더(3층) | `192.168.0.15` |
| 출발지 포트 | TCP 헤더(4층) | `51234` — 내 PC 가 그때그때 고르는 **임시 포트**(49152~65535) |
| 목적지 IP | IP 헤더(3층) | `203.0.113.10` |
| 목적지 포트 | TCP 헤더(4층) | `443` — 서비스가 정해 둔 번호 |

**헤더**(header)는 데이터 앞에 붙는 「누가 · 누구에게 · 어떻게」 정보입니다. 층마다 하나씩 붙어서, 패킷 하나에 헤더가 여러 겹 있습니다.

#### 🐍 문법 상자 · 리스트에 값이 들었는지는 `in`

```python
flags = ["SYN", "ACK"]
print("SYN" in flags)       # True
print(flags == "SYN")       # False — 리스트와 글자는 같을 수 없다
```

| 쓰는 것 | 묻는 것 | 결과 |
|---|---|---|
| `"SYN" in flags` | 리스트 **안에** 그 값이 있나 | `True` |
| `flags == "SYN"` | 리스트 **전체가** 그 글자와 같은가 | 늘 `False` |

⚠ `==` 로 잘못 쓰면 <mark style="background:#ffcdd2; color:#1a1a1a; padding:0 4px; border-radius:3px">에러 없이</mark> `False` 만 나옵니다. 탐지 규칙이 조용히 아무것도 못 잡습니다.

---

### ✍️ 문제 5-1 · 무엇이 보일까요

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 실행하지 않고 머리로 예상합니다

아래 코드를 실행하면 무엇이 보일지 적어 보세요.

```python
packet = {"src_port": 51234, "dst_port": 443, "flags": ["SYN", "ACK"]}
print("ACK" in packet["flags"])
print(packet["flags"] == "ACK")
print(packet["dst_port"])
```

막히면 바로 위 문법 상자를 다시 봅니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답</mark>

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `True` · `False` · `443` 세 줄.</mark>

**왜** — `in` 은 리스트 안에 `"ACK"` 가 있는지 묻고, `==` 는 리스트 전체를 글자 `"ACK"` 와 비교하므로 늘 `False` 입니다.

**자주 틀리는 곳** — 둘째 줄도 `True` 라고 적기 쉽습니다. 리스트 `["SYN", "ACK"]` 와 글자 `"ACK"` 는 같을 수 없습니다.

**관제에서는** — 탐지 규칙에서 `==` 로 쓰면 에러 없이 아무것도 못 잡으므로, 플래그 검사는 `in` 으로 씁니다.

**강사 메모** — 둘째 줄이 왜 에러가 아니냐고 묻는 학생이 많습니다. 「파이썬은 종류가 다른 두 값을 `==` 로 비교하면 에러 없이 `False` 를 준다」고 한 줄로 답합니다. 답을 맞힌 뒤 「`"ACK"` 를 `"FIN"` 으로 바꾸면 첫 줄은?」(`False`)을 바로 물어 확인합니다.

---

### ✍️ 문제 5-2 · TCP 일까 UDP 일까

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 명령 없이 생각해서 답하기 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 실습 기록` 에 `- 5-2: …` 한 줄

아래 다섯 가지가 TCP 인지 UDP 인지(또는 둘 다 아닌지) 적으시오. 명령은 입력하지 않습니다.

| # | 하는 일 |
|---|---|
| ① | 카카오톡으로 사진 파일 보내기 |
| ② | 유튜브 실시간 방송 보기 |
| ③ | 1과목에서 `requests.post` 로 LLM 부르기 |
| ④ | `google.com` 의 IP 를 묻기(DNS 조회) |
| ⑤ | `ping 8.8.8.8` |

| | |
|---|---|
| 🎯 나와야 하는 결과 | ① TCP ② UDP ③ TCP ④ UDP ⑤ 둘 다 아님(ICMP) |

**💡 힌트**

1. 하나라도 빠지면 안 되는가(파일) → TCP. 조금 빠져도 빠른 게 중요한가(실시간) → UDP.
2. `requests.post` 는 웹(HTTPS) 요청입니다.
3. 5.1 표 아래 줄을 다시 봅니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 5-2</mark>

| # | 답 | 이유 |
|---|---|---|
| ① 사진 보내기 | TCP | 한 조각이라도 빠지면 파일이 깨진다 |
| ② 실시간 방송 | UDP | 조금 빠져도 끊기지 않는 게 중요하다 |
| ③ `requests.post` | TCP | 웹(HTTPS) 요청이다 |
| ④ DNS 조회 | UDP | 짧은 질문 하나 · 답 하나라 연결을 맺지 않는다 |
| ⑤ `ping` | 둘 다 아님 | ICMP 라는 별도 방식이다 |

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — ① TCP ② UDP ③ TCP ④ UDP ⑤ 둘 다 아님(ICMP)</mark>

**왜** — 하나라도 빠지면 안 되는 데이터는 받았는지 확인하고 다시 보내는 TCP, 빠른 게 중요한 데이터는 확인을 하지 않는 UDP 를 씁니다.

**자주 틀리는 곳** — ⑤ `ping` 을 TCP 로 적기 쉽습니다. `ping` 은 포트도 연결도 없는 ICMP 입니다.

**관제에서는** — DNS 조회는 UDP 53번이라, UDP 53번 조회가 갑자기 많아지면 먼저 살펴봅니다.

**강사 메모** — ②번을 TCP 로 적는 학생이 많고 「유튜브도 TCP 를 쓰지 않나요?」라는 질문이 나올 수 있습니다. 실제 서비스는 방식이 섞여 있을 수 있고, 이 문제는 「조금 빠져도 되는가」로 고르는 연습이라고 답합니다. ⑤번은 오전에 본 ICMP 와 이어서 짚습니다.

---

### ✍️ 문제 5-3 · 세 번의 순서 맞히기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 명령 없이 생각해서 답하기 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 실습 기록` 에 `- 5-3: …` 한 줄

뒤섞인 세 패킷의 **올바른 순서**와 **방향**(내 PC → 서버 / 서버 → 내 PC)을 적으시오.

```
(가) [ACK]
(나) [SYN]
(다) [SYN, ACK]
```

| | |
|---|---|
| 🎯 나와야 하는 결과 | (나) 내 PC → 서버 · (다) 서버 → 내 PC · (가) 내 PC → 서버 |

**💡 힌트**

1. 연결은 내 PC 가 먼저 청합니다.
2. 서버는 「받았다」와 「나도 연결하자」를 한 번에 보냅니다.
3. 마지막 「받았다」를 보내면 `ESTABLISHED` 가 됩니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 5-3</mark>

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — (나) 내 PC → 서버 · (다) 서버 → 내 PC · (가) 내 PC → 서버</mark>

**왜** — 내 PC 가 `[SYN]` 으로 먼저 청하고, 서버는 「받았다(ACK)」와 「나도 연결하자(SYN)」를 한 줄에 실어 답합니다. 내 PC 의 마지막 `[ACK]` 뒤에 `ESTABLISHED` 가 됩니다.

**자주 틀리는 곳** — (다) `[SYN, ACK]` 를 내 PC 가 보낸다고 적기 쉽습니다. `[SYN, ACK]` 는 처음 `[SYN]` 을 받은 쪽(서버)이 보냅니다.

**관제에서는** — `[SYN]` 만 쏟아지고 세 번째 `[ACK]` 가 없으면 포트 스캔 같은 공격을 의심합니다.

**강사 메모** — (다)를 누가 보내는지를 가장 강조합니다. 「세 번째 `[ACK]` 뒤에 바로 데이터가 가나요?」에는 「네, `ESTABLISHED` 가 된 뒤 데이터를 주고받습니다」라고 답합니다. 7-2 에서 이 세 줄을 Wireshark 로 직접 본다고 미리 알려 둡니다.

---

### ✍️ 문제 5-4 · 연결 상태를 세기 (`state_count.py`)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — VS Code 에서 `state_count.py` 만들기 → 터미널에서 `python state_count.py` 실행

`netstat` 결과를 옮겨 온 리스트에서 **상태마다 몇 개인지** 세시오. `network_zt` 에 `state_count.py` 를 만들어 붙여 넣고, 번호 주석 아래를 채운 뒤 `python state_count.py` 를 입력합니다.

#### 🐍 문법 상자 · 사전으로 세기 `count.get(키, 0) + 1`

```python
# ── 강사용: 정답을 채운 코드입니다 ──
conns = [                                         # netstat -n 의 상태 칸을 옮겨 왔다고 가정합니다
    {"peer": "203.0.113.10:443", "state": "ESTABLISHED"},
    {"peer": "198.51.100.7:443", "state": "ESTABLISHED"},
    {"peer": "203.0.113.10:443", "state": "TIME_WAIT"},
    {"peer": "192.0.2.53:53", "state": "TIME_WAIT"},
    {"peer": "198.51.100.20:443", "state": "SYN_SENT"},
]
count = {}                                        # 상태마다 센 수를 담을 빈 사전

for c in conns:                                   # 연결을 하나씩 꺼낸다
    # 1. count 의 c["state"] 키에 지금까지 센 수 + 1 을 담으세요 (.get 을 씁니다)
    count[c["state"]] = count.get(c["state"], 0) + 1   # 처음 보는 상태면 0 에서 시작

for state in count:                               # 센 상태를 하나씩
    print(state, count[state])                    # 상태와 개수
```

| 쓰는 것 | 뜻 |
|---|---|
| `count.get(s, 0)` | 지금까지 센 수. 처음 보는 키면 `0` |
| `count[s] = … + 1` | 하나 더해서 다시 담는다 (1과목 9/23) |

⚠ `count[s] = count[s] + 1` 로 쓰면 처음 보는 키에서 `KeyError` 가 납니다.

```python
# ── 미리 채워 둔 줄입니다. 고치지 않습니다 ──
conns = [                                         # netstat -n 의 상태 칸을 옮겨 왔다고 가정합니다
    {"peer": "203.0.113.10:443", "state": "ESTABLISHED"},
    {"peer": "198.51.100.7:443", "state": "ESTABLISHED"},
    {"peer": "203.0.113.10:443", "state": "TIME_WAIT"},
    {"peer": "192.0.2.53:53", "state": "TIME_WAIT"},
    {"peer": "198.51.100.20:443", "state": "SYN_SENT"},
]
count = {}                                        # 상태마다 센 수를 담을 빈 사전
# ── 여기까지 ──

for c in conns:                                   # 연결을 하나씩 꺼낸다
    # 1. count 의 c["state"] 키에 지금까지 센 수 + 1 을 담으세요 (.get 을 씁니다)


for state in count:                               # 센 상태를 하나씩
    print(state, count[state])                    # 상태와 개수
```

**파일을 만들고 실행합니다**

1. VS Code 왼쪽 목록에서 `network_zt` 폴더를 오른쪽 클릭 › **New File** › 이름 `state_count.py` 를 입력하고 Enter 를 누릅니다.
2. 위 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 로 복사해 파일에 붙여 넣은 뒤, 번호 주석 아래를 채웁니다. 저장은 자동입니다.
3. 터미널에 아래 명령을 입력합니다. 터미널의 줄 위에 `…/network_zt` 가 보여야 합니다. 아니면 먼저 `cd network_zt` 를 입력합니다.

```bash
python state_count.py
```

4. 고친 뒤에는 같은 명령을 다시 입력합니다. 터미널에서 **↑(위 화살표)** 를 누르면 방금 입력한 명령이 다시 나옵니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `ESTABLISHED 2` · `TIME_WAIT 2` · `SYN_SENT 1` |

**💡 힌트**

1. 바로 위 문법 상자의 셋째 줄과 같은 모양입니다.
2. 키는 `c["state"]` 입니다.
3. `SYN_SENT`(신 센트)는 SYN 을 보내고 답을 기다리는 중 — 이게 많이 쌓이면 상대가 응답하지 않는 것입니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 5-4</mark>

(코드는 위 문제 칸에 채워 두었습니다.)

💻 **터미널에 입력합니다.**

```bash
python state_count.py
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `ESTABLISHED 2` · `TIME_WAIT 2` · `SYN_SENT 1`</mark>

**왜** — `count.get(키, 0)` 은 처음 보는 상태면 `0` 을 주므로, 상태가 나올 때마다 지금까지 센 수에 1 을 더해 다시 담습니다.

**자주 틀리는 곳** — `.get` 없이 `count[c["state"]] + 1` 로 쓰면 처음 보는 상태에서 `KeyError` 가 납니다.

**관제에서는** — `SYN_SENT` 가 많이 쌓이면 상대가 응답하지 않는 것이라, 상태별 개수를 먼저 세어 봅니다.

**강사 메모** — 「왜 `ESTABLISHED` 부터 나오나요?」에는 「사전은 처음 넣은 키 순서대로 꺼낸다」고 답합니다. 학생 화면에서는 1번 줄이 `for` 안으로 들여쓰기 됐는지 봅니다. 들여쓰기가 빠지면 `for` 안이 비어 `IndentationError` 가 납니다.

---

### ✍️ 문제 5-5 · 같은 서버로 간 두 연결은 무엇이 다른가

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 브라우저에서 같은 사이트를 탭 두 개로 열기 → 터미널에서 명령 실행 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 실습 기록` 에 `- 5-5: …` 한 줄

브라우저로 같은 사이트를 **탭 두 개**로 연 뒤 `netstat -n` 을 입력하고, 외부 주소가 **같은** 연결 두 줄을 찾아 **무엇이 다른지** 적으시오.

| | |
|---|---|
| 🎯 나와야 하는 결과 | 외부 주소(목적지 IP · 포트)는 같고 **로컬 주소 끝의 포트**(임시 포트)만 다르다 — 예: `192.168.0.15:51234` 와 `192.168.0.15:51240` |

**💡 힌트**

1. 5.3 표의 네 값 가운데 무엇이 달라야 두 연결을 구별할 수 있을까요?
2. 줄이 너무 많으면 `netstat -n | grep 443` 으로 443 줄만 봅니다.
3. 같은 줄이 안 보이면 탭을 하나 더 열고 다시 입력합니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 5-5</mark>

💻 **터미널에 입력합니다.**

```bash
netstat -n
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 외부 주소(목적지 IP · 포트)는 같고 로컬 주소 끝의 포트(임시 포트)만 다르다 — 예: `192.168.0.15:51234` 와 `192.168.0.15:51240`</mark>

**왜** — 연결 하나는 네 값(출발지 IP · 출발지 포트 · 목적지 IP · 목적지 포트)으로 구별됩니다. 목적지와 내 IP 가 같으니, 내 PC 가 연결마다 다른 임시 포트를 골라 구별합니다.

**자주 틀리는 곳** — 로컬 주소의 IP 가 다르다고 적기 쉽습니다. 같은 PC 라 IP 는 같고 `:` 뒤 포트만 다릅니다.

**관제에서는** — 한 PC 가 한 서버로 연 연결 수를 세어, 연결을 지나치게 많이 여는 PC 를 찾습니다.

**강사 메모** — 「임시 포트는 누가 정하나요?」에는 「내 PC 의 운영체제가 49152~65535 사이에서 고른다」고 답합니다. 브라우저가 연결 하나를 두 탭에 같이 쓰면 같은 외부 주소 줄이 하나만 보일 수 있으니, 힌트 3처럼 탭을 더 열게 합니다. 줄이 많아 못 찾는 학생에게는 `netstat -n | grep 443` 을 먼저 권합니다.

---

### ⭐ 도전 5-6 · 미니 패킷 필터 (`packet_filter.py`, 선택)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — VS Code 에서 `packet_filter.py` 만들기 → 터미널에서 `python packet_filter.py` 실행

캡처한 패킷 다섯 건에서 **SYN 이 든 것**만, 그리고 **서버 `203.0.113.10` 과 주고받은 것**만 골라 출력하시오. 6교시 Wireshark 필터가 하는 일을 직접 만들어 봅니다.

```python
# ── 강사용: 정답을 채운 코드입니다 ──
SERVER = "203.0.113.10"                           # 살펴볼 서버
packets = [                                       # 캡처한 패킷이라고 가정합니다
    {"no": 12, "src": "192.168.0.15", "dst": "203.0.113.10", "flags": ["SYN"]},
    {"no": 13, "src": "203.0.113.10", "dst": "192.168.0.15", "flags": ["SYN", "ACK"]},
    {"no": 14, "src": "192.168.0.15", "dst": "203.0.113.10", "flags": ["ACK"]},
    {"no": 15, "src": "192.168.0.15", "dst": "198.51.100.7", "flags": ["ACK"]},
    {"no": 16, "src": "192.168.0.15", "dst": "203.0.113.10", "flags": ["FIN", "ACK"]},
]

print("[SYN 필터]")
for p in packets:                                 # 패킷을 하나씩
    # 1. p["flags"] 안에 "SYN" 이 있으면 f"{p['no']} {p['src']} → {p['dst']} {p['flags']}" 를 출력하세요
    if "SYN" in p["flags"]:                       # 플래그 리스트 안에 SYN 이 있으면
        print(f"{p['no']} {p['src']} → {p['dst']} {p['flags']}")

print("[서버 대화 필터]")
for p in packets:
    # 2. p["src"] 가 SERVER 이거나 p["dst"] 가 SERVER 이면 같은 모양으로 출력하세요
    if p["src"] == SERVER or p["dst"] == SERVER:  # 보낸 쪽이든 받은 쪽이든 그 서버면
        print(f"{p['no']} {p['src']} → {p['dst']} {p['flags']}")
```

**파일을 만들고 실행합니다**

1. VS Code 왼쪽 목록에서 `network_zt` 폴더를 오른쪽 클릭 › **New File** › 이름 `packet_filter.py` 를 입력하고 Enter 를 누릅니다.
2. 위 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 로 복사해 파일에 붙여 넣은 뒤, 번호 주석 아래를 채웁니다. 저장은 자동입니다.
3. 터미널에 아래 명령을 입력합니다. 터미널의 줄 위에 `…/network_zt` 가 보여야 합니다. 아니면 먼저 `cd network_zt` 를 입력합니다.

```bash
python packet_filter.py
```

4. 고친 뒤에는 같은 명령을 다시 입력합니다. 터미널에서 **↑(위 화살표)** 를 누르면 방금 입력한 명령이 다시 나옵니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `[SYN 필터]` 아래 12 · 13 두 줄, `[서버 대화 필터]` 아래 12 · 13 · 14 · 16 네 줄 |

**💡 힌트**

1. 리스트 안에 있는지는 `in` 입니다(문법 상자).
2. 「이거나」는 `or` 입니다.
3. 6교시의 Wireshark 필터 `tcp.flags.syn == 1` 과 `ip.addr == 주소` 가 이 두 반복과 같은 일을 합니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 5-6</mark>

(코드는 위 문제 칸에 채워 두었습니다.)

💻 **터미널에 입력합니다.**

```bash
python packet_filter.py
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `[SYN 필터]` 아래 12 · 13 두 줄, `[서버 대화 필터]` 아래 12 · 13 · 14 · 16 네 줄</mark>

**왜** — 13번의 `["SYN", "ACK"]` 에도 SYN 이 들어 있어 `in` 이 잡습니다. 서버 필터는 보낸 쪽 · 받은 쪽을 둘 다 보므로 서버가 보낸 13번도 남습니다.

**자주 틀리는 곳** — `p["flags"] == ["SYN"]` 이나 `p["dst"] == SERVER` 만 쓰면 13번이 빠집니다.

**관제에서는** — Wireshark 의 `tcp.flags.syn == 1` · `ip.addr == 주소` 도 같은 조건으로 수많은 패킷에서 한 서버의 대화만 남깁니다.

**강사 메모** — 선택 문제라 먼저 끝난 학생만 풀게 하고, 다 같이 볼 때는 두 필터의 줄 수(2줄 · 4줄)만 맞춰 봅니다. 「Wireshark 처럼 `&&` · `||` 를 써도 되나요?」에는 「파이썬은 `and` · `or`, Wireshark 표시 필터는 `&&` · `||`」라고 답합니다. 13번이 두 필터에 모두 남는 이유를 학생 입으로 말하게 합니다.

### 5교시 한눈에

| 하려는 일 | 쓰는 것 |
|---|---|
| 연결을 맺는다 | SYN → SYN, ACK → ACK (3-way handshake) |
| 연결을 끝낸다 | FIN · ACK 두 쌍(네 번) · 급히 끊으면 RST |
| 연결 하나를 가리킨다 | 출발지 IP · 출발지 포트 · 목적지 IP · 목적지 포트 |
| 플래그가 있는지 본다 | `"SYN" in flags` |

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">6교시 (15:00–15:50) · Wireshark 실행 · 첫 캡처 · 필터</mark>

### 왜 필요한가

1. 5교시의 SYN · ACK 는 지금까지 **그림**이었습니다. Wireshark 는 내 PC 를 지나는 패킷을 붙잡아 **실제 값**으로 보여 줍니다.
2. 관제 · 침해 분석에서 「무슨 일이 있었나」를 확인하는 표준 도구입니다.
3. 캡처를 켜면 몇 초 만에 수백 줄이 쌓입니다. 그래서 **필터**(filter · 원하는 것만 남기는 조건)를 함께 배웁니다.

### 6.1 화면 읽기 — 세 칸

> ⚠ 학원 PC 의 Wireshark 메뉴는 **한국어**로 나옵니다(캡처 · 분석 · 통계 …). 아래는 한국어와 영어를 같이 적습니다.

| 칸 | 보여 주는 것 | 오늘 보는 것 |
|---|---|---|
| **위** — 패킷 목록 | 잡힌 패킷 한 줄씩. No · Time · Source · Destination · Protocol · Info | Protocol 이 `TCP` 인 줄, Info 의 `[SYN]` |
| **가운데** — 패킷 상세 | 고른 패킷의 헤더를 **층 순서대로** 펼침 | `Ethernet II`(이더넷 투 · 2층 MAC 주소) · `Internet Protocol Version 4`(IPv4 · 3층 IP 주소 · TTL 남은 거쳐 갈 횟수) · `Transmission Control Protocol`(TCP · 4층 포트 · 플래그) |
| **아래** — 바이트 | 실제 0과 1을 16진수(0~9 · A~F 로 세는 수)로 | 오늘은 보지 않음 |
| 맨 아래 상태 줄 | `패킷: 1234 · 표시됨: 56` (영문 `Packets` · `Displayed`) | 필터를 걸면 **표시됨**만 줄어든다 |

#### Wireshark 상자 · 표시 필터의 두 가지 모양

| 모양 | 예 | 뜻 |
|---|---|---|
| 이름만 | `tcp` · `udp` · `dns` · `http` | 그 종류만 남긴다 |
| `필드 == 값` | `tcp.port == 443` · `ip.addr == 203.0.113.10` | 그 칸이 그 값인 줄만 |
| 플래그 | `tcp.flags.syn == 1` · `tcp.flags.fin == 1` | SYN(또는 FIN)이 켜진 줄만 |
| 잇기 | `dns \|\| tcp.port == 443` · `tcp && ip.addr == …` | `\|\|` 는 또는, `&&` 는 그리고 |

| 필터 칸 색 | 뜻 |
|---|---|
| 초록 | 문법이 맞다 |
| 빨강 | 문법이 틀렸다(오타) |
| 노랑 | 문법은 맞지만 생각과 다르게 걸릴 수 있다 |

⚠ `ip.src`(출발지) · `ip.dst`(목적지) · `ip.addr`(둘 중 하나라도)는 다릅니다. <mark style="background:#ffcdd2; color:#1a1a1a; padding:0 4px; border-radius:3px">대화 전체</mark>를 보려면 `ip.addr` 입니다.

---

### ✍️ 문제 6-1 · 무엇이 보일까요

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 실행하지 않고 머리로 예상합니다

Wireshark 필터 칸에 아래 세 가지를 차례로 친다면, 칸이 각각 **무슨 색**이 될지 적어 보세요.

```
tcp
tpc
tcp.port == 443
```

막히면 바로 위 Wireshark 상자의 색 표를 봅니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답</mark>

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 초록 · 빨강 · 초록.</mark>

**왜** — Wireshark 는 친 글자를 아는 이름 · 문법과 맞춰 보고 색으로 알려 줍니다. `tpc` 는 없는 이름(오타)이라 빨강입니다. 6-5 에서 직접 쳐 보며 맞춰 봅니다.

**자주 틀리는 곳** — 빨간 칸인 채로 Enter 를 누르면 필터가 걸리지 않습니다. 색부터 보고 Enter 를 누릅니다.

**관제에서는** — 필터를 걸기 전에 칸이 초록인지 보는 습관이, 잘못 걸린 결과를 믿는 실수를 막습니다.

**강사 메모** — 지금은 예상만 하고, 6-5 에서 직접 쳐서 맞춰 본다고 말합니다. 「노란색은 언제 나오나요?」에는 「문법은 맞지만 생각과 다르게 걸릴 수 있을 때」라고 상자의 표대로 답합니다. 색을 보고 Enter 를 누르는 습관을 여기서 한 번 강조합니다.

---

### ✍️ 문제 6-2 · Wireshark 실행하기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — Wireshark 화면에서

아침 과제 8 에서 설치한 Wireshark 를 실행해, 첫 화면에서 **인터페이스 목록**이 보이는지 확인하시오.

1. 시작 메뉴에서 **Wireshark** 를 엽니다.
2. 아침에 설치를 못 끝냈으면 [아침 과제 8](1012_morning30.md) 의 3번을 지금 합니다 — **Windows x64 Installer**, 설치 중 **Install Npcap**(엔피캡 · 패킷을 실제로 붙잡는 부품) 체크는 **꼭 켠 채로**.

| | |
|---|---|
| 🎯 나와야 하는 결과 | 창 가운데 `Welcome to Wireshark` 아래에 **이더넷 · Wi-Fi 같은 통로 이름 목록**. 오른쪽에 작은 그래프가 붙어 있다 (통로 이름과 개수는 PC 마다 다릅니다) |

**💡 힌트**

1. 「관리자 권한으로 실행할까요?」 창이 뜨면 **예**를 누릅니다.
2. 목록이 비어 있으면 Npcap 이 빠진 것입니다. 설치 파일을 다시 실행해 Npcap 을 체크합니다.
3. 막히면 손을 듭니다 — 전원이 같이 출발해야 다음 단계가 됩니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 6-2</mark>

시작 메뉴에서 Wireshark 를 실행합니다(설치는 아침 과제 8). 첫 화면 가운데에 통로 이름 목록이 보이면 됩니다.

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `Welcome to Wireshark` 아래에 이더넷 · Wi-Fi 같은 통로 이름 목록, 오른쪽에 작은 그래프 (이름 · 개수는 PC 마다 다름)</mark>

**왜** — 통로 목록은 Npcap 이 PC 의 통로를 찾아 Wireshark 에 넘겨 줘야 보입니다.

**자주 틀리는 곳** — 설치 때 **Install Npcap** 체크를 끄면 목록이 비어 있습니다. 설치 파일을 다시 실행해 체크합니다.

**관제에서는** — 어느 통로를 잡느냐에 따라 보이는 통신이 달라지므로 통로 목록부터 확인합니다.

**강사 메모** — 전원이 이 화면까지 와야 다음 문제를 할 수 있으니, 시작 후 2~3분 안에 돌면서 목록이 비어 있는 화면을 먼저 찾습니다. 「이름이 여러 개인데 어느 것을 고르나요?」에는 「학원 PC 는 `이더넷 2`, 그래프가 움직이는 줄」이라고 답합니다. 목록이 비어 있으면 Npcap 을 체크해 다시 설치하게 합니다.

---

### ✍️ 문제 6-3 · 첫 캡처

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — Wireshark 화면에서 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 실습 기록` 에 `- 6-3: …` 한 줄

**그래프가 움직이는 통로**를 더블클릭해 캡처를 시작하고, 브라우저로 사이트 하나를 연 뒤 멈추시오. 상태 줄의 **패킷 수**와 Protocol 열에 보이는 **이름 세 개**를 적으시오.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `패킷: ○○○` (0 이 아님)과 `TCP` · `UDP` · `DNS` · `TLSv1.3`(티엘에스 · HTTPS 의 암호화 방식) 같은 이름 (패킷 수와 보이는 이름은 실행할 때마다 다릅니다) |

**💡 힌트**

1. 인터페이스(interface · 통로)는 내 PC 가 바깥과 통신하는 길입니다. 지금 통신이 흐르는 줄만 그래프가 움직입니다.
2. 멈추기는 도구 줄의 **빨간 네모**(또는 메뉴 캡처 › 정지 · Capture › Stop).
3. 사이트 하나만 열었는데 수백 줄인 것이 정상입니다 — 업데이트 · 백신 · 메신저가 쉬지 않고 통신합니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 6-3</mark>

통로 더블클릭 → 브라우저로 사이트 열기 → 빨간 네모. 상태 줄 `패킷: ○○○`, Protocol 열의 `TCP` · `UDP` · `DNS` · `TLSv1.3` 등을 적습니다.

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `패킷: ○○○` (0 이 아님)과 `TCP` · `UDP` · `DNS` · `TLSv1.3` 같은 이름 (매번 다름)</mark>

**왜** — 사이트 하나를 열어도 DNS 조회(UDP) · 연결(TCP) · 암호화된 내용(TLS)이 이어지고, 업데이트 · 메신저 같은 다른 프로그램의 통신도 함께 잡힙니다.

**자주 틀리는 곳** — 그래프가 움직이지 않는 통로를 고르면 패킷이 0 입니다. 그래프가 움직이는 통로를 더블클릭합니다.

**관제에서는** — 아무것도 안 해도 쌓이는 평소 통신을 알아야 그와 다른 이상한 통신을 구별합니다.

**강사 메모** — 수백 줄이 쌓이는 것이 정상이라는 점을 먼저 말해 둡니다. 「`TLSv1.3` 대신 `TLSv1.2` 가 보여요」에는 「사이트마다 다를 수 있고 둘 다 HTTPS 의 암호화 방식」이라고 답합니다. 캡처를 오래 켜 두면 줄이 너무 많아지니 사이트를 연 뒤 바로 멈추게 합니다.

---

### ✍️ 문제 6-4 · 패킷 하나를 층별로 펼치기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — Wireshark 화면에서

위 칸에서 Protocol 이 `TCP` 인 줄 하나를 누르고, 가운데 칸의 세 줄을 펼쳐 아래 표를 채우시오.

| 가운데 칸의 줄 | 층 | 찾을 값 |
|---|---|---|
| `Ethernet II` | 2 | Source 의 MAC 주소 |
| `Internet Protocol Version 4` | 3 | Source · Destination 의 IP, **Time to Live** |
| `Transmission Control Protocol` | 4 | Source Port · Destination Port · Flags |

| | |
|---|---|
| 🎯 나와야 하는 결과 | 세 줄이 **2층 → 3층 → 4층** 순서로 쌓여 있고, 표의 칸이 모두 찬다. Time to Live 는 오전 `ping` 의 TTL 과 같은 것 (칸의 값은 PC · 실행할 때마다 다릅니다) |

**💡 힌트**

1. 줄 앞의 삼각형(▸)을 누르면 펼쳐집니다.
2. 내 PC 가 보낸 패킷이면 Source IP 가 오전에 적은 내 IPv4 주소입니다.
3. 봉투 안에 봉투가 든 모양 — 5.3 의 「헤더가 여러 겹」을 실물로 보는 것입니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 6-4</mark>

`Ethernet II` › Source(MAC) · `Internet Protocol Version 4` › Source · Destination · Time to Live · `Transmission Control Protocol` › Source Port · Destination Port · Flags 를 펼쳐 읽습니다.

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 가운데 칸이 2층 `Ethernet II` → 3층 `Internet Protocol Version 4` → 4층 `Transmission Control Protocol` 순서로 쌓여 있고 표의 칸이 모두 찬다 (값은 PC 마다 다름)</mark>

**왜** — 보낼 때 층마다 헤더를 하나씩 붙이므로, 패킷 하나에 MAC(2층) · IP 와 TTL(3층) · 포트와 플래그(4층)가 겹쳐 들어 있습니다.

**자주 틀리는 곳** — 포트를 IP 줄에서 찾기 쉽습니다. 포트는 4층 `Transmission Control Protocol` 줄 안에 있습니다.

**관제에서는** — 의심 패킷 하나에서 출발지 IP · 목적지 포트 · 플래그를 이 세 줄로 읽어 누가 어디로 무엇을 했는지 정리합니다.

**강사 메모** — 내 PC 가 보낸 줄(Source 가 내 IPv4 주소)을 고르게 하면 7-4 의 헤더 표에 그대로 옮길 수 있습니다. 「내 PC 가 보낸 줄과 서버가 보낸 줄의 TTL 이 왜 다른가요?」에는 「보낸 쪽이 처음 정한 값에서 거쳐 온 횟수만큼 줄어든 값이라서」라고 답합니다. 포트를 IP 줄에서 찾는 학생이 많으니 층 순서를 한 번 더 짚습니다.

---

### ✍️ 문제 6-5 · 필터 세 개 걸어 보기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — Wireshark 화면에서 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 실습 기록` 에 `- 6-5: …` 한 줄

필터 칸에 아래를 **하나씩** 걸고(Enter), 상태 줄의 **표시됨** 숫자를 적으시오. 다음 것을 걸기 전에 칸 오른쪽 **X** 로 지웁니다.

```
dns
udp
tcp.port == 443
```

| | |
|---|---|
| 🎯 나와야 하는 결과 | 셋 다 `표시됨` 이 `패킷` 보다 작다. `dns` 에서는 Info 열에 방금 연 사이트 이름이 보인다 (숫자는 실행할 때마다 다릅니다) |

**💡 힌트**

1. 필터는 패킷을 지우지 않고 **가립니다.** 그래서 `패킷` 수는 그대로입니다.
2. `udp` 결과 대부분이 DNS 입니다 — 5.1 표의 「DNS 조회는 UDP」를 눈으로 확인하는 것입니다.
3. 칸이 빨간색이면 오타입니다. 6-1 의 `tpc` 도 쳐 봅니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 6-5</mark>

필터 칸에 하나씩 입력하고 Enter. 상태 줄의 `표시됨` 숫자를 적고 X 로 지운 뒤 다음 것을 겁니다.

```
dns
udp
tcp.port == 443
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 셋 다 `표시됨` 이 `패킷` 보다 작다. `dns` 에서는 Info 열에 방금 연 사이트 이름이 보인다 (숫자는 매번 다름)</mark>

**왜** — 표시 필터는 패킷을 지우지 않고 조건에 맞는 줄만 보여 줍니다. 그래서 `패킷` 수는 그대로이고 `표시됨` 만 줄어듭니다.

**자주 틀리는 곳** — 앞 필터를 X 로 지우지 않고 이어 치면 `dnsudp` 같은 없는 이름이 되어 칸이 빨간색이 됩니다.

**관제에서는** — 수천 줄의 캡처를 `dns` · `tcp.port == 443` 같은 표시 필터로 좁힌 뒤에 읽습니다.

**강사 메모** — 「`dns` 와 `udp` 숫자가 거의 같은 이유」를 반 전체에 물어 보고, UDP 대부분이 DNS 조회라는 점을 5.1 표와 이어 줍니다. 차이 나는 줄은 DNS 가 아닌 다른 UDP 통신이라고 답합니다. 돌면서 `패킷` 숫자는 그대로이고 `표시됨` 만 바뀌는지 학생 화면에서 확인합니다.

---

### ⭐ 도전 6-6 · 화면에서 찍어 필터 만들기 (선택)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — Wireshark 화면에서

필드 이름을 외우지 않고 필터를 만드시오.

1. 필터를 지우고 `TCP` 줄 하나를 고릅니다.
2. 가운데 칸 `Internet Protocol Version 4` › **Destination Address** 줄을 오른쪽 클릭 › **필터로 적용 › 선택됨**(Apply as Filter › Selected).
3. 필터 칸에 생긴 `ip.dst == …` 를 `ip.addr == …` 로 고쳐 Enter.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `ip.dst` 일 때는 나가는 줄만, `ip.addr` 로 고치면 **오고 간 줄이 모두** 남는다 |

**💡 힌트**

1. 출발지 줄을 골랐다면 `ip.src` 가 생깁니다.
2. Wireshark 상자 맨 아래 ⚠ 줄을 다시 봅니다.
3. 같은 방법으로 `Destination Port` 를 찍으면 `tcp.port == 443` 이 생깁니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 6-6</mark>

`Destination Address` 오른쪽 클릭 › 필터로 적용 › 선택됨 → 필터 칸이 `ip.dst == 주소` 가 됨 → `ip.dst` 를 `ip.addr` 로 고쳐 Enter.

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `ip.dst` 일 때는 나가는 줄만, `ip.addr` 로 고치면 오고 간 줄이 모두 남는다</mark>

**왜** — `ip.dst` 는 목적지 칸만 보고, `ip.addr` 는 출발지 · 목적지 둘 중 하나라도 그 주소면 남깁니다.

**자주 틀리는 곳** — `ip.dst` 결과만 보고 서버가 답을 안 했다고 판단하기 쉽습니다. 서버가 보낸 답은 출발지가 그 주소라 `ip.dst` 에 걸리지 않습니다.

**관제에서는** — 의심 IP 하나를 조사할 때 `ip.addr == 주소` 로 그 IP 와 오간 대화 전체를 봅니다.

**강사 메모** — 「`ip.addr == 주소` 와 `ip.src == 주소 || ip.dst == 주소` 는 같나요?」에는 「같은 줄이 남는다」고 답합니다. `ip.dst` 와 `ip.addr` 일 때의 `표시됨` 숫자를 나란히 적게 하면 차이가 바로 보입니다. 선택 문제라 7교시 시작을 늦추지 않습니다.

### 6교시 한눈에

| 하려는 일 | Wireshark 에서 |
|---|---|
| 캡처 시작 · 멈춤 | 통로 더블클릭 · 빨간 네모 |
| 층별로 보기 | 가운데 칸의 `Ethernet II` · `Internet Protocol Version 4` · `Transmission Control Protocol` |
| 종류만 남기기 | `tcp` · `udp` · `dns` |
| 값으로 남기기 | `tcp.port == 443` · `ip.addr == 주소` · `tcp.flags.syn == 1` |

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">7교시 (16:00–16:50) · 내 연결을 잡아 보고서로 남기기</mark>

### 왜 필요한가

1. 6교시에는 남이 만든 수백 줄 속에서 헤맸습니다. 이번에는 **내가 만든 연결 하나만** 깔끔하게 잡습니다.
2. 그 연결의 **열리는 순간(3-way) · 내용(HTTP) · 닫히는 순간(FIN)**을 찾아 사진과 표로 남깁니다.
3. 이것이 강의계획서의 1일 차 산출물 `day01_packet_analysis.md` 입니다. 평가 기준은 「3-way 세 단계를 찾았나 · IP 헤더의 출발지 · 목적지 · TTL 을 읽었나 · 필터로 원하는 것만 걸렀나」입니다.

### 7.1 잡을 때부터 거르기 — 캡처 필터

| | 표시 필터 (6교시) | **캡처 필터** (지금) |
|---|---|---|
| 언제 | 잡은 **뒤에** 보여 줄 것만 고른다 | **처음부터** 그것만 잡는다 |
| 어디에 | 패킷 목록 위의 필터 칸 | 메뉴 캡처 › 옵션(`Ctrl + K`) 창 아래쪽 칸 |
| 문법 | `tcp.port == 80` | **`tcp port 80`** — 점도 `==` 도 없다 |

⚠ 두 칸의 문법이 다릅니다. 캡처 필터 칸에 `tcp.port == 80` 을 치면 빨간색이 됩니다.

**왜 80번인가:** 80 은 암호화하지 않는 HTTP 입니다. 내용이 그대로 보여서 「잡은 것이 맞는지」 확인하기 좋습니다. 브라우저는 `http` 를 `https`(443, 암호화)로 바꿔 버리므로, 요청은 터미널의 **`curl`**(컬 · 터미널에서 웹 요청을 보내는 도구)로 보냅니다.

#### 🐍 문법 상자 · f-string(에프 스트링)으로 마크다운(Markdown · `#` · `|` 로 모양을 내는 글 형식) 표 한 줄 만들기

```python
i = 1
p = {"src": "192.168.0.15", "dst": "203.0.113.10", "info": "[SYN]"}
print(f"| {i} | {p['src']} | {p['dst']} | {p['info']} |")
# | 1 | 192.168.0.15 | 203.0.113.10 | [SYN] |
```

| 쓰는 것 | 뜻 |
|---|---|
| `\|` 로 칸을 나눈 한 줄 | 마크다운 표의 한 줄 (1과목 10/7) |
| `{p['src']}` | f-string 안에서 사전 값 꺼내기 — 바깥 큰따옴표, 안쪽 작은따옴표 |

⚠ 손으로 옮겨 적으면 숫자 하나가 틀리기 쉽습니다. 값만 적어 두고 <mark style="background:#ffcdd2; color:#1a1a1a; padding:0 4px; border-radius:3px">표 모양은 코드가 찍게</mark> 합니다.

---

### ✍️ 문제 7-1 · 무엇이 보일까요

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 실행하지 않고 머리로 예상합니다

아래 코드를 실행하면 무엇이 보일지 적어 보세요.

```python
packets = [{"info": "[SYN]"}, {"info": "[SYN, ACK]"}, {"info": "[ACK]"}]
i = 0
for p in packets:
    i = i + 1
    print(f"| {i} | {p['info']} |")
```

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답</mark>

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `| 1 | [SYN] |` · `| 2 | [SYN, ACK] |` · `| 3 | [ACK] |` 세 줄.</mark>

**왜** — `i = i + 1` 이 `print` 보다 위에 있어서 첫 줄 번호가 1 입니다. 번호는 반복할 때마다 1씩 늘어납니다.

**자주 틀리는 곳** — 첫 줄을 `| 0 | [SYN] |` 로 적기 쉽습니다. 더하기가 출력보다 먼저인지 봅니다.

**관제에서는** — 패킷 값을 손으로 옮기지 않고 코드가 표로 찍게 하면 보고서의 숫자가 틀리지 않습니다.

**강사 메모** — `i = i + 1` 이 `print` 보다 위에 있다는 점을 강조합니다. 바로 이어 「두 줄의 순서를 바꾸면 번호는?」(0 · 1 · 2)을 물어 봅니다. 「f-string 안에서 작은따옴표를 왜 쓰나요?」에는 「바깥이 큰따옴표라 안쪽 키는 작은따옴표로 써야 글자가 끊기지 않는다」고 답합니다.

---

### ✍️ 문제 7-2 · 내 HTTP 연결 하나만 잡기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — Wireshark 에서 캡처 시작 → 터미널에서 `curl` 실행 → Wireshark 화면을 사진으로 저장

캡처 필터 `tcp port 80` 으로 캡처를 시작하고, 터미널에서 아래 명령을 입력한 뒤 **3초쯤 기다렸다가** 멈추시오.

```bash
curl "http://example.com/?q=network_day1"
```

그다음 표시 필터 `tcp.flags.syn == 1` 을 걸어 3-way 의 앞 두 줄을 찾고, 필터를 지운 뒤 세 번째 `[ACK]` 줄까지 찾아 **세 줄을 한 화면에 잘라** `handshake.png` 로 저장하시오.

| | |
|---|---|
| 🎯 나와야 하는 결과 | Info 열에 `[SYN]` → `[SYN, ACK]` → `[ACK]` 가 차례로. 터미널에는 `<title>Example Domain</title>` 이 든 HTML(에이치티엠엘 · 웹 페이지의 글) (줄 번호와 주소는 실행할 때마다 다릅니다) |

**💡 힌트**

1. 캡처 › 옵션(`Ctrl + K`) › 내 통로 선택 › 아래쪽 캡처 필터 칸에 `tcp port 80` › **시작(Start)**.
2. 캡처가 **돌아가는 동안** `curl` 을 입력해야 잡힙니다.
3. 화면 자르기는 `Win + Shift + S`(윈도우 키 + Shift + S · 캡처 도구) → 잘라서 `network_zt` 폴더에 붙여 저장합니다(그림판에 붙여 저장해도 됩니다).

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 7-2</mark>

캡처 › 옵션(`Ctrl + K`) › 통로 선택 › 캡처 필터 `tcp port 80` › 시작. **터미널에 입력합니다.**

```bash
curl "http://example.com/?q=network_day1"
```

3초 뒤 정지 → 표시 필터 `tcp.flags.syn == 1` 로 `[SYN]` · `[SYN, ACK]` 확인 → 필터를 지우고 바로 다음 `[ACK]` 까지 세 줄을 `Win + Shift + S` 로 잘라 `handshake.png` 로 저장.

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — Info 열에 `[SYN]` → `[SYN, ACK]` → `[ACK]` 가 차례로, 터미널에는 `<title>Example Domain</title>` 이 든 HTML (줄 번호 · 주소는 매번 다름)</mark>

**왜** — 캡처 필터 `tcp port 80` 이 처음부터 80번 통신만 잡아 내 `curl` 연결이 짧게 남습니다. 세 번째 `[ACK]` 는 SYN 이 꺼져 있어 `tcp.flags.syn == 1` 에 안 걸리므로 필터를 지우고 찾습니다.

**자주 틀리는 곳** — 캡처를 멈춘 뒤에 `curl` 을 입력하거나, 캡처 필터 칸에 표시 필터 문법 `tcp.port == 80` 을 치면 아무것도 잡히지 않습니다.

**관제에서는** — 첫 `[SYN]` 의 Source 를 보면 누가 먼저 연결을 청했는지 알 수 있습니다.

**강사 메모** — 오늘 가장 많이 막히는 문제라 시간을 넉넉히 잡고, 캡처 필터는 캡처 › 옵션(`Ctrl + K`) 창에서 통로 `이더넷 2` 를 고른 뒤 넣는다는 점을 화면으로 먼저 보여 줍니다. 「`[SYN]` 이 여러 개 보여요」에는 「`curl` 을 여러 번 입력하면 연결마다 3-way 가 생기니 출발지 포트가 같은 세 줄을 고른다」고 답합니다. 돌면서 캡처 필터 칸이 초록색인지, 캡처가 돌아가는 동안 `curl` 을 입력했는지를 봅니다.

---

### ✍️ 문제 7-3 · 내용과 작별 찾기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — Wireshark 화면에서 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 실습 기록` 에 `- 7-3: …` 한 줄

7-2 의 캡처에서 아래 둘을 찾으시오.

1. 표시 필터 `http` → `GET /?q=network_day1` 줄을 찾아 **잘라** `http_request.png` 로 저장합니다.
2. 표시 필터 `tcp.flags.fin == 1` → FIN 이 든 줄이 **몇 줄**인지 적습니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | ① Info 에 `GET /?q=network_day1 HTTP/1.1` — 검색어가 그대로 보인다 ② FIN 줄 2줄(양쪽이 하나씩) (FIN 대신 RST 가 보이는 등 끝맺는 줄은 실행할 때마다 조금 다를 수 있습니다) |

**💡 힌트**

1. 암호화하지 않은 HTTP 라서 **내가 보낸 글자가 패킷에 그대로** 보입니다. 이것이 HTTPS 를 써야 하는 이유입니다.
2. FIN 이 2줄인 것은 5.2 그림의 「나는 다 보냈다」 · 「나도 다 보냈다」 두 번입니다.
3. 줄이 안 보이면 `curl` 을 캡처 중에 다시 입력합니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 7-3</mark>

표시 필터 `http` → `GET /?q=network_day1 HTTP/1.1` 줄을 잘라 `http_request.png`. 표시 필터 `tcp.flags.fin == 1` → FIN 이 든 줄 2줄.

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — ① Info 에 `GET /?q=network_day1 HTTP/1.1` — 검색어가 그대로 보인다 ② FIN 줄 2줄(양쪽이 하나씩) (FIN 대신 RST 가 보이는 등 조금 다를 수 있음)</mark>

**왜** — HTTP 는 암호화하지 않아 보낸 글자가 패킷에 그대로 실립니다. FIN 2줄은 5.2 그림의 「나는 다 보냈다」 · 「나도 다 보냈다」입니다.

**자주 틀리는 곳** — FIN 줄은 Info 에 `[FIN, ACK]` 로 보이므로, `[FIN]` 만 있는 줄을 찾으면 못 찾습니다.

**관제에서는** — 암호화하지 않은 80번 통신은 비밀번호 · 검색어가 그대로 보이므로 점검 대상으로 봅니다.

**강사 메모** — 검색어 `network_day1` 이 그대로 보이는 장면을 HTTPS 를 써야 하는 이유와 이어서 강조합니다. 「FIN 대신 RST 가 보여요」에는 「끝맺는 방식은 실행마다 다를 수 있고, RST 는 인사 없이 바로 끊은 것(5.2 표)」이라고 답합니다. FIN 줄을 못 찾는 학생은 Info 에서 `[FIN, ACK]` 를 찾게 합니다.

---

### ✍️ 문제 7-4 · 보고서 표를 코드로 찍기 (`report_table.py`)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — VS Code 에서 `report_table.py` 만들기 → 터미널에서 `python report_table.py` 실행

7-2 에서 찾은 세 줄과 6-4 에서 읽은 헤더 값을 **마크다운 표 두 개**로 출력하시오. `network_zt` 에 `report_table.py` 를 만들어 붙여 넣고, **데이터의 값을 내 화면 값으로 바꾼 뒤** 번호 주석 아래를 채웁니다. `python report_table.py`

```python
# ── 강사용: 정답을 채운 코드입니다 ──
packets = [                                       # 7-2 의 3-way 세 줄
    {"src": "192.168.0.15", "dst": "203.0.113.10", "info": "[SYN]"},
    {"src": "203.0.113.10", "dst": "192.168.0.15", "info": "[SYN, ACK]"},
    {"src": "192.168.0.15", "dst": "203.0.113.10", "info": "[ACK]"},
]
headers = [                                       # 6-4 · 7-2 에서 읽은 헤더 값
    {"item": "출발지 IP", "value": "192.168.0.15", "where": "IP 헤더 (3층)"},
    {"item": "목적지 IP", "value": "203.0.113.10", "where": "IP 헤더 (3층)"},
    {"item": "TTL", "value": "128", "where": "IP 헤더 (3층)"},
    {"item": "출발지 포트", "value": "51234", "where": "TCP 헤더 (4층)"},
    {"item": "목적지 포트", "value": "80", "where": "TCP 헤더 (4층)"},
]

print("| 순서 | Source | Destination | Info |")
print("|---|---|---|---|")
i = 0                                             # 순서 번호
for p in packets:                                 # 3-way 세 줄을 하나씩
    # 1. i 에 1 을 더하고, f"| {i} | {p['src']} | {p['dst']} | {p['info']} |" 를 출력하세요
    i = i + 1                                     # 번호를 하나 늘린다
    print(f"| {i} | {p['src']} | {p['dst']} | {p['info']} |")

print()
print("| 항목 | 값 | 어느 헤더 |")
print("|---|---|---|")
for h in headers:                                 # 헤더 값을 하나씩
    # 2. f"| {h['item']} | {h['value']} | {h['where']} |" 를 출력하세요
    print(f"| {h['item']} | {h['value']} | {h['where']} |")
```

**파일을 만들고 실행합니다**

1. VS Code 왼쪽 목록에서 `network_zt` 폴더를 오른쪽 클릭 › **New File** › 이름 `report_table.py` 를 입력하고 Enter 를 누릅니다.
2. 위 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 로 복사해 파일에 붙여 넣은 뒤, 번호 주석 아래를 채웁니다. 저장은 자동입니다.
3. 터미널에 아래 명령을 입력합니다. 터미널의 줄 위에 `…/network_zt` 가 보여야 합니다. 아니면 먼저 `cd network_zt` 를 입력합니다.

```bash
python report_table.py
```

4. 고친 뒤에는 같은 명령을 다시 입력합니다. 터미널에서 **↑(위 화살표)** 를 누르면 방금 입력한 명령이 다시 나옵니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `\| 1 \| 192.168.0.15 \| 203.0.113.10 \| [SYN] \|` 로 시작하는 표 하나와 `\| 출발지 IP \| … \| IP 헤더 (3층) \|` 로 시작하는 표 하나 — 값은 내 화면의 값 |

**💡 힌트**

1. 7-1 과 같은 모양입니다.
2. 바깥은 큰따옴표, 안쪽 키는 작은따옴표입니다.
3. 출력을 그대로 복사해 보고서에 붙입니다(7-5).

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 7-4</mark>

(코드는 위 문제 칸에 채워 두었습니다.)

💻 **터미널에 입력합니다.**

```bash
python report_table.py
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `| 1 | 192.168.0.15 | 203.0.113.10 | [SYN] |` 로 시작하는 표 하나와 `| 출발지 IP | … | IP 헤더 (3층) |` 로 시작하는 표 하나 — 값은 내 화면의 값</mark>

**왜** — f-string 이 사전 값을 `|` 칸 사이에 끼워 표 한 줄을 만들고, 반복이 패킷 · 헤더마다 그 줄을 찍습니다.

**자주 틀리는 곳** — 데이터를 예시 값(`192.168.0.15` 등) 그대로 두고 실행하기 쉽습니다. 내 화면 값으로 바꾼 뒤 실행합니다.

**관제에서는** — 분석 값을 늘 같은 모양의 표로 남기면 보고서끼리 비교하기 쉽습니다.

**강사 메모** — 값을 바꿀 때 따옴표까지 지워 `SyntaxError` 가 나는 학생이 많으니, 따옴표 안의 글자만 바꾼다고 먼저 말합니다. 「TTL 은 어느 줄의 값을 적나요?」에는 「6-4 처럼 내 PC 가 보낸 줄의 값」이라고 답합니다. 출력된 표를 7-5 에서 그대로 붙인다고 알려 둡니다.

---

### ✍️ 문제 7-5 · 보고서 완성하고 올리기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 보고서 파일 마무리 → 깃허브에 올리기(웹 화면 또는 `git push`)

`day01_packet_analysis.md` 의 오전 표 **아래에** 아래를 이어 붙이고, 괄호를 내 값으로 채운 뒤 깃허브에 올리시오.

```markdown
## 2. 연결이 열리는 순간 — 3-way handshake
![3-way handshake](handshake.png)

(report_table.py 의 첫 번째 표를 붙입니다)

세 줄이 뜻하는 것: (한두 문장)

## 3. 헤더에서 읽은 값
(report_table.py 의 두 번째 표를 붙입니다)

## 4. 내용과 작별
![HTTP 요청](http_request.png)
- 패킷에 보인 검색어: (예: network_day1)
- FIN 줄 수: (○줄) — 뜻: (한 문장)

## 5. 쓴 필터
- 캡처 필터: tcp port 80
- 표시 필터: tcp.flags.syn == 1 · http · tcp.flags.fin == 1
```

| | |
|---|---|
| 🎯 나와야 하는 결과 | 깃허브의 내 저장소 `network_zt` 폴더에 `day01_packet_analysis.md` · `handshake.png` · `http_request.png` 가 보이고, 보고서에 사진 두 장이 나온다 |

**💡 힌트**

1. 사진은 `![설명](파일이름)` 한 줄로 넣습니다. 같은 폴더면 파일 이름만 씁니다.
2. 올리기는 10/8 에 배운 순서입니다 — `security-agent-toolkit` 폴더에서 `git add network_zt` → `git commit -m "…"` → `git push`.
3. `git status` 에 `.env` 가 보이면 멈춥니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 7-5</mark>

보고서에 2~5절을 붙여 채운 뒤, **터미널(`security-agent-toolkit` 폴더)에 입력합니다.**

```bash
git status
git add network_zt
git commit -m "Add day 1 packet analysis report"
git push
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 깃허브의 내 저장소 `network_zt` 폴더에 `day01_packet_analysis.md` · `handshake.png` · `http_request.png` 가 보이고, 보고서에 사진 두 장이 나온다</mark>

**왜** — `![설명](파일이름)` 은 같은 폴더의 사진을 보고서에 띄웁니다. 그래서 사진 파일도 같은 폴더에 함께 올려야 보입니다.

**자주 틀리는 곳** — 사진을 `network_zt` 가 아닌 곳에 저장하거나 파일 이름을 다르게 적으면 보고서에 사진이 나오지 않습니다. `git status` 에 `.env` 가 보이면 멈춥니다.

**관제에서는** — 분석 보고서에 캡처 사진과 쓴 필터를 함께 남겨야 다른 사람이 같은 결과를 다시 확인할 수 있습니다.

**강사 메모** — `git add` 전에 `git status` 로 `.env` 가 목록에 없는지 확인하는 것을 가장 강조합니다. 「깃허브에서 사진이 안 보여요」에는 「보고서에 적은 파일 이름이 대소문자 · 확장자까지 실제 파일과 같아야 한다」고 답합니다. 올린 뒤 깃허브 웹 화면에서 보고서를 열어 사진 두 장이 나오는지 직접 확인하게 합니다.

---

### ✍️ 문제 7-6 · 웹 서버에 머리글만 묻기 — `curl -I`

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 터미널에서 명령 실행 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 실습 기록` 에 `- 7-6: …` 한 줄

터미널에 아래를 입력하고, **첫 줄의 상태 코드**와 **`Server:` 줄의 값**을 보고서 맨 아래에 적으시오.

```bash
curl -I http://example.com
```

| | |
|---|---|
| 🎯 나와야 하는 결과 | 첫 줄 `HTTP/1.1 200 OK`, 아래에 `Server: cloudflare` 같은 줄 — 본문(HTML)은 나오지 않는다 (값은 바뀔 수 있습니다) |

**💡 힌트**

1. `-I` 는 대문자 i 입니다. 웹 페이지 본문 없이 **머리글(헤더)만** 받아 옵니다.
2. 관제에서는 「이 웹 서버가 살아 있나 · 무슨 서버인가」를 볼 때 가장 먼저 씁니다. 화면이 짧아 읽기 쉽습니다.
3. 상태 코드 `200` 은 9/29 에 배운 「성공」입니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 7-6</mark>

💻 **터미널에 입력합니다.**

```bash
curl -I http://example.com
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 첫 줄 `HTTP/1.1 200 OK`, 아래에 `Server: cloudflare` 같은 줄 — 본문(HTML)은 나오지 않는다 (값은 바뀔 수 있음)</mark>

**왜** — `-I` 는 본문 없이 머리글(헤더)만 받아 옵니다. `200` 이 상태 코드(성공), `Server:` 줄의 값이 서버가 밝힌 서버 종류입니다.

**자주 틀리는 곳** — 소문자 `-i` 를 쓰면 머리글 뒤에 본문 HTML 까지 길게 나옵니다.

**관제에서는** — 「이 웹 서버가 살아 있나 · 무슨 서버인가」를 볼 때 가장 먼저 씁니다.

**강사 메모** — `-I` 가 대문자 i 라는 점을 화면에 크게 보여 줍니다. 「`Server:` 값이 예시와 달라요」에는 「값은 바뀔 수 있고, 첫 줄의 상태 코드가 핵심」이라고 답합니다. 반 전체에 「`200` 은 무슨 뜻이었나요?」(9/29 의 성공)를 물어 확인합니다.

---

### ⭐ 도전 7-7 · 암호화된 연결은 무엇이 다른가 (선택)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — Wireshark 에서 캡처 시작 → 터미널에서 `curl` 실행 → 다른 점을 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 실습 기록` 에 `- 7-7: …` 한 줄

캡처 필터를 **`tcp port 443`** 으로 바꿔 같은 방법으로 아래를 잡고, 7-3 의 HTTP 화면과 **무엇이 다른지** 보고서 맨 아래에 한 문장으로 적으시오.

```bash
curl "https://example.com/?q=network_day1"
```

| | |
|---|---|
| 🎯 나와야 하는 결과 | 3-way 는 똑같이 보이지만, 그 뒤가 `TLSv1.3` · `Application Data` 로만 보이고 **검색어 `network_day1` 은 어디에도 안 보인다** |

**💡 힌트**

1. 표시 필터 `tls` 로 남겨 봅니다.
2. 열리는 순간(3-way)은 암호화 **전**이라 똑같습니다.
3. 관제 관점: HTTPS 는 내용이 안 보이니 **누구와 · 언제 · 얼마나** 통신했는지를 봅니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 7-7</mark>

캡처 필터 `tcp port 443` 으로 다시 잡고 `curl "https://example.com/?q=network_day1"`. 표시 필터 `tls` 로 보면 `Client Hello` · `Application Data` 만 보이고 검색어는 보이지 않습니다. 보고서에는 예: 「HTTP 는 내용이 그대로 보였지만 HTTPS 는 3-way 뒤의 내용이 암호화돼 검색어가 보이지 않았다」.

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 3-way 는 똑같이 보이지만, 그 뒤가 `TLSv1.3` · `Application Data` 로만 보이고 검색어 `network_day1` 은 어디에도 안 보인다</mark>

**왜** — 3-way 는 암호화 전에 일어나서 똑같습니다. 그 뒤 내용은 TLS 가 암호화해 주소 뒤의 `?q=network_day1` 까지 가려집니다.

**자주 틀리는 곳** — 캡처 필터를 `tcp port 80` 그대로 두면 443 연결이 하나도 잡히지 않습니다.

**관제에서는** — HTTPS 는 내용이 안 보이니 누구와 · 언제 · 얼마나 통신했는지를 봅니다.

**강사 메모** — 3-way 는 같고 그 뒤 내용만 가려진다는 대비를 7-3 화면과 나란히 놓고 강조합니다. 「어느 사이트에 갔는지도 안 보이나요?」에는 「`Client Hello` 를 펼치면 서버 이름 `example.com` 은 보통 보이지만 `?q=network_day1` 은 보이지 않는다」고 답합니다. 선택 문제라 먼저 끝난 학생에게만 권하고, 캡처 필터를 `tcp port 443` 으로 바꿨는지부터 봅니다.

### 7교시 한눈에

| 장면 | 필터 | 보이는 것 |
|---|---|---|
| 열림 | `tcp.flags.syn == 1` | `[SYN]` · `[SYN, ACK]` (+ 다음 `[ACK]`) |
| 내용 | `http` | `GET /?q=…` — HTTP 는 글자가 그대로 |
| 닫힘 | `tcp.flags.fin == 1` | FIN 두 줄 |
| 처음부터 거르기 | 캡처 필터 `tcp port 80` | 내 연결만 스무 줄 안팎 |
| 서버가 살아 있나 | `curl -I 주소` | 상태 코드 첫 줄과 `Server:` — 본문 없이 |

---

## 오늘 마무리

| 확인 | 문제 |
|---|---|
| `day01_packet_analysis.md` 에 1~5번 절이 다 있다 | 오전 · 7-5 |
| 사진 두 장(`handshake.png` · `http_request.png`)이 보고서에 나온다 | 7-2 · 7-3 |
| 3-way 세 단계를 내 말로 설명할 수 있다 | 5-3 · 7-2 |
| 깃허브에 올렸다 | 7-5 |

내일(10/13)은 오늘 `ipconfig` 에서 본 `192.168.0.15` · `255.255.255.0` 같은 숫자의 정체 — **IP 주소와 서브넷**을 배웁니다.

---
