# 10/12(월) 오후 · TCP 와 3-way handshake · Wireshark 첫 캡처 · 1일 차 보고서 — 실습

오전에는 `netstat`(넷스탯 · 지금의 연결을 보여 주는 명령)에서 `ESTABLISHED`(이스태블리시드 · 연결된 상태)라는 글자를 봤습니다. 오후에는 그 연결이 **어떻게 맺어지고 어떻게 끝나는지**를 배우고, **Wireshark**(와이어샤크 · 오가는 패킷을 붙잡아 보여 주는 프로그램)로 실제 패킷을 눈으로 봅니다.

| 교시 | 무엇 | 쓰는 것 |
|---|---|---|
| 5교시 | TCP 와 UDP · 연결을 맺는 세 번의 신호(3-way handshake) · 끝내는 네 번 | 파이썬 · `netstat` |
| 6교시 | Wireshark 실행 · 첫 캡처 · 화면 읽기 · 필터 | Wireshark (아침 과제 8 에서 설치) |
| 7교시 | 내 연결을 직접 잡아 보고서로 남기기 | Wireshark · `curl` · 파이썬 |

**오늘 남기는 것:** `network_zt/day01_packet_analysis.md` 완성본(2~7교시 칸 + 7교시의 캡처 사진 · 표) — 강의계획서의 1일 차 산출물입니다.

> **화면은 이렇게 나눠 씁니다 — 왼쪽은 실습 자료, 오른쪽은 보고서**
>
> 1. 이 파일을 누르고 `Ctrl + Shift + V` 를 누릅니다. 실습 자료가 **미리보기**로 열립니다. 이 탭이 **왼쪽**입니다.
> 2. 왼쪽 목록(탐색기)에서 보고서 파일 `day01_packet_analysis.md` 를 오른쪽 클릭하고 **Open to the Side**(옆에서 열기)를 누릅니다. 보고서가 **오른쪽** 칸에 열립니다.
> 3. **오른쪽 보고서에만 씁니다.** 왼쪽 실습 자료는 스크롤하며 읽습니다. 쓴 모양을 보고 싶으면 오른쪽 칸에서 `Ctrl + K` 를 누른 뒤 `V`.
>
> 보고서 파일은 오전에 만든 것을 그대로 씁니다.

---

## 시작하기

### 이 파일을 여는 법

이 파일은 **카톡으로 받은 실습 안내**입니다. 노트북이 아니라 읽으면서 따라 하는 문서입니다.

1. 카톡에서 받은 이 파일(`261012_pm_tcp_wireshark.md`)을 `security-agent-toolkit` 안의 **`network_zt` 폴더**로 옮깁니다.
2. VS Code 왼쪽 목록에서 이 파일을 누르고, **`Ctrl + Shift + V`** 를 눌러 **미리보기**로 엽니다. 표 · 굵은 글씨 · 「답 보기」가 읽기 좋게 보입니다.
3. 이 파일은 **읽기만** 합니다. 내가 적는 것은 그날 **보고서 파일**과 **`.py` 파일**입니다.
4. 코드나 명령을 복사할 때는 미리보기의 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 를 누릅니다.

### 오늘 시작할 때

0. 오늘 적는 것은 모두 **오전에 만든 `day01_packet_analysis.md` 하나에** 적습니다. 5 · 6 · 7교시의 문제 소제목은 오전에 붙여 넣은 틀에 이미 있습니다 — **그 문제 소제목 아래**를 채웁니다. 문제마다 「**적는 곳**」 줄을 봅니다.
1. 오전과 같은 터미널(Git Bash)을 씁니다. 줄 앞에 `$` 가 보이면 됩니다.
2. `network_zt` 폴더에서 시작합니다 — `cd network_zt`(이미 들어와 있으면 생략).
3. 이 문서의 화면 예시는 **모양을 보여 주는 예시**입니다. 주소 · 숫자는 내 화면의 값을 읽습니다.
4. 문제 앞의 **상자**를 먼저 읽습니다 — 🐍 문법 상자(파이썬) · 명령 상자(터미널) · Wireshark 상자 · 개념 상자. 문제 제목 아래 **어디서** 줄이 실습하는 곳입니다. `→` 는 하는 순서입니다. 막히면 **💡 힌트** → 맨 아래 **「정답」** 순서로 봅니다. ⭐도전은 선택입니다.
5. 맥북으로 복습할 때는 명령 상자 바로 아래의 **「맥북:」 줄**을 칩니다(없으면 Windows 와 같은 명령). 맥의 결과는 영어이고 모양이 달라 🎯 결과와 글자가 다릅니다 — 같은 값(평균 · TTL · IP · 포트)을 찾으면 됩니다.

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">5교시 (14:00–14:50) · TCP 와 UDP · 3-way handshake</mark>

### 왜 필요한가

1. 오전에 본 4층(전송 계층)에는 데이터를 보내는 방식이 **두 가지** 있습니다 — TCP 와 UDP.
2. 웹 · 파일 · 1과목의 `requests.post` 는 TCP 입니다. TCP 는 보내기 전에 **세 번 신호를 주고받아 연결을 맺습니다.** 이것이 3-way handshake 입니다.
3. 관제 화면에 「연결을 시도만 하고 끝까지 안 맺는 패킷」이 쏟아지면 공격(포트 스캔 · 열린 포트를 차례로 두드려 찾는 공격 등)일 수 있습니다. 정상적인 세 번을 알아야 이상한 것이 보입니다.


### 5.1 패킷 플래그를 리스트에서 찾기

TCP 패킷에는 `SYN`, `ACK`처럼 여러 **플래그**(flag · 신호 표시)가 함께 켜질 수 있습니다. 파이썬에서는 이런 값을 리스트로 다룹니다. 리스트 안에 특정 플래그가 있는지 확인할 때는 `in`을 씁니다.

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

### ✍️ 문제 5-1 · 직접 실행해 보기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — VS Code 에서 `warmup.py` 에 따라 치기 → 터미널에서 `python warmup.py` → 결과와 「왜」를 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 5교시` 에서 `### 문제 5-1` 아래

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**왜 중요한가**</mark> — 패킷의 플래그는 여러 개가 한 리스트에 들어옵니다. 이 차이를 알아야 SYN · FIN 을 골라내는 탐지 코드가 아무것도 못 잡는 실수를 막습니다.

**이 문제에 나오는 말**

- **플래그 (flag)** — TCP 가 패킷에 켜고 끄는 **표시 한 칸**. 켜진 플래그로 무슨 신호인지 알린다

VS Code 에서 `network_zt` 폴더에 `warmup.py` 파일을 만들고, 아래 코드를 입력해 저장합니다. 처음 한 번만 새 파일로 만들고, 교시마다 내용을 지우고 다시 씁니다. 터미널에서 실행한 결과와 「왜 이렇게 나왔는지」 한 줄을 보고서에 적으시오.

```python
packet = {"src_port": 51234, "dst_port": 443, "flags": ["SYN", "ACK"]}
print("ACK" in packet["flags"])
print(packet["flags"] == "ACK")
print(packet["dst_port"])
```

```bash
python warmup.py
```
맥북: `python3 warmup.py`

막히면 바로 위 문법 상자를 다시 봅니다.

<details><summary>답 보기 — 결과와 「왜」를 적은 뒤에 엽니다</summary>

**결과** — `True` · `False` · `443` 세 줄.

**왜** — `in` 은 리스트 안에 `"ACK"` 가 있는지 묻고, `==` 는 리스트 전체를 글자 `"ACK"` 와 비교하므로 늘 `False` 입니다.

**자주 틀리는 곳** — 둘째 줄도 `True` 라고 적기 쉽습니다. 리스트 `["SYN", "ACK"]` 와 글자 `"ACK"` 는 같을 수 없습니다.

**관제에서는** — 탐지 규칙에서 `==` 로 쓰면 에러 없이 아무것도 못 잡으므로, 플래그 검사는 `in` 으로 씁니다.

</details>

---

### 5.2 TCP 와 UDP

**여기 나오는 말**

- **TCP (Transmission Control Protocol)** (티시피) — 보내기 전에 **연결을 맺고**, 받았는지 확인하며 보내는 방식 — 웹 · `requests.post`
- **UDP (User Datagram Protocol)** (유디피) — 연결 없이 **바로 보내는** 방식, 받았는지 확인하지 않음 — DNS 조회 · 화상회의 음성

| | TCP | UDP |
|---|---|---|
| 연결 | 보내기 **전에 연결을 맺는다** | 연결 없이 **바로 보낸다** |
| 받았는지 확인 | 한다 — 안 왔으면 **다시 보낸다** | 안 한다 |
| 순서 | 번호로 **순서를 맞춘다** | 맞추지 않는다 |
| 속도 | 확인하느라 조금 느리다 | 빠르다 |
| 쓰는 곳 | 웹(HTTP 에이치티티피 · HTTPS 에이치티티피에스) · 파일 · 메일 · SSH(에스에스에이치 · 서버 원격 접속) | DNS(디엔에스 · 이름을 IP 로 바꾸는 조회) 조회 · 실시간 영상 · 게임 · 음성 통화 |

`ping`(핑) 은 둘 다 아닙니다. 오전에 본 **ICMP**(아이시엠피 · 「살아 있나」만 묻는 방식)라는 별도 방식입니다.

### ✍️ 문제 5-2 · TCP 일까 UDP 일까

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 명령 없이 생각해서 답하기 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 5교시` 에서 `### 문제 5-2` 아래

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**왜 중요한가**</mark> — TCP 와 UDP 를 구별해야 Wireshark 의 Protocol 열을 읽을 수 있습니다. 6-4 에서 `udp` 필터를 걸 때 무엇이 걸릴지 미리 짐작하는 근거가 됩니다.

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
3. 위 TCP/UDP 표 아래 줄을 다시 봅니다.

---

### 5.3 연결을 맺는 세 번, 끝내는 네 번

**여기 나오는 말**

- **3-way handshake** (스리웨이 핸드셰이크) — 데이터를 보내기 전에 **세 번 신호를 주고받아** 연결을 맺는 절차 — SYN → SYN, ACK → ACK
- **SYN (synchronize)** (신) — 「**연결하자**」는 신호. 연결을 처음 청할 때 켜는 플래그
- **ACK (acknowledge)** (액) — 「**받았다**」는 신호. 상대가 보낸 것을 받았다고 알릴 때 켜는 플래그

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

> **검색해서 채웁니다.** 표의 **[찾아 쓰기]** 칸은 비워 두었습니다. 검색하고 직접 실행해 확인한 뒤, 오늘 보고서의 그 교시 `### 찾아본 것` 아래에 **내 말로** 적습니다. 다 적은 뒤 맨 아래 「정답」의 표와 비교합니다.
> 검색어 예: `TCP RST 뜻` · `TCP FIN RST 차이` · `RST 포트 스캔`
> ⚠ 검색 결과는 영어 · 리눅스 화면이 많습니다. 내 화면(한국어 Windows)의 글자와 짝을 맞춰 읽습니다.

| 이름 | 읽는 법 · 원래 말 | 뜻 |
|---|---|---|
| SYN | 신 · synchronize | 연결하자 (번호를 맞추자) |
| ACK | 액 · acknowledge | 받았다 (알았다) — 그림의 ③ |
| FIN | 핀 · finish | 나는 다 보냈다 — 정상으로 끝내자 |
| RST | 리셋 · reset | **[찾아 쓰기]** FIN 과 무엇이 다른가? 언제 보이나? |

- **왜 맺을 때는 세 번인가:** 서버의 「알았다(ACK)」와 「나도 연결하자(SYN)」는 그 순간 둘 다 참이라 **한 신호에 같이 실을 수 있습니다** → ②번 하나.
- **왜 끝낼 때는 네 번인가:** 서버는 「알았다」는 바로 답하지만, 아직 보낼 데이터가 남아 있을 수 있어 「나도 다 보냈다(FIN)」는 **나중에 따로** 보냅니다.
- 끝난 연결은 바로 사라지지 않고 잠시 **`TIME_WAIT`**(타임 웨이트) 상태로 남습니다. `netstat` 에서 자주 보입니다 — 이상한 것이 아닙니다.

### ✍️ 문제 5-3 · 세 번의 순서 맞히기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 명령 없이 생각해서 답하기 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 5교시` 에서 `### 문제 5-3` 아래

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**왜 중요한가**</mark> — 이 순서를 알아야 7-1 에서 Wireshark 로 잡은 줄이 연결의 시작인지 가릴 수 있습니다. 관제에서는 연결이 끝까지 맺어지지 않는 시도가 쌓이면 공격을 의심합니다.

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

---


### 5.4 연결 하나를 가리키는 네 값

**여기 나오는 말**

- **임시 포트** — 내 PC 가 연결할 때마다 **그때그때 정해 쓰는** 내 쪽 포트 번호(보통 49152 이상)

| 값 | 어디에 적혀 있나 | 예 |
|---|---|---|
| 출발지 IP | IP 헤더(3층) | `192.168.0.15` |
| 출발지 포트 | TCP 헤더(4층) | `51234` — 내 PC 가 그때그때 고르는 **임시 포트**(49152~65535) |
| 목적지 IP | IP 헤더(3층) | `203.0.113.10` |
| 목적지 포트 | TCP 헤더(4층) | `443` — 서비스가 정해 둔 번호 |

**헤더**(header)는 데이터 앞에 붙는 「누가 · 누구에게 · 어떻게」 정보입니다. 층마다 하나씩 붙어서, 패킷 하나에 헤더가 여러 겹 있습니다.

### ✍️ 문제 5-4 · 같은 서버로 간 두 연결은 무엇이 다른가

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 브라우저에서 같은 사이트를 탭 두 개로 열기 → 터미널에서 명령 실행 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 5교시` 에서 `### 문제 5-4` 아래

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**왜 중요한가**</mark> — 관제 로그에서 연결 하나를 정확히 짚으려면 5.4 의 네 값을 모두 봐야 합니다. 같은 서버로 간 연결이 여러 개일 때 어느 것인지 가리는 근거가 됩니다.

브라우저로 같은 사이트를 **탭 두 개**로 연 뒤 `netstat -n` 을 입력하고, 외부 주소가 **같은** 연결 두 줄을 찾아 **무엇이 다른지** 적으시오.

| | |
|---|---|
| 🎯 나와야 하는 결과 | 외부 주소(목적지 IP · 포트)는 같고 **로컬 주소 끝의 포트**(임시 포트)만 다르다 — 예: `192.168.0.15:51234` 와 `192.168.0.15:51240` |

**💡 힌트**

1. 5.4 표의 네 값 가운데 무엇이 달라야 두 연결을 구별할 수 있을까요?
2. 줄이 너무 많으면 `netstat -n | grep 443` 으로 443 줄만 봅니다.
3. 같은 줄이 안 보이면 탭을 하나 더 열고 다시 입력합니다.

---


# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">6교시 (15:00–15:50) · Wireshark 실행 · 첫 캡처 · 필터</mark>

### 왜 필요한가

1. 5교시의 SYN · ACK 는 지금까지 **그림**이었습니다. Wireshark 는 내 PC 를 지나는 패킷을 붙잡아 **실제 값**으로 보여 줍니다.
2. 관제 · 침해 분석에서 「무슨 일이 있었나」를 확인하는 표준 도구입니다.
3. 캡처를 켜면 몇 초 만에 수백 줄이 쌓입니다. 그래서 **필터**(filter · 원하는 것만 남기는 조건)를 함께 배웁니다.


### 6.1 Wireshark를 열고 통로를 확인하기

Wireshark는 내 PC를 지나는 패킷을 붙잡아 보여 줍니다. 패킷을 잡으려면 먼저 네트워크 어댑터인 **인터페이스**(interface · Wi-Fi나 이더넷 같은 통신 통로)를 골라야 합니다. 첫 화면에서 이름 오른쪽 그래프가 움직이는 통로를 찾습니다. 학원 PC는 보통 `이더넷 2`입니다.

인터페이스 목록이 비어 있으면 패킷을 붙잡는 부품인 **Npcap**이 설치되지 않았을 수 있습니다. 설치할 때 `Install Npcap`을 선택해야 합니다.

### ✍️ 문제 6-1 · Wireshark 실행하기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — Wireshark 화면에서

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 6교시` 에서 `### 문제 6-1` 아래

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**왜 중요한가**</mark> — Wireshark 가 인터페이스를 보지 못하면 6 · 7교시 실습을 하나도 할 수 없습니다. 지금 확인해야 캡처 단계에서 멈추지 않습니다.

**이 문제에 나오는 말**

- **Npcap** (엔피캡) — Wireshark 가 패킷을 실제로 붙잡게 해 주는 **부품**. Wireshark 와 함께 설치한다

아침 과제 8 에서 설치한 Wireshark 를 실행해, 첫 화면에서 **인터페이스 목록**이 보이는지 확인하시오.

1. 시작 메뉴에서 **Wireshark** 를 엽니다.
2. 아침에 설치를 못 끝냈으면 [아침 과제 8](1012_morning30.md) 의 3번을 지금 합니다 — **Windows x64 Installer**, 설치 중 **Install Npcap**(엔피캡 · 패킷을 실제로 붙잡는 부품) 체크는 **꼭 켠 채로**.

| | |
|---|---|
| 🎯 나와야 하는 결과 | 창 가운데 `Wireshark에 오신 것을 환영합니다`(영어 화면은 `Welcome to Wireshark`) 아래에 **이더넷 · Wi-Fi 같은 인터페이스 이름 목록**. 오른쪽에 작은 그래프가 붙어 있다 (인터페이스 이름과 개수는 PC 마다 다릅니다) |

**💡 힌트**

1. 「관리자 권한으로 실행할까요?」 창이 뜨면 **예**를 누릅니다.
2. 목록이 비어 있으면 Npcap 이 빠진 것입니다. 설치 파일을 다시 실행해 Npcap 을 체크합니다.

맥북: 인터페이스는 `en0`(Wi-Fi) 입니다. 첫 화면에 **ChmodBPF** 설치 안내가 보이면 그 링크로 설치해야 캡처가 됩니다(설치 전에는 「권한이 없다」며 0 개가 잡힙니다).
3. 막히면 손을 듭니다 — 전원이 같이 출발해야 다음 단계가 됩니다.

---

### 6.2 캡처를 시작하고 멈추기

인터페이스를 더블클릭하면 **캡처**(capture · 내 PC를 지나는 패킷을 붙잡는 것)가 시작되고 패킷이 위쪽 목록에 한 줄씩 쌓입니다. 사이트에 접속한 뒤 도구 줄의 **빨간 네모**를 누르면 멈춥니다. 캡처한 전체 개수는 화면 맨 아래 상태 줄의 `Packets`에서 확인합니다.

### ✍️ 문제 6-2 · 첫 캡처

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — Wireshark 화면에서 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 6교시` 에서 `### 문제 6-2` 아래

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**왜 중요한가**</mark> — 사이트 하나를 열 때 실제로 몇 개의 패킷과 어떤 종류가 오가는지 숫자로 봅니다. 이 `Packets` 수가 6-4 에서 필터로 얼마나 줄었는지 비교하는 기준이 됩니다.

**그래프가 움직이는 인터페이스**를 더블클릭해 캡처를 시작하고, 브라우저로 사이트 하나를 연 뒤 멈추시오. 화면 맨 아래 오른쪽 끝 상태 줄의 **Packets** 숫자와 Protocol 열에 보이는 **이름 세 개**를 적으시오.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `Packets: ○○○` (0 이 아님)과 `TCP` · `UDP` · `DNS` · `TLSv1.3`(티엘에스 · HTTPS 의 암호화 방식) 같은 이름 (패킷 수와 보이는 이름은 실행할 때마다 다릅니다) |

**💡 힌트**

1. 인터페이스(interface)는 내 PC 의 네트워크 어댑터입니다. 지금 통신이 흐르는 줄만 그래프가 움직입니다. 학원 PC 는 **`이더넷 2`** 입니다.
2. 멈추기는 도구 줄의 **빨간 네모**(또는 메뉴 캡처 › 정지 · Capture › Stop).
3. 사이트 하나만 열었는데 수백 줄인 것이 정상입니다 — 업데이트 · 백신 · 메신저가 쉬지 않고 통신합니다.

---

### 6.3 패킷 한 줄의 상세 정보 펼치기

화면은 세 부분입니다. 위쪽 목록에서 패킷 한 줄을 고르면 아래쪽 왼편에서 그 패킷의 헤더 정보를 층별로 펼쳐 볼 수 있고, 아래쪽 오른편에는 원래 바이트가 보입니다. 지금 실습에서는 아래 왼쪽의 상세 정보를 읽으면 됩니다.

패킷에는 층마다 **헤더**(header · 주소와 번호 같은 정보)가 붙습니다. `Ethernet II`는 2층의 MAC 주소, `Internet Protocol Version 4`는 3층의 출발지·목적지 IP와 `Time to Live`, `Transmission Control Protocol`은 4층의 포트와 플래그를 담습니다. 줄 앞의 삼각형을 눌러 항목을 펼칩니다.

### ✍️ 문제 6-3 · 패킷 하나를 층별로 펼치기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — Wireshark 화면에서

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 6교시` 에서 `### 문제 6-3` 아래

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**왜 중요한가**</mark> — 관제에서 출발지 · 목적지 IP 와 포트를 읽는 곳이 이 칸입니다. 7교시 보고서의 평가 기준인 출발지 · 목적지 · TTL 도 여기서 읽습니다.

위 칸에서 Protocol 이 `TCP` 인 줄 하나를 누르고, 아래 왼쪽 칸의 세 줄을 펼쳐 아래 표의 값을 찾고, 보고서에 적으시오.

| 아래 왼쪽 칸(패킷 상세)의 줄 | 층 | 찾을 값 |
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
3. 층마다 헤더가 하나씩 붙은 모양 — 5.4 의 「헤더가 여러 겹」을 실물로 보는 것입니다.
4. `Time to Live` 는 `Internet Protocol Version 4` 를 펼친 안쪽 중간쯤에, `Flags` 는 `Transmission Control Protocol` 안에 `Flags: 0x018 (PSH, ACK)` 꼴로 있습니다 — 괄호 안 이름을 적습니다.

---

### 6.4 표시 필터로 필요한 패킷만 보기

캡처하면 수백 줄이 쌓이므로 조건에 맞는 줄만 보이도록 **표시 필터**(display filter)를 씁니다. 입력 칸은 패킷 목록 바로 위의 긴 칸입니다. 필터를 걸어도 패킷이 삭제되지는 않고, 조건에 맞는 줄만 화면에 표시됩니다. 그래서 맨 아래 `Packets` 전체 수는 유지되고 `Displayed` 숫자만 바뀝니다.

필터는 `dns`처럼 종류 이름만 쓰거나, `tcp.port == 443`처럼 필드와 값을 함께 쓸 수 있습니다. 입력 후 Enter를 누릅니다. 칸이 초록색이면 문법이 맞고, 빨간색이면 오타가 있습니다. 한 번에 하나씩 시험할 때는 오른쪽 `X`로 지운 뒤 다음 필터를 입력합니다.

### ✍️ 문제 6-4 · 필터 세 개 걸어 보기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — Wireshark 화면에서 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 6교시` 에서 `### 문제 6-4` 아래

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**왜 중요한가**</mark> — 화면 맨 아래 오른쪽 `Displayed` 는 필터에 걸린 패킷 수입니다. 이 숫자로 필터가 제대로 걸렸는지 확인하고, 관제에서는 수천 줄을 몇 줄로 좁혔는지 판단합니다.

필터 세 개를 **한 번에 하나씩** 걸어 보고, 걸 때마다 화면 맨 아래 오른쪽 끝 상태 줄의 **Displayed** 숫자를 적으시오. 세 줄을 한 칸에 같이 치지 않습니다.

1. 필터 칸에 `dns` 를 치고 Enter → `Displayed` 숫자를 적고, 칸 오른쪽 **X** 로 지웁니다.
2. 필터 칸에 `udp` 를 치고 Enter → `Displayed` 숫자를 적고, **X** 로 지웁니다.
3. 필터 칸에 `tcp.port == 443` 을 치고 Enter → `Displayed` 숫자를 적습니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | 셋 다 `Displayed` 이 `Packets` 보다 작다. `dns` 에서는 Info 열에 방금 연 사이트 이름이 보인다 (숫자는 실행할 때마다 다릅니다) |

**💡 힌트**

1. 필터 칸은 **패킷 목록 바로 위** `표시 필터 적용` 칸입니다(6.4 설명). 필터는 패킷을 지우지 않고 **가립니다.** 그래서 `Packets` 수는 그대로입니다.
2. `udp` 결과 대부분이 DNS 입니다 — 5.2 표의 「DNS 조회는 UDP」를 눈으로 확인하는 것입니다.
3. 칸이 빨간색이면 오타입니다. 일부러 `tpc` 를 쳐서 칸이 빨강이 되는 것도 봅니다.

---


# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">7교시 (16:00–16:50) · 내 연결을 잡아 보고서로 남기기</mark>

### 왜 필요한가

1. 6교시에는 남이 만든 수백 줄 속에서 헤맸습니다. 이번에는 **내가 만든 연결 하나만** 깔끔하게 잡습니다.
2. 그 연결의 **열리는 순간(3-way) · 내용(HTTP) · 닫히는 순간(FIN)**을 찾아 사진과 값으로 남깁니다.
3. 이것이 강의계획서의 1일 차 산출물 `day01_packet_analysis.md` 입니다. 평가 기준은 「3-way 세 단계를 찾았나 · IP 헤더의 출발지 · 목적지 · TTL 을 읽었나 · 필터로 원하는 것만 걸렀나」입니다.


### 7.1 잡을 때부터 거르기 — 캡처 필터

**여기 나오는 말**

- **캡처 필터 (capture filter)** — 캡처를 **시작하기 전에** 걸어, 조건에 맞는 패킷만 처음부터 잡는 조건 — `tcp port 80`
- **HTTP (HyperText Transfer Protocol)** (에이치티티피) — 웹 요청과 응답을 **암호화하지 않고** 주고받는 방식 — 포트 80
- **HTTPS** (에이치티티피에스) — HTTP 를 **암호화**해서 주고받는 웹 — 포트 443. 요즘 웹은 거의 다 이것
- **TLS (Transport Layer Security)** (티엘에스) — HTTPS 가 쓰는 **암호화 방식**. Wireshark 의 Protocol 열에 `TLSv1.3` 으로 보인다(6-2 첫 캡처)
- **`curl`** (컬) — 터미널에서 **웹 요청을 보내는** 명령. Windows 에 기본으로 들어 있다
- **상태 코드** — 서버가 답 맨 앞에 붙이는 숫자 — `200` 성공 · `404` 없음 — 7-2 의 `HTTP/1.1 200 OK`

| | 표시 필터 (6교시) | **캡처 필터** (지금) |
|---|---|---|
| 언제 | 잡은 **뒤에** 보여 줄 것만 고른다 | **처음부터** 그것만 잡는다 |
| 어디에 | 패킷 목록 위의 필터 칸 | 메뉴 캡처 › 옵션(`Ctrl + K`) 창 아래쪽 칸 |
| 문법 | `tcp.port == 80` | **`tcp port 80`** — 점도 `==` 도 없다 |

⚠ 두 칸의 문법이 다릅니다. 캡처 필터 칸에 `tcp.port == 80` 을 치면 빨간색이 됩니다.

**왜 80번인가:** 80 은 암호화하지 않는 HTTP 입니다. 내용이 그대로 보여서 「잡은 것이 맞는지」 확인하기 좋습니다. 브라우저는 `http` 를 `https`(443, 암호화)로 바꿔 버리므로, 요청은 터미널의 **`curl`**(컬 · 터미널에서 웹 요청을 보내는 도구)로 보냅니다.

---


### ✍️ 문제 7-1 · 내 HTTP 연결 하나만 잡기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — Wireshark 에서 캡처 시작 → 터미널에서 `curl` 실행 → Wireshark 화면을 사진으로 저장

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 7교시` 에서 `### 문제 7-1` 아래

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**왜 중요한가**</mark> — 캡처 필터로 내 연결만 잡으면 수백 줄 속에서 헤매지 않고 3-way 세 줄을 바로 찾습니다. 이 사진이 오늘 보고서의 첫 증거입니다.

캡처 필터 `tcp port 80` 으로 캡처를 시작하고, 터미널에서 아래 명령을 입력한 뒤 **3초쯤 기다렸다가** 멈추시오.

```bash
curl "http://example.com/?q=network_day1"
```

그다음 표시 필터 `tcp.flags.syn == 1` 을 걸어 3-way 의 앞 두 줄을 찾고, 필터를 지운 뒤 세 번째 `[ACK]` 줄까지 찾아 **세 줄을 한 화면에 잘라** `handshake.png` 로 저장하시오.

| | |
|---|---|
| 🎯 나와야 하는 결과 | Info 열에 `[SYN]` → `[SYN, ACK]` → `[ACK]` 가 차례로. 터미널에는 `<title>Example Domain</title>` 이 든 HTML(에이치티엠엘 · 웹 페이지의 글) (줄 번호와 주소는 실행할 때마다 다릅니다) |

**💡 힌트**

1. 순서: 지금 캡처 중이면 빨간 네모로 먼저 멈춤 → 메뉴 **캡처(C) › 옵션(O)…**(`Ctrl + K`) → 위 목록에서 **`이더넷 2`** 한 줄 클릭 → 창 아래 `선택한 인터페이스에 대한 캡처 필터:` 칸에 `tcp port 80`(칸이 **초록**인지 확인) → 오른쪽 아래 **시작(S)**. 「저장하지 않고 계속」 창이 뜨면 그 단추를 누릅니다.
2. 캡처가 **돌아가는 동안** `curl` 을 입력해야 잡힙니다.
3. 화면 자르기는 `Win + Shift + S`(윈도우 키 + Shift + S · 캡처 도구) → 잘라서 `network_zt` 폴더에 붙여 저장합니다(그림판에 붙여 저장해도 됩니다).
4. 멈췄는데 한 줄도 없으면: 캡처 필터 칸이 초록이었는지, `curl` 을 캡처가 **돌아가는 동안** 쳤는지 봅니다.

---

### ✍️ 문제 7-2 · HTTP 요청과 연결 종료 찾기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — Wireshark 화면에서 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 7교시` 에서 `### 문제 7-2` 아래

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**왜 중요한가**</mark> — HTTP 패킷에 내가 보낸 글자가 어떻게 남는지 직접 보면 암호화하지 않은 웹 통신을 왜 막는지 알 수 있습니다. FIN 줄은 연결이 정상으로 끝났는지 가리는 근거입니다.

7-1 의 캡처에서 아래 둘을 찾으시오.

1. 표시 필터 `http` → `GET /?q=network_day1` 줄을 찾아 **잘라** `http_request.png` 로 저장합니다.
2. 표시 필터 `tcp.flags.fin == 1` → FIN 이 든 줄이 **몇 줄**인지 적습니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | ① Info 에 `GET /?q=network_day1 HTTP/1.1` — 검색어가 그대로 보인다 ② FIN 줄 2줄(양쪽이 하나씩) (FIN 대신 RST 가 보이는 등 끝맺는 줄은 실행할 때마다 조금 다를 수 있습니다) |

**💡 힌트**

1. 암호화하지 않은 HTTP 라서 **내가 보낸 글자가 패킷에 그대로** 보입니다. 이것이 HTTPS 를 써야 하는 이유입니다.
2. FIN 이 2줄인 것은 5.3 그림의 「나는 다 보냈다」 · 「나도 다 보냈다」 두 번입니다. Info 에는 `[FIN]` 이 아니라 **`[FIN, ACK]`** 로 보입니다.
3. 줄이 안 보이면 `curl` 을 캡처 중에 다시 입력합니다.

---


### ✍️ 문제 7-3 · 보고서 완성하고 올리기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 보고서 파일 마무리 → 깃허브에 올리기(웹 화면 또는 `git push`)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 7교시` 에서 `### 문제 7-3` 아래

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**왜 중요한가**</mark> — 사진과 값을 한 보고서로 남겨야 다른 사람이 같은 결과를 확인할 수 있습니다. 관제에서도 분석 결과는 근거 사진과 값을 붙인 보고서로 넘깁니다.

`day01_packet_analysis.md` 의 **빈 칸**(5 · 6 · 7교시와 맨 아래 「최종 분석」)을 마저 채우고 깃허브에 올리시오. 사진 줄과 값을 적는 줄은 오전에 붙여 넣은 틀에 이미 있습니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | 깃허브의 내 저장소 `network_zt` 폴더에 `day01_packet_analysis.md` · `handshake.png` · `http_request.png` 가 보이고, 보고서에 사진 두 장이 나온다 |

**💡 힌트**

1. 사진 줄 `![설명](파일이름)` 은 틀에 이미 있습니다. 사진이 안 보이면 파일 이름과 저장한 폴더(`network_zt`)를 봅니다.
2. 올리기는 10/8 에 배운 순서입니다 — `security-agent-toolkit` 폴더에서 `git add network_zt` → `git commit -m "…"` → `git push`.
3. `git status` 에 `.env` 가 보이면 멈춥니다.

---


## 오늘 마무리

| 확인 | 문제 |
|---|---|
| `day01_packet_analysis.md` 의 2~7교시와 「최종 분석」에 빈 칸이 없다(⭐ 제외) | 모든 문제 · 7-3 |
| 사진 두 장(`handshake.png` · `http_request.png`)이 보고서에 나온다 | 7-1 · 7-2 |
| 3-way 세 단계를 내 말로 설명할 수 있다 | 5-3 · 7-1 |
| 깃허브에 올렸다 | 7-3 |

내일(10/13)은 오늘 `ipconfig` 에서 본 `192.168.0.15` · `255.255.255.0` 같은 숫자의 정체 — **IP 주소와 서브넷**을 배웁니다.

---

# 정답 · 먼저 풀어 본 뒤에 봅니다

교시 첫 문제(5-1)의 답은 문제 바로 아래 「답 보기」에 있습니다. 화면의 주소 · 숫자는 PC 마다 다릅니다.

---

### 정답 · 5.3 TCP 신호 표

| 이름 | 읽는 법 · 원래 말 | 뜻 |
|---|---|---|
| SYN | 신 · synchronize | 연결하자 (번호를 맞추자) |
| ACK | 액 · acknowledge | 받았다 |
| FIN | 핀 · finish | 나는 다 보냈다 |
| RST | 리셋 · reset | 인사 없이 **바로 끊는다** — 닫힌 포트에 접속하거나 방화벽이 끊을 때 |

---

### 정답 5-2

| # | 답 | 이유 |
|---|---|---|
| ① 사진 보내기 | TCP | 한 조각이라도 빠지면 파일이 깨진다 |
| ② 실시간 방송 | UDP | 조금 빠져도 끊기지 않는 게 중요하다 |
| ③ `requests.post` | TCP | 웹(HTTPS) 요청이다 |
| ④ DNS 조회 | UDP | 짧은 질문 하나 · 답 하나라 연결을 맺지 않는다 |
| ⑤ `ping` | 둘 다 아님 | ICMP 라는 별도 방식이다 |

**결과** — ① TCP ② UDP ③ TCP ④ UDP ⑤ 둘 다 아님(ICMP)

**왜** — 하나라도 빠지면 안 되는 데이터는 받았는지 확인하고 다시 보내는 TCP, 빠른 게 중요한 데이터는 확인을 하지 않는 UDP 를 씁니다.

**자주 틀리는 곳** — ⑤ `ping` 을 TCP 로 적기 쉽습니다. `ping` 은 포트도 연결도 없는 ICMP 입니다.

**관제에서는** — DNS 조회는 UDP 53번이라, UDP 53번 조회가 갑자기 많아지면 먼저 살펴봅니다.

---

### 정답 5-3

**결과** — (나) 내 PC → 서버 · (다) 서버 → 내 PC · (가) 내 PC → 서버

**왜** — 내 PC 가 `[SYN]` 으로 먼저 청하고, 서버는 「받았다(ACK)」와 「나도 연결하자(SYN)」를 한 줄에 실어 답합니다. 내 PC 의 마지막 `[ACK]` 뒤에 `ESTABLISHED` 가 됩니다.

**자주 틀리는 곳** — (다) `[SYN, ACK]` 를 내 PC 가 보낸다고 적기 쉽습니다. `[SYN, ACK]` 는 처음 `[SYN]` 을 받은 쪽(서버)이 보냅니다.

**관제에서는** — `[SYN]` 만 쏟아지고 세 번째 `[ACK]` 가 없으면 포트 스캔 같은 공격을 의심합니다.

---

---

### 정답 5-4

💻 **터미널에 입력합니다.**

```bash
netstat -n
```
맥북: `netstat -an -p tcp` (포트는 주소 끝 마지막 점 뒤의 숫자)

**결과** — 외부 주소(목적지 IP · 포트)는 같고 로컬 주소 끝의 포트(임시 포트)만 다르다 — 예: `192.168.0.15:51234` 와 `192.168.0.15:51240`

**왜** — 연결 하나는 네 값(출발지 IP · 출발지 포트 · 목적지 IP · 목적지 포트)으로 구별됩니다. 목적지와 내 IP 가 같으니, 내 PC 가 연결마다 다른 임시 포트를 골라 구별합니다.

**자주 틀리는 곳** — 로컬 주소의 IP 가 다르다고 적기 쉽습니다. 같은 PC 라 IP 는 같고 `:` 뒤 포트만 다릅니다.

**관제에서는** — 한 PC 가 한 서버로 연 연결 수를 세어, 연결을 지나치게 많이 여는 PC 를 찾습니다.

---

---

### 정답 6-1

시작 메뉴에서 Wireshark 를 실행합니다(설치는 아침 과제 8). 첫 화면 가운데에 인터페이스 이름 목록이 보이면 됩니다.

**결과** — `Welcome to Wireshark` 아래에 이더넷 · Wi-Fi 같은 인터페이스 이름 목록, 오른쪽에 작은 그래프 (이름 · 개수는 PC 마다 다름)

**왜** — 인터페이스 목록은 Npcap 이 PC 의 인터페이스를 찾아 Wireshark 에 넘겨 줘야 보입니다.

**자주 틀리는 곳** — 설치 때 **Install Npcap** 체크를 끄면 목록이 비어 있습니다. 설치 파일을 다시 실행해 체크합니다.

**관제에서는** — 어느 인터페이스를 잡느냐에 따라 보이는 통신이 달라지므로 인터페이스 목록부터 확인합니다.

---

### 정답 6-2

인터페이스 더블클릭 → 브라우저로 사이트 열기 → 빨간 네모. 상태 줄 `Packets: ○○○`, Protocol 열의 `TCP` · `UDP` · `DNS` · `TLSv1.3` 등을 적습니다.

**결과** — `Packets: ○○○` (0 이 아님)과 `TCP` · `UDP` · `DNS` · `TLSv1.3` 같은 이름 (매번 다름)

**왜** — 사이트 하나를 열어도 DNS 조회(UDP) · 연결(TCP) · 암호화된 내용(TLS)이 이어지고, 업데이트 · 메신저 같은 다른 프로그램의 통신도 함께 잡힙니다.

**자주 틀리는 곳** — 그래프가 움직이지 않는 인터페이스를 고르면 패킷이 0 입니다. 그래프가 움직이는 인터페이스를 더블클릭합니다.

**관제에서는** — 아무것도 안 해도 쌓이는 평소 통신을 알아야 그와 다른 이상한 통신을 구별합니다.

---

### 정답 6-3

`Ethernet II` › Source(MAC) · `Internet Protocol Version 4` › Source · Destination · Time to Live · `Transmission Control Protocol` › Source Port · Destination Port · Flags 를 펼쳐 읽습니다.

**결과** — 아래 왼쪽 칸이 2층 `Ethernet II` → 3층 `Internet Protocol Version 4` → 4층 `Transmission Control Protocol` 순서로 쌓여 있고 표의 칸이 모두 찬다 (값은 PC 마다 다름)

**왜** — 보낼 때 층마다 헤더를 하나씩 붙이므로, 패킷 하나에 MAC(2층) · IP 와 TTL(3층) · 포트와 플래그(4층)가 겹쳐 들어 있습니다.

**자주 틀리는 곳** — 포트를 IP 줄에서 찾기 쉽습니다. 포트는 4층 `Transmission Control Protocol` 줄 안에 있습니다.

**관제에서는** — 의심 패킷 하나에서 출발지 IP · 목적지 포트 · 플래그를 이 세 줄로 읽어 누가 어디로 무엇을 했는지 정리합니다.

---

### 정답 6-4

필터 칸에 하나씩 입력하고 Enter. 상태 줄의 `Displayed` 숫자를 적고 X 로 지운 뒤 다음 것을 겁니다.

```
dns
udp
tcp.port == 443
```

**결과** — 셋 다 `Displayed` 이 `Packets` 보다 작다. `dns` 에서는 Info 열에 방금 연 사이트 이름이 보인다 (숫자는 매번 다름)

**왜** — 표시 필터는 패킷을 지우지 않고 조건에 맞는 줄만 보여 줍니다. 그래서 `Packets` 수는 그대로이고 `Displayed` 만 줄어듭니다.

**자주 틀리는 곳** — 앞 필터를 X 로 지우지 않고 이어 치면 `dnsudp` 같은 없는 이름이 되어 칸이 빨간색이 됩니다.

**관제에서는** — 수천 줄의 캡처를 `dns` · `tcp.port == 443` 같은 표시 필터로 좁힌 뒤에 읽습니다.

---

---

### 정답 7-1

캡처 › 옵션(`Ctrl + K`) › 인터페이스 선택 › 캡처 필터 `tcp port 80` › 시작. **터미널에 입력합니다.**

```bash
curl "http://example.com/?q=network_day1"
```

3초 뒤 정지 → 표시 필터 `tcp.flags.syn == 1` 로 `[SYN]` · `[SYN, ACK]` 확인 → 필터를 지우고 바로 다음 `[ACK]` 까지 세 줄을 `Win + Shift + S` 로 잘라 `handshake.png` 로 저장.

**결과** — Info 열에 `[SYN]` → `[SYN, ACK]` → `[ACK]` 가 차례로, 터미널에는 `<title>Example Domain</title>` 이 든 HTML (줄 번호 · 주소는 매번 다름)

**왜** — 캡처 필터 `tcp port 80` 이 처음부터 80번 통신만 잡아 내 `curl` 연결이 짧게 남습니다. 세 번째 `[ACK]` 는 SYN 이 꺼져 있어 `tcp.flags.syn == 1` 에 안 걸리므로 필터를 지우고 찾습니다.

**자주 틀리는 곳** — 캡처를 멈춘 뒤에 `curl` 을 입력하거나, 캡처 필터 칸에 표시 필터 문법 `tcp.port == 80` 을 치면 아무것도 잡히지 않습니다.

**관제에서는** — 첫 `[SYN]` 의 Source 를 보면 누가 먼저 연결을 청했는지 알 수 있습니다.

---

### 정답 7-2

표시 필터 `http` → `GET /?q=network_day1 HTTP/1.1` 줄을 잘라 `http_request.png`. 표시 필터 `tcp.flags.fin == 1` → FIN 이 든 줄 2줄.

**결과** — ① Info 에 `GET /?q=network_day1 HTTP/1.1` — 검색어가 그대로 보인다 ② FIN 줄 2줄(양쪽이 하나씩) (FIN 대신 RST 가 보이는 등 조금 다를 수 있음)

**왜** — HTTP 는 암호화하지 않아 보낸 글자가 패킷에 그대로 실립니다. FIN 2줄은 5.3 그림의 「나는 다 보냈다」 · 「나도 다 보냈다」입니다.

**자주 틀리는 곳** — FIN 줄은 Info 에 `[FIN, ACK]` 로 보이므로, `[FIN]` 만 있는 줄을 찾으면 못 찾습니다.

**관제에서는** — 암호화하지 않은 80번 통신은 비밀번호 · 검색어가 그대로 보이므로 점검 대상으로 봅니다.

---

---

### 정답 7-3

보고서의 빈 줄을 다 채운 뒤, **터미널(`security-agent-toolkit` 폴더)에 입력합니다.**

```bash
git status
git add network_zt
git commit -m "Add day 1 packet analysis report"
git push
```

**결과** — 깃허브의 내 저장소 `network_zt` 폴더에 `day01_packet_analysis.md` · `handshake.png` · `http_request.png` 가 보이고, 보고서에 사진 두 장이 나온다

**왜** — `![설명](파일이름)` 은 같은 폴더의 사진을 보고서에 띄웁니다. 그래서 사진 파일도 같은 폴더에 함께 올려야 보입니다.

**자주 틀리는 곳** — 사진을 `network_zt` 가 아닌 곳에 저장하거나 파일 이름을 다르게 적으면 보고서에 사진이 나오지 않습니다. `git status` 에 `.env` 가 보이면 멈춥니다.

**관제에서는** — 분석 보고서에 캡처 사진과 사용한 필터를 함께 남겨야 다른 사람이 같은 결과를 다시 확인할 수 있습니다.

---

---

