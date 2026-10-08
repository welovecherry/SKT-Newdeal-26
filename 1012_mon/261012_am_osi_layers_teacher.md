# 10/12(월) 오전 · 네트워크 첫 관찰 · OSI 7계층 — 실습

> **강사용 · 학생에게 나눠 주지 않습니다.** 모든 문제 바로 아래에 「정답」과 해설이 있습니다. 찾아 쓰기 표는 채워 두었습니다.
>
> **수업 전에 확인할 것**
> 1. 학원 PC 터미널이 Git Bash 인지(`$`), `network_zt` 폴더가 있는지
> 2. 인터넷 · `ping 8.8.8.8` 이 되는지(학원망은 ICMP 통과 — 10/6 실측)
> 3. `ipconfig //all` 처럼 슬래시 두 번 — 한 번이면 사용법 안내만 나온다

오늘부터 2과목 **네트워크 · ZT(제로 트러스트, Zero Trust) 운영 기초**입니다. 제로 트러스트는 「회사 안이라도 아무도 그냥 믿지 않고 매번 확인한다」는 보안 원칙으로, 6일 차 10/19(월)에 배웁니다. 1과목에서 `requests.post(url, …)` 한 줄로 경보를 보내고 LLM 에 질문했습니다. 그 한 줄이 실행될 때 데이터는 **잘게 나뉘어 선과 공유기를 지나 서버까지 갔다가** 답을 들고 돌아왔습니다. 오늘은 그 길을 처음으로 들여다봅니다.

관제 데스크에 오는 문의는 대부분 「인터넷이 안 돼요」 한 문장입니다. 선이 빠졌는지, 주소를 못 찾는지, 서버가 죽었는지 — 원인은 여러 가지인데 증상은 하나입니다. 통신을 일곱 층으로 나눠 놓은 표준 모델이 **OSI(오에스아이) 7계층**입니다. 층마다 맡은 일이 달라서, 어느 층에서 막혔는지 차례로 좁혀 갈 수 있습니다.

| 교시 | 무엇 | 쓰는 명령 |
|---|---|---|
| 2교시 | 첫 관찰 — 내 PC 에서 서버까지 닿나 | `ping`(핑) |
| 3교시 | OSI 7계층 ① 아래 세 층 — MAC(맥) 주소와 IP(아이피) 주소 | `ipconfig //all`(아이피컨피그) · `arp -a`(에이알피) |
| 4교시 | OSI 7계층 ② 위 네 층 — 포트 번호와 지금의 연결 | `netstat`(넷스탯 · network statistics) |

**오전에 남기는 것:** `network_zt/day01_packet_analysis.md` 의 **「1. 내 PC 와 네트워크」** 표. 오후에 Wireshark(와이어샤크 · 오가는 패킷을 붙잡아 보여 주는 프로그램)로 이어 씁니다.

---

## 시작하기

### 0.1 이 파일을 여는 법

이 파일은 **카톡으로 받은 실습 안내**입니다. 노트북이 아니라 읽으면서 따라 하는 문서입니다.

1. 카톡에서 받은 이 파일(`261012_am_osi_layers.md`)을 `security-agent-toolkit` 안의 **`network_zt` 폴더**로 옮깁니다.
2. VS Code 왼쪽 목록에서 이 파일을 누르고, **`Ctrl + Shift + V`** 를 눌러 **미리보기**로 엽니다. 표 · 굵은 글씨 · 「답 보기」가 읽기 좋게 보입니다. (화면을 둘로 나눠 보려면 `Ctrl + K` 를 누른 뒤 `V`.)
3. 이 파일은 **읽기만** 합니다. 내가 적는 것은 그날 **보고서 파일**과 **`.py` 파일**입니다.
4. 코드나 명령을 복사할 때는 미리보기의 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 를 누릅니다.

명령은 VS Code 아래쪽 터미널에 직접 입력합니다. 오늘 오전에는 노트북을 쓰지 않습니다.

### 0.2 터미널은 지금까지처럼 Git Bash 를 씁니다

⚠ 명령은 <mark style="background:#ffcdd2; color:#1a1a1a; padding:0 4px; border-radius:3px">이 문서에 적힌 그대로</mark> 입력합니다. 예를 들어 `ipconfig //all` 처럼 슬래시가 두 번인 것도 그대로 칩니다.

1. VS Code 에서 `security-agent-toolkit` 폴더를 엽니다.
2. 아래쪽 터미널이 Git Bash 인지 봅니다. 줄 앞에 `$` 가 보이면 됩니다.
3. 아래를 입력해 `network_zt` 폴더로 들어갑니다(아침 과제에서 만든 폴더).

```bash
cd network_zt
```

> 화면의 숫자 · 주소는 **PC 마다 다릅니다.** 이 문서의 화면 예시는 모양을 보여 주는 예시입니다. 내 화면의 값을 읽어 적습니다.

### 0.3 문제를 푸는 법

1. 문제 앞의 **상자**를 먼저 읽습니다 — 🐍 문법 상자(파이썬) · 명령 상자(터미널) · Wireshark 상자 · 개념 상자. 문제 제목 아래 **어디서** 줄이 실습하는 곳입니다. `→` 는 하는 순서입니다.
2. 「💻 **터미널에 입력합니다.**」 아래의 명령은 터미널에 그대로 입력하고 Enter 를 누릅니다.
3. 막히면 **💡 힌트**를 보고, 그래도 막히면 문서 맨 아래 **「정답」**을 봅니다.
4. ⭐도전은 안 풀고 넘어가도 됩니다.

### 0.4 오늘의 보고서 파일을 만듭니다

1. VS Code 창 **왼쪽 끝의 세로 아이콘 줄**에서 맨 위 **탐색기**(Explorer · 종이 두 장 모양 · `Ctrl + Shift + E`)를 누릅니다. 그 오른쪽에 파일 · 폴더 목록이 열립니다. 이 문서에서 「**왼쪽 목록**」은 이 목록입니다.
2. 목록 맨 위 `SECURITY-AGENT-TOOLKIT` 아래에서 **`network_zt` 폴더**를 찾아 오른쪽 클릭 › **New File** 을 누릅니다. `network_zt` 가 안 보이면 아침 과제 8 의 4번(새 과목 폴더 만들기)으로 돌아갑니다.
3. 이름 칸에 `day01_packet_analysis.md` 를 입력하고 Enter 를 누릅니다. `network_zt` 폴더 **안에** 파일이 생겼는지 봅니다.
4. 아래 **틀 전체**를 붙여 넣습니다. 오늘 쓸 절이 처음부터 다 들어 있습니다 — 오전 · 오후 문제를 풀면서 빈칸만 채웁니다. 사진 두 줄은 오후에 사진을 저장하면 보입니다.

```markdown
# Day 1 패킷 분석 보고서 (이름 · 2026-10-12)

## 1. 내 PC 와 네트워크
(오전 2-2 · 3-2 · 3-3 · 3-4 에서 채웁니다)

| 항목 | 내 값 | 찾은 명령 |
|---|---|---|
| IPv4 주소 |  | ipconfig |
| MAC 주소(물리적 주소) |  | ipconfig //all |
| 기본 게이트웨이 |  | ipconfig |
| 게이트웨이까지 왕복 평균 |  ms | ping |
| 8.8.8.8 까지 왕복 평균 |  ms | ping |
| 8.8.8.8 의 TTL |  | ping |

## 2. 연결이 열리는 순간 — 3-way handshake
(오후 7-2 · 7-4 에서 채웁니다)

![3-way handshake](handshake.png)

(report_table.py 의 첫 번째 표를 붙입니다)

세 줄이 뜻하는 것: 

## 3. 헤더에서 읽은 값
(오후 7-4 에서 채웁니다)

(report_table.py 의 두 번째 표를 붙입니다)

## 4. 내용과 작별
(오후 7-3 에서 채웁니다)

![HTTP 요청](http_request.png)

- 패킷에 보인 검색어: 
- FIN 줄 수:  줄 — 뜻: 

## 5. 쓴 필터
(오후 7-2 · 7-3 에서 쓴 것)

- 캡처 필터: tcp port 80
- 표시 필터: tcp.flags.syn == 1 · http · tcp.flags.fin == 1

## 실습 기록
(「적는 곳」이 실습 기록인 문제 — 줄 뒤에 이어 씁니다)

- 2-4: 
- 2-5: 
- 3-5: 
- 4-2: 
- 4-4: 
- 4-5: 
- 5-2: 
- 5-3: 
- 5-5: 
- 6-3: 
- 6-5: 
- 7-3: 
- 7-6: 
- ⭐7-7(선택): 

## 찾아본 것
(**[찾아 쓰기]** 칸을 내 말로 한 줄씩)

- TTL: 
- 손실: 
- 평균: 
- 포트 22 · 3389 · 135 · 445: 
- ACK · FIN · RST: 
```
째는 …, 둘째는 …`)

## 찾아본 것
(**[찾아 쓰기]** 칸을 내 말로 — 예: `- TTL: …`)

```
⚠ <mark style="background:#ffcdd2; color:#1a1a1a; padding:0 4px; border-radius:3px">오늘 적는 것은 모두 이 파일(`day01_packet_analysis.md`) 하나에</mark> 적습니다. 문제마다 「<mark style="background:#ffcdd2; color:#1a1a1a; padding:0 4px; border-radius:3px">적는 곳</mark>」 줄이 이 파일의 어느 절인지 알려 줍니다. 절은 틀에 다 있으니 <mark style="background:#ffcdd2; color:#1a1a1a; padding:0 4px; border-radius:3px">새로 붙이지 않고 빈칸만</mark> 채웁니다.


---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">2교시 (10:00–10:50) · 첫 관찰 — `ping`</mark>

### 왜 필요한가

1. 「인터넷이 안 돼요」가 오면 관제는 먼저 **닿는지**부터 봅니다. 그 첫 명령이 `ping` 입니다.
2. `ping` 은 상대에게 「거기 있어요?」 하고 작은 신호를 보내고, 답이 오는 데 걸린 시간을 잽니다.
3. 답이 오면 **상대까지 패킷이 오가고 있다**는 뜻입니다. 안 오면 어느 단계에서 끊겼는지 좁혀 갑니다(4교시).

### 2.1 `ping` 의 결과 읽기

```
Ping 8.8.8.8 32바이트 데이터 사용:
8.8.8.8의 응답: 바이트=32 시간=34ms TTL=115
8.8.8.8의 응답: 바이트=32 시간=33ms TTL=115
8.8.8.8의 응답: 바이트=32 시간=35ms TTL=115
8.8.8.8의 응답: 바이트=32 시간=34ms TTL=115

8.8.8.8에 대한 Ping 통계:
    패킷: 보냄 = 4, 받음 = 4, 손실 = 0 (0% 손실),
왕복 시간(밀리초):
    최소 = 33ms, 최대 = 35ms, 평균 = 34ms
```

> 학생 문서에서는 아래 표의 일부 칸이 **[찾아 쓰기]** 로 비어 있습니다. 강사용에는 채운 표를 둡니다.

| 보이는 것 | 뜻 |
|---|---|
| `8.8.8.8의 응답` | 답이 왔다 — 상대까지 패킷이 오간다. `8.8.8.8` 은 구글의 공개 DNS(디엔에스 · 이름을 IP 주소로 바꿔 주는 시스템) 서버 주소다 |
| `시간=34ms` | 갔다가 돌아오는 데 걸린 시간(**왕복 시간**). ms(밀리초)는 1000분의 1초 |
| `TTL=115` | TTL(티티엘 · Time To Live) — 패킷(데이터를 잘게 나눈 한 조각)이 거쳐 갈 수 있는 남은 횟수. 공유기 · 라우터(망과 망을 잇는 장비)를 하나 지날 때마다 1씩 줄어든다 |
| `손실 = 0 (0% 손실)` | 보낸 4개가 모두 돌아왔다 |
| `평균 = 34ms` | 네 번의 왕복 시간의 평균 |

`ping` 이 쓰는 방식을 **ICMP**(아이시엠피 · Internet Control Message Protocol)라고 부릅니다. 웹 페이지(HTTP · 에이치티티피)와 달리 「살아 있나」만 묻는 통신입니다.

#### 명령 상자 · `ping` 의 옵션

`ping` 은 **터미널**에 입력하는 명령입니다.

```bash
ping 8.8.8.8          # 4번 보내고 끝난다
ping -n 10 8.8.8.8    # 10번 보낸다
ping -t 8.8.8.8       # 멈출 때까지 계속 보낸다 — Ctrl + C 로 멈춘다
```

| 쓰는 것 | 뜻 |
|---|---|
| `-n 숫자` | 보낼 횟수 (number) |
| `-t` | 멈출 때까지 계속 |
| `Ctrl + C` | 터미널에서 실행 중인 명령을 멈춘다 |

⚠ 리눅스 · 맥의 `ping` 은 옵션이 다릅니다(`-c 10`). 검색한 글이 리눅스 기준이면 Windows 에서 안 될 수 있습니다.

---

### ✍️ 문제 2-1 · 무엇이 보일까요

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 실행하지 않고 머리로 예상합니다

아래 결과를 보고 **세 가지**를 적어 보세요. 명령은 실행하지 않습니다.

```
1.1.1.1에 대한 Ping 통계:
    패킷: 보냄 = 4, 받음 = 3, 손실 = 1 (25% 손실),
왕복 시간(밀리초):
    최소 = 41ms, 최대 = 58ms, 평균 = 47ms
```

1. 몇 번 보내서 몇 번 돌아왔나요?
2. 손실은 몇 % 인가요?
3. 평균 왕복 시간은 몇 ms 인가요?

막히면 바로 위 `2.1` 표를 다시 봅니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답</mark>

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 4번 보내서 3번 돌아왔습니다 · 25% 손실 · 평균 47ms.</mark>

**왜** — 손실은 보낸 수와 받은 수의 차이입니다. 4개 중 1개가 돌아오지 않았으니 1 ÷ 4 = 25% 입니다.

**자주 틀리는 곳** — `최소 = 41ms` 나 `최대 = 58ms` 를 평균으로 적는 실수가 많습니다. 평균은 `평균 =` 뒤의 숫자입니다.

**관제에서는** — 손실이 0% 가 아니면 상대까지 가는 구간 어딘가가 불안정하다는 신호로 보고 다시 측정합니다.

**강사 메모** — 손실은 「돌아오지 않은 수 ÷ 보낸 수」라는 식을 칠판에 한 줄로 적어 두고 넘어갑니다. 「25% 손실이면 인터넷이 끊긴 건가요?」라는 질문에는 「끊긴 것이 아니라 넷 중 하나가 돌아오지 않아 불안정하다는 뜻」이라고 답합니다. 답을 맞춘 뒤 「보냄 10, 받음 9 이면 몇 % 인가요?」(10%)를 바로 물어 확인합니다.

---

### ✍️ 문제 2-2 · 구글 DNS 서버에 `ping` 보내기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 터미널에서 명령 실행 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 **1절 표**

터미널에서 `8.8.8.8` 에 `ping` 을 보내고, **평균 왕복 시간**과 **TTL** 을 보고서 표에 적으시오.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `8.8.8.8의 응답:` 네 줄과 `평균 = ○○ms`. 숫자는 PC 마다 다릅니다 |

**💡 힌트**

1. 명령은 `ping` 뒤에 한 칸 띄우고 주소입니다.
2. 평균은 맨 아래 `왕복 시간` 줄에 있습니다.
3. TTL 은 `응답:` 줄의 맨 끝에 있습니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 2-2</mark>

💻 **터미널에 입력합니다.**

```bash
ping 8.8.8.8
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `8.8.8.8의 응답:` 네 줄이 나옵니다. 맨 아래 `평균 = ○○ms` 의 숫자와 `응답:` 줄 끝의 `TTL=○○○` 을 보고서에 적습니다.</mark>

**왜** — 옵션이 없으면 4번 보내므로 답이 오면 `응답:` 줄이 네 개입니다. TTL 은 라우터를 하나 지날 때마다 1씩 줄어서, 거쳐 온 장비 수에 따라 값이 달라집니다.

**자주 틀리는 곳** — `시간=` 뒤 숫자 하나를 평균으로 적는 실수가 많습니다. 평균은 맨 아래 `평균 =` 줄에서 읽습니다.

**관제에서는** — 평소 평균을 적어 두었다가 「느려요」 문의가 오면 지금 값과 비교해 판단합니다.

**강사 메모** — 평균과 TTL 숫자는 학생마다 달라도 정상이라는 점을 먼저 말해 둡니다. 「TTL 은 왜 115 처럼 애매한 숫자인가요?」라는 질문에는 「상대가 처음 정한 값에서 거쳐 온 라우터 수만큼 줄어든 값」이라고 답합니다. `응답:` 줄 대신 `요청 시간이 만료되었습니다` 가 보이는 학생은 랜선과 네트워크 연결부터 확인합니다.

---

### ✍️ 문제 2-3 · 이름으로 `ping` 보내기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 터미널에서 명령 실행

터미널에서 `google.com` 에 `ping` 을 보내고, 첫 줄에서 **이름 옆 대괄호 `[ ]` 안의 숫자**를 찾으시오.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `Ping google.com [142.250.x.x] 32바이트 데이터 사용:` 꼴의 첫 줄. 대괄호 안이 이름에 해당하는 IP 주소입니다 (IP 는 장소 · 실행할 때마다 다를 수 있습니다) |

**💡 힌트**

1. 주소 자리에 이름을 그대로 씁니다.
2. 컴퓨터는 이름으로 통신하지 못합니다. 먼저 이름을 IP 주소로 바꾼 뒤 보냅니다 — 그 결과가 대괄호에 보입니다.
3. 이름을 IP 로 바꾸는 일은 **DNS** 가 합니다. 3일 차(10/14)에 자세히 배웁니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 2-3</mark>

💻 **터미널에 입력합니다.**

```bash
ping google.com
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 첫 줄 `Ping google.com [○○○.○○○.○.○] 32바이트 데이터 사용:` 의 대괄호 안이 google.com 의 IP 주소입니다.</mark>

**왜** — 컴퓨터는 이름으로 통신하지 못합니다. `ping` 이 먼저 DNS 로 이름을 IP 주소로 바꾼 뒤 보내고, 바꾼 결과를 대괄호에 보여 줍니다.

**자주 틀리는 곳** — 옆자리와 IP 가 다르면 틀렸다고 여기는데, IP 는 장소 · 실행할 때마다 다를 수 있으니 틀린 것이 아닙니다.

**관제에서는** — 로그에 수상한 도메인 이름이 보이면 그 이름이 어느 IP 로 바뀌는지 확인해 IP 기록과 맞춰 봅니다.

**강사 메모** — 대괄호 안의 IP 가 옆자리와 달라도 틀린 것이 아니라는 점을 강조합니다. 「왜 사람마다 IP 가 달라요?」라는 질문에는 「큰 서비스는 서버를 여러 대 두고, DNS 가 그중 하나의 주소를 알려 주기 때문」이라고 답합니다. 학원 PC 가 이름을 물어보는 DNS 서버는 `168.126.63.1`(kns.kornet.net)이고, 3일 차에 다시 봅니다.

---

### ✍️ 문제 2-4 · 두 가지 실패를 구별하기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 터미널에서 명령 실행 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 실습 기록` 의 `- 2-4:` 줄

아래 두 명령을 터미널에 차례로 입력하고, **실패 문구가 어떻게 다른지** 한 줄씩 적으시오.

```bash
ping abc.nowhere-not-exist
ping 192.0.2.1
```

| | |
|---|---|
| 🎯 나와야 하는 결과 | 첫째는 `호스트를 찾을 수 없습니다` — **이름을 IP 로 못 바꿨다.** 둘째는 `요청 시간이 만료되었습니다` 네 줄 — **주소는 있는데 답이 안 온다** |

**💡 힌트**

1. 첫째는 존재하지 않는 이름입니다. 보내 보기도 전에 멈춥니다.
2. 둘째 `192.0.2.1` 은 문서 예시용으로 비워 둔 주소라 아무도 답하지 않습니다.
3. 둘 다 「안 된다」지만 **멈춘 자리가 다릅니다.** 4교시에 이 차이로 층을 좁힙니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 2-4</mark>

💻 **터미널에 입력합니다.**

```bash
ping abc.nowhere-not-exist
ping 192.0.2.1
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 첫째는 `Ping 요청에서 abc.nowhere-not-exist 호스트를 찾을 수 없습니다.` 한 줄, 둘째는 `요청 시간이 만료되었습니다.` 네 줄입니다.</mark>

**왜** — 첫째는 이름을 IP 로 바꾸지 못해 보내기 전에 멈췄습니다. 둘째는 주소로 보냈지만 `192.0.2.1` 은 아무도 쓰지 않는 주소라 답이 오지 않았습니다.

**자주 틀리는 곳** — 둘 다 「안 된다」로 묶어 적는 실수가 많습니다. 멈춘 자리(이름 변환 · 응답)를 나눠 적습니다.

**관제에서는** — 첫째 문구면 DNS 를, 둘째 문구면 망이나 상대 서버를 확인하러 가므로 첫 판단이 여기서 갈립니다.

**강사 메모** — 두 실패 문구를 칠판에 나란히 적고 「멈춘 자리가 다르다」를 강조합니다. 이 구별이 4-5 의 층 좁히기로 이어집니다. 「`192.0.2.1` 은 왜 아무도 안 쓰나요?」라는 질문에는 「문서 예시용으로 비워 둔 주소 범위라 실제 장비에 주지 않는다」고 답합니다. 둘째 명령은 네 줄이 모두 나올 때까지 몇 초씩 걸리므로 끝날 때까지 기다리게 합니다.

---

### ✍️ 문제 2-5 · 열 번 보내서 손실 보기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 터미널에서 명령 실행 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 실습 기록` 의 `- 2-5:` 줄

터미널에서 `8.8.8.8` 에 **열 번** `ping` 을 보내고, 받은 개수와 손실 % 를 적으시오.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `패킷: 보냄 = 10, 받음 = 10, 손실 = 0 (0% 손실)` 꼴. 학원망이 붐비면 손실이 생길 수 있습니다 (받음 · 손실 숫자는 실행할 때마다 다릅니다) |

**💡 힌트**

1. 횟수를 정하는 옵션은 바로 위 명령 상자에 있습니다.
2. 옵션은 주소 **앞**에 씁니다.
3. 10번이라 10초쯤 걸립니다. 기다립니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 2-5</mark>

💻 **터미널에 입력합니다.**

```bash
ping -n 10 8.8.8.8
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `패킷: 보냄 = 10, 받음 = ○○, 손실 = ○ (○% 손실)` 줄을 읽습니다. 학원망이 붐비지 않으면 `받음 = 10, 손실 = 0 (0% 손실)` 입니다.</mark>

**왜** — `-n 10` 이 보낼 횟수를 10번으로 정합니다. 4번보다 많이 보내야 가끔 생기는 손실도 숫자로 잡힙니다.

**자주 틀리는 곳** — 검색한 글을 따라 리눅스식 `-c 10` 을 쓰는 실수가 많습니다. Windows 의 `ping` 은 `-n 10` 입니다.

**관제에서는** — 장애 보고에 「10번 중 몇 번 손실」처럼 손실 % 를 숫자로 남겨 회선 상태를 기록합니다.

**강사 메모** — 대부분 `손실 = 0 (0% 손실)` 이 나오므로, 손실이 난 학생이 있으면 그 화면을 반 전체에 보여 줍니다. 「`-t` 로 보내도 되나요?」라는 질문에는 「`Ctrl + C` 로 멈춘 시점까지의 개수가 통계에 나오므로 10번으로 정해지지 않는다」고 답합니다. 10초쯤 기다리는 동안 다음 문제를 미리 안내합니다.

---

### ⭐ 도전 2-6 · `ping` 결과를 파이썬으로 판정하기 (선택)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — VS Code 에서 `ping_check.py` 만들기 → 터미널에서 `python ping_check.py` 실행

`ping` 결과를 사람이 매번 읽는 대신, 파이썬이 「정상 · 느림 · 실패」를 판정하게 하시오.

1. `network_zt` 폴더에 `ping_check.py` 를 만들고 아래를 붙여 넣습니다.
2. 번호 주석 아래를 채웁니다.
3. 터미널에 `python ping_check.py` 를 입력합니다.

```python
# ── 강사용: 정답을 채운 코드입니다 ──
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
```

**파일을 만들고 실행합니다**

1. VS Code 왼쪽 목록에서 `network_zt` 폴더를 오른쪽 클릭 › **New File** › 이름 `ping_check.py` 를 입력하고 Enter 를 누릅니다.
2. 위 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 로 복사해 파일에 붙여 넣은 뒤, 번호 주석 아래를 채웁니다. 저장은 자동입니다.
3. 터미널에 아래 명령을 입력합니다. 터미널의 줄 위에 `…/network_zt` 가 보여야 합니다. 아니면 먼저 `cd network_zt` 를 입력합니다.

```bash
python ping_check.py
```

4. 고친 뒤에는 같은 명령을 다시 입력합니다. 터미널에서 **↑(위 화살표)** 를 누르면 방금 입력한 명령이 다시 나옵니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `[정상] 8.8.8.8 34ms` · `[느림] 1.1.1.1 120ms` · `[실패] 192.0.2.1 응답 없음` |

**💡 힌트**

1. 갈래가 셋이라 `if` · `elif` · `else` 를 씁니다.
2. `None` 인지는 `is None` 으로 봅니다. **이 비교를 맨 먼저** 합니다 — `None > 100` 은 에러가 납니다.
3. 1과목 10/8 의 `needs_approval` 처럼 「기준값은 맨 위 변수 하나」로 둡니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 2-6</mark>

(코드는 위 문제 칸에 채워 두었습니다.)

💻 **터미널에 입력합니다.**

```bash
python ping_check.py
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `[정상] 8.8.8.8 34ms` · `[느림] 1.1.1.1 120ms` · `[실패] 192.0.2.1 응답 없음` 세 줄입니다.</mark>

**왜** — `None` 검사를 맨 앞에 두어서 답이 없는 결과는 숫자 비교까지 가지 않습니다. `120` 은 `LIMIT` 100 보다 커서 느림입니다.

**자주 틀리는 곳** — `> LIMIT` 비교를 먼저 쓰면 `None > 100` 에서 `TypeError` 가 나고 멈춥니다.

**관제에서는** — 여러 대상의 결과를 같은 기준으로 나눠 두면 사람은 [느림] · [실패] 줄만 확인하면 됩니다.

**강사 메모** — `None` 검사를 맨 앞에 두는 순서가 이 문제의 핵심이라는 점을 강조합니다. 「`== None` 으로 써도 되나요?」라는 질문에는 「이 코드에서는 결과가 같지만, `None` 비교는 `is None` 으로 쓰는 것이 관례」라고 답합니다. `TypeError` 가 난 학생에게는 조건의 순서만 바꾸게 하고, 끝난 학생에게는 「`LIMIT` 을 30 으로 바꾸면?」(`8.8.8.8` 도 [느림])을 물어 봅니다.

### 2교시 한눈에

| 하려는 일 | 명령 |
|---|---|
| 닿는지 본다 | `ping 주소` |
| 횟수를 정한다 | `ping -n 10 주소` |
| 이름이 IP 로 바뀌는지 본다 | `ping 이름` — 첫 줄의 대괄호 |
| 실패를 구별한다 | `호스트를 찾을 수 없습니다`(이름) vs `요청 시간이 만료되었습니다`(응답 없음) |

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">3교시 (11:00–11:50) · OSI 7계층 ① 아래 세 층 — MAC 과 IP</mark>

### 왜 필요한가

1. 네트워크는 하는 일을 **일곱 층**으로 나눠 놓았습니다. 층마다 맡은 일이 달라서, 문제가 생기면 층을 나눠 원인을 찾을 수 있습니다.
2. 3교시에는 **아래 세 층**을 봅니다 — 신호(1층), 같은 망 안의 배달(2층), 멀리까지 길 찾기(3층).
3. 2층과 3층에는 각각 **주소**가 있습니다 — MAC 주소와 IP 주소. 둘을 구별하는 것이 오늘의 핵심입니다.

### 3.1 OSI 7계층 한눈에

| 층 | 이름 | 하는 일 | 쓰는 주소 · 단위 | 오늘 보는 명령 |
|---|---|---|---|---|
| 7 | 응용 (Application) | 사용자가 쓰는 서비스 — 웹 · 메일 · DNS | URL(유알엘 · 웹 주소) · 도메인 이름(`google.com` 같은 이름) | `ping 이름` |
| 6 | 표현 (Presentation) | 암호화 · 압축 · 글자 형식 | — | — |
| 5 | 세션 (Session) | 대화의 시작과 끝을 관리 | — | — |
| 4 | 전송 (Transport) | 어느 프로그램에 줄지 — TCP(티시피) · UDP(유디피) | **포트 번호** | `netstat` (4교시) |
| 3 | 네트워크 (Network) | 멀리 있는 상대까지 길 찾기 | **IP 주소** | `ipconfig` · `ping` |
| 2 | 데이터링크 (Data Link) | 같은 망 안에서 옆 장비로 배달 | **MAC 주소** | `ipconfig //all` · `arp -a` |
| 1 | 물리 (Physical) | 전기 · 빛 · 전파 신호 | — | 랜선 · Wi-Fi |

실무에서는 5 · 6 · 7층을 묶어 「응용 계층」으로 부르는 **TCP/IP 4계층**도 많이 씁니다.

#### 개념 상자 · IP 주소와 MAC 주소

| | IP 주소 | MAC 주소 (물리적 주소) |
|---|---|---|
| 층 | 3층 | 2층 |
| 모양 | 숫자 4덩어리, 점으로 구분 — `192.168.0.15` | 16진수(0~9 와 A~F 로 세는 수) 6덩어리, `-` 로 구분 — `A4-B1-C2-D3-E4-F5` |
| 누가 정하나 | 망에 들어갈 때 받는다 — 장소가 바뀌면 바뀐다 | 랜카드(랜선을 꽂는 부품) · Wi-Fi(와이파이) 장치에 새겨져 나온다 |
| 쓰는 범위 | 인터넷 전체 — 멀리 있는 상대 | **같은 망 안** — 바로 옆 장비까지 |

⚠ 한 PC 에 MAC 주소가 여러 개일 수 있습니다. 랜 · Wi-Fi · 가상 장치마다 하나씩입니다. <mark style="background:#ffcdd2; color:#1a1a1a; padding:0 4px; border-radius:3px">기본 게이트웨이가 적힌 장치</mark>가 지금 쓰는 장치입니다. 게이트웨이(gateway)는 우리 망에서 바깥 인터넷으로 나가는 출구로, 보통 공유기입니다.

---

### ✍️ 문제 3-1 · 무엇이 보일까요

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 실행하지 않고 머리로 예상합니다

아래는 `ipconfig //all` 결과의 일부입니다. ① MAC 주소 ② IP 주소 ③ 기본 게이트웨이가 각각 몇째 줄인지 적어 보세요.

```
이더넷 어댑터 이더넷:

   물리적 주소 . . . . . . . . . . . : A4-B1-C2-D3-E4-F5
   IPv4 주소 . . . . . . . . . . . . : 192.168.0.15(기본 설정)
   서브넷 마스크 . . . . . . . . . . : 255.255.255.0
   기본 게이트웨이 . . . . . . . . . : 192.168.0.1
```

막히면 바로 위 개념 상자를 다시 봅니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답</mark>

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — ① `물리적 주소` 줄 ② `IPv4 주소` 줄 ③ `기본 게이트웨이` 줄.</mark>

**왜** — 모양으로 가립니다. MAC 주소는 `-` 로 나뉜 16진수 6덩어리, IP 주소는 점으로 나뉜 숫자 4덩어리입니다. 게이트웨이는 우리 망에서 바깥 인터넷으로 나가는 장비(보통 공유기)의 IP 주소입니다.

**자주 틀리는 곳** — `서브넷 마스크` 의 `255.255.255.0` 도 점으로 나뉜 4덩어리라 IP 주소로 착각하기 쉽습니다.

**관제에서는** — 로그에는 IP 와 MAC 이 섞여 나오므로 모양만 보고 몇 층의 주소인지 바로 가려야 합니다.

**강사 메모** — 서브넷 마스크를 IP 주소로 착각하는 학생이 많으므로, 줄 이름(`IPv4 주소` · `서브넷 마스크`)을 먼저 읽는 습관을 강조합니다. 「서브넷 마스크는 뭔가요?」라는 질문에는 「IP 주소 가운데 어디까지가 같은 망 번호인지 정하는 값」이라고 한 줄로 답합니다. 학원 PC 에서는 `255.255.0.0` 이 나와 예시와 다르다는 점도 미리 알려 둡니다.

---

### ✍️ 문제 3-2 · 내 IP 주소와 게이트웨이 찾기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 터미널에서 명령 실행 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 **1절 표**

`ipconfig` 를 입력하고, **기본 게이트웨이가 적힌 장치**의 IPv4(아이피 브이포 · 지금 널리 쓰는 IP 주소 형식) 주소와 기본 게이트웨이를 보고서 표에 적으시오.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `IPv4 주소 . . . : ○○○.○○○.○.○○` 와 `기본 게이트웨이 . . . : ○○○.○○○.○.○` (값은 PC 마다 다릅니다) |

**💡 힌트**

1. 옵션 없이 `ipconfig` 만 입력합니다.
2. 장치가 여러 개 보이면 **기본 게이트웨이 칸이 비어 있지 않은 것**을 고릅니다.
3. 학원 PC 는 보통 `이더넷 어댑터`, 노트북은 `무선 LAN 어댑터 Wi-Fi` 입니다. 어댑터(adapter)는 네트워크에 연결하는 장치, 이더넷(Ethernet)은 랜선 연결입니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 3-2</mark>

💻 **터미널에 입력합니다.**

```bash
ipconfig
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `IPv4 주소 . . . : ○○○.○○○.○.○○` 와 `기본 게이트웨이 . . . : ○○○.○○○.○.○`. 기본 게이트웨이 칸이 비어 있지 않은 장치의 두 값을 적습니다.</mark>

**왜** — 게이트웨이가 적힌 장치가 지금 바깥 인터넷과 통신하는 장치입니다. IP 주소는 망에 들어갈 때 받는 값이라 PC 마다 다릅니다.

**자주 틀리는 곳** — 맨 위에 보이는 장치의 값을 그대로 적는 실수가 많습니다. 게이트웨이 칸이 빈 장치는 지금 쓰는 장치가 아닙니다.

**관제에서는** — 경보에 찍힌 IP 가 어느 PC 인지 찾을 때 이 값으로 맞춰 봅니다.

**강사 메모** — 학원 PC 는 기본 게이트웨이가 `192.168.1.1`, 서브넷 마스크가 `255.255.0.0` 으로 나오는지 학생 화면에서 확인합니다. 「장치가 여러 개 나오는데 어느 것인가요?」라는 질문에는 「기본 게이트웨이 칸이 차 있는 장치 하나만 본다」고 답합니다. 학원 PC 에서 쓰는 장치 이름은 `이더넷 2` 로, Wireshark 에서 고르는 인터페이스 이름과 같습니다.

---

### ✍️ 문제 3-3 · 내 MAC 주소 찾기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 터미널에서 명령 실행 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 **1절 표**

`ipconfig //all` 을 입력하고, 3-2 와 **같은 장치**의 물리적 주소를 보고서 표에 적으시오.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `물리적 주소 . . . : ○○-○○-○○-○○-○○-○○` (값은 PC 마다 다릅니다) |

**💡 힌트**

1. `//all` 은 「자세히 전부」 보여 달라는 옵션입니다. Git Bash 에서는 슬래시를 두 번 씁니다(0.2).
2. 줄이 많습니다. 3-2 에서 고른 장치 이름 아래를 봅니다.
3. 사용법 안내만 나오면 슬래시를 하나만 쓴 것입니다. `ipconfig //all` 로 다시 입력합니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 3-3</mark>

💻 **터미널에 입력합니다.**

```bash
ipconfig //all
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 3-2 와 같은 장치 이름 아래의 `물리적 주소 . . . : ○○-○○-○○-○○-○○-○○` 를 적습니다.</mark>

**왜** — MAC 주소는 2층 주소라 옵션 없는 `ipconfig` 에는 나오지 않고 `//all` 로 자세히 볼 때 나옵니다.

**자주 틀리는 곳** — `/all` 처럼 슬래시를 하나만 쓰면 Git Bash 가 경로로 바꿔서 사용법 안내만 나옵니다.

**관제에서는** — IP 는 장소가 바뀌면 바뀌지만 MAC 은 장치에 새겨져 있어서, 같은 기기인지 확인할 때 MAC 을 봅니다.

**강사 메모** — Git Bash 에서는 슬래시를 두 번 써야 한다는 점을 다시 강조합니다. 「왜 슬래시를 두 번 쓰나요?」라는 질문에는 「Git Bash 가 `/all` 을 폴더 경로로 바꿔 버리기 때문에, 두 번 써서 그대로 넘긴다」고 답합니다. 화면에 사용법 안내만 나온 학생이 있는지 돌아보고, 3-2 와 다른 장치의 값을 적지 않았는지 장치 이름을 함께 확인합니다.

---

### ✍️ 문제 3-4 · 게이트웨이까지 `ping`

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 터미널에서 명령 실행 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 **1절 표**

터미널에서 3-2 에서 찾은 기본 게이트웨이에 `ping` 을 보내고, 평균 왕복 시간을 **2-2 의 `8.8.8.8` 결과와 비교**하시오.

| | |
|---|---|
| 🎯 나와야 하는 결과 | 게이트웨이 평균은 보통 `1~5ms` — `8.8.8.8` 보다 훨씬 짧습니다 (시간은 PC · 실행할 때마다 다릅니다) |

**💡 힌트**

1. `ping` 뒤에 게이트웨이 주소를 씁니다.
2. 게이트웨이는 같은 건물 안, `8.8.8.8` 은 인터넷 건너편입니다. 거리가 시간 차이로 보입니다.
3. 게이트웨이에서 이미 답이 없으면 **바깥이 아니라 우리 망 안**이 문제입니다(4교시 4-5).

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 3-4</mark>

💻 **터미널에 입력합니다.** 주소 자리에는 3-2 에서 찾은 내 기본 게이트웨이를 씁니다.

```bash
ping 192.168.0.1
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 게이트웨이 평균은 보통 `1~5ms` 로, 2-2 의 `8.8.8.8` 평균보다 훨씬 작게 나옵니다.</mark>

**왜** — 게이트웨이는 같은 건물 안에 있고 `8.8.8.8` 은 인터넷 건너편에 있습니다. 거리가 가깝고 거쳐 가는 장비가 적을수록 왕복 시간이 짧습니다.

**자주 틀리는 곳** — 예시의 `192.168.0.1` 을 그대로 입력하는 실수가 많습니다. 3-2 에서 찾은 내 게이트웨이 주소를 씁니다.

**관제에서는** — 게이트웨이까지도 느리거나 답이 없으면 우리 망 안을, 게이트웨이는 빠른데 바깥만 느리면 우리 망 바깥을 먼저 봅니다.

**강사 메모** — 학원 망의 게이트웨이는 `192.168.1.1` 이므로, 정답 예시의 `192.168.0.1` 을 그대로 입력한 학생이 없는지 확인합니다. 「게이트웨이가 답을 안 하면 망이 끊긴 건가요?」라는 질문에는 「대개 그렇지만, 장비 설정에 따라 `ping` 에 답하지 않게 해 둔 경우도 있다」고 답합니다. 두세 명의 게이트웨이 평균과 `8.8.8.8` 평균을 불러 칠판에 나란히 적으면 차이가 바로 보입니다.

---

### ✍️ 문제 3-5 · 같은 망의 이웃 명단 보기 — `arp -a`

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 터미널에서 명령 실행 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 실습 기록` 의 `- 3-5:` 줄

`arp -a` 를 입력하고, **기본 게이트웨이 IP 의 MAC 주소**와 그 줄의 **유형**을 적으시오.

```
인터페이스: 192.168.0.15 --- 0x9
  인터넷 주소           물리적 주소           유형
  192.168.0.1           a8-5e-45-01-2b-3c     동적
  192.168.0.255         ff-ff-ff-ff-ff-ff     정적
```

| | |
|---|---|
| 🎯 나와야 하는 결과 | 게이트웨이 IP 줄의 `물리적 주소` 와 `동적` (주소 값은 PC 마다 다릅니다) |

**💡 힌트**

1. **ARP**(에이알피 · Address Resolution Protocol) 는 「이 IP 의 MAC 이 뭐예요?」 하고 같은 망에 묻는 방법입니다. 그 답을 PC 가 잠시 적어 둔 명단이 이 표입니다.
2. `동적` 은 물어봐서 알아낸 것, `정적` 은 미리 정해진 것입니다.
3. `ff-ff-ff-ff-ff-ff` 는 특정 장비가 아니라 **같은 망 전체에 보내는 주소**(브로드캐스트)입니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 3-5</mark>

💻 **터미널에 입력합니다.**

```bash
arp -a
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `인터넷 주소` 가 내 기본 게이트웨이인 줄의 `물리적 주소`(○○-○○-○○-○○-○○-○○)를 적고, 유형은 `동적` 입니다.</mark>

**왜** — PC 는 같은 망의 게이트웨이에 보내려면 그 MAC 주소를 알아야 해서 ARP 로 물어봅니다. 물어봐서 알아낸 값이라 `동적` 입니다.

**자주 틀리는 곳** — `ff-ff-ff-ff-ff-ff` 를 게이트웨이 MAC 으로 적는 실수가 많습니다. 그것은 같은 망 전체에 보내는 브로드캐스트 주소입니다.

**관제에서는** — 게이트웨이 IP 의 MAC 이 평소와 달라지면 ARP 스푸핑(가짜 ARP 답으로 이 명단을 바꾸는 공격)을 의심합니다.

**강사 메모** — `ff-ff-ff-ff-ff-ff` 는 특정 장비가 아니라는 점과, 게이트웨이 줄을 IP 로 찾는다는 점을 강조합니다. 「`ipconfig //all` 에서는 대문자였는데 여기는 소문자예요」라는 질문에는 「표기만 다를 뿐 같은 주소」라고 답합니다. `인터페이스:` 줄이 여러 개면 내 IP 가 적힌 줄 아래를 보게 하고, 게이트웨이 줄이 없으면 3-4 의 `ping` 을 한 번 보낸 뒤 다시 `arp -a` 를 입력하게 합니다.

---

### ⭐ 도전 3-6 · 주소 모양으로 IP 와 MAC 구별하기 (선택)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — VS Code 에서 `addr_kind.py` 만들기 → 터미널에서 `python addr_kind.py` 실행

로그에 섞여 들어온 주소가 IP 인지 MAC 인지 파이썬이 가려내게 하시오. `network_zt` 에 `addr_kind.py` 를 만들어 붙여 넣고, 번호 주석 아래를 채운 뒤 `python addr_kind.py` 를 입력합니다.

```python
# ── 강사용: 정답을 채운 코드입니다 ──
def kind(address):                                # 주소의 모양을 보고 종류를 돌려주는 함수
    # 1. address 를 "." 로 나눈 조각이 4개이면 "IP" 를 return 하세요
    if len(address.split(".")) == 4:              # 점으로 나눠 네 조각이면
        return "IP"
    # 2. address 를 "-" 로 나눈 조각이 6개이면 "MAC" 을 return 하세요
    if len(address.split("-")) == 6:              # - 로 나눠 여섯 조각이면
        return "MAC"
    # 3. 둘 다 아니면 "모름" 을 return 하세요
    return "모름"                                  # 둘 다 아니면


for a in ["192.168.0.15", "a8-5e-45-01-2b-3c", "ff-ff-ff-ff-ff-ff", "192.168.0"]:
    print(kind(a), a)                             # 종류와 주소를 한 줄에
```

**파일을 만들고 실행합니다**

1. VS Code 왼쪽 목록에서 `network_zt` 폴더를 오른쪽 클릭 › **New File** › 이름 `addr_kind.py` 를 입력하고 Enter 를 누릅니다.
2. 위 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 로 복사해 파일에 붙여 넣은 뒤, 번호 주석 아래를 채웁니다. 저장은 자동입니다.
3. 터미널에 아래 명령을 입력합니다. 터미널의 줄 위에 `…/network_zt` 가 보여야 합니다. 아니면 먼저 `cd network_zt` 를 입력합니다.

```bash
python addr_kind.py
```

4. 고친 뒤에는 같은 명령을 다시 입력합니다. 터미널에서 **↑(위 화살표)** 를 누르면 방금 입력한 명령이 다시 나옵니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `IP 192.168.0.15` · `MAC a8-5e-45-01-2b-3c` · `MAC ff-ff-ff-ff-ff-ff` · `모름 192.168.0` |

**💡 힌트**

1. `"192.168.0.15".split(".")` 은 `['192', '168', '0', '15']` 입니다.
2. 조각의 개수는 `len()` 으로 셉니다.
3. `return` 을 만나면 함수는 거기서 끝납니다. 그래서 `else` 없이 순서대로 써도 됩니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 3-6</mark>

(코드는 위 문제 칸에 채워 두었습니다.)

💻 **터미널에 입력합니다.**

```bash
python addr_kind.py
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `IP 192.168.0.15` · `MAC a8-5e-45-01-2b-3c` · `MAC ff-ff-ff-ff-ff-ff` · `모름 192.168.0` 네 줄입니다.</mark>

**왜** — `192.168.0` 은 점으로 나누면 3조각, `-` 로 나누면 1조각이라 두 조건에 모두 맞지 않아 `모름` 입니다. `return` 을 만나면 함수가 끝나서 위 조건부터 차례로 검사됩니다.

**자주 틀리는 곳** — `len()` 없이 `address.split(".") == 4` 로 쓰면 목록과 숫자를 비교하게 되어 늘 거짓이고 전부 `모름` 이 나옵니다.

**관제에서는** — 로그에 섞여 들어온 주소를 종류별로 나눠야 IP 는 IP 끼리, MAC 은 MAC 끼리 모아 볼 수 있습니다.

**강사 메모** — `len()` 으로 조각의 개수를 센다는 점과, `return` 에서 함수가 끝나는 흐름을 강조합니다. 「`192.168.0.999` 도 IP 로 나오는데 맞나요?」라는 질문에는 「이 함수는 모양만 보므로 맞고, 숫자 범위는 검사하지 않는다」고 답합니다. 끝난 학생에게는 「`255.255.0.0` 을 넣으면?」(IP)을 물어 3-1 의 서브넷 마스크 착각과 이어 줍니다.

### 3교시 한눈에

| 층 | 주소 | 보는 명령 |
|---|---|---|
| 3 네트워크 | IP 주소 — `192.168.0.15` | `ipconfig` |
| 2 데이터링크 | MAC 주소 — `A4-B1-C2-D3-E4-F5` | `ipconfig //all` |
| 2 ↔ 3 잇기 | IP → MAC 명단 | `arp -a` |

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">4교시 (12:00–12:50) · OSI 7계층 ② 위 네 층 — 포트와 지금의 연결</mark>

### 왜 필요한가

1. IP 주소는 **어느 컴퓨터**인지까지만 알려 줍니다. 한 컴퓨터에는 브라우저 · 메신저 · 업데이트 같은 프로그램이 동시에 통신합니다.
2. 그중 **어느 프로그램**에 줄지는 4층의 **포트 번호**가 정합니다.
3. 관제는 「지금 이 PC 가 **누구와 · 어느 포트로** 연결돼 있나」를 봅니다. 모르는 연결이 있으면 의심합니다.

### 4.1 관제가 외워 두는 포트

> 학생 문서에서는 아래 표의 일부 칸이 **[찾아 쓰기]** 로 비어 있습니다. 강사용에는 채운 표를 둡니다.

| 포트 | 서비스 | 쓰임 |
|---|---|---|
| 22 | SSH(에스에스에이치) | 서버 원격 접속 (리눅스) |
| 53 | DNS | 이름 → IP 주소 |
| 80 | HTTP | 웹 (암호화 없음) |
| 443 | HTTPS(에이치티티피에스) | 웹 (암호화) — 요즘 웹은 거의 다 이것 |
| 3389 | RDP(알디피) | 원격 데스크톱 (Windows) — 외부에 열려 있으면 공격 대상 |
| 135 · 445 | RPC(알피시) · SMB(에스엠비) | Windows 파일 공유 — 랜섬웨어(파일을 잠그고 돈을 요구하는 악성 코드)가 자주 노리는 문 |

#### 명령 상자 · 포트 번호와 PID, `netstat` 의 옵션

| | 포트 번호 | PID(피아이디 · Process ID) |
|---|---|---|
| 뜻 | 통신의 **문 번호** | 실행 중인 **프로그램의 번호** |
| 어디서 보나 | 주소 뒤 `:443` | `netstat -ano` 의 맨 끝 칸 |

| 쓰는 것 | 뜻 |
|---|---|
| `netstat -n` | 지금의 연결을 숫자 주소로 보여 준다 |
| `-a` | 연결뿐 아니라 **듣고 있는(LISTENING · 리스닝) 문**까지 전부 |
| `-o` | 그 연결을 가진 프로그램의 **PID** 를 붙인다 |
| `\| grep 글자` | 앞 명령의 결과에서 그 글자가 든 줄만 남긴다. `\|` 는 파이프(pipe) — 앞 결과를 뒤 명령에 넘긴다. `grep`(그렙) |
| `tasklist` | 실행 중인 프로그램 목록과 PID(태스크리스트). `tasklist \| grep 1234` 는 PID 가 1234 인 줄만 |

⚠ `192.168.0.15:51234` 처럼 <mark style="background:#ffcdd2; color:#1a1a1a; padding:0 4px; border-radius:3px">내 쪽 포트가 큰 숫자</mark>인 것은 PC 가 그때그때 고른 임시 번호입니다. 서비스를 알려 주는 것은 <mark style="background:#ffcdd2; color:#1a1a1a; padding:0 4px; border-radius:3px">상대 쪽 포트</mark>(`:443`)입니다.

---

### ✍️ 문제 4-1 · 무엇이 보일까요

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 실행하지 않고 머리로 예상합니다

아래 파이썬 코드를 실행하면 화면에 무엇이 보일지 적어 보세요.

```python
PORTS = {80: "HTTP", 443: "HTTPS", 53: "DNS"}
print(PORTS[443])
print(PORTS.get(3389, "모름"))
```

막히면 바로 위 `4.1` 표와 1과목의 `.get()` 을 떠올립니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답</mark>

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `HTTPS` 와 `모름` 두 줄입니다.</mark>

**왜** — `PORTS[443]` 은 키 443 의 값을 꺼냅니다. `3389` 는 사전에 없는 키라 `.get` 의 두 번째 값 `"모름"` 이 나옵니다.

**자주 틀리는 곳** — `.get(3389, "모름")` 에서 에러가 난다고 답하는 실수가 많습니다. 에러(`KeyError`)는 `PORTS[3389]` 처럼 대괄호로 꺼낼 때 납니다.

**관제에서는** — 표에 없는 포트를 「모름」으로 표시해 두면 그 줄만 따로 골라 확인할 수 있습니다.

**강사 메모** — 대괄호로 꺼내기와 `.get` 으로 꺼내기의 차이를 다시 짚습니다. 「`.get` 에 두 번째 값을 안 주면 어떻게 되나요?」라는 질문에는 「에러 없이 `None` 이 나온다」고 답합니다. 이 차이가 4-6 에서 그대로 쓰이므로 여기서 확실히 정리합니다.

---

### ✍️ 문제 4-2 · 지금의 연결 보기 — `netstat -n`

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 터미널에서 명령 실행 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 실습 기록` 의 `- 4-2:` 줄

`netstat -n` 을 입력하고, `ESTABLISHED`(이스태블리시드 · 연결된 상태) 줄 하나를 골라 **외부 주소의 포트**와 그 포트의 **서비스 이름**(4.1 표)을 적으시오.

```
활성 연결

  프로토콜  로컬 주소              외부 주소              상태
  TCP    192.168.0.15:51234     203.0.113.10:443       ESTABLISHED
```

| | |
|---|---|
| 🎯 나와야 하는 결과 | 예: 외부 포트 `443` → `HTTPS`. 브라우저를 켜 두면 443 줄이 여러 개 보입니다 |

**💡 힌트**

1. `ESTABLISHED` 는 「연결된 상태」입니다.
2. 외부 주소의 **`:` 뒤 숫자**가 상대 쪽 포트입니다.
3. 줄이 너무 많으면 브라우저를 하나 열어 둔 채 다시 입력합니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 4-2</mark>

💻 **터미널에 입력합니다.**

```bash
netstat -n
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `ESTABLISHED` 줄의 `외부 주소` 에서 `:` 뒤 숫자를 읽고, 4.1 표에서 서비스 이름을 찾습니다. 예: `443` 이면 `HTTPS` 입니다.</mark>

**왜** — 서비스를 알려 주는 것은 상대 쪽 포트입니다. 요즘 웹은 거의 다 HTTPS 라서 브라우저를 켜 두면 443 줄이 여러 개 보입니다.

**자주 틀리는 곳** — `로컬 주소` 의 `:51234` 같은 큰 숫자를 읽는 실수가 많습니다. 그것은 내 PC 가 그때그때 고른 임시 번호입니다.

**관제에서는** — 외부 포트가 평소 보지 못한 번호면 그 연결을 확인 대상으로 올립니다.

**강사 메모** — 로컬 주소가 아니라 외부 주소의 포트를 읽는다는 점을 강조합니다. 「외부 주소가 `127.0.0.1` 인 줄은 뭔가요?」라는 질문에는 「내 PC 안의 프로그램끼리 연결된 것」이라고 답합니다. 줄이 너무 많은 학생에게는 `netstat -n | grep ESTABLISHED` 로 연결된 줄만 남기게 하고, 브라우저가 켜져 있는지 확인합니다.

---

### ✍️ 문제 4-3 · 그 연결은 어느 프로그램의 것인가

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 터미널에서 명령 실행

터미널에 `netstat -ano | grep ESTABLISHED` 를 입력해 4-2 에서 고른 줄의 **PID** 를 찾고, `tasklist | grep PID숫자` 로 그 PID 의 프로그램 이름을 찾으시오. 침해 대응에서 「이 연결은 누가 열었나」를 찾는 순서 그대로입니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | PID 숫자 하나와 프로그램 이름(예: `chrome.exe` · `msedge.exe`) |

**💡 힌트**

1. PID 는 줄의 **맨 끝 칸**입니다.
2. `tasklist | grep 1234` 처럼 PID 숫자를 넣습니다. 첫 칸이 프로그램 이름입니다.
3. 아무것도 안 나오면 작업 관리자(`Ctrl + Shift + Esc`) › **세부 정보** 탭의 PID 열에서 찾습니다.
4. PID 는 프로그램을 다시 켤 때마다 바뀝니다. 지금 화면의 숫자로 찾습니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 4-3</mark>

💻 **터미널에 입력합니다.**

```bash
netstat -ano | grep ESTABLISHED
tasklist | grep 1234
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 첫 줄로 4-2 의 줄을 찾아 맨 끝 숫자(PID)를 읽고, 둘째 줄의 `1234` 자리에 그 숫자를 넣습니다. 나온 줄의 첫 칸(예: `chrome.exe` · `msedge.exe`)이 프로그램 이름입니다.</mark>

**왜** — `-o` 가 연결 줄 맨 끝에 PID 를 붙이고, `tasklist` 는 PID 와 프로그램 이름을 함께 보여 줍니다. 같은 PID 로 두 결과를 이어서 연결을 연 프로그램을 찾습니다.

**자주 틀리는 곳** — `1234` 를 그대로 입력하는 실수가 많습니다. 내 화면에서 읽은 PID 숫자로 바꿉니다.

**관제에서는** — 수상한 외부 연결을 찾으면 이 순서로 그 연결을 연 프로그램을 밝혀 차단할 대상을 정합니다.

**강사 메모** — 「연결 → PID → 프로그램 이름」 순서가 침해 대응에서 그대로 쓰인다는 점을 강조합니다. 「`tasklist | grep` 결과가 여러 줄 나와요」라는 질문에는 「그 숫자가 메모리 칸 등에도 들어 있을 수 있으니 둘째 칸이 PID 인 줄을 고른다」고 답합니다. 브라우저는 같은 이름의 프로그램이 여러 개 떠 있어서 PID 가 여럿 보인다는 점도 함께 알려 줍니다.

---

### ✍️ 문제 4-4 · 내 PC 가 열어 둔 문 찾기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 터미널에서 명령 실행 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 실습 기록` 의 `- 4-4:` 줄

내 PC 가 **듣고 있는(LISTENING) 포트**만 골라 보고, 그중 **4.1 표에 있는 포트**를 적으시오.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `TCP    0.0.0.0:135 … LISTENING` · `TCP    0.0.0.0:445 … LISTENING` 꼴의 줄. 135 · 445 는 Windows 파일 공유입니다. 다른 번호(예: 22 · 80)가 더 있어도 정상입니다 — PC 마다 켜 둔 프로그램이 다릅니다 |

**💡 힌트**

1. 듣고 있는 문까지 보려면 `-a` 가 필요합니다.
2. 결과에서 `LISTENING` 이 든 줄만 남기는 방법은 명령 상자의 `| grep` 줄에 있습니다.
3. `0.0.0.0` 은 「이 PC 의 모든 주소에서 듣는다」는 뜻입니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 4-4</mark>

💻 **터미널에 입력합니다.**

```bash
netstat -an | grep LISTENING
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `TCP    0.0.0.0:135 … LISTENING` · `TCP    0.0.0.0:445 … LISTENING` 꼴의 줄에서 4.1 표에 있는 포트(135 · 445 등)를 적습니다. 다른 번호가 더 있어도 정상입니다.</mark>

**왜** — `-a` 가 듣고 있는 포트까지 보여 주고, `| grep LISTENING` 이 그 줄만 남깁니다. 135 · 445 는 Windows 파일 공유가 쓰는 포트입니다.

**자주 틀리는 곳** — `-a` 를 빼고 `netstat -n | grep LISTENING` 을 입력하면 듣고 있는 포트가 빠져서 아무 줄도 나오지 않습니다.

**관제에서는** — 듣고 있는 포트는 바깥에서 접속해 올 수 있는 곳이라, 쓰지 않는 445 · 3389 가 열려 있으면 닫도록 보고합니다.

**강사 메모** — `-a` 가 있어야 듣고 있는 포트가 보인다는 점을 강조합니다. 「445 가 열려 있으면 위험한가요?」라는 질문에는 「학원 PC 처럼 Windows 파일 공유를 쓰는 PC 에서는 기본으로 열려 있고, 바깥 인터넷에서 닿을 때 문제가 된다」고 답합니다. 학생 화면에 `3389` 가 보이면 원격 데스크톱이 켜진 PC 이므로 반 전체에 예로 보여 줍니다.

---

### ✍️ 문제 4-5 · 증상으로 층 좁히기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 명령 없이 생각해서 답하기 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day01_packet_analysis.md` 의 `## 실습 기록` 의 `- 4-5:` 줄

아래 세 증상이 **몇 층 문제일 가능성이 큰지** 3.1 표를 보며 한 줄씩 적으시오. 명령은 입력하지 않습니다.

| 증상 | 확인한 것 |
|---|---|
| ① | `ping 8.8.8.8` 은 되는데 `ping google.com` 은 `호스트를 찾을 수 없습니다` |
| ② | 기본 게이트웨이에 `ping` 해도 `요청 시간이 만료되었습니다` |
| ③ | `ping` 은 다 되는데 특정 웹 사이트만 안 열린다 |

| | |
|---|---|
| 🎯 나와야 하는 결과 | ① 이름 → IP 변환(DNS, 7층) ② 우리 망 안 — 1~3층(선 · Wi-Fi · 공유기) ③ 4층 이상 — 그 서버의 포트나 서비스 |

**💡 힌트**

1. 아래 층이 되면 그 아래는 다 된다는 뜻입니다. 「어디까지 됐나」를 먼저 봅니다.
2. ①은 숫자 주소로는 됐습니다. 그럼 3층(IP)까지는 문제가 없습니다.
3. ③은 `ping`(3층)이 됩니다. 남은 것은 그 위입니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 4-5</mark>

| 증상 | 층 | 이유 |
|---|---|---|
| ① 숫자는 되는데 이름이 안 됨 | 7층 — DNS(이름 → IP) | 숫자 주소로는 닿았으니 3층까지는 된다 |
| ② 게이트웨이도 응답 없음 | 1~3층 — 우리 망 안 | 바깥까지 가기 전에, 우리 망 안의 게이트웨이부터 답이 없다 |
| ③ `ping` 은 되는데 웹 하나만 안 됨 | 4층 이상 — 그 서버의 포트 · 서비스 | 3층(`ping`)은 되니, 그 위의 포트나 서비스가 문제다 |

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — ① 7층 DNS(이름 → IP 변환) ② 1~3층 우리 망 안(선 · Wi-Fi · 공유기) ③ 4층 이상 그 서버의 포트나 서비스.</mark>

**왜** — 아래 층부터 되는지 확인하고, 처음으로 안 되는 층을 원인으로 봅니다. 숫자 주소 `ping` 이 되면 3층까지는 정상입니다.

**자주 틀리는 곳** — ①을 「인터넷이 끊겼다」(1~3층)로 적는 실수가 많습니다. `ping 8.8.8.8` 이 되었으니 아래 층은 정상입니다.

**관제에서는** — 「인터넷이 안 돼요」 문의를 받으면 이 순서로 원인 층을 좁힌 뒤 맞는 담당자에게 넘깁니다.

**강사 메모** — 「아래 층부터 확인하고, 처음으로 안 되는 층을 원인으로 본다」는 순서를 강조합니다. 「②에서 게이트웨이가 `ping` 에 답하지 않게 설정돼 있으면요?」라는 질문에는 「그래서 `arp -a` 에 게이트웨이 MAC 이 있는지도 함께 본다」고 답합니다. 증상 ①②③을 하나씩 읽고 층 번호를 손으로 들게 하면 빨리 확인할 수 있습니다.

---

### ⭐ 도전 4-6 · 포트에 이름 붙이기 (선택)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — VS Code 에서 `port_name.py` 만들기 → 터미널에서 `python port_name.py` 실행

`netstat` 에서 본 포트 번호들에 서비스 이름을 붙여 출력하시오. 모르는 포트는 「모름」으로 둡니다. `network_zt` 에 `port_name.py` 를 만들어 붙여 넣고, 채운 뒤 `python port_name.py` 를 입력합니다.

```python
# ── 강사용: 정답을 채운 코드입니다 ──
PORTS = {22: "SSH", 53: "DNS", 80: "HTTP", 443: "HTTPS", 3389: "RDP", 135: "RPC", 445: "SMB"}
seen = [443, 445, 3389, 51234]                    # netstat 에서 본 포트라고 가정합니다

for port in seen:                                 # 포트를 하나씩 꺼낸다
    # 1. name 이라는 변수에 PORTS 에서 port 의 이름을 꺼내 담으세요. 없으면 "모름" 입니다
    name = PORTS.get(port, "모름")                 # 없는 포트는 "모름"
    # 2. f"{port} → {name}" 을 출력하세요
    print(f"{port} → {name}")
```

**파일을 만들고 실행합니다**

1. VS Code 왼쪽 목록에서 `network_zt` 폴더를 오른쪽 클릭 › **New File** › 이름 `port_name.py` 를 입력하고 Enter 를 누릅니다.
2. 위 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 로 복사해 파일에 붙여 넣은 뒤, 번호 주석 아래를 채웁니다. 저장은 자동입니다.
3. 터미널에 아래 명령을 입력합니다. 터미널의 줄 위에 `…/network_zt` 가 보여야 합니다. 아니면 먼저 `cd network_zt` 를 입력합니다.

```bash
python port_name.py
```

4. 고친 뒤에는 같은 명령을 다시 입력합니다. 터미널에서 **↑(위 화살표)** 를 누르면 방금 입력한 명령이 다시 나옵니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `443 → HTTPS` · `445 → SMB` · `3389 → RDP` · `51234 → 모름` |

**💡 힌트**

1. 없는 키에 기본값을 주는 방법은 4-1 에서 봤습니다.
2. `51234` 처럼 큰 숫자는 대개 내 쪽의 임시 포트입니다.
3. 관제에서는 `3389` 가 바깥에 열려 있으면 바로 확인합니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 4-6</mark>

(코드는 위 문제 칸에 채워 두었습니다.)

💻 **터미널에 입력합니다.**

```bash
python port_name.py
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `443 → HTTPS` · `445 → SMB` · `3389 → RDP` · `51234 → 모름` 네 줄입니다.</mark>

**왜** — `PORTS.get(port, "모름")` 은 사전에 키가 있으면 그 이름을, 없으면 `"모름"` 을 돌려줍니다. `51234` 는 사전에 없는 임시 포트입니다.

**자주 틀리는 곳** — `PORTS[port]` 로 꺼내면 `51234` 에서 `KeyError` 가 나고 멈춥니다.

**관제에서는** — `3389 → RDP` 처럼 이름이 붙어 나오면 바깥에 열려 있으면 안 되는 포트를 바로 골라 확인합니다.

**강사 메모** — 4-1 의 `.get(키, 기본값)` 을 그대로 쓰는 문제라는 점을 짚고 넘어갑니다. 「`51234` 를 「모름」 대신 「임시 포트」로 표시할 수 있나요?」라는 질문에는 「Windows 가 임시 포트로 쓰는 범위가 49152 이상이라, 조건을 하나 더 두면 된다」고 답합니다. `KeyError` 가 난 학생에게는 대괄호를 `.get` 으로 바꾸게만 합니다.

### 4교시 한눈에

| 하려는 일 | 명령 |
|---|---|
| 지금의 연결 | `netstat -n` |
| 그 연결의 프로그램 | `netstat -ano` → 작업 관리자 › 세부 정보 › PID |
| 열어 둔 문 | `netstat -an \| grep LISTENING` |
| 층 좁히기 | 숫자 주소 `ping` → 이름 `ping` → 서비스 |

---

## 오전 마무리 — 보고서 「1. 내 PC 와 네트워크」 채우기

`day01_packet_analysis.md` 의 표 여섯 칸이 모두 찼는지 봅니다. 빈 칸은 그 문제로 돌아갑니다.

| 칸 | 문제 |
|---|---|
| IPv4 주소 · 기본 게이트웨이 | 3-2 |
| MAC 주소 | 3-3 |
| 게이트웨이까지 왕복 평균 | 3-4 |
| 8.8.8.8 까지 왕복 평균 · TTL | 2-2 |

오후에는 **Wireshark** 로 오늘 `ping` · 웹 접속이 실제로 어떤 패킷이었는지 봅니다. 4교시의 `ESTABLISHED` 가 만들어지는 순간 — **3-way handshake**(쓰리웨이 핸드셰이크 · 연결을 시작할 때 주고받는 세 번의 신호)를 찾습니다.

---
