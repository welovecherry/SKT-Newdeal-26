# 10/14(수) 오전 · DNS — 이름을 IP 로 · 계층 · 레코드 · 캐시 — 실습

> **강사용 · 학생에게 나눠 주지 않습니다.** 모든 문제 바로 아래에 「정답」과 해설이 있습니다. 찾아 쓰기 표는 채워 두었습니다.
>
> **수업 전에 확인할 것**
> 1. `nslookup` 결과가 한국어(`서버:` · `권한 없는 응답:` · `이름:`)로 나오는지 — 학원 DNS 는 `kns.kornet.net`(`168.126.63.1`)
> 2. `ipconfig //flushdns` 는 관리자 권한 없이 된다(10/6 실측)
> 3. `nslookup` 은 PC 캐시를 거치지 않는다 — 캐시 실습(4-4)은 `ping` 으로 채운다

12일에 `ping google.com` 을 쳤을 때 첫 줄의 대괄호 안에 IP 주소가 나왔습니다. 그 주소는 어디서 왔을까요? 오늘은 이름을 IP 주소로 바꿔 주는 **DNS**(디엔에스 · Domain Name System)를 배웁니다.

| 교시 | 무엇 | 쓰는 것 |
|---|---|---|
| 2교시 | DNS 가 필요한 이유 · `nslookup` 첫 사용 · 이름을 못 찾을 때 | `nslookup`(엔에스룩업) · 파이썬 |
| 3교시 | DNS 계층 — 루트 · TLD · 담당 네임서버 · 「권한 없는 응답」 | `nslookup -type=ns` · 파이썬 |
| 4교시 | DNS 레코드(A · CNAME · MX · NS) · TTL · 캐시 | `nslookup -type=…` · `ipconfig //displaydns` · 파이썬 |

**오전에 남기는 것:** `network_zt/day03_dns_analysis.md` 의 **2 · 3 · 4교시 칸**. 오후에 의심 도메인 판정을 더해 완성합니다 — 강의계획서의 3일 차 산출물입니다. 평가 기준은 「`nslookup` 을 정확히 썼나 · 의심 도메인을 합리적 근거로 골랐나 · 판단 기준을 문서로 남겼나」입니다.

> **화면은 이렇게 나눠 씁니다 — 왼쪽은 실습 자료, 오른쪽은 보고서**
>
> 1. 이 파일을 누르고 `Ctrl + Shift + V` 를 누릅니다. 실습 자료가 **미리보기**로 열립니다. 이 탭이 **왼쪽**입니다.
> 2. 왼쪽 목록(탐색기)에서 보고서 파일 `day03_dns_analysis.md` 를 오른쪽 클릭하고 **Open to the Side**(옆에서 열기)를 누릅니다. 보고서가 **오른쪽** 칸에 열립니다.
> 3. **오른쪽 보고서에만 씁니다.** 왼쪽 실습 자료는 스크롤하며 읽습니다. 쓴 모양을 보고 싶으면 오른쪽 칸에서 `Ctrl + K` 를 누른 뒤 `V`.
>
> 보고서 파일은 아래 「0.4 오늘의 보고서 파일을 만듭니다」에서 만듭니다. 만든 뒤 2번부터 합니다.

---

## 시작하기

### 0.1 이 파일을 여는 법

이 파일은 **카톡으로 받은 실습 안내**입니다. 노트북이 아니라 읽으면서 따라 하는 문서입니다.

1. 카톡에서 받은 이 파일(`261014_am_dns.md`)을 `security-agent-toolkit` 안의 **`network_zt` 폴더**로 옮깁니다.
2. VS Code 왼쪽 목록에서 이 파일을 누르고, **`Ctrl + Shift + V`** 를 눌러 **미리보기**로 엽니다. 표와 굵은 글씨가 읽기 좋게 보입니다.
3. 이 파일은 **읽기만** 합니다. 내가 적는 것은 그날 **보고서 파일**과 **`.py` 파일**입니다.
4. 코드나 명령을 복사할 때는 미리보기의 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 를 누릅니다.

### 0.2 오늘 시작할 때

1. 어제와 같은 터미널(Git Bash), `network_zt` 폴더에서 합니다. 줄 앞에 `$` 가 보이면 됩니다.
2. 강의계획서에는 `dig`(디그)도 나오지만 **Windows 에는 기본으로 없습니다**(실측). 오늘은 Windows 에 들어 있는 `nslookup` 을 씁니다. 둘은 같은 일을 합니다.
3. 결과 화면 예시는 **학원 PC(한국어 Windows)에서 보이는 모양**입니다. 주소는 시간 · 장소마다 바뀔 수 있습니다.

> 맥북으로 복습할 때는 명령 상자 바로 아래의 **「맥북:」 줄**을 칩니다(없으면 Windows 와 같은 명령). 맥의 결과는 영어이고 모양이 달라 맨 아래 정답의 결과와 글자가 다릅니다 — 같은 값(IP · 이름 · TTL)을 찾으면 됩니다.

### 0.3 문제를 푸는 법

1. 문제마다 **할 일 → 왜 중요한가 → 이 문제에 나오는 말 → 순서**를 읽습니다. 순서의 `[창 이름]`을 보고 지금 할 일을 어디서 하는지 확인합니다. 마지막 `[보고서]` 단계에서 보고서에 적습니다. 문제 앞의 상자는 🐍 문법 상자(파이썬) · 명령 상자(터미널) · 개념 상자입니다.
2. 「💻 **터미널에 입력합니다.**」 아래의 명령은 터미널에 그대로 입력하고 Enter 를 누릅니다.
3. 막히면 **💡 힌트**를 보고, 그래도 막히면 문서 맨 아래 **「정답」**을 봅니다.
4. ⭐도전은 안 풀고 넘어가도 됩니다.

### 0.4 오늘의 보고서 파일을 만듭니다

1. VS Code 창 **왼쪽 끝의 세로 아이콘 줄**에서 맨 위 **탐색기**(Explorer · 종이 두 장 모양 · `Ctrl + Shift + E`)를 누릅니다. 그 오른쪽에 파일 · 폴더 목록이 열립니다. 이 문서에서 「**왼쪽 목록**」은 이 목록입니다.
2. 목록 맨 위 `SECURITY-AGENT-TOOLKIT` 아래에서 **`network_zt` 폴더**를 찾아 오른쪽 클릭 › **New File** 을 누릅니다.
3. 이름 칸에 `day03_dns_analysis.md` 를 입력하고 Enter 를 누릅니다. `network_zt` 폴더 **안에** 파일이 생겼는지 봅니다.
4. 아래 **틀 전체**를 붙여 넣습니다. 교시마다 **문제 소제목**(`### 문제 2-1 · …`)이 처음부터 다 들어 있습니다 — 문제를 풀면 그 소제목 아래를 채웁니다.
5. 쓸 때는 보고서 파일을 열고 `Ctrl + K` 를 누른 뒤 `V` 를 누릅니다. 오른쪽에 미리보기가 열려, 왼쪽에 쓰는 것이 바로 보입니다. 값은 콜론(:) 뒤에, 생각하는 질문은 `답:` 뒤에 적습니다.

```markdown
# Day 3 DNS 분석서 (이름 · 2026-10-14)

> **쓰는 법**
> - 문제를 하나 풀 때마다 그 교시의 **문제 소제목 아래**를 채웁니다.
> - **값을 적는 줄**(끝이 `:`)은 콜론 뒤에 내 화면의 값을 씁니다.
> - **생각하는 질문**(물음표)은 아래 `답:` 뒤에, 내가 확인한 것과 그렇게 생각한 이유를 씁니다. 길어지면 다음 줄에 이어 써도 됩니다.
> - 🔍 는 그 교시에 배운 내용으로 답하는 핵심 질문입니다. 답을 못 찾았으면 「모름 — 막힌 곳: …」 을 씁니다.
> - ⭐ 도전은 선택이라 비워도 됩니다.

---

## 2교시 · nslookup

### 문제 2-1 · 직접 실행해 보기

- 출력 두 줄:
- `parts[2]` 에서 도메인 이름이 나온 이유는 무엇인가요? 첫째 줄의 칸을 0 번부터 세어 보고, `//` 사이에서 무엇이 생겼는지 설명합니다.
  - 답:

### 문제 2-2 · 이름을 IP 로 — 두 DNS 서버에 묻기

- example.com 의 IPv4 · 두 번 물은 DNS 서버(위쪽 `Address`):
- 🔍 위 두 줄의 `Address` 와 아래 `Addresses` 는 각각 무엇의 주소인가요? 두 번 물은 화면을 예로 들어 설명합니다.
  - 답:

### 문제 2-3 · 내 PC 는 어느 DNS 서버에 묻나

- `DNS 서버` 줄의 주소 · 2-2 처음 화면의 위쪽 `Address` 와 같은지:

### 문제 2-4 · 없는 이름을 물으면

- 나온 문구:
- 이 답은 인터넷이 끊겼다는 뜻인가요? 10/12 2-4 의 `ping` 실패 문구와 비교해 설명합니다.
  - 답:

### ⭐ 도전 2-5 · 파이썬으로 이름 묻기

- 출력 첫 줄:

### 찾아본 것

- 2.2 표에서 찾아 쓴 「권한 없는 응답」의 뜻과 `Addresses` 의 두 가지 주소:

### 이 교시에 새로 안 것

- 이 교시에서 새로 알게 된 것:

---

## 3교시 · DNS 계층

### 문제 3-1 · 직접 실행해 보기

- 출력 두 줄:
- 둘째 줄이 첫째 줄과 다르게 나온 이유는 무엇인가요? `[-1]` 과 `[-2:]` 가 각각 무엇을 꺼냈고, 그 조각이 이름의 어느 층인지 설명합니다.
  - 답:

### 문제 3-2 · 이름을 층으로 펼치기

- `mail.google.co.kr` 의 출력:

### 문제 3-3 · example.com 의 담당 네임서버 찾기

- `nameserver =` 뒤의 담당 네임서버:

### 문제 3-4 · TLD 의 담당 네임서버 보기

- `kr.` 의 네임서버 두세 개:

### 문제 3-5 · 담당 네임서버에게 직접 물으면

- `권한 없는 응답:` 줄이 있었나 · 답의 IPv4:
- 🔍 권한 있는 응답과 권한 없는 응답은 누가 준 답인지에서 어떻게 다른가요? 2-2 와 3-5 의 화면을 예로 들어 설명합니다.
  - 답:

### 이 교시에 새로 안 것

- 이 교시에서 새로 알게 된 것:

---

## 4교시 · 레코드와 캐시

### 문제 4-1 · 직접 실행해 보기

- 출력 두 줄:
- 두 줄은 각각 안쪽 사전의 어느 칸을 꺼낸 것이고, 그 값은 DNS 레코드에서 무엇을 뜻하나요?
  - 답:

### 문제 4-2 · 메일은 어디로 가나 — MX

- 메일 서버(`mail exchanger`) · `MX preference`:

### 문제 4-3 · 별명 따라가기 — CNAME

- `canonical name` · 최종 이름(`이름:` 줄) · 별명 단계 수:

### 문제 4-4 · 내 PC 의 DNS 캐시 보기

- example.com 의 TTL · 비운 뒤 목록 · 다시 `ping` 한 뒤 목록:
- `nslookup` 이 아니라 `ping` 으로 캐시를 채운 이유는 무엇인가요?
  - 답:

### 문제 4-5 · 캐시 흉내 내기

- 출력 다섯 줄:
- 🔍 담당 네임서버에서 IP 를 바꿔도 한동안 옛 IP 로 접속되는 이유는 무엇인가요? 출력의 299초 · 300초 줄을 예로 들어 설명합니다.
  - 답:

### 이 교시에 새로 안 것

- 이 교시에서 새로 알게 된 것:

---

## 5교시 · 의심 도메인

### 문제 5-1 · 직접 실행해 보기

- 출력:
- 셋째 값(모음 수)이 그렇게 나온 이유는 무엇인가요? 조각의 글자를 하나씩 보고, 숫자 `0` 이 모음으로 세어졌는지 설명합니다.
  - 답:

### 문제 5-2 · 볼 조각 꺼내기

- `e6030.a.akamaiedge.net` 줄의 조각 · TLD:

### 문제 5-3 · 숫자 수와 모음 비율

- `kxq3vz9a.top` 줄의 출력:

### 문제 5-4 · 사칭 도메인 찾기

- `[사칭 의심]` 으로 나온 이름:

### 문제 5-5 · NXDOMAIN 이 쏟아지는 PC 찾기

- 출력:
- 🔍 DGA 에 감염된 PC 에서 NXDOMAIN 이 쏟아지는 이유는 무엇인가요?
  - 답:

### 이 교시에 새로 안 것

- 이 교시에서 새로 알게 된 것:

---

## 6교시 · 점수 규칙

### 문제 6-1 · 직접 실행해 보기

- 출력:
- 규칙마다 몇 점이 더해졌나요? 둘째 값이 그렇게 나온 이유를 설명합니다.
  - 답:

### 실습 1 · 점수 함수를 만들어 로그에 걸어 보기

#### 문제 6-2 · 점수 함수 만들기

- 출력 두 줄:

#### 문제 6-3 · 로그 12건 판정하기

- 판정이 틀린 세 줄:

### 실습 2 · 규칙을 채점하고 고치기

#### 문제 6-4 · 맞힘 · 오탐 · 미탐 세기

- 맞힘 · 오탐 · 미탐:
- 🔍 오탐과 미탐은 각각 무엇인가요? 문턱값을 낮추면 둘은 어떻게 바뀌나요?
  - 답:

#### 문제 6-5 · 예외 목록으로 오탐 줄이기

- 예외를 넣은 뒤 맞힘 · 오탐 · 미탐:
- 예외 목록에 넣는 이름이 많아지면 어떤 위험이 생기나요?
  - 답:

### 찾아본 것

- 6.3 표에서 찾아 쓴 오탐 · 미탐이 많아지면 관제에 생기는 일:

### 이 교시에 새로 안 것

- 이 교시에서 새로 알게 된 것:

---

## 7교시 · 판정표

### 문제 7-1 · 직접 실행해 보기

- 출력:
- 셋째 칸(근거)은 어떤 모양으로 찍혔나요? `', '.join(...)` 이 리스트에 한 일을 설명합니다.
  - 답:

### 문제 7-2 · 판정표 만들기

- 「의심」으로 판정된 이름:

### 문제 7-3 · 판정을 `nslookup` 으로 확인하기

- 첫째 이름의 답 · 둘째 이름의 답:

### 문제 7-4 · 분석서 완성하고 올리기

- 깃허브 `network_zt` 폴더에 보고서가 보이나요:

### 이 교시에 새로 안 것

- 이 교시에서 새로 알게 된 것:

---

## 최종 분석서 — 7교시에 완성합니다

> 오늘 만든 **의심 도메인 판별 규칙**을 다른 사람이 쓸 수 있게 정리합니다. 위에서 적은 5교시 · 6교시 · 7-2 · 7-3 의 답을 다시 보며 씁니다.

### 1. 의심 도메인 판정 — 7-2

- `report_table3.py` 의 출력을 아래에 붙여 넣는다:
- 「의심」으로 판정한 이름 하나는 어떤 규칙에 걸렸고, 그 규칙이 왜 의심의 근거가 되나요?
  - 답:

### 2. 판단 기준 — 6교시

- 규칙 다섯 개와 점수 · 문턱값 · 예외:
- 지표 하나가 아니라 점수를 더해 판정하는 이유는 무엇인가요? `xn--3e0b707e.kr` 을 예로 들어 설명합니다.
  - 답:

### 3. 규칙의 한계 — 6-5 · 7-3

- 예외를 넣은 뒤에도 놓친 이름 두 개(미탐):
- 두 이름은 왜 놓쳤고, 무엇을 더 보면 잡을 수 있나요?
  - 답:

### 4. 오늘 하루 정리

- 오늘 배운 것 가운데 가장 중요하다고 생각하는 것과 그 이유:
```

⚠ <mark style="background:#ffcdd2; color:#1a1a1a; padding:0 4px; border-radius:3px">오늘 적는 것은 모두 이 파일(`day03_dns_analysis.md`) 하나에</mark> 적습니다. 문제마다 마지막 **[보고서]** 단계에 적을 위치가 나옵니다. 각 문제의 소제목은 틀에 다 있으니 <mark style="background:#ffcdd2; color:#1a1a1a; padding:0 4px; border-radius:3px">그 소제목 아래</mark>를 채웁니다.

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">2교시 (10:00–10:50) · DNS 가 필요한 이유 · `nslookup` 첫 사용</mark>

### 왜 필요한가

1. 사람은 `naver.com` 같은 이름을 기억하지만, 컴퓨터는 **IP 주소**로만 보낼 수 있습니다. 그 사이를 잇는 것이 DNS 입니다.
2. 악성 코드도 공격자의 서버를 **이름으로** 찾아갑니다. 그래서 DNS 질의 기록은 관제가 가장 먼저 보는 로그 중 하나입니다.
3. 「인터넷이 안 돼요」의 상당수가 DNS 문제입니다. 12일 4-5 에서 「숫자 주소는 되는데 이름만 안 된다」면 7층(DNS) 문제라고 했습니다.

### 2.1 URL 과 DNS 가 묻는 것

**여기 나오는 말**

- **도메인 이름 (domain name)** (도메인 네임) — 사람이 외우는 **인터넷 이름** — `example.com`
- **URL** (유알엘) — 웹 주소 전체 — `https://example.com/news`. DNS 는 그 가운데 **도메인 이름만** 묻는다
- **DNS (Domain Name System)** (디엔에스) — 이름을 **IP 주소로 바꿔 주는** 체계

`https://example.com/news/today` 를 주소창에 치면:

| 부분 | 이름 | DNS 가 묻나 |
|---|---|---|
| `https://` | 방식(scheme) — 암호화한 웹 | 아니요 |
| `example.com` | **도메인 이름** | **예 — 이것만 묻는다** |
| `/news/today` | 경로(path) — 서버 안의 어느 페이지 | 아니요 — IP 를 알아낸 뒤 웹 서버에 묻는다 |

---

### ✍️ 문제 2-1 · 직접 실행해 보기

**할 일** — URL 을 `/` 로 자르는 코드 네 줄을 실행하고, 나온 결과 두 줄과 그 이유를 보고서에 적습니다.

**왜 중요한가** — 접속 로그의 URL 에서 DNS 가 묻는 도메인 이름만 잘라 내는 연습입니다. 오후 5교시에 도메인을 조각으로 나눠 의심 여부를 따질 때 같은 `split` 을 씁니다.

**순서**
1. **[VS Code]** `network_zt` 폴더의 `warmup.py` 를 엽니다. 없으면 새 파일로 만들고, 안에 있던 내용은 지웁니다.
2. **[VS Code]** 아래 코드를 `warmup.py` 에 그대로 따라 칩니다.
   ```python
   url = "https://example.com/news/today"   # 주소창에 친 URL
   parts = url.split("/")                   # "/" 를 기준으로 잘라 리스트로 만든다
   print(parts)                             # 잘린 조각 전체
   print(parts[2])                          # 리스트의 셋째 칸(번호 2)
   ```
3. **[터미널]** `network_zt` 폴더에서 `python warmup.py` 를 실행합니다.
   ```bash
   python warmup.py
   ```
   맥북: `python3 warmup.py`
4. **[보고서]** `day03_dns_analysis.md` 의 `## 2교시` › `### 문제 2-1` 아래를 채웁니다.
   - 출력 두 줄:
   - `parts[2]` 에서 도메인 이름이 나온 이유는 무엇인가요? 첫째 줄의 칸을 0 번부터 세어 보고, `//` 사이에서 무엇이 생겼는지 설명합니다.

막히면 바로 위 2.1 표와 1과목의 `split` 을 떠올립니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 2-1</mark>

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `['https:', '', 'example.com', 'news', 'today']` 와 `example.com` 두 줄입니다.</mark>

**왜** — `/` 로 자르면 `//` 사이가 비어 있어 빈 글자 `''` 가 하나 생깁니다. 그래서 0 번 `https:`, 1 번 `''`, 2 번 `example.com` 이 됩니다. DNS 가 묻는 것은 `parts[2]`, 곧 도메인 이름 하나입니다.

**자주 틀리는 곳** — 빈 글자 `''` 를 빼고 세어 `parts[2]` 를 `news` 로 적는 경우가 많습니다.

**관제에서는** — 접속 로그의 URL 에서 도메인만 잘라 DNS 질의 기록과 맞춰 봅니다.

**강사 메모** — 빈 글자 `''` 가 생기는 까닭은 `https:` 와 `example.com` 사이에 `/` 가 두 개 붙어 있어서라고 `/` 위치를 하나씩 짚어 주면 빠릅니다. 「빈 글자도 한 칸으로 세나요?」라는 질문에는 「네, `split` 은 빈 칸도 한 조각으로 리턴합니다」라고 답합니다. 맞힌 뒤 「`parts[3]` 은 무엇일까요?」(`news`)를 바로 물어 확인합니다.

---

### 2.2 질문이 오가는 경로와 `nslookup` 결과

**여기 나오는 말**

- **재귀 리졸버 (recursive resolver)** (리커시브 리졸버) — 내 PC **대신 여기저기 물어** 답을 찾아 주는 DNS 서버 — 학원 · 통신사 DNS · `8.8.8.8`(구글)
- **`nslookup`** (엔에스룩업) — DNS 서버에 이름을 **직접 물어보는** 명령

```
내 PC  ──「example.com 의 IP 는?」──▶  DNS 서버(재귀 리졸버)  ──…──▶ 여러 네임서버
       ◀──「104.20.23.154 입니다」──
```

내 PC 가 어느 리졸버에 묻는지는 `ipconfig //all` 의 **DNS 서버** 줄에 있습니다(2-3).

#### 명령 상자 · `nslookup` 결과 읽기

```
$ nslookup example.com
서버:    kns.kornet.net
Address:  168.126.63.1

권한 없는 응답:
이름:    example.com
Addresses:  2606:4700:10::ac42:93f3
          2606:4700:10::6814:179a
          172.66.147.243
          104.20.23.154
```

> 학생은 아래 질문을 한 번에 하나씩 검색합니다. 답은 보고서에 자기 말로 적습니다. 강사용에는 채운 표를 둡니다.
> - `nslookup` 결과의 「권한 없는 응답」(Non-authoritative answer)은 누가 준 답이라는 뜻인가요?
> - `nslookup` 결과의 `Addresses` 에서 `:` 가 든 주소와 점 네 개짜리 주소는 각각 무엇인가요?

| 줄 | 뜻 |
|---|---|
| `서버` · `Address` (위 두 줄) | **내가 물어본** DNS 서버(리졸버)의 이름 · 주소 |
| `권한 없는 응답` | 담당 네임서버가 아니라 리졸버가 찾아다 준 답(3교시 3.2) |
| `이름` | 물어본 이름 |
| `Addresses` | 답 — `:` 가 든 것은 IPv6(아이피 브이식스 · 새 방식의 긴 주소), 점 네 개짜리가 **IPv4** |

⚠ 위 두 줄의 `Address` 는 <mark style="background:#ffcdd2; color:#1a1a1a; padding:0 4px; border-radius:3px">물어본 DNS 서버</mark>의 주소입니다. example.com 의 주소는 <mark style="background:#ffcdd2; color:#1a1a1a; padding:0 4px; border-radius:3px">아래</mark> `Addresses` 입니다. 가장 많이 헷갈리는 곳입니다.

---

### ✍️ 문제 2-2 · 이름을 IP 로 — 두 DNS 서버에 묻기

**할 일** — `example.com` 을 내 PC 의 DNS 서버와 구글 DNS 서버 `8.8.8.8` 에 차례로 묻고, 답의 IPv4 주소와 두 번 물은 DNS 서버를 보고서에 적습니다.

**왜 중요한가** — 오늘 DNS 문제는 모두 `nslookup` 결과 화면을 읽고 풉니다. 관제에서는 의심 도메인이 어느 IP 로 연결되는지 이 명령으로 먼저 확인하고, 사내 DNS 서버와 외부 DNS 서버의 답을 비교해 사내 DNS 설정에 문제가 있는지 가려냅니다. 이름 뒤에 물어볼 서버를 적는 형식은 3-5 에서 다시 씁니다.

**순서**
1. **[터미널]** 내 PC 의 DNS 서버에 묻습니다.
   ```bash
   nslookup example.com
   ```
2. **[터미널]** 아래쪽 `Addresses` 에서 점 네 개짜리 IPv4 주소를 찾고, 위 두 줄(`서버` · `Address`)을 읽습니다.
3. **[터미널]** 이번에는 이름 뒤에 물어볼 DNS 서버 주소를 적어 구글 DNS 서버에 묻습니다.
   ```bash
   nslookup example.com 8.8.8.8
   ```
4. **[터미널]** 위 두 줄과 아래 답(IPv4)을 1번 화면과 비교합니다.
5. **[보고서]** `day03_dns_analysis.md` 의 `## 2교시` › `### 문제 2-2` 아래를 채웁니다.
   - example.com 의 IPv4 · 두 번 물은 DNS 서버(위쪽 `Address`):
   - 🔍 위 두 줄의 `Address` 와 아래 `Addresses` 는 각각 무엇의 주소인가요? 두 번 물은 화면을 예로 들어 설명합니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | 첫째는 위 두 줄이 `서버:    kns.kornet.net` · `Address:  168.126.63.1`(학원 PC), 아래 `Addresses` 에 `104.20.○○.○○○` · `172.66.○○○.○○○` 같은 IPv4 두 개. 둘째는 위 두 줄만 `서버:    dns.google` · `Address:  8.8.8.8` 로 바뀌고 아래 답(IPv4)은 같다 (값은 바뀔 수 있습니다) |

**💡 힌트**

1. 위쪽 `Address` 는 물어본 DNS 서버입니다(명령 상자 ⚠).
2. 이름 하나에 IP 가 여러 개일 수 있습니다 — 큰 서비스는 서버를 여러 대 둡니다.
3. 학원망이 외부 DNS 를 막으면 둘째 명령에서 시간 초과가 납니다 — 그 자체가 「회사가 DNS 를 통제한다」는 관찰이니 그대로 적습니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 2-2</mark>

💻 **터미널에 입력합니다.**

```bash
nslookup example.com
nslookup example.com 8.8.8.8
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 첫째는 `이름:    example.com` 아래 `Addresses` 의 점 네 개짜리 주소 두 개(예: `104.20.23.154` · `172.66.147.243`)가 답이고, 위 두 줄은 학원 DNS 서버(`kns.kornet.net` · `168.126.63.1`)입니다. 둘째는 위 두 줄이 `서버:    dns.google` · `Address:  8.8.8.8` 로 바뀌고 답의 IPv4 는 같습니다(값은 바뀔 수 있습니다).</mark>

**왜** — 위 두 줄은 「누구에게 물었나」라서 물어볼 서버를 바꾸면 바뀝니다. 아래 `Addresses` 는 example.com 의 답이고, 같은 담당 네임서버의 원본에서 오므로 어느 리졸버에 물어도 대개 같습니다. 큰 서비스는 서버를 여러 대 두어 IP 가 여러 개입니다.

**자주 틀리는 곳** — `서버:` 바로 아래의 `Address`(`168.126.63.1` · `8.8.8.8`)를 example.com 의 주소로 적는 경우가 많습니다. 그것은 물어본 DNS 서버의 주소입니다.

**관제에서는** — 의심 도메인이 가리키는 IP 를 확인해 방화벽 로그의 접속 IP 와 맞춰 봅니다. 사내 PC 가 회사 DNS 서버 대신 `8.8.8.8` 같은 외부 DNS 에 직접 묻는 기록은 회사의 차단 · 기록을 피하려는 신호일 수 있어 확인합니다.

**강사 메모** — 위쪽 `Address:  168.126.63.1` 과 아래쪽 `Addresses` 를 화면에서 나눠 보여 주는 것이 이 문제의 핵심입니다. 둘째 명령에서는 위 두 줄만 바뀌고 아래 답은 그대로라는 것을 첫째 화면과 나란히 놓고 비교하게 합니다. 「IP 가 왜 네 개나 나오나요?」라는 질문에는 「IPv6 두 개와 IPv4 두 개이고, 서버를 여러 대 둬서 그렇습니다」라고, 「`8.8.8.8` 의 이름이 왜 `dns.google` 인가요?」라는 질문에는 「구글이 그 주소에 붙여 둔 이름입니다」라고 답합니다. 학원망에서 둘째 명령이 시간 초과가 나는 학생이 있으면 틀린 것이 아니라 관찰 결과로 적게 하고, 강사 화면으로 결과를 보여 줍니다. 돌아다니며 학생 보고서의 IPv4 칸에 `168.126.63.1` 이 적혀 있지 않은지 봅니다.

---

### ✍️ 문제 2-3 · 내 PC 는 어느 DNS 서버에 묻나

**할 일** — `ipconfig //all` 에서 내 PC 의 DNS 서버 주소를 찾아, 2-2 처음 화면의 위쪽 `Address` 와 같은지 확인하고 보고서에 적습니다.

**왜 중요한가** — 내 PC 가 어느 DNS 서버를 쓰는지 알아야 「숫자로는 되는데 이름으로 안 되는」 장애에서 점검할 서버를 정할 수 있습니다. 악성 코드가 DNS 서버 설정을 바꿨는지도 이 줄로 확인합니다.

**순서**
1. **[터미널]** `ipconfig //all` 을 입력합니다.
   ```bash
   ipconfig //all
   ```
   맥북: `scutil --dns | grep nameserver`
2. **[터미널]** 기본 게이트웨이가 찬 장치를 찾고, 그 장치의 `DNS 서버` 줄을 읽습니다.
3. **[터미널]** 그 주소가 2-2 처음 화면의 위쪽 `Address` 와 같은지 봅니다.
4. **[보고서]** `day03_dns_analysis.md` 의 `## 2교시` › `### 문제 2-3` 아래를 채웁니다.
   - `DNS 서버` 줄의 주소 · 2-2 처음 화면의 위쪽 `Address` 와 같은지:

| | |
|---|---|
| 🎯 나와야 하는 결과 | `DNS 서버 . . . . : ○○○.○○○.○.○` — 2-2 처음 화면의 위쪽 `Address` 와 같다 (값은 PC 마다 다릅니다) |

**💡 힌트**

1. 12일에 찾은 장치(기본 게이트웨이가 찬 것)의 줄 가운데 `DNS 서버` 입니다.
2. 집에서는 공유기 주소가, 회사에서는 사내 DNS 서버 주소가 많습니다.
3. 이 서버가 멈추면 「숫자로는 되는데 이름으로 안 되는」 장애가 납니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 2-3</mark>

💻 **터미널에 입력합니다.**

```bash
ipconfig //all
```
맥북: `scutil --dns | grep nameserver`

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `DNS 서버 . . . . : ○○○.○○○.○.○` 의 주소가 2-2 처음 화면의 위쪽 `Address` 와 같습니다(값은 PC 마다 다릅니다).</mark>

**왜** — `nslookup` 은 서버를 따로 적지 않으면 PC 에 설정된 DNS 서버(리졸버)에 묻습니다. 그래서 두 값이 같습니다.

**자주 틀리는 곳** — 기본 게이트웨이가 비어 있는 다른 장치의 `DNS 서버` 줄을 적는 경우가 많습니다.

**관제에서는** — PC 의 DNS 서버가 회사가 정한 주소가 아니면 악성 코드가 설정을 바꿨는지 의심합니다.

**강사 메모** — `ipconfig //all` 결과가 길어서 스크롤하다 헤매기 쉬우니, 기본 게이트웨이가 찬 장치를 먼저 찾게 합니다. 학원 PC 는 대개 2-2 처음 화면의 위쪽 `Address`(`168.126.63.1`)와 같은 주소가 보입니다. 「DNS 서버가 두 줄인데요?」라는 질문에는 「첫째를 먼저 쓰고, 첫째가 답하지 않을 때 둘째를 씁니다」라고 답합니다.

---

### ✍️ 문제 2-4 · 없는 이름을 물으면

**할 일** — 없는 이름을 `nslookup` 으로 묻고, 나온 문구와 그 뜻을 보고서에 적습니다.

**왜 중요한가** — 없는 이름에 DNS 가 어떤 답을 주는지 알아야 오후 5-5 에서 NXDOMAIN 이 쏟아지는 PC 를 찾을 수 있습니다. 12일의 `ping` 실패가 DNS 단계에서 난 것인지도 이 답으로 구분합니다.

**이 문제에 나오는 말**

- **NXDOMAIN** (엔엑스도메인) — 「**그런 이름은 없다**」는 DNS 의 답 — 화면에는 `Non-existent domain`

**순서**
1. **[터미널]** 없는 이름을 묻습니다.
   ```bash
   nslookup abc.nowhere-not-exist.com
   ```
2. **[터미널]** 나온 문구를 12일 2-4 의 `ping` 실패 문구와 비교합니다.
3. **[보고서]** `day03_dns_analysis.md` 의 `## 2교시` › `### 문제 2-4` 아래를 채웁니다.
   - 나온 문구:
   - 이 답은 인터넷이 끊겼다는 뜻인가요? 10/12 2-4 의 `ping` 실패 문구와 비교해 설명합니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `*** UnKnown can't find abc.nowhere-not-exist.com: Non-existent domain` (한국어 Windows 는 문구가 조금 다를 수 있습니다) |

**💡 힌트**

1. `Non-existent domain` 은 「그런 이름은 없다」는 DNS 의 공식 답입니다.
2. 12일의 `ping` 「호스트를 찾을 수 없습니다」도 같은 원인 — DNS 가 「없다」고 답한 것입니다.
3. DNS 서버가 답을 **했다**는 점에 주목합니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 2-4</mark>

💻 **터미널에 입력합니다.**

```bash
nslookup abc.nowhere-not-exist.com
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `*** UnKnown can't find abc.nowhere-not-exist.com: Non-existent domain` (한국어 Windows 는 문구가 조금 다를 수 있음) — 그런 이름이 없다는 DNS 의 답(NXDOMAIN)입니다. 인터넷이 끊긴 것이 아닙니다.</mark>

**왜** — DNS 서버는 「그런 이름은 없다」를 공식 답으로 리턴합니다. 12일 `ping` 의 「호스트를 찾을 수 없습니다」도 이 답 때문에 보내기 전에 멈춘 것입니다.

**자주 틀리는 곳** — 인터넷 연결이 끊긴 것으로 적는 경우가 많습니다. DNS 서버는 정상으로 답했고, 그 답이 「이름이 없다」입니다.

**관제에서는** — 한 PC 에서 짧은 시간에 NXDOMAIN 이 쏟아지면 악성 코드를 의심합니다(오후 5-5).

**강사 메모** — 「연결이 끊긴 것」과 「이름이 없다는 답을 받은 것」은 다르다는 점을 강조합니다. 「`UnKnown` 은 무슨 뜻인가요?」라는 질문에는 「`nslookup` 이 물어본 DNS 서버의 이름을 표시하지 못했다는 뜻이고, 이름이 없다는 답과는 관계가 없습니다」라고 답합니다. 화면 문구가 예시와 조금 달라도 `Non-existent domain` 이 보이면 맞은 것으로 봅니다.

---

### ⭐ 도전 2-5 · 파이썬으로 이름 묻기 (선택)

**할 일** — 이름 네 개를 차례로 물어 IP 를 출력하는 `dns_lookup.py` 를 완성해 실행합니다. 못 찾은 이름은 「찾지 못함」으로 출력합니다.

**왜 중요한가** — 로그에 나온 도메인 수십 개를 하나씩 `nslookup` 하지 않고 프로그램으로 한꺼번에 조회할 수 있게 됩니다. 없는 이름에서 멈추지 않게 하는 처리는 자동화 코드에 꼭 들어갑니다.

**이 문제에 나오는 말**

- **`socket`** (소켓) — 파이썬에 들어 있는 **네트워크 도구** 모음

#### 🐍 문법 상자 · `socket.gethostbyname` 과 실패 잡기

```python
import socket
try:
    socket.gethostbyname("abc.nowhere-not-exist.com")
except socket.gaierror:
    print("이름을 찾지 못함")
# 이름을 찾지 못함
```

| 쓰는 것 | 뜻 |
|---|---|
| `socket.gethostbyname("이름")` | 내 PC 의 DNS 설정으로 이름을 묻고 IPv4 하나를 리턴한다 |
| `socket.gaierror` | 이름을 못 찾았을 때 나는 에러 |
| `try` · `except` | 실패해도 멈추지 않게 (1과목 9/28) |

⚠ `except` 없이 쓰면 없는 이름 하나에서 프로그램이 멈춥니다. 로그의 도메인을 여러 개 조회할 때는 꼭 잡습니다.

**순서**
1. **[VS Code]** `network_zt` 폴더에 `dns_lookup.py` 를 만듭니다.
2. **[VS Code]** 아래 코드를 파일에 붙여 넣습니다.
   ```python
   # ── 강사용: 정답을 채운 코드입니다 ──
   import socket

   names = ["example.com", "google.com", "www.naver.com", "abc.nowhere-not-exist.com"]
   # 1. 이름을 하나씩 꺼내 socket.gethostbyname 으로 묻고 「example.com → 104.20.23.154」 꼴로 출력하세요. 못 찾으면 「… → 찾지 못함」
   for name in names:                                # 이름을 하나씩
       try:
           ip = socket.gethostbyname(name)           # 내 PC 의 DNS 설정으로 묻는다
           print(name, "→", ip)
       except socket.gaierror:                       # 이름이 없으면
           print(name, "→ 찾지 못함")
   ```
3. **[VS Code]** 번호 주석 아래를 채웁니다.
4. **[터미널]** `network_zt` 폴더에서 `python dns_lookup.py` 를 실행합니다. 고친 뒤에는 **↑(위 화살표)** 를 눌러 같은 명령을 다시 실행합니다.
   ```bash
   python dns_lookup.py
   ```
   맥북: `python3 dns_lookup.py`
5. **[보고서]** `day03_dns_analysis.md` 의 `## 2교시` › `### ⭐ 도전 2-5` 아래를 채웁니다.
   - 출력 첫 줄:

| | |
|---|---|
| 🎯 나와야 하는 결과 | 앞 셋은 `이름 → IPv4 주소`, 마지막은 `abc.nowhere-not-exist.com → 찾지 못함` (주소는 실행할 때마다 다를 수 있습니다) |

**💡 힌트**

1. 반복 안에 `try` · `except` 를 둡니다.
2. 바로 위 문법 상자와 같은 모양입니다.
3. 프로그램도 사람과 같은 DNS 서버(2-3)에 묻습니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 2-5</mark>

(코드는 위 문제 칸에 채워 두었습니다.)

💻 **터미널에 입력합니다.**

```bash
python dns_lookup.py
```
맥북: `python3 dns_lookup.py`

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 앞 셋은 `이름 → IPv4 주소`, 마지막은 `abc.nowhere-not-exist.com → 찾지 못함` 입니다(주소는 실행할 때마다 다를 수 있음).</mark>

**왜** — 프로그램도 PC 에 설정된 DNS 서버(2-3)에 묻습니다. 이름이 없다는 답(NXDOMAIN)이 오면 `socket.gaierror` 가 납니다.

**자주 틀리는 곳** — `try` · `except` 없이 쓰면 마지막 이름에서 에러가 나 프로그램이 멈춥니다.

**관제에서는** — 로그에 나온 도메인 여러 개를 이렇게 한 번에 조회해 지금 어느 IP 를 가리키는지 확인합니다.

**강사 메모** — 도전 문제라 2교시 끝에 시간이 남는 학생만 풀게 합니다. 「`nslookup` 은 IP 가 여러 개인데 왜 하나만 나오나요?」라는 질문에는 「`gethostbyname` 은 IPv4 하나만 리턴합니다」라고 답합니다. 에러가 나는 학생 화면에서는 `import socket` 이 빠졌는지, `except` 뒤에 `socket.gaierror` 를 정확히 적었는지 먼저 봅니다.

### 2교시 한눈에

| 하려는 일 | 명령 |
|---|---|
| 이름 → IP | `nslookup 이름` — 아래쪽 `Addresses` |
| 다른 DNS 서버에 묻기 | `nslookup 이름 8.8.8.8` |
| 내 PC 의 DNS 서버 | `ipconfig //all` 의 DNS 서버 |
| 없는 이름 | `Non-existent domain` (NXDOMAIN) |

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">3교시 (11:00–11:50) · DNS 계층 — 누가 원본을 알고 있나</mark>

### 왜 필요한가

1. 세상의 모든 이름을 한 서버가 다 알 수는 없습니다. 이름은 **점으로 나뉜 층**마다 담당자가 따로 있습니다.
2. 리졸버는 위층부터 차례로 물어 **담당 네임서버**(원본을 가진 서버)를 찾아갑니다.
3. 공격자가 담당자 정보를 바꾸면 이름 전체를 가로챌 수 있습니다. 그래서 「누가 담당인가」를 읽을 줄 알아야 합니다.

### 3.1 이름은 오른쪽부터 읽는다

**여기 나오는 말**

- **루트 (root)** — 이름의 **맨 위층** — 이름 끝에 숨은 점 `.`
- **TLD (Top-Level Domain)** (티엘디) — 이름의 **맨 끝 조각** — `com` · `kr`
- **네임서버 (name server)** — 이름에 대한 답을 가진 **DNS 서버**
- **권한 있는 네임서버 (authoritative)** (어소리테이티브) — 그 이름의 **원본 답**을 가진 담당 서버 — `hera.ns.cloudflare.com`

`www.example.com` 은 사실 맨 끝에 점이 하나 더 있는 `www.example.com.` 입니다. **오른쪽이 위층**입니다.

| 층 | 이 이름에서 | 담당 |
|---|---|---|
| 루트 | `.` (맨 끝 점) | 루트 네임서버 — 세계에 13개 이름 |
| TLD | `com` | `.com` 을 맡은 네임서버 — `.kr` · `.net` 도 각각 |
| 2단계 도메인 | `example.com` | **권한 있는 네임서버**(원본을 가진 담당자) |
| 호스트 이름 | `www.example.com` | 위 담당자가 함께 답한다 |

리졸버의 질문 순서:

```
리졸버 ─ ① 「com 담당은?」 ─▶ 루트          ─▶ 「com 담당은 ○○」
       ─ ② 「example.com 담당은?」 ─▶ com 담당  ─▶ 「hera.ns.cloudflare.com 이야」
       ─ ③ 「www.example.com 의 IP 는?」 ─▶ hera.ns.cloudflare.com ─▶ 「104.20.23.154」 ← 원본 답
```

#### 🐍 문법 상자 · 끝에서부터 꺼내기 `[-1]` · `reversed()`

```python
parts = "www.example.com".split(".")
print(parts[-1], len(parts))
print(list(reversed(parts)))
# com 3
# ['com', 'example', 'www']
```

| 쓰는 것 | 뜻 |
|---|---|
| `리스트[-1]` | 맨 끝 하나 — 이름이면 TLD |
| `reversed(리스트)` | 뒤에서부터 차례로 꺼낸다 — `list()` 로 감싸면 리스트 |
| `".".join(리스트)` | 리스트를 점으로 이어 붙인다 |

⚠ `reversed()` 는 원래 리스트를 바꾸지 않습니다. 뒤집힌 것을 쓰려면 새 변수에 담습니다.

---

### ✍️ 문제 3-1 · 직접 실행해 보기

**할 일** — 이름을 끝에서부터 꺼내는 코드 네 줄을 실행하고, 나온 결과 두 줄과 그 이유를 보고서에 적습니다.

**왜 중요한가** — 도메인을 오른쪽 조각부터 꺼내는 연습입니다. 오후 5-2 에서 TLD 와 그 앞 조각을 꺼내 의심 도메인을 가를 때 같은 `[-1]` · `[-2]` 를 씁니다.

**순서**
1. **[VS Code]** `network_zt` 폴더의 `warmup.py` 를 엽니다. 안에 있던 내용은 지웁니다.
2. **[VS Code]** 아래 코드를 `warmup.py` 에 그대로 따라 칩니다.
   ```python
   name = "mail.google.co.kr"       # 이름 하나
   parts = name.split(".")          # 점으로 잘라 조각 리스트로 만든다
   print(parts[-1])                 # 맨 끝 조각 하나
   print(".".join(parts[-2:]))      # 끝에서 두 번째부터 끝까지를 점으로 이은 것
   ```
3. **[터미널]** `network_zt` 폴더에서 `python warmup.py` 를 실행합니다.
   ```bash
   python warmup.py
   ```
   맥북: `python3 warmup.py`
4. **[보고서]** `day03_dns_analysis.md` 의 `## 3교시` › `### 문제 3-1` 아래를 채웁니다.
   - 출력 두 줄:
   - 둘째 줄이 첫째 줄과 다르게 나온 이유는 무엇인가요? `[-1]` 과 `[-2:]` 가 각각 무엇을 꺼냈고, 그 조각이 이름의 어느 층인지 설명합니다.

막히면 바로 위 문법 상자와 3.1 표를 다시 봅니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 3-1</mark>

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `kr` 과 `co.kr` 두 줄입니다.</mark>

**왜** — 이름은 오른쪽이 위층이라 `[-1]` 이 TLD `kr` 입니다. `[-2:]` 는 끝의 두 조각을 담은 리스트이고, 그것을 점으로 이은 `co.kr` 은 한국의 회사용 2단계 이름입니다.

**자주 틀리는 곳** — `[-2:]` 를 끝에서 두 번째 하나(`co`)만 꺼내는 것으로 읽는 경우가 많습니다.

**관제에서는** — 로그의 도메인을 TLD 별로 묶어 어느 나라 · 어느 종류의 이름에 많이 묻는지 셉니다.

**강사 메모** — `[-1]` 은 조각 하나, `[-2:]` 는 끝의 두 조각이 든 리스트라는 차이를 두 줄로 나란히 적어 보여 줍니다. 「그럼 `co.kr` 이 TLD 인가요?」라는 질문에는 「TLD 는 `kr` 이고, `co.kr` 은 그 아래 2단계입니다」라고 답합니다. 이어서 `".".join(parts[-3:])` 을 물으면(`google.co.kr`) 잘라 쓰기를 한 번 더 확인할 수 있습니다.

---

### ✍️ 문제 3-2 · 이름을 층으로 펼치기

**할 일** — 이름 하나를 받아 루트부터 한 층씩 내려가며 출력하는 `dns_tree.py` 를 완성해 실행하고, 둘째 이름의 출력을 보고서에 적습니다.

**왜 중요한가** — 이름이 어느 층을 거쳐 풀리는지 직접 펼쳐 보면, 3-3 · 3-4 에서 담당 네임서버를 물을 때 지금 어느 층을 묻는지 알 수 있습니다.

**순서**
1. **[VS Code]** `network_zt` 폴더에 `dns_tree.py` 를 만듭니다.
2. **[VS Code]** 아래 코드를 파일에 붙여 넣습니다.
   ```python
   # ── 강사용: 정답을 채운 코드입니다 ──
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
   ```
3. **[VS Code]** 번호 주석 아래를 채웁니다.
4. **[터미널]** `network_zt` 폴더에서 `python dns_tree.py` 를 실행합니다. 고친 뒤에는 **↑(위 화살표)** 를 눌러 같은 명령을 다시 실행합니다.
   ```bash
   python dns_tree.py
   ```
   맥북: `python3 dns_tree.py`
5. **[보고서]** `day03_dns_analysis.md` 의 `## 3교시` › `### 문제 3-2` 아래를 채웁니다.
   - `mail.google.co.kr` 의 출력:

| | |
|---|---|
| 🎯 나와야 하는 결과 | `루트 (.)` · `→ com` · `→ example.com` · `→ www.example.com`, 그리고 `루트 (.)` · `→ kr` · `→ co.kr` · `→ google.co.kr` · `→ mail.google.co.kr` |

**💡 힌트**

1. 처음에는 `current` 가 `""` 입니다 — `if current == "":`.
2. 새 층은 **왼쪽에** 붙습니다: `label + "." + current`.
3. 출력이 3.1 표의 층 순서와 같은지 봅니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 3-2</mark>

(코드는 위 문제 칸에 채워 두었습니다.)

💻 **터미널에 입력합니다.**

```bash
python dns_tree.py
```
맥북: `python3 dns_tree.py`

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `루트 (.)` · `→ com` · `→ example.com` · `→ www.example.com`, 그리고 `루트 (.)` · `→ kr` · `→ co.kr` · `→ google.co.kr` · `→ mail.google.co.kr`</mark>

**왜** — 이름은 오른쪽이 위층입니다. 뒤에서부터 꺼내 새 조각을 왼쪽에 붙이면 리졸버가 묻는 순서(루트 → TLD → 담당 네임서버)가 됩니다.

**자주 틀리는 곳** — `current + "." + label` 로 오른쪽에 붙여 `com.example` 처럼 거꾸로 나오는 경우가 많습니다.

**관제에서는** — `google.com.evil.top` 처럼 앞에 유명한 이름을 붙였지만 실제 위층은 `evil.top` 인 피싱 도메인을 가려냅니다.

**강사 메모** — 출력을 3.1 표의 층과 한 줄씩 맞춰 보게 해야 코드와 계층이 이어집니다. 학생 화면에서 `com.example` 처럼 거꾸로 나오면 붙이는 순서(`label + "." + current`)를 짚어 줍니다. 「`if` 없이 할 수는 없나요?」라는 질문에는 「첫 층에서 뒤에 점이 붙어 `com.` 이 되므로 처음만 따로 다룹니다」라고 답합니다.

---

### ✍️ 문제 3-3 · example.com 의 담당 네임서버 찾기

**할 일** — `-type=ns` 로 example.com 을 담당하는 네임서버를 묻고, 담당 네임서버를 보고서에 적습니다.

**왜 중요한가** — 담당 네임서버를 보면 그 도메인을 어느 DNS 업체가 관리하는지 알 수 있습니다. 담당 네임서버가 갑자기 바뀐 도메인은 공격자가 가로챘는지 의심합니다. 여기서 찾은 이름을 3-5 에서 씁니다.

**이 문제에 나오는 말**

- **NS 레코드** (엔에스 레코드) — 그 이름의 **담당 네임서버**를 적은 기록 — `-type=ns` 로 묻는다

**순서**
1. **[터미널]** 담당 네임서버를 묻습니다.
   ```bash
   nslookup -type=ns example.com
   ```
2. **[터미널]** `nameserver =` 줄을 찾습니다.
3. **[보고서]** `day03_dns_analysis.md` 의 `## 3교시` › `### 문제 3-3` 아래를 채웁니다.
   - `nameserver =` 뒤의 담당 네임서버:

| | |
|---|---|
| 🎯 나와야 하는 결과 | `example.com  nameserver = hera.ns.cloudflare.com` · `example.com  nameserver = elliott.ns.cloudflare.com` (담당자는 바뀔 수 있습니다) |

**💡 힌트**

1. `-type=ns` 는 「IP 말고 **담당 네임서버**를 달라」는 뜻입니다.
2. 담당자가 둘인 것은 하나가 멈춰도 답하게 하려는 것입니다.
3. 아래 `internet address` 줄은 그 네임서버들의 IP 입니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 3-3</mark>

💻 **터미널에 입력합니다.**

```bash
nslookup -type=ns example.com
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `example.com  nameserver = hera.ns.cloudflare.com` · `example.com  nameserver = elliott.ns.cloudflare.com` 두 줄의 이름을 적습니다(담당자는 바뀔 수 있음).</mark>

**왜** — NS 레코드는 이 이름의 원본을 가진 권한 있는 네임서버를 알려 줍니다. 하나가 멈춰도 답하도록 둘 이상 둡니다.

**자주 틀리는 곳** — 아래 `internet address` 줄의 IP 를 담당자로 적는 경우가 많습니다. 담당자는 `nameserver =` 뒤의 이름입니다.

**관제에서는** — 도메인의 NS 가 갑자기 낯선 서버로 바뀌면 도메인을 빼앗긴 신호일 수 있어 확인합니다.

**강사 메모** — `-type=ns` 를 붙이면 IP 대신 담당자 이름이 나오고, 결과 위쪽 `서버:` 는 여전히 학원 DNS(`kns.kornet.net`)라는 점을 함께 짚습니다. 「왜 cloudflare 가 나오나요?」라는 질문에는 「example.com 이 담당 네임서버를 Cloudflare 에 맡겨 두었기 때문입니다」라고 답합니다. `hera.ns.cloudflare.com` 은 3-5 에서 다시 쓰니 보고서에 적어 두게 합니다.

---

### ✍️ 문제 3-4 · TLD 의 담당 네임서버 보기

**할 일** — 한 층 위, `kr` 을 담당하는 네임서버를 묻고 위에서부터 두세 개를 보고서에 적습니다.

**왜 중요한가** — 리졸버가 TLD 담당 서버에게서 도메인의 담당자를 알아낸다는 것을 직접 확인합니다. 3.1 의 질문 순서 가운데 ②번을 받는 서버를 실제 이름으로 보는 문제입니다.

**순서**
1. **[터미널]** 아래 명령을 입력합니다. 이름 끝의 **점(`.`)까지** 그대로 칩니다.
   ```bash
   nslookup -type=ns kr.
   ```
2. **[터미널]** `kr  nameserver =` 줄을 찾습니다.
3. **[보고서]** `day03_dns_analysis.md` 의 `## 3교시` › `### 문제 3-4` 아래를 채웁니다.
   - `kr.` 의 네임서버 두세 개:

| | |
|---|---|
| 🎯 나와야 하는 결과 | `kr  nameserver = b.dns.kr` · `c.dns.kr` … 여섯 줄 안팎 — `.kr` 전체를 맡은 서버들 (서버 이름과 줄 수는 바뀔 수 있습니다) |

**💡 힌트**

1. 끝의 점은 3.1 의 「맨 끝 점 = 루트」입니다. 점을 빼면 PC 가 회사 안의 짧은 이름으로 여겨 `can't find kr` 이 나옵니다(실측).
2. 이 서버들은 「`naver.com` 은 몰라도 `○○.kr` 의 담당자가 누군지는 안다」 — 3.1 의 ②번 질문을 받는 곳입니다.
3. 결과가 길면 위 몇 줄만 봅니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 3-4</mark>

💻 **터미널에 입력합니다.**

```bash
nslookup -type=ns kr.
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `kr  nameserver = b.dns.kr` · `c.dns.kr` … 여섯 줄 안팎이 `.kr` 을 맡은 TLD 네임서버입니다(서버 이름과 줄 수는 바뀔 수 있습니다).</mark>

**왜** — 루트 바로 아래 TLD 층의 담당자입니다. 이 서버들은 `○○.kr` 의 담당 네임서버가 누구인지 알려 주고, IP 는 그 담당자가 답합니다.

**자주 틀리는 곳** — 끝의 점을 빼고 `kr` 로 쳐서 `can't find kr` 이 나오는 경우가 많습니다. 그때는 `kr.` 로 다시 칩니다.

**관제에서는** — 낯선 TLD 의 이름이 로그에 나오면 그 TLD 를 맡은 곳이 어디인지부터 확인합니다.

**강사 메모** — 끝의 점이 3.1 의 루트라는 것을 다시 이어 주면 「점을 왜 치나요?」라는 질문이 미리 풀립니다. 점을 빼고 친 학생이 많으니 `can't find kr` 이 보이면 바로 `kr.` 로 다시 치게 합니다. 「`.com` 도 이렇게 볼 수 있나요?」라는 질문에는 「`nslookup -type=ns com.` 처럼 같은 방법으로 봅니다」라고 답합니다.

---

### 3.2 권한 있는 응답과 권한 없는 응답

**여기 나오는 말**

- **권한 없는 응답 (Non-authoritative answer)** (논 어소리테이티브) — 2.2 표에서 찾아 쓴 말. 아래 표로 확인한다

| | 권한 있는 응답 | 권한 없는 응답 |
|---|---|---|
| 누가 답했나 | **담당 네임서버**가 직접 | 리졸버가 **찾아다 준** 답(또는 잠시 저장해 둔 답) |
| 언제 보나 | 담당 서버에 직접 물을 때(3-5) | 평소 `nslookup` 할 때 거의 항상 |
| 틀렸나 | 아니요 | **아니요 — 원본을 옮겨 온 것일 뿐.** 다만 바뀐 지 얼마 안 된 값이면 옛 값일 수 있다(4교시 캐시) |

---

### ✍️ 문제 3-5 · 담당 네임서버에게 직접 물으면

**할 일** — 3-3 에서 찾은 담당 네임서버에 직접 묻고, `권한 없는 응답:` 줄이 있는지 2-2 와 비교해 보고서에 적습니다.

**왜 중요한가** — 리졸버가 찾아다 준 답과 담당 네임서버의 원본 답을 구분할 수 있게 됩니다. 캐시에 남은 옛 값이 의심될 때 담당 네임서버에 직접 물어 원본과 비교합니다.

**순서**
1. **[터미널]** 이번에는 리졸버가 아니라 담당 네임서버에 묻습니다.
   ```bash
   nslookup example.com hera.ns.cloudflare.com
   ```
2. **[터미널]** `권한 없는 응답:` 줄이 있는지 2-2 의 화면과 비교합니다.
3. **[보고서]** `day03_dns_analysis.md` 의 `## 3교시` › `### 문제 3-5` 아래를 채웁니다.
   - `권한 없는 응답:` 줄이 있었나 · 답의 IPv4:
   - 🔍 권한 있는 응답과 권한 없는 응답은 누가 준 답인지에서 어떻게 다른가요? 2-2 와 3-5 의 화면을 예로 들어 설명합니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | 같은 IPv4 가 나오지만 **`권한 없는 응답:` 줄이 없다** — 담당자의 원본 답(권한 있는 응답) |

**💡 힌트**

1. 2-2 의 둘째 명령처럼 이름 뒤에 물어볼 서버를 적습니다. 이번에는 리졸버가 아니라 담당자입니다.
2. 3.2 표를 다시 봅니다.
3. 학원망이 외부 DNS 를 막으면 시간 초과가 납니다. 그때는 강사 화면으로 확인합니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 3-5</mark>

💻 **터미널에 입력합니다.**

```bash
nslookup example.com hera.ns.cloudflare.com
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 답의 IPv4 는 2-2 와 같고, `권한 없는 응답:` 줄이 **없습니다**.</mark>

**왜** — 담당 네임서버(권한 있는 서버)가 원본을 직접 답했기 때문입니다. 2-2 는 리졸버가 찾아다 준 답이라 그 줄이 붙었습니다.

**자주 틀리는 곳** — `권한 없는 응답` 을 「틀린 답」으로 적는 경우가 많습니다. 원본을 옮겨 온 답일 뿐입니다.

**관제에서는** — 리졸버의 답이 의심스러우면 담당자에게 직접 물어 원본과 같은지 비교합니다.

**강사 메모** — 2-2 화면과 나란히 놓고 `권한 없는 응답:` 줄 하나만 사라진 것을 찾게 합니다. 「그럼 평소에도 담당자에게 직접 물으면 되지 않나요?」라는 질문에는 「이름마다 담당자를 먼저 찾아야 하므로, 그 일을 리졸버가 대신 해 줍니다」라고 답합니다. 학원망에서 시간 초과가 나는 PC 가 많으면 강사 화면 하나로 확인하고 넘어갑니다.

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">4교시 (12:00–12:50) · DNS 레코드 · TTL · 캐시</mark>

### 왜 필요한가

1. DNS 는 IP 만 알려 주지 않습니다. **메일은 어디로 받나 · 이 이름의 진짜 이름은 뭔가** 같은 정보도 **레코드**로 담고 있습니다.
2. 답은 매번 처음부터 찾지 않고 **잠시 저장(캐시)** 해 두고 씁니다. 얼마나 오래 쓸지는 **TTL** 이 정합니다.
3. 피싱 · 악성 코드 분석에서 「이 도메인의 메일 서버는? 별명은? 언제 바뀌었나?」를 묻습니다. 레코드를 읽을 줄 알아야 합니다.

### 4.1 자주 보는 레코드

**여기 나오는 말**

- **레코드 (record)** — DNS 서버에 적힌 **기록 한 줄** — 이름 하나에 값 하나
- **A 레코드** (에이 레코드) — 이름 → **IPv4 주소**
- **CNAME (canonical name)** (씨네임) — **별명** — 「이 이름의 진짜 이름은 저것」
- **MX (mail exchanger)** (엠엑스) — 그 도메인의 **메일을 받을 서버**

| 레코드 | 담는 것 | 예 (실측 10/4) | `nslookup` 옵션 |
|---|---|---|---|
| **A** | IPv4 주소 | `example.com` → `104.20.23.154` | (기본) |
| **AAAA**(쿼드 에이) | IPv6 주소(새 방식의 긴 주소) | `example.com` → `2606:4700:10::6814:179a` | `-type=aaaa` |
| **CNAME** | 별명 | `www.naver.com` → `www.naver.com.nheos.com` | `-type=cname` |
| **MX** | 메일을 받을 서버 | `google.com` → `smtp.google.com` (우선순위 10) | `-type=mx` |
| **NS** | 담당 네임서버 | `example.com` → `hera.ns.cloudflare.com` | `-type=ns` |
| **TXT**(텍스트) | 글 — 메일 위조 방지 설정 등 | (오늘은 안 봄) | `-type=txt` |

#### 🐍 문법 상자 · 사전 안의 사전에서 꺼내기 · `while` 로 따라가기

```python
records = {"a.test": {"type": "CNAME", "value": "b.test"},
           "b.test": {"type": "A", "value": "192.0.2.10"}}
name = "a.test"
while records[name]["type"] == "CNAME":
    name = records[name]["value"]
print(name, records[name]["value"])
# b.test 192.0.2.10
```

| 쓰는 것 | 뜻 |
|---|---|
| `records[name]["type"]` | 바깥 사전에서 이름으로, 안쪽 사전에서 `type` 으로 |
| `while 조건:` | 조건이 참인 **동안** 되풀이한다 (1과목) |

⚠ CNAME 이 서로를 가리키면(a → b → a) `while` 이 끝나지 않습니다. 실무 코드는 횟수 제한을 둡니다.

---

### ✍️ 문제 4-1 · 직접 실행해 보기

**할 일** — 레코드를 사전 안의 사전으로 담은 코드 여섯 줄을 실행하고, 나온 결과 두 줄과 그 이유를 보고서에 적습니다.

**왜 중요한가** — DNS 레코드를 사전 안의 사전으로 다루는 연습입니다. 4-5 의 캐시 코드도 같은 모양으로 `cache[name]["expire"]` 를 꺼냅니다.

**순서**
1. **[VS Code]** `network_zt` 폴더의 `warmup.py` 를 엽니다. 안에 있던 내용은 지웁니다.
2. **[VS Code]** 아래 코드를 `warmup.py` 에 그대로 따라 칩니다.
   ```python
   records = {                                                                  # 이름 → 레코드 사전
       "google.com": {"type": "MX", "value": "smtp.google.com"},                # google.com 의 레코드
       "www.naver.com": {"type": "CNAME", "value": "www.naver.com.nheos.com"},  # www.naver.com 의 레코드
   }                                                                            # 사전 끝
   print(records["google.com"]["value"])     # google.com 레코드의 value 칸
   print(records["www.naver.com"]["type"])   # www.naver.com 레코드의 type 칸
   ```
3. **[터미널]** `network_zt` 폴더에서 `python warmup.py` 를 실행합니다.
   ```bash
   python warmup.py
   ```
   맥북: `python3 warmup.py`
4. **[보고서]** `day03_dns_analysis.md` 의 `## 4교시` › `### 문제 4-1` 아래를 채웁니다.
   - 출력 두 줄:
   - 두 줄은 각각 안쪽 사전의 어느 칸을 꺼낸 것이고, 그 값은 DNS 레코드에서 무엇을 뜻하나요?

막히면 바로 위 문법 상자와 4.1 표를 다시 봅니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 4-1</mark>

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `smtp.google.com` 과 `CNAME` 두 줄입니다.</mark>

**왜** — 바깥 키로 이름을, 안쪽 키(`value` · `type`)로 칸을 꺼냅니다. 첫째 줄은 google.com 레코드의 `value` 칸 — MX 의 값인 메일 서버 이름이고, 둘째 줄은 www.naver.com 레코드의 `type` 칸 — 별명(CNAME)이라는 레코드 종류입니다.

**자주 틀리는 곳** — 둘째 줄에서 `type` 이 아니라 `value` 를 읽어 `www.naver.com.nheos.com` 으로 적는 경우가 많습니다.

**관제에서는** — 조회한 레코드를 이름 → 종류 · 값 모양으로 모아 두면 여러 도메인의 메일 서버 · 별명을 한 번에 비교할 수 있습니다.

**강사 메모** — 대괄호 두 번을 「바깥 사전에서 이름, 안쪽 사전에서 칸」 순서로 소리 내어 읽게 하면 실수가 줄어듭니다. 「`records["google.com"]` 만 쓰면 무엇이 나오나요?」라는 질문에는 「안쪽 사전 `{'type': 'MX', 'value': 'smtp.google.com'}` 전체가 나옵니다」라고 답합니다. 이 모양이 4-5 에서 그대로 쓰인다고 미리 알려 둡니다.

---

### ✍️ 문제 4-2 · 메일은 어디로 가나 — MX

**할 일** — `google.com` 의 메일 서버를 묻고, 메일 서버 이름과 우선순위를 보고서에 적습니다.

**왜 중요한가** — MX 레코드로 그 도메인의 메일을 받는 서버를 확인할 수 있습니다. 피싱 메일을 분석할 때 보낸 쪽 도메인에 메일 서버가 있는지 이 명령으로 봅니다.

**이 문제에 나오는 말**

- **`MX preference`** (엠엑스 프리퍼런스) — 메일 서버의 **우선순위** — 숫자가 작을수록 먼저 쓴다

**순서**
1. **[터미널]** 메일 서버를 묻습니다.
   ```bash
   nslookup -type=mx google.com
   ```
2. **[터미널]** `mail exchanger =` 줄을 찾고, 같은 줄의 `MX preference` 숫자를 읽습니다.
3. **[보고서]** `day03_dns_analysis.md` 의 `## 4교시` › `### 문제 4-2` 아래를 채웁니다.
   - 메일 서버(`mail exchanger`) · `MX preference`:

| | |
|---|---|
| 🎯 나와야 하는 결과 | `google.com  MX preference = 10, mail exchanger = smtp.google.com` (값은 바뀔 수 있습니다) |

**💡 힌트**

1. 메일 서버는 `mail exchanger =` 뒤의 **이름**입니다.
2. 메일 서버도 이름이라, 아래에 그 이름의 IP(A 레코드)가 함께 나옵니다.
3. 피싱 메일 분석에서 「보낸 쪽 도메인에 MX 가 있나」를 확인합니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 4-2</mark>

💻 **터미널에 입력합니다.**

```bash
nslookup -type=mx google.com
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `google.com  MX preference = 10, mail exchanger = smtp.google.com` — 메일 서버 `smtp.google.com` · 우선순위 `10` 을 적습니다(값은 바뀔 수 있습니다).</mark>

**왜** — MX 레코드는 이 도메인으로 오는 메일을 받을 서버를 알려 줍니다. `preference` 숫자가 작을수록 먼저 씁니다.

**자주 틀리는 곳** — 아래에 함께 나오는 `smtp.google.com` 의 IP 를 메일 서버로 적는 경우가 많습니다. MX 의 답은 서버 이름입니다.

**관제에서는** — 피싱 메일의 보낸 쪽 도메인에 MX 가 있는지 확인합니다.

**강사 메모** — MX 의 답은 IP 가 아니라 서버 이름이고, 그 IP 는 아래에 덧붙여 나올 뿐이라는 점을 강조합니다. 「서버가 하나뿐인데 `preference` 숫자가 의미가 있나요?」라는 질문에는 「서버가 여러 개일 때 작은 숫자부터 쓰는 순서이고, 하나뿐이면 그 서버로 갑니다」라고 답합니다. 보고서 칸에 `smtp.google.com` 과 우선순위 10 이 함께 적혔는지 봅니다.

---

### ✍️ 문제 4-3 · 별명 따라가기 — CNAME

**할 일** — `www.naver.com` 의 CNAME 을 묻고, 이어서 그냥 `nslookup` 해 별명이 몇 단계인지 세어 보고서에 적습니다.

**왜 중요한가** — 큰 사이트가 별명을 여러 단계 거쳐 CDN 이름으로 연결된다는 것을 확인합니다. 오후 5교시에 `akamaiedge` 같은 CDN 이름이 무작위처럼 보여도 정상일 수 있다는 근거가 됩니다.

**이 문제에 나오는 말**

- **CDN (Content Delivery Network)** (시디엔) — 사용자와 **가까운 곳에서 내용을 대신 내주는** 서비스
- **`Aliases`** (에일리어시스) — `nslookup` 결과에서 **거쳐 온 별명들**

**순서**
1. **[터미널]** 별명(CNAME)을 묻습니다.
   ```bash
   nslookup -type=cname www.naver.com
   ```
2. **[터미널]** `canonical name =` 줄을 찾습니다.
3. **[터미널]** 이번에는 그냥 묻습니다.
   ```bash
   nslookup www.naver.com
   ```
4. **[터미널]** `Aliases:` 아래의 별명을 세고, `이름:` 줄의 최종 이름을 찾습니다.
5. **[보고서]** `day03_dns_analysis.md` 의 `## 4교시` › `### 문제 4-3` 아래를 채웁니다.
   - `canonical name` · 최종 이름(`이름:` 줄) · 별명 단계 수:

| | |
|---|---|
| 🎯 나와야 하는 결과 | 첫째 `canonical name = www.naver.com.nheos.com`. 둘째는 `Aliases:` 아래에 `www.naver.com` · `www.naver.com.nheos.com` · … 그리고 `이름:` 에 최종 이름과 IP (단계 수는 바뀔 수 있습니다) |

**💡 힌트**

1. `canonical name` = 진짜 이름. `Aliases` = 거쳐 온 별명들입니다.
2. 큰 사이트는 CNAME 으로 CDN 에 연결합니다.
3. 별명이 여러 단계인 것은 정상입니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 4-3</mark>

💻 **터미널에 입력합니다.**

```bash
nslookup -type=cname www.naver.com
nslookup www.naver.com
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 첫째 `canonical name = www.naver.com.nheos.com`. 둘째는 `Aliases:` 아래에 `www.naver.com` · `www.naver.com.nheos.com` · … 그리고 `이름:`(영어 화면은 `Name:`)에 최종 이름과 IP 가 나옵니다. `Aliases:` 줄 수가 별명 단계입니다(단계 수는 바뀔 수 있음).</mark>

**왜** — CNAME 은 「이 이름의 진짜 이름은 저것」이라는 레코드입니다. 리졸버가 별명을 끝까지 따라가 마지막 이름의 A 레코드로 IP 를 줍니다.

**자주 틀리는 곳** — `Aliases:` 의 마지막 이름을 최종 이름으로 적는 경우가 많습니다. 최종 이름은 `이름:` 줄입니다.

**관제에서는** — 잘 아는 이름이 처음 보는 도메인으로 CNAME 이 걸려 있으면 별명 끝까지 따라가 누구 서버인지 확인합니다.

**강사 메모** — 단계 수는 바뀔 수 있으니 정답 숫자를 하나로 정하지 말고 각자 화면의 `Aliases:` 줄 수를 세게 합니다. 「첫째 명령에서는 왜 IP 가 안 나오나요?」라는 질문에는 「`-type=cname` 은 별명만 묻기 때문입니다」라고 답합니다. 최종 이름을 `Aliases:` 마지막 줄로 적은 학생이 많으니 `이름:` 줄을 가리켜 확인합니다.

---

### 4.2 TTL 과 캐시

**여기 나오는 말**

- **캐시 (cache)** — 받은 답을 **정해진 시간 동안 저장**해 두고 다시 쓰는 것
- **TTL (DNS 에서)** (티티엘) — 답을 캐시에 **몇 초 동안 둘지** — 10/12 `ping` 의 TTL 과 이름만 같다

| | |
|---|---|
| **TTL** | 이 답을 **몇 초 동안** 저장해 써도 되는지. 담당 네임서버가 정한다 |
| **캐시** | 리졸버와 내 PC 가 TTL 동안 답을 저장해 두는 곳 — 빠르고 DNS 서버 부담이 줄어든다 |
| 그래서 생기는 일 | 담당자가 IP 를 바꿔도 **TTL 이 지날 때까지는 옛 IP 로** 간다 |

내 PC 의 캐시는 `ipconfig //displaydns`(디스플레이 디엔에스)로 보고, `ipconfig //flushdns`(플러시 디엔에스)로 비웁니다.

⚠ `nslookup` 은 PC 의 캐시를 거치지 않고 DNS 서버에 바로 묻습니다. 그래서 <mark style="background:#ffcdd2; color:#1a1a1a; padding:0 4px; border-radius:3px">`nslookup` 으로는 캐시가 채워지지 않습니다.</mark> 캐시를 채울 때는 `ping` · 브라우저처럼 보통 프로그램이 쓰는 길로 접속합니다.

---

### ✍️ 문제 4-4 · 내 PC 의 DNS 캐시 보기

**할 일** — 터미널에서 DNS 캐시를 보고 · 비우고 · 다시 채워 보며, 세 번 본 결과를 보고서에 적습니다.

**왜 중요한가** — 캐시를 보고 비울 수 있으면 이상한 주소로 계속 접속될 때 PC 에 남은 옛 답을 지우고 다시 확인할 수 있습니다. DNS 장애 대응에서 가장 먼저 하는 조치입니다.

**순서**
1. **[터미널]** 한 번 접속해 캐시에 넣습니다.
   ```bash
   ping -n 1 example.com
   ```
   맥북: `ping -c 1 example.com`
2. **[터미널]** 캐시를 보고, **`example.com`** 항목의 **TTL**(남은 초)을 찾습니다.
   ```bash
   ipconfig //displaydns
   ```
   맥북: 캐시 내용을 보는 명령이 맥에 없어서 이 단계는 건너뜁니다.
3. **[터미널]** 캐시를 비웁니다.
   ```bash
   ipconfig //flushdns
   ```
   맥북: `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder` (맥 암호를 묻습니다)
4. **[터미널]** `ipconfig //displaydns` 를 다시 입력해 목록이 비었는지 봅니다.
5. **[터미널]** `ping -n 1 example.com` 으로 다시 접속합니다(맥북: `ping -c 1 example.com`).
6. **[터미널]** `ipconfig //displaydns` 를 다시 입력해 `example.com` 항목이 돌아왔는지 봅니다.
7. **[보고서]** `day03_dns_analysis.md` 의 `## 4교시` › `### 문제 4-4` 아래를 채웁니다.
   - example.com 의 TTL · 비운 뒤 목록 · 다시 `ping` 한 뒤 목록:
   - `nslookup` 이 아니라 `ping` 으로 캐시를 채운 이유는 무엇인가요?

| | |
|---|---|
| 🎯 나와야 하는 결과 | 처음 `TTL(Time To Live) . : ○○○` · 비운 뒤 `DNS 확인자 캐시를 플러시했습니다.` 와 `Windows IP 구성` 한 줄뿐 · 다시 `ping` 한 뒤 `example.com` 항목이 돌아온다 |

**💡 힌트**

1. `//flushdns` 는 캐시를 비우는 명령입니다. 이상한 주소로 계속 접속될 때 관제가 가장 먼저 하는 조치입니다.
2. 슬래시는 두 번입니다 — `ipconfig //displaydns`(12일 오전 0.2).
3. 「표시할 수 없습니다」가 나오는 PC 도 있습니다(설정에 따라 다름). 그때는 옆 사람 화면과 같이 봅니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 4-4</mark>

💻 **터미널에 입력합니다.**

```bash
ping -n 1 example.com
ipconfig //displaydns
ipconfig //flushdns
ipconfig //displaydns
ping -n 1 example.com
ipconfig //displaydns
```
맥북: `ping -c 1 example.com` → `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`(캐시 비우기 · 맥 암호를 묻습니다) → `ping -c 1 example.com`. 캐시 내용을 보는 `ipconfig //displaydns` 는 맥에 없어서 그 단계는 건너뜁니다.

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 처음에는 `example.com` 아래 `TTL(Time To Live) . : ○○○` 이 보입니다. `//flushdns` 뒤에는 `DNS 확인자 캐시를 플러시했습니다.` 가 나오고, 다시 본 목록은 `Windows IP 구성` 한 줄뿐입니다. `ping` 으로 다시 접속하면 `example.com` 항목이 다시 생깁니다.</mark>

**왜** — PC 는 받은 답을 TTL 초 동안 캐시에 두고 그동안 다시 묻지 않습니다. `//flushdns` 는 그 저장을 모두 지웁니다. `nslookup` 은 PC 의 캐시를 거치지 않고 DNS 서버에 바로 물어서 캐시에 남기지 않으므로, 보통 프로그램이 쓰는 길인 `ping` 으로 채웁니다.

**자주 틀리는 곳** — `ipconfig /displaydns` 처럼 슬래시를 하나만 치는 경우가 많습니다. Git Bash 에서는 `//` 두 번입니다.

**관제에서는** — 이상한 주소로 계속 접속될 때 캐시에서 그 이름의 IP 를 확인하고, 옛 답이 남아 있으면 `//flushdns` 로 비웁니다.

**강사 메모** — 시작 전에 `nslookup` 은 PC 캐시를 거치지 않아 이 문제에서는 `ping` 을 쓴다고 먼저 말해 두면 「`nslookup` 했는데 캐시에 없어요」라는 질문이 줄어듭니다. `TTL(Time To Live) . :` 값은 시간이 지나면 줄어드니, 1분쯤 뒤 `ipconfig //displaydns` 를 다시 쳐서 값이 작아진 것을 보게 하면 「남은 초」라는 뜻이 바로 보입니다. 비운 뒤에도 다른 항목이 보이는 학생은 그사이 다른 프로그램이 다시 채운 것이니 `example.com` 이 없는지만 보게 합니다.

---

### ✍️ 문제 4-5 · 캐시 흉내 내기

**할 일** — TTL 이 지나기 전에는 저장해 둔 답을, 지나면 새로 물은 답을 쓰는 캐시를 `dns_cache.py` 에 완성해 실행하고, 출력과 그 이유를 보고서에 적습니다.

**왜 중요한가** — TTL 이 지나기 전까지 저장해 둔 답을 쓰는 규칙을 코드로 확인합니다. 담당자가 IP 를 바꿔도 한동안 옛 IP 로 접속되는 이유를 설명할 수 있게 됩니다.

**이 문제에 나오는 말**

- **만료 시각 (`expire`)** — 저장한 답을 **더는 쓰지 않는 시각** — 저장한 시각 + TTL

**순서**
1. **[VS Code]** `network_zt` 폴더에 `dns_cache.py` 를 만듭니다.
2. **[VS Code]** 아래 코드를 파일에 붙여 넣습니다.
   ```python
   # ── 강사용: 정답을 채운 코드입니다 ──
   cache = {}                                        # 이름 → {"ip": 주소, "expire": 만료 시각}
   TTL = 300                                         # 답을 300초 동안 쓴다
   answers = {"example.com": "104.20.23.154"}        # 담당자에게 물었다고 가정한 답

   def resolve(name, now):                           # now 초에 name 을 묻는다
       # 1. name 이 cache 에 있고 now 가 cache[name]["expire"] 보다 작으면 "캐시 " + 그 IP 를 return 하세요
       if name in cache and now < cache[name]["expire"]:   # 저장해 둔 답이 아직 유효하면
           return "캐시 " + cache[name]["ip"]
       ip = answers[name]                            # 새로 묻는다
       cache[name] = {"ip": ip, "expire": now + TTL}   # 만료 시각과 함께 저장
       return "새로 물음 " + ip

   for t in [0, 100, 299, 300, 450]:
       print(t, "초:", resolve("example.com", t))
   ```
3. **[VS Code]** 번호 주석 아래를 채웁니다.
4. **[터미널]** `network_zt` 폴더에서 `python dns_cache.py` 를 실행합니다. 고친 뒤에는 **↑(위 화살표)** 를 눌러 같은 명령을 다시 실행합니다.
   ```bash
   python dns_cache.py
   ```
   맥북: `python3 dns_cache.py`
5. **[보고서]** `day03_dns_analysis.md` 의 `## 4교시` › `### 문제 4-5` 아래를 채웁니다.
   - 출력 다섯 줄:
   - 🔍 담당 네임서버에서 IP 를 바꿔도 한동안 옛 IP 로 접속되는 이유는 무엇인가요? 출력의 299초 · 300초 줄을 예로 들어 설명합니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `0 초: 새로 물음 104.20.23.154` · `100 초: 캐시 104.20.23.154` · `299 초: 캐시 …` · `300 초: 새로 물음 …` · `450 초: 캐시 …` |

**💡 힌트**

1. `cache[name]` 은 사전입니다 — `cache[name]["expire"]` 가 만료 시각, `cache[name]["ip"]` 가 주소.
2. 두 조건은 `and` 로 잇습니다. 이름이 없으면 먼저 `in` 에서 걸러져 `KeyError` 가 나지 않습니다.
3. 300초에는 **같거나 지났으니** 새로 묻습니다 — `<` 를 씁니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 4-5</mark>

(코드는 위 문제 칸에 채워 두었습니다.)

💻 **터미널에 입력합니다.**

```bash
python dns_cache.py
```
맥북: `python3 dns_cache.py`

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `0 초: 새로 물음 104.20.23.154` · `100 초: 캐시 104.20.23.154` · `299 초: 캐시 104.20.23.154` · `300 초: 새로 물음 104.20.23.154` · `450 초: 캐시 104.20.23.154`</mark>

**왜** — 0초에 저장하면 만료는 300초입니다. 299초까지는 저장해 둔 답을 그대로 쓰므로, 그사이 담당 네임서버에서 IP 를 바꿨어도 옛 IP 가 나옵니다. 300초에 새로 물으면서 만료가 600초로 다시 정해져 450초는 캐시를 씁니다.

**자주 틀리는 곳** — `<=` 를 써서 300초에도 캐시를 쓰는 경우가 많습니다. 만료 시각이 되면 새로 묻습니다.

**관제에서는** — 도메인의 IP 가 바뀐 직후에는 TTL 이 지날 때까지 옛 IP 와 새 IP 가 섞여 로그에 나옵니다.

**강사 메모** — 299 · 300 두 줄은 `<` 와 `<=` 의 차이를 보여 주려고 넣은 값이라는 점을 강조합니다. 「450초는 왜 캐시인가요?」라는 질문이 가장 많은데, 「300초에 새로 물으며 만료가 600초로 다시 정해졌기 때문입니다」라고 답합니다. 학생 화면에서 300초 줄이 `캐시` 로 나오면 `<=` 를 썼는지 봅니다.

---

## 오전 마무리 — 보고서 2 · 3 · 4교시 칸 확인

`day03_dns_analysis.md` 의 2 · 3 · 4교시 칸에 **빈 줄**이 없는지 봅니다. 빈 줄은 그 문제로 돌아갑니다(⭐ 줄은 비워도 됩니다).

오후에는 DNS 로그에서 **수상한 도메인**을 골라내는 규칙을 만들고, 판단 기준을 문서로 남깁니다.
