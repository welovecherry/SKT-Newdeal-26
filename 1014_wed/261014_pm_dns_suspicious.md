# 10/14(수) 오후 · DNS 로 보는 공격 · 의심 도메인 판별 규칙 · 3일 차 보고서 — 실습

오전에 DNS 가 이름을 IP 로 바꾸는 과정을 봤습니다. 악성 코드도 똑같이 DNS 에 이름을 물어 **공격자의 서버**를 찾아갑니다. 오후에는 DNS 질의 기록(로그)에서 **수상한 도메인을 골라내는 규칙**을 직접 만들고, 그 규칙이 얼마나 잘 맞는지 재고, **판단 기준을 문서로** 남깁니다.

| 교시 | 무엇 | 쓰는 것 |
|---|---|---|
| 5교시 | 의심 도메인의 특징 — 무작위 이름(DGA) · 사칭 · NXDOMAIN 폭증 | 파이썬 |
| 6교시 | 점수 규칙 만들기 · 맞힘 · 오탐 · 미탐 재기 · 예외 목록 | 파이썬 |
| 7교시 | 3일 차 DNS 분석서 완성 — 판정표 · 판단 기준 · 한계 | 파이썬 · `nslookup` |

**오늘 남기는 것:** `network_zt/day03_dns_analysis.md` 완성본(2~7교시 칸과 맨 아래 「최종 분석서」) — 강의계획서의 3일 차 산출물입니다. 평가 기준 「의심 도메인을 **합리적 근거**로 골랐나 · **판단 기준이 문서화**됐나」를 이 오후에 채웁니다.

> **화면은 이렇게 나눠 씁니다 — 왼쪽은 실습 자료, 오른쪽은 보고서**
>
> 1. 이 파일을 누르고 `Ctrl + Shift + V` 를 누릅니다. 실습 자료가 **미리보기**로 열립니다. 이 탭이 **왼쪽**입니다.
> 2. 왼쪽 목록(탐색기)에서 보고서 파일 `day03_dns_analysis.md` 를 오른쪽 클릭하고 **Open to the Side**(옆에서 열기)를 누릅니다. 보고서가 **오른쪽** 칸에 열립니다.
> 3. **오른쪽 보고서에만 씁니다.** 왼쪽 실습 자료는 스크롤하며 읽습니다. 쓴 모양을 보고 싶으면 오른쪽 칸에서 `Ctrl + K` 를 누른 뒤 `V`.
>
> 보고서 파일은 오전에 만든 것을 그대로 씁니다.

---

## 시작하기

### 이 파일을 여는 법

이 파일은 **카톡으로 받은 실습 안내**입니다. 노트북이 아니라 읽으면서 따라 하는 문서입니다.

1. 카톡에서 받은 이 파일(`261014_pm_dns_suspicious.md`)을 `security-agent-toolkit` 안의 **`network_zt` 폴더**로 옮깁니다.
2. VS Code 왼쪽 목록에서 이 파일을 누르고, **`Ctrl + Shift + V`** 를 눌러 **미리보기**로 엽니다. 표와 굵은 글씨가 읽기 좋게 보입니다.
3. 이 파일은 **읽기만** 합니다. 내가 적는 것은 그날 **보고서 파일**과 **`.py` 파일**입니다.
4. 코드나 명령을 복사할 때는 미리보기의 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 를 누릅니다.

### 오늘 시작할 때

0. 오늘 적는 것은 모두 **오전에 만든 `day03_dns_analysis.md` 하나에** 적습니다. 5 · 6 · 7교시의 문제 소제목은 오전에 붙여 넣은 틀에 이미 있습니다 — **그 문제 소제목 아래**를 채웁니다. 각 문제의 마지막 **[보고서]** 단계에서 보고서에 적을 위치와 항목을 확인합니다.
1. 오전과 같은 터미널(Git Bash)을 씁니다. 줄 앞에 `$` 가 보이면 됩니다.
2. `network_zt` 폴더에서 시작합니다 — `cd network_zt`(이미 들어와 있으면 생략).
3. 오늘 쓰는 의심 도메인은 **수업용으로 지어낸 이름**입니다. 실제로 접속하지 않습니다 — `nslookup` 으로 「있는지」만 봅니다(7-3).
4. 문제마다 **할 일 → 왜 중요한가 → 이 문제에 나오는 말 → 순서**를 읽습니다. 순서 앞의 `[창 이름]`을 보고 해당 창에서 적힌 행동을 합니다. 마지막 **[보고서]** 단계에서 답을 적습니다. 문제 앞의 상자는 🐍 문법 상자(파이썬) · 명령 상자(터미널) · 개념 상자입니다. 막히면 **💡 힌트** → 맨 아래 **「정답」** 순서로 봅니다. ⭐도전은 선택입니다.
5. 맥북으로 복습할 때는 명령 상자 바로 아래의 **「맥북:」 줄**을 칩니다(없으면 Windows 와 같은 명령). 오후 파이썬은 `python` 대신 `python3` 입니다.

### 오늘 쓰는 DNS 로그

여러 문제에서 같은 로그를 씁니다. 문제마다 코드에 다시 적어 두었습니다.

| # | 물어본 이름 | 답(rcode) | 실제 |
|---|---|---|---|
| 1 | `www.naver.com` | NOERROR | 정상 |
| 2 | `mail.google.com` | NOERROR | 정상 |
| 3 | `update.microsoft.com` | NOERROR | 정상 |
| 4 | `e6030.a.akamaiedge.net` | NOERROR | 정상 — CDN 이름(오전 4-3) |
| 5 | `cdn.jsdelivr.net` | NOERROR | 정상 |
| 6 | `xn--3e0b707e.kr` | NOERROR | 정상 — 한글 도메인을 영문으로 바꾼 모양 |
| 7 | `kxq3vz9a.top` | **NXDOMAIN** | 의심 |
| 8 | `p0w8rk2mzq.xyz` | **NXDOMAIN** | 의심 |
| 9 | `qwrtpzkx7v.com` | NOERROR | 의심 |
| 10 | `zzx9q2lk.top` | **NXDOMAIN** | 의심 |
| 11 | `bnk-secure-login.xyz` | NOERROR | 의심 — 은행 사칭 |
| 12 | `www.example.com` | NOERROR | 정상 |

- **rcode**(알코드 · response code) — DNS 답의 **결과 코드**. `NOERROR`(노에러) = 답이 있었다 · `NXDOMAIN` = 그런 이름이 없다(오전 2-4).
- 「실제」 칸은 나중에 규칙이 맞았는지 채점하는 **정답지**입니다. 규칙은 이 칸을 보지 않습니다.

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">5교시 (14:00–14:50) · 의심 도메인의 특징</mark>

### 왜 필요한가

1. 악성 코드가 고정된 이름 하나만 쓰면 그 이름을 막으면 끝납니다. 그래서 공격자는 **이름을 매일 수백 개씩 자동으로 만들어** 그중 하나만 실제로 등록해 둡니다. 이것이 **DGA** 입니다.
2. 감염된 PC 는 그 이름들을 차례로 물어봅니다. 대부분 없는 이름이라 **NXDOMAIN 이 쏟아집니다.**
3. 또 하나는 **사칭**입니다 — `naver.com` 을 `nav3r.com` 처럼 비슷하게 만들어 사람을 속입니다(5-4).

### 5.1 의심 도메인을 가르는 지표

**여기 나오는 말**

- **DGA (Domain Generation Algorithm)** (디지에이) — 악성 코드가 도메인 이름을 **매일 수백 개씩 자동으로** 만드는 방식 — `kxq3vz9a.top`
- **C2 서버 (Command and Control)** (씨투 서버) — 공격자가 감염된 PC 에 **명령을 내리는** 서버. DGA 로 만든 이름 가운데 등록된 하나가 이 서버를 가리킨다

| 특징 | 정상 도메인 | DGA 도메인 | 왜 |
|---|---|---|---|
| 이름의 길이 | 짧고 뜻이 있다 — `naver` | 길고 뜻이 없다 — `p0w8rk2mzq` | 기계가 만든 글자 줄 |
| 숫자 | 거의 없다 | 여러 개 섞여 있다 | 무작위로 뽑으니 숫자도 섞인다 |
| 모음(a · e · i · o · u) | 사람이 읽을 수 있게 섞여 있다 | **거의 없다** — `kxq3vz9a` | 발음할 수 없는 이름 |
| TLD(맨 끝 이름) | `.com` · `.net` · `.kr` | 값싼 `.top` · `.xyz` · `.tk` 가 많다 | 한꺼번에 싸게 등록 |
| 답 | NOERROR | **NXDOMAIN 이 많다** | 대부분 등록하지 않은 이름 |

**어느 부분을 볼까:** `e6030.a.akamaiedge.net` 처럼 정상 서비스도 맨 앞 조각은 무작위로 보입니다(오전 4-3 의 CDN). 그래서 오늘은 **TLD 바로 앞 조각**(2단계 이름 — `akamaiedge` · `naver` · `kxq3vz9a`)을 봅니다.

#### 🐍 문법 상자 · 글자를 하나씩 보며 세기

```python
label = "kxq3vz9a"
digits = 0
for ch in label:
    if ch in "0123456789":
        digits = digits + 1
print(digits, len(label))
print("a" in "aeiou", "x" in "aeiou")
# 2 8
# True False
```

| 쓰는 것 | 뜻 |
|---|---|
| `for ch in 글자:` | 글자를 **한 자씩** 꺼낸다 |
| `ch in "0123456789"` | 그 한 자가 숫자 중 하나인가 |
| `ch in "aeiou"` | 그 한 자가 모음인가 |

⚠ `"kxq3vz9a" in "0123456789"` 처럼 글자 <mark style="background:#ffcdd2; color:#1a1a1a; padding:0 4px; border-radius:3px">전체</mark>로 물으면 늘 `False` 입니다. 한 자씩 꺼내서 묻습니다.

---

### ✍️ 문제 5-1 · 직접 실행해 보기

**할 일** — TLD 앞 조각의 길이와 모음 수를 세는 코드 여덟 줄을 실행하고, 나온 결과와 그 이유를 보고서에 적습니다.

**왜 중요한가** — 도메인에서 TLD 앞 조각의 길이와 모음 수를 세는 연습입니다. 6-2 의 점수 함수가 이 두 값으로 규칙 ①·③을 매깁니다.

**순서**
1. **[VS Code]** 왼쪽 목록에서 `network_zt` 폴더를 오른쪽 클릭 › **New File** › 이름 `warmup_5_1.py` 를 입력하고 Enter 를 누릅니다.
2. **[VS Code]** 아래 코드를 `warmup_5_1.py` 에 그대로 따라 칩니다.
   ```python
   name = "p0w8rk2mzq.xyz"            # 로그에 나온 이름
   parts = name.split(".")            # 점으로 잘라 조각 리스트로 만든다
   label = parts[-2]                  # TLD 바로 앞 조각
   vowels = 0                         # 모음 수를 셀 변수
   for ch in label:                   # 조각에서 한 자씩 꺼낸다
       if ch in "aeiou":              # 그 한 자가 모음인가?
           vowels = vowels + 1        # 모음이면 1 을 더한다
   print(label, len(label), vowels)   # 조각 · 길이 · 모음 수
   ```
3. **[터미널]** `network_zt` 폴더에서 `python warmup_5_1.py` 를 실행합니다.
   ```bash
   python warmup_5_1.py
   ```
   맥북: `python3 warmup_5_1.py`
4. **[보고서]** `day03_dns_analysis.md` 의 `## 5교시` › `### 문제 5-1` 아래를 채웁니다.
   - 출력:
   - 셋째 값(모음 수)이 그렇게 나온 이유는 무엇인가요? 조각의 글자를 하나씩 보고, 숫자 `0` 이 모음으로 세어졌는지 설명합니다.

막히면 바로 위 문법 상자를 다시 봅니다.

다 했으면 · 막히면 문서 맨 아래 「정답 5-1」에서 결과를 확인합니다.

---

### ✍️ 문제 5-2 · 볼 조각 꺼내기

**할 일** — 이름마다 TLD 바로 앞 조각과 TLD 를 꺼내 출력하는 `label.py` 를 완성해 실행하고, CDN 이름 줄의 결과를 보고서에 적습니다.

**왜 중요한가** — 어느 조각을 볼지 정해야 맨 앞 조각만 무작위인 CDN 같은 정상 도메인을 의심으로 잘못 판정하지 않습니다. 6-2 의 점수 함수도 이 두 조각으로 규칙을 매깁니다.

**순서**
1. **[VS Code]** `network_zt` 폴더에 `label.py` 를 만듭니다.
2. **[VS Code]** 아래 코드를 파일에 붙여 넣습니다.
   ```python
   # ── 미리 채워 둔 줄입니다. 고치지 않습니다 ──
   names = ["www.naver.com", "e6030.a.akamaiedge.net", "kxq3vz9a.top", "bnk-secure-login.xyz"]
   # ── 여기까지 ──

   for name in names:                                # 이름을 하나씩
       parts = name.split(".")                       # 점으로 나눈 조각들
       # 1. label 에 parts 의 끝에서 둘째(-2)를, tld 에 맨 끝(-1)을 담으세요

       print(name, "조각:", label, "TLD:", tld)
   ```
3. **[VS Code]** 번호 주석 아래를 채웁니다.
4. **[터미널]** `network_zt` 폴더에서 `python label.py` 를 실행합니다. 고친 뒤에는 **↑(위 화살표)** 를 눌러 같은 명령을 다시 실행합니다.
   ```bash
   python label.py
   ```
   맥북: `python3 label.py`
5. **[보고서]** `day03_dns_analysis.md` 의 `## 5교시` › `### 문제 5-2` 아래를 채웁니다.
   - `e6030.a.akamaiedge.net` 줄의 조각 · TLD:

**💡 힌트**

1. 끝에서부터는 `[-1]` · `[-2]` 입니다(오전 3교시 문법 상자).
2. 출력 줄은 미리 채워 두었습니다. `label` · `tld` 두 변수만 만들면 됩니다.
3. `e6030` 이 아니라 `akamaiedge` 를 보는 이유는 5.1 표 아래에 있습니다.
4. 다 했으면 · 막히면 문서 맨 아래 「정답 5-2」에서 결과를 확인합니다.

---

### ✍️ 문제 5-3 · 숫자 수와 모음 비율

**할 일** — TLD 앞 조각의 숫자 개수와 모음 비율(모음 수 ÷ 길이)을 계산하는 함수를 `features.py` 에 완성해 실행하고, DGA 이름 줄의 출력을 보고서에 적습니다.

**왜 중요한가** — 숫자 개수와 모음 비율은 사람이 지은 이름과 기계가 만든 DGA 이름을 가르는 지표입니다. 6교시 점수 규칙의 ②·③번이 이 두 값을 씁니다.

**이 문제에 나오는 말**

- **모음 비율** — 조각 글자 가운데 모음(a · e · i · o · u)이 차지하는 몫 — 모음 수 ÷ 길이

**순서**
1. **[VS Code]** `network_zt` 폴더에 `features.py` 를 만듭니다.
2. **[VS Code]** 아래 코드를 파일에 붙여 넣습니다.
   ```python
   def features(name):                               # 이름 하나의 특징을 사전으로 리턴한다
       label = name.split(".")[-2]                   # TLD 앞 조각
       digits = 0                                    # 숫자 개수
       vowels = 0                                    # 모음 개수
       for ch in label:                              # 한 자씩
           # 1. ch 가 숫자면 digits 에 1 을 더하세요

           # 2. ch 가 모음(aeiou)이면 vowels 에 1 을 더하세요

       return {"label": label, "len": len(label), "digits": digits, "vowel_ratio": round(vowels / len(label), 2)}

   # ── 미리 채워 둔 줄입니다. 고치지 않습니다 ──
   for name in ["www.naver.com", "kxq3vz9a.top", "xn--3e0b707e.kr"]:
       print(features(name))
   # ── 여기까지 ──
   ```
3. **[VS Code]** 번호 주석 아래를 채웁니다.
4. **[터미널]** `network_zt` 폴더에서 `python features.py` 를 실행합니다. 고친 뒤에는 **↑(위 화살표)** 를 눌러 같은 명령을 다시 실행합니다.
   ```bash
   python features.py
   ```
   맥북: `python3 features.py`
5. **[보고서]** `day03_dns_analysis.md` 의 `## 5교시` › `### 문제 5-3` 아래를 채웁니다.
   - `kxq3vz9a.top` 줄의 출력:

**💡 힌트**

1. 바로 위 문법 상자의 반복과 같은 모양입니다 — `if` 두 개.
2. `round(값, 2)` 는 소수 둘째 자리까지 반올림합니다(미리 채워 둔 줄).
3. 셋째 줄 `xn--3e0b707e` 는 **정상** 도메인인데 숫자가 많고 모음이 적습니다. 6교시에 다시 봅니다.
4. 다 했으면 · 막히면 문서 맨 아래 「정답 5-3」에서 결과를 확인합니다.

---

### ✍️ 문제 5-4 · 사칭 도메인 찾기

**할 일** — `0` → `o`, `1` → `l`, `3` → `e` 로 바꿨을 때 믿을 만한 도메인과 똑같아지면 사칭으로 판정하는 `typosquat.py` 를 완성해 실행하고, `[사칭 의심]` 으로 나온 이름을 보고서에 적습니다.

**왜 중요한가** — 진짜 도메인과 한두 글자만 다른 사칭 도메인은 피싱에 자주 쓰입니다. 무작위처럼 보이지 않아 DGA 지표로는 잡기 어려운 이름을 이 규칙으로 따로 찾습니다.

**이 문제에 나오는 말**

- **타이포스쿼팅 (typosquatting)** (타이포스쿼팅) — 진짜 도메인과 **비슷하게** 만들어 사람을 속이는 사칭 — `nav3r.com`
- **피싱 (phishing)** (피싱) — 가짜 사이트 · 메일로 사람을 속여 정보를 빼내는 공격

**순서**
1. **[VS Code]** `network_zt` 폴더에 `typosquat.py` 를 만듭니다.
2. **[VS Code]** 아래 코드를 파일에 붙여 넣습니다.
   ```python
   # ── 미리 채워 둔 줄입니다. 고치지 않습니다 ──
   TRUSTED = ["naver.com", "google.com", "kbstar.com"]   # 우리 회사가 쓰는 진짜 도메인
   seen = ["nav3r.com", "google.com", "g00gle.com", "kbstar.com", "kb5tar.com"]   # 로그에 나온 이름
   # ── 여기까지 ──

   for name in seen:                                 # 로그에 나온 이름을 하나씩
       # 1. plain 에 name 의 0 을 o 로, 1 을 l 로, 3 을 e 로 바꾼 글자를 담으세요

       if name in TRUSTED:                           # 진짜 도메인 그대로면
           print("[정상]", name)
       # 2. 아니고 plain 이 TRUSTED 안에 있으면 「[사칭 의심] nav3r.com → naver.com 흉내」 를 출력하세요

       else:                                         # 둘 다 아니면
           print("[모름]", name)
   ```
3. **[VS Code]** 번호 주석 아래를 채웁니다.
4. **[터미널]** `network_zt` 폴더에서 `python typosquat.py` 를 실행합니다. 고친 뒤에는 **↑(위 화살표)** 를 눌러 같은 명령을 다시 실행합니다.
   ```bash
   python typosquat.py
   ```
   맥북: `python3 typosquat.py`
5. **[보고서]** `day03_dns_analysis.md` 의 `## 5교시` › `### 문제 5-4` 아래를 채웁니다.
   - `[사칭 의심]` 으로 나온 이름:

**💡 힌트**

1. `.replace("0", "o")` 를 세 번 이어 붙입니다 — `name.replace(…).replace(…).replace(…)`.
2. 2번은 `elif` 입니다.
3. `kb5tar` 는 `5 → s` 바꾸기를 넣지 않아 「모름」입니다 — 규칙은 넣은 만큼만 잡습니다.
4. 다 했으면 · 막히면 문서 맨 아래 「정답 5-4」에서 결과를 확인합니다.

---

### ✍️ 문제 5-5 · NXDOMAIN 이 쏟아지는 PC 찾기

**할 일** — DNS 로그에서 PC 마다 NXDOMAIN 이 몇 번인지 세고, 3번 이상인 PC 를 출력하는 `nx_count.py` 를 완성해 실행하고, 출력과 그 이유를 보고서에 적습니다.

**왜 중요한가** — 도메인 하나가 아니라 PC 별로 NXDOMAIN 을 세면 DGA 이름을 연달아 묻는 감염 의심 PC 를 찾을 수 있습니다. 관제에서 어느 PC 를 먼저 점검할지 정하는 기준이 됩니다.

**순서**
1. **[VS Code]** `network_zt` 폴더에 `nx_count.py` 를 만듭니다.
2. **[VS Code]** 아래 코드를 파일에 붙여 넣습니다.
   ```python
   # ── 미리 채워 둔 줄입니다. 고치지 않습니다 ──
   logs = [                                          # (PC 주소, 물어본 이름, 답)
       ("10.20.0.15", "www.naver.com", "NOERROR"),
       ("10.20.0.42", "kxq3vz9a.top", "NXDOMAIN"),
       ("10.20.0.42", "p0w8rk2mzq.xyz", "NXDOMAIN"),
       ("10.20.0.15", "mail.google.com", "NOERROR"),
       ("10.20.0.42", "zzx9q2lk.top", "NXDOMAIN"),
       ("10.20.0.33", "typo-nevar.com", "NXDOMAIN"),
       ("10.20.0.42", "qwrtpzkx7v.com", "NOERROR"),
   ]
   nx = {}                                           # PC 주소 → NXDOMAIN 횟수
   # ── 여기까지 ──

   for pc, name, rcode in logs:                      # 로그를 한 줄씩
       # 1. rcode 가 "NXDOMAIN" 이면 nx 의 pc 키를 1 늘리세요 (.get)

   for pc in nx:                                     # 센 PC 를 하나씩
       # 2. 횟수가 3 이상이면 「[확인 필요] 10.20.0.42 NXDOMAIN 3번」 을 출력하세요

   ```
3. **[VS Code]** 번호 주석 아래를 채웁니다.
4. **[터미널]** `network_zt` 폴더에서 `python nx_count.py` 를 실행합니다. 고친 뒤에는 **↑(위 화살표)** 를 눌러 같은 명령을 다시 실행합니다.
   ```bash
   python nx_count.py
   ```
   맥북: `python3 nx_count.py`
5. **[보고서]** `day03_dns_analysis.md` 의 `## 5교시` › `### 문제 5-5` 아래를 채웁니다.
   - 출력:
   - 🔍 DGA 에 감염된 PC 에서 NXDOMAIN 이 쏟아지는 이유는 무엇인가요?

**💡 힌트**

1. 세기는 1과목에서 쓴 `nx[pc] = nx.get(pc, 0) + 1` 모양입니다.
2. 한 번 틀린 이름은 사람의 오타일 가능성이 큽니다. **짧은 시간에 여러 번**이 신호입니다.
3. `10.20.0.42` 는 마지막에 `qwrtpzkx7v.com` 의 답을 받았습니다 — DGA 이름 가운데 **실제로 등록된 하나**를 찾아낸 것일 수 있습니다.
4. 다 했으면 · 막히면 문서 맨 아래 「정답 5-5」에서 결과를 확인합니다.

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">6교시 (15:00–15:50) · 점수 규칙 · 맞힘 · 오탐 · 미탐</mark>

### 왜 필요한가

1. 지표 하나로 판정하면 틀리기 쉽습니다. 여러 지표에 **점수**를 주고 합이 기준을 넘으면 의심으로 봅니다.
2. 어떤 규칙도 완벽하지 않습니다. **정상을 의심으로 잘못 고르는 것(오탐)**과 **의심을 놓치는 것(미탐)**을 숫자로 재야 합니다.
3. 관제 실무의 탐지 룰도 이렇게 만들고, 재고, 고칩니다. 1과목 9/29 의 탐지 룰이 이 일의 시작이었습니다.

### 6.1 점수 규칙

**여기 나오는 말**

- **문턱값 (threshold)** (스레숄드) — 점수 합이 **이 값 이상이면 의심**으로 판정하는 기준 — `3`

| 규칙 | 점수 |
|---|---|
| ① TLD 앞 조각 길이가 10 이상 | +1 |
| ② 숫자가 2개 이상 | +1 |
| ③ 모음 비율이 0.25 미만 | +1 |
| ④ TLD 가 `top` · `xyz` · `tk` | +1 |
| ⑤ 답이 NXDOMAIN | **+2** — 가장 강한 지표 |
| **합이 3 이상이면 「의심」** | 문턱값 = 3 |

---

### ✍️ 문제 6-1 · 직접 실행해 보기

**할 일** — 규칙 세 개로 점수를 더하는 코드 열한 줄을 실행하고, 나온 결과와 그 이유를 보고서에 적습니다.

**왜 중요한가** — 규칙마다 점수를 더하고 문턱값과 비교하는 방식을 손으로 확인합니다. 6-2 의 점수 함수가 같은 방식으로 규칙 다섯 개를 더합니다.

**순서**
1. **[VS Code]** 왼쪽 목록에서 `network_zt` 폴더를 오른쪽 클릭 › **New File** › 이름 `warmup_6_1.py` 를 입력하고 Enter 를 누릅니다.
2. **[VS Code]** 아래 코드를 `warmup_6_1.py` 에 그대로 따라 칩니다.
   ```python
   score = 0                          # 합계 점수
   label = "kxq3vz9a"                 # TLD 앞 조각
   tld = "top"                        # TLD
   rcode = "NXDOMAIN"                 # DNS 의 답
   if len(label) >= 10:               # 조각이 10글자 이상인가?
       score = score + 1              # 그렇다면 1점
   if tld in ["top", "xyz", "tk"]:    # 값싼 TLD 인가?
       score = score + 1              # 그렇다면 1점
   if rcode == "NXDOMAIN":            # 없는 이름이라는 답인가?
       score = score + 2              # 그렇다면 2점
   print(score, score >= 3)           # 합계, 그리고 합계가 문턱값 3 이상인가?
   ```
3. **[터미널]** `network_zt` 폴더에서 `python warmup_6_1.py` 를 실행합니다.
   ```bash
   python warmup_6_1.py
   ```
   맥북: `python3 warmup_6_1.py`
4. **[보고서]** `day03_dns_analysis.md` 의 `## 6교시` › `### 문제 6-1` 아래를 채웁니다.
   - 출력:
   - 규칙마다 몇 점이 더해졌나요? 둘째 값이 그렇게 나온 이유를 설명합니다.

막히면 바로 위 6.1 표를 다시 봅니다.

다 했으면 · 막히면 문서 맨 아래 「정답 6-1」에서 결과를 확인합니다.

---

### 실습 1 · 점수 함수를 만들어 로그에 걸어 보기

`dga_score.py` 에 점수 함수를 만들고(6-2), 그 함수를 `judge.py` 에서 불러와 로그 12건에 겁니다(6-3). 두 파일은 같은 `network_zt` 폴더에 둡니다.

#### 6.2 다른 파일의 함수 불러 쓰기

#### 🐍 문법 상자 · `from 파일 import 함수` · `if __name__ == "__main__":`

```python
# dga_score.py 안
def score(name, rcode):
    ...
if __name__ == "__main__":       # python dga_score.py 로 직접 실행할 때만
    print(score("kxq3vz9a.top", "NXDOMAIN"))

# judge.py 안
from dga_score import score      # 위 파일의 함수를 꺼내 쓴다 — 시험 줄은 실행되지 않는다
```

| 쓰는 것 | 뜻 |
|---|---|
| `from 파일이름 import 함수` | 같은 폴더의 `파일이름.py` 에서 함수를 가져온다 (1과목 10/6) |
| `if __name__ == "__main__":` | 그 파일을 **직접** 실행할 때만 아래 줄을 실행한다 (1과목 10/8) |

⚠ 이 줄 없이 시험 `print` 를 두면, 다른 파일이 `import` 할 때마다 그 `print` 가 같이 찍힙니다.

#### ✍️ 문제 6-2 · 점수 함수 만들기

**할 일** — 6.1 의 규칙대로 점수와 걸린 규칙 이름을 리턴하는 함수를 `dga_score.py` 에 완성해 실행하고, 출력 두 줄을 보고서에 적습니다. 비어 있는 두 규칙만 채웁니다.

**왜 중요한가** — 여러 지표를 점수 하나로 모으면 도메인마다 의심 정도를 같은 기준으로 비교할 수 있습니다. 걸린 규칙 이름은 7교시 판정표의 근거 칸이 됩니다.

**순서**
1. **[VS Code]** `network_zt` 폴더에 `dga_score.py` 를 만듭니다.
2. **[VS Code]** 아래 코드를 파일에 붙여 넣습니다.
   ```python
   CHEAP_TLD = ["top", "xyz", "tk"]                  # 값싼 TLD

   def score(name, rcode):                           # 이름과 답을 받아 점수 · 이유를 리턴한다
       parts = name.split(".")                       # 점으로 나눈 조각들
       label = parts[-2]                             # TLD 앞 조각
       tld = parts[-1]                               # TLD
       points = 0                                    # 합계 점수
       why = []                                      # 걸린 규칙 이름
       if len(label) >= 10:                          # 규칙 ① 길이
           points = points + 1
           why.append("길이")
       digits = 0                                    # 숫자 개수
       vowels = 0                                    # 모음 개수
       for ch in label:                              # 한 자씩 센다
           if ch in "0123456789":
               digits = digits + 1
           if ch in "aeiou":
               vowels = vowels + 1
       if digits >= 2:                               # 규칙 ② 숫자
           points = points + 1
           why.append("숫자")
       # 1. 모음 비율(vowels / len(label))이 0.25 미만이면 points 에 1 을 더하고 why 에 "모음" 을 더하세요

       if tld in CHEAP_TLD:                          # 규칙 ④ 값싼 TLD
           points = points + 1
           why.append("TLD")
       # 2. rcode 가 "NXDOMAIN" 이면 points 에 2 를 더하고 why 에 "NXDOMAIN" 을 더하세요

       return {"points": points, "why": why}

   if __name__ == "__main__":                        # 직접 실행할 때만 시험한다
       print(score("www.naver.com", "NOERROR"))
       print(score("kxq3vz9a.top", "NXDOMAIN"))
   ```
3. **[VS Code]** 번호 주석 아래를 채웁니다.
4. **[터미널]** `network_zt` 폴더에서 `python dga_score.py` 를 실행합니다. 고친 뒤에는 **↑(위 화살표)** 를 눌러 같은 명령을 다시 실행합니다.
   ```bash
   python dga_score.py
   ```
   맥북: `python3 dga_score.py`
5. **[보고서]** `day03_dns_analysis.md` 의 `## 6교시` › `#### 문제 6-2` 아래를 채웁니다.
   - 출력 두 줄:

**💡 힌트**

1. 1번은 `if vowels / len(label) < 0.25:` 아래 두 줄입니다 — 위 규칙 ②와 같은 모양.
2. 2번은 2점입니다.
3. `why` 에 쌓인 이름이 7교시 판정표의 「근거」 칸이 됩니다.
4. 다 했으면 · 막히면 문서 맨 아래 「정답 6-2」에서 결과를 확인합니다.

---

#### ✍️ 문제 6-3 · 로그 12건 판정하기

**할 일** — 6-2 의 `score` 를 불러와 로그 12건을 문턱값 3 으로 판정하는 `judge.py` 를 완성해 실행하고, 판정이 틀린 줄 세 개를 보고서에 적습니다.

**왜 중요한가** — 만든 규칙을 로그 전체에 걸어 봐야 어느 도메인을 잘못 판정하는지 보입니다. 다른 파일의 함수를 불러 쓰는 방식은 6-4 · 7-2 에서도 씁니다.

**순서**
1. **[VS Code]** `network_zt` 폴더에 `judge.py` 를 만듭니다. `dga_score.py` 와 같은 폴더입니다.
2. **[VS Code]** 아래 코드를 파일에 붙여 넣습니다.
   ```python
   from dga_score import score                       # 6-2 의 함수를 꺼내 쓴다

   # ── 미리 채워 둔 줄입니다. 고치지 않습니다 ──
   LOG = [                                           # (이름, 답, 실제)
       ("www.naver.com", "NOERROR", "정상"), ("mail.google.com", "NOERROR", "정상"),
       ("update.microsoft.com", "NOERROR", "정상"), ("e6030.a.akamaiedge.net", "NOERROR", "정상"),
       ("cdn.jsdelivr.net", "NOERROR", "정상"), ("xn--3e0b707e.kr", "NOERROR", "정상"),
       ("kxq3vz9a.top", "NXDOMAIN", "의심"), ("p0w8rk2mzq.xyz", "NXDOMAIN", "의심"),
       ("qwrtpzkx7v.com", "NOERROR", "의심"), ("zzx9q2lk.top", "NXDOMAIN", "의심"),
       ("bnk-secure-login.xyz", "NOERROR", "의심"), ("www.example.com", "NOERROR", "정상"),
   ]
   THRESHOLD = 3                                     # 문턱값
   # ── 여기까지 ──

   for name, rcode, truth in LOG:                    # 로그를 한 줄씩
       result = score(name, rcode)                   # 점수와 걸린 규칙
       # 1. judged 에 result["points"] 가 THRESHOLD 이상이면 "의심", 아니면 "정상" 을 담으세요

       print(name, f"{result['points']}점", judged, f"(실제 {truth})")
   ```
3. **[VS Code]** 번호 주석 아래를 채웁니다.
4. **[터미널]** `network_zt` 폴더에서 `python judge.py` 를 실행합니다. 고친 뒤에는 **↑(위 화살표)** 를 눌러 같은 명령을 다시 실행합니다.
   ```bash
   python judge.py
   ```
   맥북: `python3 judge.py`
5. **[보고서]** `day03_dns_analysis.md` 의 `## 6교시` › `#### 문제 6-3` 아래를 채웁니다.
   - 판정이 틀린 세 줄:

**💡 힌트**

1. 두 갈래 값 고르기는 `if` · `else` 로 `judged` 를 정합니다.
2. `dga_score.py` 와 같은 폴더에서 실행해야 `import` 가 됩니다.
3. 틀린 줄은 판정과 `(실제 …)` 가 다른 줄입니다.
4. 다 했으면 · 막히면 문서 맨 아래 「정답 6-3」에서 결과를 확인합니다.

---

### 실습 2 · 규칙을 채점하고 고치기

6-3 의 판정을 정답지와 맞춰 채점하는 `evaluate.py` 를 만들고(6-4), `dga_score.py` 를 고친 뒤 같은 `evaluate.py` 로 다시 채점합니다(6-5).

#### 6.3 채점 — 맞힘 · 오탐 · 미탐

**여기 나오는 말**

- **오탐 (false positive)** (폴스 포지티브) — 실제로는 정상인데 규칙이 **「의심」으로 잘못 고른** 것
- **미탐 (false negative)** (폴스 네거티브) — 실제로는 의심인데 규칙이 **「정상」으로 놓친** 것

| | 실제 정상 | 실제 의심 |
|---|---|---|
| **규칙이 「의심」** | **오탐** | 맞힘(true positive) |
| **규칙이 「정상」** | 맞음 | **미탐** |

문턱값을 **낮추면** 미탐은 줄고 오탐은 늡니다. **높이면** 그 반대입니다.

> **검색해서 채웁니다.** 아래 질문을 한 번에 하나씩 검색합니다. 답은 오늘 보고서의 그 교시 `### 찾아본 것` 아래에 복사하지 말고 내 말로 적습니다. 다 적은 뒤 맨 아래 「정답」 표와 비교합니다.
> - 보안 관제에서 오탐이 많아지면 어떤 일이 생기나요?
> - 보안 관제에서 미탐이 많아지면 어떤 일이 생기나요?
> ⚠ 검색 결과는 영어 화면이 많습니다. 오탐은 false positive, 미탐은 false negative 와 짝을 맞춰 읽습니다.

| 많아지면 | 관제에 생기는 일 |
|---|---|
| 오탐 | **[찾아 쓰기]** 오탐이 많아지면 관제에 어떤 일이 생기나요? |
| 미탐 | **[찾아 쓰기]** 미탐이 많아지면 관제에 어떤 일이 생기나요? |

#### ✍️ 문제 6-4 · 맞힘 · 오탐 · 미탐 세기

**할 일** — 6-3 의 판정을 정답지(실제)와 비교해 맞힘 · 오탐 · 미탐 수를 세는 `evaluate.py` 를 완성해 실행하고, 세 숫자를 보고서에 적습니다.

**왜 중요한가** — 규칙의 성능을 맞힘 · 오탐 · 미탐 숫자로 적어 두어야 규칙을 고친 뒤 나아졌는지 비교할 수 있습니다. 관제에서 탐지 규칙을 평가할 때 쓰는 기준입니다.

**순서**
1. **[VS Code]** `network_zt` 폴더에 `evaluate.py` 를 만듭니다.
2. **[VS Code]** 아래 코드를 파일에 붙여 넣습니다.
   ```python
   from dga_score import score                       # 6-2 의 함수를 꺼내 쓴다

   # ── 미리 채워 둔 줄입니다. 고치지 않습니다 ──
   LOG = [                                           # (이름, 답, 실제)
       ("www.naver.com", "NOERROR", "정상"), ("mail.google.com", "NOERROR", "정상"),
       ("update.microsoft.com", "NOERROR", "정상"), ("e6030.a.akamaiedge.net", "NOERROR", "정상"),
       ("cdn.jsdelivr.net", "NOERROR", "정상"), ("xn--3e0b707e.kr", "NOERROR", "정상"),
       ("kxq3vz9a.top", "NXDOMAIN", "의심"), ("p0w8rk2mzq.xyz", "NXDOMAIN", "의심"),
       ("qwrtpzkx7v.com", "NOERROR", "의심"), ("zzx9q2lk.top", "NXDOMAIN", "의심"),
       ("bnk-secure-login.xyz", "NOERROR", "의심"), ("www.example.com", "NOERROR", "정상"),
   ]
   THRESHOLD = 3                                     # 문턱값
   hit = 0                                           # 맞힘 — 의심을 의심으로
   false_alarm = 0                                   # 오탐 — 정상을 의심으로
   missed = 0                                        # 미탐 — 의심을 정상으로
   # ── 여기까지 ──

   for name, rcode, truth in LOG:                    # 로그를 한 줄씩
       if score(name, rcode)["points"] >= THRESHOLD:   # 기준을 넘으면 의심
           judged = "의심"
       else:
           judged = "정상"
       # 1. judged 가 "의심" 이고 truth 가 "의심" 이면 hit 에 1 을 더하세요

       # 2. judged 가 "의심" 이고 truth 가 "정상" 이면 false_alarm 에 1 을 더하세요

       # 3. judged 가 "정상" 이고 truth 가 "의심" 이면 missed 에 1 을 더하세요

   print("맞힘", hit, "· 오탐", false_alarm, "· 미탐", missed)
   ```
3. **[VS Code]** 번호 주석 아래를 채웁니다.
4. **[터미널]** `network_zt` 폴더에서 `python evaluate.py` 를 실행합니다. 고친 뒤에는 **↑(위 화살표)** 를 눌러 같은 명령을 다시 실행합니다.
   ```bash
   python evaluate.py
   ```
   맥북: `python3 evaluate.py`
5. **[보고서]** `day03_dns_analysis.md` 의 `## 6교시` › `#### 문제 6-4` 아래를 채웁니다.
   - 맞힘 · 오탐 · 미탐:
   - 🔍 오탐과 미탐은 각각 무엇인가요? 문턱값을 낮추면 둘은 어떻게 바뀌나요?

**💡 힌트**

1. 세 개 모두 `and` 로 두 조건을 잇습니다.
2. `judged` 를 정하는 네 줄은 6-3 에서 쓴 것과 같아 미리 채워 두었습니다.
3. 6.3 표의 네 칸 가운데 세 칸을 세는 것입니다.
4. 다 했으면 · 막히면 문서 맨 아래 「정답 6-4」에서 결과를 확인합니다.

---

#### ✍️ 문제 6-5 · 예외 목록으로 오탐 줄이기

**할 일** — `dga_score.py` 의 `score` 안에 `xn--` 로 시작하는 조각은 0점으로 리턴하는 줄을 넣고, `evaluate.py` 를 다시 실행한 결과를 보고서에 적습니다.

**왜 중요한가** — 근거가 분명한 정상 도메인을 예외로 빼면 오탐이 줄어 관제 담당자가 확인할 경보가 줄어듭니다. 고친 뒤 6-4 를 다시 실행해 효과를 숫자로 확인합니다.

**이 문제에 나오는 말**

- **예외 목록 (allowlist)** (얼라우리스트) — 근거가 분명한 정상을 규칙에서 **빼 주는** 목록
- **퓨니코드 (Punycode)** (퓨니코드) — 한글 같은 글자의 도메인을 **영문으로 바꾼 모양** — `xn--` 로 시작한다. 오탐 `xn--3e0b707e.kr` 이 이것이라 무작위처럼 보인다

**순서**
1. **[VS Code]** 왼쪽 목록에서 6-2 에서 만든 `dga_score.py` 를 엽니다.
2. **[VS Code]** `label = parts[-2]` 바로 아래에 예외 두 줄을 넣습니다(💡 힌트 2). 새 코드를 붙여 넣지 않고 **있는 파일을 고칩니다.**
3. **[터미널]** `network_zt` 폴더에서 `python dga_score.py` 를 실행해 에러가 없는지 봅니다.
   ```bash
   python dga_score.py
   ```
   맥북: `python3 dga_score.py`
4. **[터미널]** `python evaluate.py` 로 6-4 를 다시 실행합니다.
   ```bash
   python evaluate.py
   ```
   맥북: `python3 evaluate.py`
5. **[보고서]** `day03_dns_analysis.md` 의 `## 6교시` › `#### 문제 6-5` 아래를 채웁니다.
   - 예외를 넣은 뒤 맞힘 · 오탐 · 미탐:
   - 예외 목록에 넣는 이름이 많아지면 어떤 위험이 생기나요?

**💡 힌트**

1. 넣을 곳은 `label = parts[-2]` 바로 아래입니다 — 점수를 세기 전에 끝내야 합니다.
2. `label.startswith("xn--")` 이면 `return {"points": 0, "why": ["한글 도메인 예외"]}`.
3. 예외는 **근거가 분명할 때만** 넣습니다. 예외에 든 이름은 규칙이 아예 보지 않습니다.
4. 다 했으면 · 막히면 문서 맨 아래 「정답 6-5」에서 결과를 확인합니다.

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">7교시 (16:00–16:50) · 3일 차 DNS 분석서 완성</mark>

### 왜 필요한가

1. 규칙을 만든 사람만 아는 규칙은 쓸 수 없습니다. **무엇을 · 왜 · 얼마나 맞았나**를 문서로 남겨야 다른 사람이 쓰고 고칩니다.
2. 강의계획서의 평가 기준이 바로 「합리적 근거」와 「판단 기준 문서화」입니다.
3. 마지막으로 판정이 맞는지 `nslookup` 으로 한 번 더 확인합니다.

### 7.1 판정표의 근거 칸 — 리스트를 글자로 잇기

**여기 나오는 말**

- **판정표** — 이름마다 **점수 · 판정 · 근거**를 한 줄씩 적은 표
- **근거** — 왜 그렇게 판정했는지 — 6-2 의 `why` 에 쌓인 **걸린 규칙 이름**

#### 🐍 문법 상자 · 리스트를 글자로 잇기 `", ".join()`

```python
why = ["숫자", "모음", "TLD"]
print(", ".join(why))
print(", ".join([]) == "")
# 숫자, 모음, TLD
# True
```

| 쓰는 것 | 뜻 |
|---|---|
| `"구분자".join(리스트)` | 리스트의 글자들을 구분자로 이어 하나로 |
| 빈 리스트를 이으면 | 빈 글자 `""` |

⚠ 리스트 안이 숫자면 `join` 이 에러를 냅니다. 글자 리스트에만 씁니다.

---

### ✍️ 문제 7-1 · 직접 실행해 보기

**할 일** — 점수 결과를 마크다운 표 한 줄로 찍는 코드 두 줄을 실행하고, 나온 결과와 그 이유를 보고서에 적습니다.

**왜 중요한가** — 근거 리스트를 글자 한 줄로 이어 마크다운 표의 한 줄로 만드는 연습입니다. 7-2 판정표의 근거 칸이 이 방식으로 채워집니다.

**순서**
1. **[VS Code]** 왼쪽 목록에서 `network_zt` 폴더를 오른쪽 클릭 › **New File** › 이름 `warmup_7_1.py` 를 입력하고 Enter 를 누릅니다.
2. **[VS Code]** 아래 코드를 `warmup_7_1.py` 에 그대로 따라 칩니다.
   ```python
   result = {"points": 5, "why": ["숫자", "모음", "TLD", "NXDOMAIN"]}                  # 6-2 의 score 가 리턴하는 모양
   print(f"| kxq3vz9a.top | {result['points']} | {', '.join(result['why'])} |")   # 이름 · 점수 · 근거를 표 한 줄로
   ```
3. **[터미널]** `network_zt` 폴더에서 `python warmup_7_1.py` 를 실행합니다.
   ```bash
   python warmup_7_1.py
   ```
   맥북: `python3 warmup_7_1.py`
4. **[보고서]** `day03_dns_analysis.md` 의 `## 7교시` › `### 문제 7-1` 아래를 채웁니다.
   - 출력:
   - 셋째 칸(근거)은 어떤 모양으로 찍혔나요? `', '.join(...)` 이 리스트에 한 일을 설명합니다.

막히면 바로 위 문법 상자를 다시 봅니다.

다 했으면 · 막히면 문서 맨 아래 「정답 7-1」에서 결과를 확인합니다.

---

### ✍️ 문제 7-2 · 판정표 만들기

**할 일** — 로그 12건의 점수 · 판정 · 근거를 마크다운 표로 출력하는 `report_table3.py` 를 완성해 실행하고, 그 표를 보고서 맨 아래 「1. 의심 도메인 판정」에 붙입니다. 근거가 없으면 `-` 로 적습니다.

**왜 중요한가** — 도메인마다 점수 · 판정 · 근거를 한 표로 남기면 다른 분석가가 판정 이유를 바로 확인하고 규칙을 고칠 수 있습니다. 이 표가 오늘 분석서의 「의심 도메인 판정」 칸이 됩니다.

**순서**
1. **[VS Code]** `network_zt` 폴더에 `report_table3.py` 를 만듭니다.
2. **[VS Code]** 아래 코드를 파일에 붙여 넣습니다.
   ```python
   from dga_score import score                       # 6-5 에서 고친 함수를 꺼내 쓴다

   # ── 미리 채워 둔 줄입니다. 고치지 않습니다 ──
   LOG = [                                           # (이름, 답)
       ("www.naver.com", "NOERROR"), ("mail.google.com", "NOERROR"), ("update.microsoft.com", "NOERROR"),
       ("e6030.a.akamaiedge.net", "NOERROR"), ("cdn.jsdelivr.net", "NOERROR"), ("xn--3e0b707e.kr", "NOERROR"),
       ("kxq3vz9a.top", "NXDOMAIN"), ("p0w8rk2mzq.xyz", "NXDOMAIN"), ("qwrtpzkx7v.com", "NOERROR"),
       ("zzx9q2lk.top", "NXDOMAIN"), ("bnk-secure-login.xyz", "NOERROR"), ("www.example.com", "NOERROR"),
   ]
   print("| 이름 | 답 | 점수 | 판정 | 근거 |")           # 표 머리
   print("|---|---|---|---|---|")                    # 표 구분 줄
   # ── 여기까지 ──

   for name, rcode in LOG:                           # 로그를 한 줄씩
       result = score(name, rcode)                   # 점수와 걸린 규칙
       if result["points"] >= 3:                     # 문턱값 3
           judged = "의심"
       else:
           judged = "정상"
       # 1. reason 에 result["why"] 를 ", " 로 이은 글자를 담고, 비어 있으면 "-" 를 담으세요

       print(f"| {name} | {rcode} | {result['points']} | {judged} | {reason} |")
   ```
3. **[VS Code]** 번호 주석 아래를 채웁니다.
4. **[터미널]** `network_zt` 폴더에서 `python report_table3.py` 를 실행합니다. 고친 뒤에는 **↑(위 화살표)** 를 눌러 같은 명령을 다시 실행합니다.
   ```bash
   python report_table3.py
   ```
   맥북: `python3 report_table3.py`
5. **[터미널]** 출력된 표를 `| 이름 |` 줄부터 마지막 줄까지 끌어 선택해 복사합니다.
6. **[보고서]** 맨 아래 `## 최종 분석서` › `### 1. 의심 도메인 판정` 의 첫 줄 아래에 붙여 넣습니다.
7. **[보고서]** `day03_dns_analysis.md` 의 `## 7교시` › `### 문제 7-2` 아래를 채웁니다.
   - 「의심」으로 판정된 이름:

**💡 힌트**

1. 바로 위 문법 상자의 `", ".join(…)` 입니다.
2. 비어 있는지는 `if reason == "":` 로 봅니다.
3. 6-5 에서 고친 `dga_score.py` 를 불러오므로 한글 도메인은 예외로 나옵니다.
4. 다 했으면 · 막히면 문서 맨 아래 「정답 7-2」에서 결과를 확인합니다.

---

### ✍️ 문제 7-3 · 판정을 `nslookup` 으로 확인하기

**할 일** — 규칙이 「정상」이라고 한 CDN 이름과 지어낸 무작위 이름을 각각 `nslookup` 으로 물어 있는 이름인지 확인하고, 두 답을 보고서에 적습니다.

**왜 중요한가** — 겉모습만으로 내린 판정을 실제 DNS 조회로 한 번 더 확인합니다. 관제에서는 의심 도메인에 접속하지 않고 `nslookup` 으로 존재 여부를 먼저 봅니다.

**이 문제에 나오는 말**

- **`.invalid`** (닷 인밸리드) — **절대 존재하지 않도록** 정해 둔 TLD. 시험용으로 쓴다
- **위협 정보 (threat intelligence)** (스레트 인텔리전스) — 알려진 악성 도메인 · IP 를 모아 둔 **정보 · 사이트**

**순서**
1. **[터미널]** 규칙이 「정상」이라고 한 CDN 이름을 묻습니다.
   ```bash
   nslookup e6030.a.akamaiedge.net
   ```
2. **[터미널]** 지어낸 무작위 이름을 묻습니다.
   ```bash
   nslookup qzkx7wp2v.invalid
   ```
3. **[보고서]** `day03_dns_analysis.md` 의 `## 7교시` › `### 문제 7-3` 아래를 채웁니다.
   - 첫째 이름의 답 · 둘째 이름의 답:

**💡 힌트**

1. 겉모습만으로는 둘 다 무작위처럼 보입니다. **실제로 물어보는 것**이 가장 확실한 근거입니다. `.invalid` 는 「절대 존재하지 않는 이름」으로 정해 둔 TLD 라 시험용으로 씁니다(`example.com` 은 아무 하위 이름에도 답하도록 돼 있어 쓰지 않습니다 — 실측).
2. 실무에서는 여기에 「언제 처음 등록됐나」, 「위협 정보 사이트에 올라 있나」를 더 봅니다.
3. 의심 도메인에 **브라우저로 접속하지 않습니다.** `nslookup` 은 이름만 묻고 접속하지 않습니다.
4. 다 했으면 · 막히면 문서 맨 아래 「정답 7-3」에서 결과를 확인합니다.

---

### ✍️ 문제 7-4 · 분석서 완성하고 올리기

**할 일** — 보고서 맨 아래 「최종 분석서」의 판단 기준 · 한계를 포함해 빈칸을 다 채우고, 터미널의 git 명령으로 내 GitHub 저장소의 `network_zt` 폴더에 올립니다.

**왜 중요한가** — 판단 기준과 한계를 적어 두어야 다른 사람이 규칙을 다시 쓰고, 못 잡는 경우를 다른 규칙으로 보완할 수 있습니다. 강의계획서의 평가 기준인 「판단 기준 문서화」가 이 칸입니다. 올리기 전에 `git status` 로 무엇이 골라지는지 먼저 보아야 `.env` 같은 비밀 파일이 깃허브에 올라가지 않습니다.

**순서**
1. **[보고서]** `day03_dns_analysis.md` 맨 아래 `## 최종 분석서` 의 `### 2. 판단 기준` · `### 3. 규칙의 한계` · `### 4. 오늘 하루 정리` 를 채웁니다. 6교시 · 7-3 에 적은 답을 다시 봅니다.
2. **[보고서]** 5 · 6 · 7교시 칸에서 빈 줄을 찾아 채웁니다. ⭐ 는 비워도 됩니다.
3. **[터미널]** `security-agent-toolkit` 폴더로 옮깁니다. 터미널이 `network_zt` 에 있으면 `cd ..` 를 입력합니다.
   ```bash
   cd ..
   ```
4. **[터미널]** 무엇이 바뀌었는지 먼저 봅니다. 빨간 목록에 `.env` 나 `.venv` 가 보이면 멈추고 강사를 부릅니다.
   ```bash
   git status
   ```
5. **[터미널]** 바뀐 것을 한 번에 고릅니다.
   ```bash
   git add .
   ```
6. **[터미널]** 기록하고 올립니다.
   ```bash
   git commit -m "Add day 3 DNS analysis report"
   git push
   ```
7. **[브라우저]** 깃허브의 내 저장소를 새로 고쳐 `network_zt` 폴더에 보고서가 보이는지 확인합니다.

**💡 힌트**

1. 「2. 판단 기준」은 6.1 표와 6-5 의 예외를 내 말로 다시 씁니다.
2. 미탐 `bnk-secure-login.xyz` 는 DGA 가 아니라 **사칭**이라 이 점수 규칙으로는 못 잡습니다 — 5-4 같은 다른 규칙이 필요합니다. 한계를 숨기지 않는 것이 좋은 보고서입니다.
3. 빨간 목록에 `.env` 가 보이면 멈춥니다 — 아침 과제 7번에서 본 것과 같습니다. `.gitignore` 를 확인하고 강사를 부릅니다.
4. `git push` 가 거절(`rejected`)되면 강사를 부릅니다.
5. 다 했으면 · 막히면 문서 맨 아래 「정답 7-4」에서 결과를 확인합니다.

---

## 오늘 마무리

| 확인 | 문제 |
|---|---|
| `day03_dns_analysis.md` 의 2~7교시와 「최종 분석서」에 빈 칸이 없다(⭐ 제외) | 모든 문제 · 7-4 |
| DGA · 사칭 · NXDOMAIN 폭증의 지표를 말할 수 있다 | 5교시 |
| 오탐과 미탐의 차이를 숫자로 설명할 수 있다 | 6-4 · 6-5 |
| 깃허브에 올렸다 | 7-4 |

내일(10/15(목))은 **VPN 과 방화벽**을 배웁니다.

---

# 정답 · 먼저 풀어 본 뒤에 봅니다

수업용 로그의 점수는 실행해 확인한 값입니다. `nslookup` 의 IP 는 실행할 때마다 다를 수 있습니다.

---

### 정답 · 6.3 오탐 · 미탐 표

| 많아지면 | 관제에 생기는 일 |
|---|---|
| 오탐 | 관제 요원이 헛경보를 확인하느라 지친다 — 정상 경보를 쫓느라 진짜를 볼 시간이 줄어든다 |
| 미탐 | 공격을 놓친다 — 경보가 울리지 않으니 아무도 모른다 |

---

### 정답 5-1

**결과** — `p0w8rk2mzq 10 0`

**왜** — `parts[-2]` 는 TLD(`xyz`) 바로 앞 조각 `p0w8rk2mzq` 입니다. 열 글자인데 모음이 하나도 없습니다. 둘째 글자 `0` 은 숫자라 `"aeiou"` 안에 없으므로 모음으로 세지 않습니다. 모음이 없는 이름은 사람이 지은 이름에서는 드문 DGA 의 특징입니다.

**자주 틀리는 곳** — `parts[-1]` 과 헷갈려 `xyz 3 0` 으로 적거나, 숫자 `0` 을 모음 `o` 로 잘못 세는 경우가 많습니다.

**관제에서는** — 로그에서 길이와 모음 수만 뽑아 봐도 사람이 지은 이름과 기계가 만든 이름이 먼저 갈립니다.

---

### 정답 5-2

```python
names = ["www.naver.com", "e6030.a.akamaiedge.net", "kxq3vz9a.top", "bnk-secure-login.xyz"]

for name in names:                                # 이름을 하나씩
    parts = name.split(".")                       # 점으로 나눈 조각들
    # 1. label 에 parts 의 끝에서 둘째(-2)를, tld 에 맨 끝(-1)을 담으세요
    label = parts[-2]                             # TLD 앞 조각
    tld = parts[-1]                               # TLD
    print(name, "조각:", label, "TLD:", tld)
```

💻 **터미널에 입력합니다.**

```bash
python label.py
```
맥북: `python3 label.py`

**결과** — `www.naver.com 조각: naver TLD: com` · `e6030.a.akamaiedge.net 조각: akamaiedge TLD: net` · `kxq3vz9a.top 조각: kxq3vz9a TLD: top` · `bnk-secure-login.xyz 조각: bnk-secure-login TLD: xyz`

**왜** — `split(".")` 로 나눈 조각 수는 이름마다 다르지만, `[-1]` · `[-2]` 처럼 끝에서 세면 TLD 와 그 앞 조각을 늘 같은 자리에서 꺼냅니다.

**자주 틀리는 곳** — `parts[1]` 처럼 앞에서 세면 `e6030.a.akamaiedge.net` 에서 `a` 가 나옵니다.

**관제에서는** — CDN 처럼 맨 앞이 무작위인 정상 이름에 속지 않도록 실제 등록된 이름인 TLD 앞 조각을 봅니다.

---

### 정답 5-3

```python
def features(name):                               # 이름 하나의 특징을 사전으로 리턴한다
    label = name.split(".")[-2]                   # TLD 앞 조각
    digits = 0                                    # 숫자 개수
    vowels = 0                                    # 모음 개수
    for ch in label:                              # 한 자씩
        # 1. ch 가 숫자면 digits 에 1 을 더하세요
        if ch in "0123456789":
            digits = digits + 1
        # 2. ch 가 모음(aeiou)이면 vowels 에 1 을 더하세요
        if ch in "aeiou":
            vowels = vowels + 1
    return {"label": label, "len": len(label), "digits": digits, "vowel_ratio": round(vowels / len(label), 2)}

for name in ["www.naver.com", "kxq3vz9a.top", "xn--3e0b707e.kr"]:
    print(features(name))
```

💻 **터미널에 입력합니다.**

```bash
python features.py
```
맥북: `python3 features.py`

**결과** — `{'label': 'naver', 'len': 5, 'digits': 0, 'vowel_ratio': 0.4}` · `{'label': 'kxq3vz9a', 'len': 8, 'digits': 2, 'vowel_ratio': 0.12}` · `{'label': 'xn--3e0b707e', 'len': 12, 'digits': 5, 'vowel_ratio': 0.17}`

**왜** — `if` 두 개가 한 자씩 숫자와 모음을 따로 셉니다. DGA 이름인 `kxq3vz9a` 는 숫자가 많고 모음 비율이 0.12 로 낮습니다.

**자주 틀리는 곳** — `if` 를 `for` 와 같은 높이로 들여 쓰면 반복이 끝난 뒤 마지막 글자 하나만 보게 되어 숫자 · 모음 수가 틀립니다.

**관제에서는** — 정상인 `xn--3e0b707e` 도 숫자가 많고 모음이 적으므로, 지표 하나만 보고 의심으로 정하지 않습니다(6교시 오탐).

---

### 정답 5-4

```python
TRUSTED = ["naver.com", "google.com", "kbstar.com"]   # 우리 회사가 쓰는 진짜 도메인
seen = ["nav3r.com", "google.com", "g00gle.com", "kbstar.com", "kb5tar.com"]   # 로그에 나온 이름

for name in seen:                                 # 로그에 나온 이름을 하나씩
    # 1. plain 에 name 의 0 을 o 로, 1 을 l 로, 3 을 e 로 바꾼 글자를 담으세요
    plain = name.replace("0", "o").replace("1", "l").replace("3", "e")   # 숫자를 닮은 글자로
    if name in TRUSTED:                           # 진짜 도메인 그대로면
        print("[정상]", name)
    # 2. 아니고 plain 이 TRUSTED 안에 있으면 「[사칭 의심] nav3r.com → naver.com 흉내」 를 출력하세요
    elif plain in TRUSTED:                        # 바꾸니 진짜와 같아지면
        print("[사칭 의심]", name, "→", plain, "흉내")
    else:                                         # 둘 다 아니면
        print("[모름]", name)
```

💻 **터미널에 입력합니다.**

```bash
python typosquat.py
```
맥북: `python3 typosquat.py`

**결과** — `[사칭 의심] nav3r.com → naver.com 흉내` · `[정상] google.com` · `[사칭 의심] g00gle.com → google.com 흉내` · `[정상] kbstar.com` · `[모름] kb5tar.com`

**왜** — `replace` 로 숫자를 닮은 글자로 되돌렸을 때 진짜 도메인과 같아지면 사칭입니다. `kb5tar` 는 `5 → s` 바꾸기가 없어 `[모름]` 입니다.

**자주 틀리는 곳** — `if name in TRUSTED` 보다 `plain` 검사를 먼저 두면, 진짜 `google.com` 도 바꾼 뒤 같으니 `[사칭 의심]` 으로 찍힙니다.

**관제에서는** — 우리 회사와 거래처의 진짜 도메인 목록을 두고, 비슷하게 생긴 이름이 로그에 나오면 피싱으로 의심합니다.

---

### 정답 5-5

```python
logs = [                                          # (PC 주소, 물어본 이름, 답)
    ("10.20.0.15", "www.naver.com", "NOERROR"),
    ("10.20.0.42", "kxq3vz9a.top", "NXDOMAIN"),
    ("10.20.0.42", "p0w8rk2mzq.xyz", "NXDOMAIN"),
    ("10.20.0.15", "mail.google.com", "NOERROR"),
    ("10.20.0.42", "zzx9q2lk.top", "NXDOMAIN"),
    ("10.20.0.33", "typo-nevar.com", "NXDOMAIN"),
    ("10.20.0.42", "qwrtpzkx7v.com", "NOERROR"),
]
nx = {}                                           # PC 주소 → NXDOMAIN 횟수

for pc, name, rcode in logs:                      # 로그를 한 줄씩
    # 1. rcode 가 "NXDOMAIN" 이면 nx 의 pc 키를 1 늘리세요 (.get)
    if rcode == "NXDOMAIN":
        nx[pc] = nx.get(pc, 0) + 1                # 처음 보는 PC 면 0 에서

for pc in nx:                                     # 센 PC 를 하나씩
    # 2. 횟수가 3 이상이면 「[확인 필요] 10.20.0.42 NXDOMAIN 3번」 을 출력하세요
    if nx[pc] >= 3:
        print(f"[확인 필요] {pc} NXDOMAIN {nx[pc]}번")
```

💻 **터미널에 입력합니다.**

```bash
python nx_count.py
```
맥북: `python3 nx_count.py`

**결과** — `[확인 필요] 10.20.0.42 NXDOMAIN 3번` 한 줄

**왜** — `nx.get(pc, 0) + 1` 이 PC 마다 NXDOMAIN 횟수를 쌓습니다. `10.20.0.42` 는 3번, `10.20.0.33` 은 1번이라 문턱 3 을 넘는 PC 는 하나입니다. DGA 에 감염된 PC 는 자동으로 만든 이름을 차례로 묻는데, 대부분 등록하지 않은 이름이라 NXDOMAIN 이 쏟아집니다.

**자주 틀리는 곳** — `nx[pc] = nx[pc] + 1` 로 쓰면 처음 보는 PC 에서 `KeyError` 가 납니다. 그래서 `.get(pc, 0)` 을 씁니다.

**관제에서는** — 없는 이름을 연달아 묻는 PC 는 DGA 악성 코드에 감염됐을 수 있어 그 PC 부터 확인합니다.

---

### 정답 6-1

**결과** — `3 True`

**왜** — 길이는 8 이라 0점, TLD `top` 1점, NXDOMAIN 2점입니다. 합이 3 이라 `score >= 3` 이 `True` 입니다.

**자주 틀리는 곳** — NXDOMAIN 을 1점으로 세어 `2 False` 로 적는 경우가 많습니다. 이 줄만 `+ 2` 입니다.

**관제에서는** — 없는 이름을 물었다는 것(NXDOMAIN)이 가장 강한 신호라서 점수를 더 크게 줍니다.

---

### 정답 6-2

```python
CHEAP_TLD = ["top", "xyz", "tk"]                  # 값싼 TLD

def score(name, rcode):                           # 이름과 답을 받아 점수 · 이유를 리턴한다
    parts = name.split(".")                       # 점으로 나눈 조각들
    label = parts[-2]                             # TLD 앞 조각
    tld = parts[-1]                               # TLD
    points = 0                                    # 합계 점수
    why = []                                      # 걸린 규칙 이름
    if len(label) >= 10:                          # 규칙 ① 길이
        points = points + 1
        why.append("길이")
    digits = 0                                    # 숫자 개수
    vowels = 0                                    # 모음 개수
    for ch in label:                              # 한 자씩 센다
        if ch in "0123456789":
            digits = digits + 1
        if ch in "aeiou":
            vowels = vowels + 1
    if digits >= 2:                               # 규칙 ② 숫자
        points = points + 1
        why.append("숫자")
    # 1. 모음 비율(vowels / len(label))이 0.25 미만이면 points 에 1 을 더하고 why 에 "모음" 을 더하세요
    if vowels / len(label) < 0.25:                # 규칙 ③ 모음 적음
        points = points + 1
        why.append("모음")
    if tld in CHEAP_TLD:                          # 규칙 ④ 값싼 TLD
        points = points + 1
        why.append("TLD")
    # 2. rcode 가 "NXDOMAIN" 이면 points 에 2 를 더하고 why 에 "NXDOMAIN" 을 더하세요
    if rcode == "NXDOMAIN":                       # 규칙 ⑤ 없는 이름 — 가장 강한 지표
        points = points + 2
        why.append("NXDOMAIN")
    return {"points": points, "why": why}

if __name__ == "__main__":                        # 직접 실행할 때만 시험한다
    print(score("www.naver.com", "NOERROR"))
    print(score("kxq3vz9a.top", "NXDOMAIN"))
```

💻 **터미널에 입력합니다.**

```bash
python dga_score.py
```
맥북: `python3 dga_score.py`

**결과** — `{'points': 0, 'why': []}` · `{'points': 5, 'why': ['숫자', '모음', 'TLD', 'NXDOMAIN']}`

**왜** — `kxq3vz9a` 는 8글자라 길이 규칙만 빠지고, 숫자 · 모음 · TLD 각 1점에 NXDOMAIN 2점이 더해져 5점입니다. `why` 에 걸린 규칙 이름이 차례로 쌓입니다.

**자주 틀리는 곳** — NXDOMAIN 에 `points + 1` 을 써서 4점이 나오는 경우가 많습니다. 이 규칙만 2점입니다.

**관제에서는** — 점수와 함께 `why` 를 남겨야 경보를 받은 분석가가 어떤 근거로 걸렸는지 바로 봅니다.

---

### 정답 6-3

```python
from dga_score import score                       # 6-2 의 함수를 꺼내 쓴다

LOG = [                                           # (이름, 답, 실제)
    ("www.naver.com", "NOERROR", "정상"), ("mail.google.com", "NOERROR", "정상"),
    ("update.microsoft.com", "NOERROR", "정상"), ("e6030.a.akamaiedge.net", "NOERROR", "정상"),
    ("cdn.jsdelivr.net", "NOERROR", "정상"), ("xn--3e0b707e.kr", "NOERROR", "정상"),
    ("kxq3vz9a.top", "NXDOMAIN", "의심"), ("p0w8rk2mzq.xyz", "NXDOMAIN", "의심"),
    ("qwrtpzkx7v.com", "NOERROR", "의심"), ("zzx9q2lk.top", "NXDOMAIN", "의심"),
    ("bnk-secure-login.xyz", "NOERROR", "의심"), ("www.example.com", "NOERROR", "정상"),
]
THRESHOLD = 3                                     # 문턱값

for name, rcode, truth in LOG:                    # 로그를 한 줄씩
    result = score(name, rcode)                   # 점수와 걸린 규칙
    # 1. judged 에 result["points"] 가 THRESHOLD 이상이면 "의심", 아니면 "정상" 을 담으세요
    if result["points"] >= THRESHOLD:             # 기준을 넘으면
        judged = "의심"
    else:
        judged = "정상"
    print(name, f"{result['points']}점", judged, f"(실제 {truth})")
```

💻 **터미널에 입력합니다.**

```bash
python judge.py
```
맥북: `python3 judge.py`

**결과** — 열두 줄. `xn--3e0b707e.kr 3점 의심 (실제 정상)` 과 `qwrtpzkx7v.com 2점 정상 (실제 의심)` · `bnk-secure-login.xyz 2점 정상 (실제 의심)` 이 **틀린 줄**입니다.

**왜** — `result["points"] >= THRESHOLD` 한 줄이 판정을 정합니다. `qwrtpzkx7v.com` 은 실제로 등록돼 NOERROR 라 NXDOMAIN 2점을 못 받았고, `bnk-secure-login` 은 모음이 충분해 길이 · TLD 2점에 그쳤습니다.

**자주 틀리는 곳** — `>=` 대신 `>` 를 쓰면 3점인 `xn--3e0b707e.kr` 이 정상으로 바뀌어 틀린 줄 수가 달라집니다.

**관제에서는** — 규칙이 틀린 줄을 하나씩 열어 보고 왜 틀렸는지 찾는 것이 탐지 룰을 고치는 출발점입니다.

---

### 정답 6-4

```python
from dga_score import score                       # 6-2 의 함수를 꺼내 쓴다

LOG = [                                           # (이름, 답, 실제)
    ("www.naver.com", "NOERROR", "정상"), ("mail.google.com", "NOERROR", "정상"),
    ("update.microsoft.com", "NOERROR", "정상"), ("e6030.a.akamaiedge.net", "NOERROR", "정상"),
    ("cdn.jsdelivr.net", "NOERROR", "정상"), ("xn--3e0b707e.kr", "NOERROR", "정상"),
    ("kxq3vz9a.top", "NXDOMAIN", "의심"), ("p0w8rk2mzq.xyz", "NXDOMAIN", "의심"),
    ("qwrtpzkx7v.com", "NOERROR", "의심"), ("zzx9q2lk.top", "NXDOMAIN", "의심"),
    ("bnk-secure-login.xyz", "NOERROR", "의심"), ("www.example.com", "NOERROR", "정상"),
]
THRESHOLD = 3                                     # 문턱값
hit = 0                                           # 맞힘 — 의심을 의심으로
false_alarm = 0                                   # 오탐 — 정상을 의심으로
missed = 0                                        # 미탐 — 의심을 정상으로

for name, rcode, truth in LOG:                    # 로그를 한 줄씩
    if score(name, rcode)["points"] >= THRESHOLD:   # 기준을 넘으면 의심
        judged = "의심"
    else:
        judged = "정상"
    # 1. judged 가 "의심" 이고 truth 가 "의심" 이면 hit 에 1 을 더하세요
    if judged == "의심" and truth == "의심":
        hit = hit + 1
    # 2. judged 가 "의심" 이고 truth 가 "정상" 이면 false_alarm 에 1 을 더하세요
    if judged == "의심" and truth == "정상":
        false_alarm = false_alarm + 1
    # 3. judged 가 "정상" 이고 truth 가 "의심" 이면 missed 에 1 을 더하세요
    if judged == "정상" and truth == "의심":
        missed = missed + 1

print("맞힘", hit, "· 오탐", false_alarm, "· 미탐", missed)
```

💻 **터미널에 입력합니다.**

```bash
python evaluate.py
```
맥북: `python3 evaluate.py`

**결과** — `맞힘 3 · 오탐 1 · 미탐 2`

**왜** — `and` 로 판정과 실제를 함께 봅니다. 맞힘은 NXDOMAIN 세 개, 오탐은 한글 도메인 `xn--3e0b707e.kr`, 미탐은 `qwrtpzkx7v.com` · `bnk-secure-login.xyz` 입니다. 문턱값을 낮추면 2점짜리 미탐이 「의심」으로 넘어와 미탐은 줄지만, 정상 이름도 더 쉽게 걸려 오탐은 늡니다.

**자주 틀리는 곳** — 조건을 `judged == "의심"` 하나만 쓰면 맞힘과 오탐이 섞여 맞힘이 4 로 나옵니다.

**관제에서는** — 오탐이 많으면 분석가가 헛경보에 시간을 쓰고, 미탐이 있으면 공격을 놓치므로 둘을 따로 세어 룰을 평가합니다.

---

### 정답 6-5

`dga_score.py` 의 `label = parts[-2]` 바로 아래에 두 줄을 넣습니다.

```python
CHEAP_TLD = ["top", "xyz", "tk"]                  # 값싼 TLD

def score(name, rcode):                           # 이름과 답을 받아 점수 · 이유를 리턴한다
    parts = name.split(".")                       # 점으로 나눈 조각들
    label = parts[-2]                             # TLD 앞 조각
    if label.startswith("xn--"):                  # 한글 도메인을 영문으로 바꾼 모양이면
        return {"points": 0, "why": ["한글 도메인 예외"]}
    tld = parts[-1]                               # TLD
    points = 0                                    # 합계 점수
    why = []                                      # 걸린 규칙 이름
    if len(label) >= 10:                          # 규칙 ① 길이
        points = points + 1
        why.append("길이")
    digits = 0                                    # 숫자 개수
    vowels = 0                                    # 모음 개수
    for ch in label:                              # 한 자씩 센다
        if ch in "0123456789":
            digits = digits + 1
        if ch in "aeiou":
            vowels = vowels + 1
    if digits >= 2:                               # 규칙 ② 숫자
        points = points + 1
        why.append("숫자")
    if vowels / len(label) < 0.25:                # 규칙 ③ 모음 적음
        points = points + 1
        why.append("모음")
    if tld in CHEAP_TLD:                          # 규칙 ④ 값싼 TLD
        points = points + 1
        why.append("TLD")
    if rcode == "NXDOMAIN":                       # 규칙 ⑤ 없는 이름 — 가장 강한 지표
        points = points + 2
        why.append("NXDOMAIN")
    return {"points": points, "why": why}

if __name__ == "__main__":                        # 직접 실행할 때만 시험한다
    print(score("www.naver.com", "NOERROR"))
    print(score("kxq3vz9a.top", "NXDOMAIN"))
```

💻 **터미널에 입력합니다.**

```bash
python dga_score.py
python evaluate.py
```
맥북: `python3 dga_score.py` → `python3 evaluate.py`

**결과** — `python dga_score.py` 의 두 줄은 6-2 와 같고, `python evaluate.py` 는 `맞힘 3 · 오탐 0 · 미탐 2` 입니다.

**왜** — `label.startswith("xn--")` 이면 점수를 세기 전에 0점으로 리턴하므로, 한글 도메인 하나가 오탐에서 빠집니다. 다른 이름의 점수는 그대로입니다. 예외에 든 이름은 규칙이 아예 보지 않으므로, 예외가 많아지면 공격자가 그 모양의 이름으로 숨을 틈이 커집니다.

**자주 틀리는 곳** — 두 줄을 `return {"points": points, …}` 바로 앞(맨 끝)에 넣으면 이미 점수를 다 센 뒤라 소용이 없습니다. `label = parts[-2]` 바로 아래에 넣습니다.

**관제에서는** — 예외는 근거가 분명한 것만 넣고 보고서에 적어 둡니다. 예외가 늘면 공격자가 그 틈으로 숨습니다.

---

### 정답 7-1

**결과** — `| kxq3vz9a.top | 5 | 숫자, 모음, TLD, NXDOMAIN |`

**왜** — `', '.join(...)` 이 리스트 네 개를 쉼표와 빈칸으로 이어 글자 하나로 만듭니다. 그래서 대괄호와 따옴표 없이 찍힙니다. 앞뒤의 `|` 덕분에 마크다운 표의 한 줄이 됩니다.

**자주 틀리는 곳** — 리스트 모양 그대로 `['숫자', '모음', …]` 이 찍힌다고 적는 경우가 많습니다. `join` 을 거치면 대괄호와 따옴표가 사라집니다.

**관제에서는** — 걸린 규칙 이름을 근거로 함께 적어 두어야 다른 분석가가 왜 의심인지 바로 확인합니다.

---

### 정답 7-2

```python
from dga_score import score                       # 6-5 에서 고친 함수를 꺼내 쓴다

LOG = [                                           # (이름, 답)
    ("www.naver.com", "NOERROR"), ("mail.google.com", "NOERROR"), ("update.microsoft.com", "NOERROR"),
    ("e6030.a.akamaiedge.net", "NOERROR"), ("cdn.jsdelivr.net", "NOERROR"), ("xn--3e0b707e.kr", "NOERROR"),
    ("kxq3vz9a.top", "NXDOMAIN"), ("p0w8rk2mzq.xyz", "NXDOMAIN"), ("qwrtpzkx7v.com", "NOERROR"),
    ("zzx9q2lk.top", "NXDOMAIN"), ("bnk-secure-login.xyz", "NOERROR"), ("www.example.com", "NOERROR"),
]
print("| 이름 | 답 | 점수 | 판정 | 근거 |")           # 표 머리
print("|---|---|---|---|---|")                    # 표 구분 줄

for name, rcode in LOG:                           # 로그를 한 줄씩
    result = score(name, rcode)                   # 점수와 걸린 규칙
    if result["points"] >= 3:                     # 문턱값 3
        judged = "의심"
    else:
        judged = "정상"
    # 1. reason 에 result["why"] 를 ", " 로 이은 글자를 담고, 비어 있으면 "-" 를 담으세요
    reason = ", ".join(result["why"])             # 걸린 규칙을 이어 붙인다
    if reason == "":                              # 아무 규칙에도 안 걸렸으면
        reason = "-"
    print(f"| {name} | {rcode} | {result['points']} | {judged} | {reason} |")
```

💻 **터미널에 입력합니다.**

```bash
python report_table3.py
```
맥북: `python3 report_table3.py`

**결과** — `| www.naver.com | NOERROR | 0 | 정상 | - |` 로 시작하는 열두 줄 — `xn--3e0b707e.kr` 은 `0 | 정상 | 한글 도메인 예외`, 「의심」은 `kxq3vz9a.top` · `p0w8rk2mzq.xyz` · `zzx9q2lk.top` 세 줄입니다.

**왜** — `", ".join(result["why"])` 가 걸린 규칙을 한 칸에 이어 붙이고, 아무 규칙에도 안 걸려 빈 글자면 `-` 로 바꿉니다.

**자주 틀리는 곳** — `if result["why"] == "":` 처럼 리스트를 빈 글자와 비교하면 늘 거짓이라 `-` 가 나오지 않습니다. `join` 한 뒤의 `reason` 을 비교합니다.

**관제에서는** — 판정마다 근거가 있어야 보고서를 읽는 사람이 판정을 다시 확인할 수 있습니다.

---

### 정답 7-3

💻 **터미널에 입력합니다.**

```bash
nslookup e6030.a.akamaiedge.net
nslookup qzkx7wp2v.invalid
```

**결과** — 첫째는 `Address` 에 IP 가 나오고(있는 이름), 둘째는 `Non-existent domain`(없는 이름)입니다. IP 는 실행할 때마다 다를 수 있습니다.

**왜** — 둘 다 겉모습은 무작위지만, `nslookup` 은 DNS 에 실제로 물어 답(NOERROR · NXDOMAIN)을 받아 옵니다. `.invalid` 는 존재하지 않도록 정해 둔 TLD 입니다.

**자주 틀리는 곳** — 확인하려고 의심 이름을 브라우저 주소창에 넣는 경우가 있습니다. 접속하지 않고 `nslookup` 으로 묻기만 합니다.

**관제에서는** — 규칙의 판정을 실제 조회 결과와 등록일 · 위협 정보 사이트로 한 번 더 확인한 뒤 차단을 정합니다.

---

### 정답 7-4

보고서 「최종 분석서」의 예 — 판단 기준: 「규칙 ① 길이 10 이상 +1 · ② 숫자 2개 이상 +1 · ③ 모음 비율 0.25 미만 +1 · ④ TLD `top` · `xyz` · `tk` +1 · ⑤ NXDOMAIN +2, 합이 3 이상이면 의심, `xn--` 로 시작하면 0점(한글 도메인 예외)」. 한계: 「`qwrtpzkx7v.com` 은 실제로 등록돼 NOERROR 라 2점에 그쳤다 · `bnk-secure-login.xyz` 는 사칭이라 DGA 점수 규칙으로 못 잡는다 · 12건으로 정한 문턱값은 믿기 어렵다」.

`security-agent-toolkit` 폴더에서 터미널에 입력합니다. `git status` 결과에 `.env` · `.venv` 가 없는 것을 본 뒤 나머지를 입력합니다.

```bash
git status
git add .
git commit -m "Add day 3 DNS analysis report"
git push
```

**결과** — 깃허브의 내 저장소 `network_zt` 폴더에 `day03_dns_analysis.md` 가 보이고, 열면 2~7교시 칸과 「최종 분석서」가 빈칸 없이 채워져 있습니다.

**왜** — 규칙마다 「왜 의심스러운가」를 적어야 다른 사람이 규칙을 이해하고 고칩니다. 미탐 두 건의 이유가 곧 다음에 넣을 지표입니다. `git add .` 는 `.gitignore` 에 적힌 것을 빼고 지금 폴더 아래 바뀐 것을 전부 고릅니다. 그래서 고르기 전에 `git status` 로 `.env` 가 목록에 없는지 먼저 봅니다.

**자주 틀리는 곳** — 미탐을 6-4 의 숫자로 적거나, 최종 분석서를 비운 채 올리는 경우가 많습니다. `git status` 를 건너뛰고 `git add .` 부터 하면 `.env` 가 섞여도 모릅니다. `git commit` 만 하고 `git push` 를 빠뜨리면 깃허브에 안 보입니다.

**관제에서는** — 탐지 룰 문서에 판단 기준과 한계를 함께 적어 두어야 다음 근무자가 같은 기준으로 이어서 보고, 어떤 공격은 이 룰로 안 잡히는지 팀이 압니다.

---
