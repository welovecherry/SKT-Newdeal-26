# 10/14(수) 오후 · DNS 로 보는 공격 · 의심 도메인 판별 규칙 · 3일 차 보고서 — 실습

> **강사용 · 학생에게 나눠 주지 않습니다.** 모든 문제 바로 아래에 「정답」과 해설이 있습니다. 찾아 쓰기 표는 채워 두었습니다.
>
> **수업 전에 확인할 것**
> 1. 의심 도메인은 수업용으로 지어낸 이름 — 접속하지 않고 `nslookup` 으로 있는지만 본다
> 2. 점수 · 문턱값 표는 코드로 실행해 확인한 값
> 3. `python 파일.py` 실행 안내 반복

오전에 DNS 가 이름을 IP 로 바꾸는 과정을 봤습니다. 악성 코드도 똑같이 DNS 에 이름을 물어 **공격자의 서버**를 찾아갑니다. 오후에는 DNS 질의 기록(로그)에서 **수상한 도메인을 골라내는 규칙**을 직접 만들고, 그 규칙이 얼마나 잘 맞는지 재고, **판단 기준을 문서로** 남깁니다.

| 교시 | 무엇 | 쓰는 것 |
|---|---|---|
| 5교시 | 의심 도메인의 특징 — 무작위 이름(DGA) · 사칭 · NXDOMAIN 폭증 | 파이썬 |
| 6교시 | 점수 규칙 만들기 · 맞힘 · 오탐 · 미탐 재기 · 예외 목록 | 파이썬 |
| 7교시 | 3일 차 DNS 분석서 완성 — 판정표 · 판단 기준 · 한계 | 파이썬 · `nslookup` · 마크다운 |

**오늘 남기는 것:** `network_zt/day03_dns_analysis.md` 완성본. 평가 기준 「의심 도메인을 **합리적 근거**로 골랐나 · **판단 기준이 문서화**됐나」를 이 오후에 채웁니다.

---

## 시작하기

### 이 파일을 여는 법

이 파일은 **카톡으로 받은 실습 안내**입니다. 노트북이 아니라 읽으면서 따라 하는 문서입니다.

1. 카톡에서 받은 이 파일(`261014_pm_dns_suspicious.md`)을 `security-agent-toolkit` 안의 **`network_zt` 폴더**로 옮깁니다.
2. VS Code 왼쪽 목록에서 이 파일을 누르고, **`Ctrl + Shift + V`** 를 눌러 **미리보기**로 엽니다. 표 · 굵은 글씨 · 「답 보기」가 읽기 좋게 보입니다. (화면을 둘로 나눠 보려면 `Ctrl + K` 를 누른 뒤 `V`.)
3. 이 파일은 **읽기만** 합니다. 내가 적는 것은 그날 **보고서 파일**과 **`.py` 파일**입니다.
4. 코드나 명령을 복사할 때는 미리보기의 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 를 누릅니다.

### 오늘 시작할 때

0. 오늘 적는 것은 모두 **오전에 만든 `day03_dns_analysis.md` 하나에** 이어서 적습니다 — 문제 답은 `## 실습 기록`, 찾아 쓰기는 `## 찾아본 것`, 새 절은 `## 실습 기록` **위에** 붙입니다. 문제마다 「**적는 곳**」 줄을 봅니다.
1. 오전과 같은 터미널, `network_zt` 폴더에서 합니다.
2. 오늘 쓰는 의심 도메인은 **수업용으로 지어낸 이름**입니다. 실제로 접속하지 않습니다 — `nslookup` 으로 「있는지」만 봅니다(7-3).
3. 문제 앞의 **상자**를 먼저 읽습니다 — 🐍 문법 상자(파이썬) · 명령 상자(터미널) · Wireshark 상자 · 개념 상자. 문제 제목 아래 **어디서** 줄이 실습하는 곳입니다. `→` 는 하는 순서입니다. 막히면 **💡 힌트** → 맨 아래 **「정답」** 순서로 봅니다. ⭐도전은 선택입니다.

### 오늘 쓰는 DNS 로그

여러 문제에서 같은 로그를 씁니다. 문제마다 코드에 다시 적어 두었습니다.

| # | 물어본 이름 | 답(rcode) | 실제 |
|---|---|---|---|
| 1 | `www.naver.com` | NOERROR | 정상 |
| 2 | `mail.google.com` | NOERROR | 정상 |
| 3 | `update.microsoft.com` | NOERROR | 정상 |
| 4 | `e6030.a.akamaiedge.net` | NOERROR | 정상 — CDN(시디엔 · 가까운 곳에서 내용을 대신 내주는 서비스) 이름(오전 4-3) |
| 5 | `cdn.jsdelivr.net` | NOERROR | 정상 |
| 6 | `xn--3e0b707e.kr` | NOERROR | 정상 — 한글 도메인을 영문으로 바꾼 모양 |
| 7 | `kxq3vz9a.top` | **NXDOMAIN** | 의심 |
| 8 | `p0w8rk2mzq.xyz` | **NXDOMAIN** | 의심 |
| 9 | `qwrtpzkx7v.com` | NOERROR | 의심 |
| 10 | `zzx9q2lk.top` | **NXDOMAIN** | 의심 |
| 11 | `bnk-secure-login.xyz` | NOERROR | 의심 — 은행 사칭 |
| 12 | `www.example.com` | NOERROR | 정상 |

- **rcode**(알코드 · 답의 결과 코드): `NOERROR` = 답이 있었다 · `NXDOMAIN` = 그런 이름이 없다(오전 2-5).
- 「실제」 칸은 나중에 규칙이 맞았는지 채점하는 **정답지**입니다. 규칙은 이 칸을 보지 않습니다.

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">5교시 (14:00–14:50) · 의심 도메인의 특징</mark>

### 왜 필요한가

1. 악성 코드가 고정된 이름 하나만 쓰면 그 이름을 막으면 끝납니다. 그래서 공격자는 **이름을 매일 수백 개씩 자동으로 만들어** 그중 하나만 실제로 등록해 둡니다. 이것이 **DGA**(디지에이 · Domain Generation Algorithm · 도메인 생성 알고리즘)입니다.
2. 감염된 PC 는 그 이름들을 차례로 물어봅니다. 대부분 없는 이름이라 **NXDOMAIN 이 쏟아집니다.**
3. 또 하나는 **사칭**입니다 — `naver.com` 을 `nav3r.com` 처럼 비슷하게 만들어 사람을 속입니다(타이포스쿼팅 · typosquatting).

### 5.1 의심 도메인을 가르는 지표

| 특징 | 정상 도메인 | DGA 도메인 | 왜 |
|---|---|---|---|
| 이름의 길이 | 짧고 뜻이 있다 — `naver` | 길고 뜻이 없다 — `p0w8rk2mzq` | 기계가 만든 글자 줄 |
| 숫자 | 거의 없다 | 여러 개 섞여 있다 | 무작위로 뽑으니 숫자도 섞인다 |
| 모음(a · e · i · o · u) | 사람이 읽을 수 있게 섞여 있다 | **거의 없다** — `kxq3vz9a` | 발음할 수 없는 이름 |
| TLD(티엘디 · 맨 끝 이름) | `.com` · `.net` · `.kr` | 값싼 `.top` · `.xyz` · `.tk` 가 많다 | 한꺼번에 싸게 등록 |
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

### ✍️ 문제 5-1 · 무엇이 보일까요

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 실행하지 않고 머리로 예상합니다

아래 코드를 실행하면 무엇이 보일지 적어 보세요.

```python
name = "p0w8rk2mzq.xyz"
parts = name.split(".")
label = parts[-2]
vowels = 0
for ch in label:
    if ch in "aeiou":
        vowels = vowels + 1
print(label, len(label), vowels)
```

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답</mark>

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `p0w8rk2mzq 10 0`</mark>

**왜** — `parts[-2]` 는 TLD(`xyz`) 바로 앞 조각 `p0w8rk2mzq` 입니다. 열 글자인데 모음이 하나도 없습니다 — 사람이 지은 이름에서는 드문 DGA 의 특징입니다.

**자주 틀리는 곳** — `parts[-1]` 과 헷갈려 `xyz 3 0` 으로 적거나, 숫자 `0` 을 모음 `o` 로 잘못 세는 경우가 많습니다.

**관제에서는** — 로그에서 길이와 모음 수만 뽑아 봐도 사람이 지은 이름과 기계가 만든 이름이 먼저 갈립니다.

**강사 메모** — 칠판에 `p0w8rk2mzq` 를 한 자씩 적고 숫자 `0` 과 모음 `o` 를 짚어 구분해 줍니다. 「왜 `parts[-2]` 인가요?」 라는 질문에는 「`[-1]` 은 TLD `xyz` 이고, 그 바로 앞 조각이 실제로 등록한 이름이라서」 라고 답합니다. 답을 맞힌 뒤 「`naver` 는 모음이 몇 개일까요?」(2개) 를 물어 정상 이름과 비교하게 합니다.

---

### ✍️ 문제 5-2 · 볼 조각 꺼내기 (`label.py`)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — VS Code 에서 `label.py` 만들기 → 터미널에서 `python label.py` 실행

이름마다 **TLD 바로 앞 조각**과 **TLD** 를 꺼내 출력하시오.

```python
# ── 강사용: 정답을 채운 코드입니다 ──
names = ["www.naver.com", "e6030.a.akamaiedge.net", "kxq3vz9a.top", "bnk-secure-login.xyz"]

for name in names:                                # 이름을 하나씩
    parts = name.split(".")                       # 점으로 나눈 조각들
    # 1. label 에 parts 의 끝에서 둘째(-2)를, tld 에 맨 끝(-1)을 담으세요
    label = parts[-2]                             # TLD 앞 조각
    tld = parts[-1]                               # TLD
    print(name, "조각:", label, "TLD:", tld)
```

**파일을 만들고 실행합니다**

1. VS Code 왼쪽 목록에서 `network_zt` 폴더를 오른쪽 클릭 › **New File** › 이름 `label.py` 를 입력하고 Enter 를 누릅니다.
2. 위 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 로 복사해 파일에 붙여 넣은 뒤, 번호 주석 아래를 채웁니다. 저장은 자동입니다.
3. 터미널에 아래 명령을 입력합니다. 터미널의 줄 위에 `…/network_zt` 가 보여야 합니다. 아니면 먼저 `cd network_zt` 를 입력합니다.

```bash
python label.py
```

4. 고친 뒤에는 같은 명령을 다시 입력합니다. 터미널에서 **↑(위 화살표)** 를 누르면 방금 입력한 명령이 다시 나옵니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `www.naver.com … 조각: naver … TLD: com` · `e6030.a.akamaiedge.net … 조각: akamaiedge … TLD: net` · `kxq3vz9a.top … 조각: kxq3vz9a … TLD: top` · `bnk-secure-login.xyz … 조각: bnk-secure-login … TLD: xyz` |

**💡 힌트**

1. 끝에서부터는 `[-1]` · `[-2]` 입니다(오전 3교시 문법 상자).
2. 출력 줄은 미리 채워 두었습니다. `label` · `tld` 두 변수만 만들면 됩니다.
3. `e6030` 이 아니라 `akamaiedge` 를 보는 이유는 5.1 표 아래에 있습니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 5-2</mark>

(코드는 위 문제 칸에 채워 두었습니다.)

💻 **터미널에 입력합니다.** `python label.py`

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `www.naver.com 조각: naver TLD: com` · `e6030.a.akamaiedge.net 조각: akamaiedge TLD: net` · `kxq3vz9a.top 조각: kxq3vz9a TLD: top` · `bnk-secure-login.xyz 조각: bnk-secure-login TLD: xyz`</mark>

**왜** — `split(".")` 로 나눈 조각 수는 이름마다 다르지만, `[-1]` · `[-2]` 처럼 끝에서 세면 TLD 와 그 앞 조각을 늘 같은 자리에서 꺼냅니다.

**자주 틀리는 곳** — `parts[1]` 처럼 앞에서 세면 `e6030.a.akamaiedge.net` 에서 `a` 가 나옵니다.

**관제에서는** — CDN 처럼 맨 앞이 무작위인 정상 이름에 속지 않도록 실제 등록된 이름인 TLD 앞 조각을 봅니다.

**강사 메모** — 조각 수가 이름마다 다르다는 점을 강조합니다 — `www.naver.com` 은 3조각, `e6030.a.akamaiedge.net` 은 4조각입니다. 「`e6030` 도 무작위처럼 보이는데 왜 안 보나요?」 라는 질문에는 「맨 앞 조각은 정상 서비스도 마음대로 붙이므로, 등록한 이름인 TLD 앞 조각을 본다」 고 답합니다. 학생 화면에서 `조각: a` 가 찍혔다면 `parts[1]` 로 앞에서 센 것입니다.

---

### ✍️ 문제 5-3 · 숫자 수와 모음 비율 (`features.py`)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — VS Code 에서 `features.py` 만들기 → 터미널에서 `python features.py` 실행

TLD 앞 조각의 **숫자 개수**와 **모음 비율**(모음 수 ÷ 길이)을 계산하는 함수를 완성하시오.

```python
# ── 강사용: 정답을 채운 코드입니다 ──
def features(name):                               # 이름 하나의 특징을 사전으로 돌려준다
    label = name.split(".")[-2]                   # TLD 앞 조각
    digits = 0
    vowels = 0
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

**파일을 만들고 실행합니다**

1. VS Code 왼쪽 목록에서 `network_zt` 폴더를 오른쪽 클릭 › **New File** › 이름 `features.py` 를 입력하고 Enter 를 누릅니다.
2. 위 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 로 복사해 파일에 붙여 넣은 뒤, 번호 주석 아래를 채웁니다. 저장은 자동입니다.
3. 터미널에 아래 명령을 입력합니다. 터미널의 줄 위에 `…/network_zt` 가 보여야 합니다. 아니면 먼저 `cd network_zt` 를 입력합니다.

```bash
python features.py
```

4. 고친 뒤에는 같은 명령을 다시 입력합니다. 터미널에서 **↑(위 화살표)** 를 누르면 방금 입력한 명령이 다시 나옵니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `{'label': 'naver', 'len': 5, 'digits': 0, 'vowel_ratio': 0.4}` · `{'label': 'kxq3vz9a', 'len': 8, 'digits': 2, 'vowel_ratio': 0.12}` · `{'label': 'xn--3e0b707e', 'len': 12, 'digits': 5, 'vowel_ratio': 0.17}` |

**💡 힌트**

1. 바로 위 문법 상자의 반복과 같은 모양입니다 — `if` 두 개.
2. `round(값, 2)` 는 소수 둘째 자리까지 반올림합니다(미리 채워 둔 줄).
3. 셋째 줄 `xn--3e0b707e` 는 **정상** 도메인인데 숫자가 많고 모음이 적습니다. 6교시에 다시 봅니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 5-3</mark>

(코드는 위 문제 칸에 채워 두었습니다.)

💻 **터미널에 입력합니다.** `python features.py`

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `{'label': 'naver', 'len': 5, 'digits': 0, 'vowel_ratio': 0.4}` · `{'label': 'kxq3vz9a', 'len': 8, 'digits': 2, 'vowel_ratio': 0.12}` · `{'label': 'xn--3e0b707e', 'len': 12, 'digits': 5, 'vowel_ratio': 0.17}`</mark>

**왜** — `if` 두 개가 한 자씩 숫자와 모음을 따로 셉니다. DGA 이름인 `kxq3vz9a` 는 숫자가 많고 모음 비율이 0.12 로 낮습니다.

**자주 틀리는 곳** — `if` 를 `for` 와 같은 높이로 들여 쓰면 반복이 끝난 뒤 마지막 글자 하나만 보게 되어 숫자 · 모음 수가 틀립니다.

**관제에서는** — 정상인 `xn--3e0b707e` 도 숫자가 많고 모음이 적으므로, 지표 하나만 보고 의심으로 정하지 않습니다(6교시 오탐).

**강사 메모** — 두 `if` 가 모두 `for` 안으로 들여 써졌는지를 먼저 짚습니다 — 한 글자는 숫자와 모음 중 하나이거나 둘 다 아니므로, 두 `if` 를 따로 물어도 겹치지 않습니다. 「0.12 는 1 ÷ 8 인데 왜 0.125 가 아닌가요?」 라는 질문에는 「`round(값, 2)` 는 0.125 처럼 딱 가운데인 값을 짝수 쪽으로 맞춰 0.12 를 낸다(실행해 확인한 값)」 고 답합니다. 셋째 줄 `xn--3e0b707e` 는 6-3 의 오탐으로 다시 나오니, 지금 표시만 해 두라고 말합니다.

---

### ✍️ 문제 5-4 · 사칭 도메인 찾기 (`typosquat.py`)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — VS Code 에서 `typosquat.py` 만들기 → 터미널에서 `python typosquat.py` 실행

`0` → `o`, `1` → `l`, `3` → `e` 로 바꿨을 때 **믿을 만한 도메인과 똑같아지면** 사칭으로 판정하시오.

```python
# ── 강사용: 정답을 채운 코드입니다 ──
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
```

**파일을 만들고 실행합니다**

1. VS Code 왼쪽 목록에서 `network_zt` 폴더를 오른쪽 클릭 › **New File** › 이름 `typosquat.py` 를 입력하고 Enter 를 누릅니다.
2. 위 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 로 복사해 파일에 붙여 넣은 뒤, 번호 주석 아래를 채웁니다. 저장은 자동입니다.
3. 터미널에 아래 명령을 입력합니다. 터미널의 줄 위에 `…/network_zt` 가 보여야 합니다. 아니면 먼저 `cd network_zt` 를 입력합니다.

```bash
python typosquat.py
```

4. 고친 뒤에는 같은 명령을 다시 입력합니다. 터미널에서 **↑(위 화살표)** 를 누르면 방금 입력한 명령이 다시 나옵니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `[사칭 의심] nav3r.com → naver.com 흉내` · `[정상] google.com` · `[사칭 의심] g00gle.com → google.com 흉내` · `[정상] kbstar.com` · `[모름] kb5tar.com` |

**💡 힌트**

1. `.replace("0", "o")` 를 세 번 이어 붙입니다 — `name.replace(…).replace(…).replace(…)`.
2. 2번은 `elif` 입니다.
3. `kb5tar` 는 `5 → s` 바꾸기를 넣지 않아 「모름」입니다 — 규칙은 넣은 만큼만 잡습니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 5-4</mark>

(코드는 위 문제 칸에 채워 두었습니다.)

💻 **터미널에 입력합니다.** `python typosquat.py`

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `[사칭 의심] nav3r.com → naver.com 흉내` · `[정상] google.com` · `[사칭 의심] g00gle.com → google.com 흉내` · `[정상] kbstar.com` · `[모름] kb5tar.com`</mark>

**왜** — `replace` 로 숫자를 닮은 글자로 되돌렸을 때 진짜 도메인과 같아지면 사칭입니다. `kb5tar` 는 `5 → s` 바꾸기가 없어 `[모름]` 입니다.

**자주 틀리는 곳** — `if name in TRUSTED` 보다 `plain` 검사를 먼저 두면, 진짜 `google.com` 도 바꾼 뒤 같으니 `[사칭 의심]` 으로 찍힙니다.

**관제에서는** — 우리 회사와 거래처의 진짜 도메인 목록을 두고, 비슷하게 생긴 이름이 로그에 나오면 피싱(가짜 사이트로 속이는 공격)으로 의심합니다.

**강사 메모** — `if` 와 `elif` 의 순서가 결과를 바꾼다는 점을 꼭 짚습니다. 「`kb5tar.com` 도 사칭 아닌가요?」 라는 질문에는 「맞습니다. 규칙에 `5 → s` 가 없어서 못 잡은 것이고, 규칙은 넣은 만큼만 잡는다」 고 답합니다. 시간이 남으면 `.replace("5", "s")` 를 하나 더 붙여 `kb5tar.com` 이 `[사칭 의심]` 으로 바뀌는지 직접 해 보게 합니다.

---

### ✍️ 문제 5-5 · NXDOMAIN 이 쏟아지는 PC 찾기 (`nx_count.py`)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — VS Code 에서 `nx_count.py` 만들기 → 터미널에서 `python nx_count.py` 실행

DNS 로그에서 PC 마다 **NXDOMAIN 이 몇 번인지** 세고, **3번 이상**인 PC 를 출력하시오.

```python
# ── 강사용: 정답을 채운 코드입니다 ──
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

for pc in nx:
    # 2. 횟수가 3 이상이면 「[확인 필요] 10.20.0.42 NXDOMAIN 3번」 을 출력하세요
    if nx[pc] >= 3:
        print(f"[확인 필요] {pc} NXDOMAIN {nx[pc]}번")
```

**파일을 만들고 실행합니다**

1. VS Code 왼쪽 목록에서 `network_zt` 폴더를 오른쪽 클릭 › **New File** › 이름 `nx_count.py` 를 입력하고 Enter 를 누릅니다.
2. 위 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 로 복사해 파일에 붙여 넣은 뒤, 번호 주석 아래를 채웁니다. 저장은 자동입니다.
3. 터미널에 아래 명령을 입력합니다. 터미널의 줄 위에 `…/network_zt` 가 보여야 합니다. 아니면 먼저 `cd network_zt` 를 입력합니다.

```bash
python nx_count.py
```

4. 고친 뒤에는 같은 명령을 다시 입력합니다. 터미널에서 **↑(위 화살표)** 를 누르면 방금 입력한 명령이 다시 나옵니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `[확인 필요] 10.20.0.42 NXDOMAIN 3번` 한 줄 — `10.20.0.33` 은 1번이라 오타로 본다 |

**💡 힌트**

1. 세기는 12일 5-4 의 `nx[pc] = nx.get(pc, 0) + 1` 입니다.
2. 한 번 틀린 이름은 사람의 오타일 가능성이 큽니다. **짧은 시간에 여러 번**이 신호입니다.
3. `10.20.0.42` 는 마지막에 `qwrtpzkx7v.com` 의 답을 받았습니다 — DGA 이름 가운데 **실제로 등록된 하나**를 찾아낸 것일 수 있습니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 5-5</mark>

(코드는 위 문제 칸에 채워 두었습니다.)

💻 **터미널에 입력합니다.** `python nx_count.py`

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `[확인 필요] 10.20.0.42 NXDOMAIN 3번` 한 줄</mark>

**왜** — `nx.get(pc, 0) + 1` 이 PC 마다 NXDOMAIN 횟수를 쌓습니다. `10.20.0.42` 는 3번, `10.20.0.33` 은 1번이라 문턱 3 을 넘는 PC 는 하나입니다.

**자주 틀리는 곳** — `nx[pc] = nx[pc] + 1` 로 쓰면 처음 보는 PC 에서 `KeyError` 가 납니다. 그래서 `.get(pc, 0)` 을 씁니다.

**관제에서는** — 없는 이름을 연달아 묻는 PC 는 DGA 악성 코드에 감염됐을 수 있어 그 PC 부터 확인합니다.

**강사 메모** — `.get(pc, 0)` 은 12일 5-4 에서 쓴 것이라 그 문제를 떠올리게 하고 바로 넘어갑니다. 「`qwrtpzkx7v.com` 은 NOERROR 인데 왜 더 위험한가요?」 라는 질문에는 「여러 이름 중 실제로 등록된 하나에 답이 왔다는 뜻이라 그 이름이 공격자 서버일 수 있다」 고 답합니다. 학생 화면에 `10.20.0.33` 이 찍혔다면 `>= 3` 이 아니라 `>= 1` 로 쓴 것입니다.

---

### ⭐ 도전 5-6 · 너무 긴 하위 이름 찾기 (`long_label.py`, 선택)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — VS Code 에서 `long_label.py` 만들기 → 터미널에서 `python long_label.py` 실행

DNS 질의에 데이터를 몰래 실어 보내는 **DNS 터널링**은 맨 앞 조각이 비정상적으로 깁니다. 맨 앞 조각이 **30글자 이상**인 이름을 찾으시오.

```python
# ── 강사용: 정답을 채운 코드입니다 ──
names = [
    "www.naver.com",
    "aGVsbG8gd29ybGQgdGhpcyBpcyBzZWNyZXQ.t1.example.com",
    "update.microsoft.com",
    "c2VjcmV0X3Bhc3N3b3JkX2Zvcl9hZG1pbl91c2Vy.t1.example.com",
]
# 1. 이름마다 맨 앞 조각의 길이를 재서 30 이상이면 「[터널링 의심] 길이 35 : 이름」 꼴로 출력하세요
for name in names:                                # 이름을 하나씩
    first = name.split(".")[0]                    # 맨 앞 조각
    if len(first) >= 30:                          # 비정상적으로 길면
        print("[터널링 의심] 길이", len(first), ":", name)
```

**파일을 만들고 실행합니다**

1. VS Code 왼쪽 목록에서 `network_zt` 폴더를 오른쪽 클릭 › **New File** › 이름 `long_label.py` 를 입력하고 Enter 를 누릅니다.
2. 위 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 로 복사해 파일에 붙여 넣은 뒤, 번호 주석 아래를 채웁니다. 저장은 자동입니다.
3. 터미널에 아래 명령을 입력합니다. 터미널의 줄 위에 `…/network_zt` 가 보여야 합니다. 아니면 먼저 `cd network_zt` 를 입력합니다.

```bash
python long_label.py
```

4. 고친 뒤에는 같은 명령을 다시 입력합니다. 터미널에서 **↑(위 화살표)** 를 누르면 방금 입력한 명령이 다시 나옵니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `[터널링 의심] 길이 35 : aGVsbG8…` · `[터널링 의심] 길이 40 : c2VjcmV0…` 두 줄 |

**💡 힌트**

1. 맨 앞 조각은 `name.split(".")[0]` 입니다.
2. 이 글자들은 정보를 숨기는 방식(Base64 · 베이스64)으로 바꾼 것이라 뜻 없는 글자처럼 보입니다.
3. 5.1 표의 「길이」 지표를 맨 앞 조각에 쓴 것입니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 5-6</mark>

(코드는 위 문제 칸에 채워 두었습니다.)

💻 **터미널에 입력합니다.** `python long_label.py`

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `[터널링 의심] 길이 35 : aGVsbG8…` · `[터널링 의심] 길이 40 : c2VjcmV0…` 두 줄</mark>

**왜** — `split(".")[0]` 이 맨 앞 조각을 꺼냅니다. 숨긴 데이터를 실은 조각은 35 · 40 글자로, `www` · `update` 보다 훨씬 깁니다.

**자주 틀리는 곳** — `len(name)` 으로 이름 전체 길이를 재면 뒤의 `.t1.example.com` 까지 세어 35 · 40 이 아닌 더 큰 숫자가 찍힙니다.

**관제에서는** — 한 조각이 비정상적으로 긴 질의가 같은 도메인으로 반복되면 DNS 로 정보를 빼내는 터널링을 의심합니다.

**강사 메모** — 맨 앞 조각을 보는 문제라 5-2 의 `[-2]` 와 반대 방향이라는 점을 짚어 줍니다. 「이 글자들을 풀면 뭐가 나오나요?」 라는 질문에는 「Base64 로 바꾼 글자라 풀면 뜻 있는 문장이 나오지만, 오늘은 길이만 본다」 고 답합니다. 선택 문제이므로 기본 문제를 끝낸 학생에게만 권합니다.

### 5교시 한눈에

| 의심 유형 | 지표 | 코드 |
|---|---|---|
| DGA | 길이 · 숫자 · 모음 적음 · 값싼 TLD · NXDOMAIN | `features()` |
| 사칭 | 숫자를 글자로 바꾸면 진짜와 같다 | `.replace()` 후 `in TRUSTED` |
| 감염 PC | NXDOMAIN 이 짧은 시간에 여러 번 | PC 별 세기 |
| 터널링 | 맨 앞 조각이 매우 길다 | `split(".")[0]` 길이 |

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">6교시 (15:00–15:50) · 점수 규칙 · 맞힘 · 오탐 · 미탐</mark>

### 왜 필요한가

1. 지표 하나로 판정하면 틀리기 쉽습니다. 여러 지표에 **점수**를 주고 합이 기준을 넘으면 의심으로 봅니다.
2. 어떤 규칙도 완벽하지 않습니다. **정상을 의심으로 잘못 고르는 것(오탐)**과 **의심을 놓치는 것(미탐)**을 숫자로 재야 합니다.
3. 관제 실무의 탐지 룰도 이렇게 만들고, 재고, 고칩니다. 1과목 9/29 의 탐지 룰이 이 일의 시작이었습니다.

### 6.1 점수 규칙

| 규칙 | 점수 |
|---|---|
| TLD 앞 조각 길이가 10 이상 | +1 |
| 숫자가 2개 이상 | +1 |
| 모음 비율이 0.25 미만 | +1 |
| TLD 가 `top` · `xyz` · `tk` | +1 |
| 답이 NXDOMAIN | **+2** — 가장 강한 지표 |
| **합이 3 이상이면 「의심」** | 문턱값(threshold) = 3 |

### 6.2 채점 — 맞힘 · 오탐 · 미탐

| | 실제 정상 | 실제 의심 |
|---|---|---|
| **규칙이 「의심」** | **오탐**(false positive · 정상을 의심으로) | 맞힘(true positive) |
| **규칙이 「정상」** | 맞음 | **미탐**(false negative · 의심을 놓침) |


> 학생 문서에서는 아래 표의 일부 칸이 **[찾아 쓰기]** 로 비어 있습니다. 강사용에는 채운 표를 둡니다.

| 많아지면 | 관제에 생기는 일 |
|---|---|
| 오탐 | 관제 요원이 헛걸음을 하느라 지친다 — 정상 경보를 쫓느라 진짜를 볼 시간이 줄어든다 |
| 미탐 | 공격을 놓친다 — 경보가 울리지 않으니 아무도 모른다 |

- 문턱값을 **낮추면** 미탐은 줄고 오탐은 늡니다. **높이면** 그 반대입니다(⭐6-6).

#### 🐍 문법 상자 · 다른 파일의 함수 불러 쓰기 · `if __name__ == "__main__":`

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

---

### ✍️ 문제 6-1 · 무엇이 보일까요

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 실행하지 않고 머리로 예상합니다

아래 코드를 실행하면 무엇이 보일지 적어 보세요.

```python
score = 0
label = "kxq3vz9a"
tld = "top"
rcode = "NXDOMAIN"
if len(label) >= 10:
    score = score + 1
if tld in ["top", "xyz", "tk"]:
    score = score + 1
if rcode == "NXDOMAIN":
    score = score + 2
print(score, score >= 3)
```

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답</mark>

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `3 True`</mark>

**왜** — 길이는 8 이라 0점, TLD `top` 1점, NXDOMAIN 2점입니다. 숫자 · 모음 규칙을 빼도 합이 3 이라 `score >= 3` 이 `True` 입니다.

**자주 틀리는 곳** — NXDOMAIN 을 1점으로 세어 `2 False` 로 적는 경우가 많습니다. 이 줄만 `+ 2` 입니다.

**관제에서는** — 없는 이름을 물었다는 것(NXDOMAIN)이 가장 강한 신호라서 점수를 더 크게 줍니다.

**강사 메모** — 이 코드에는 숫자 · 모음 규칙이 빠져 있다는 점을 먼저 말해 둡니다. 6-2 에서 모든 규칙을 넣으면 같은 이름이 5점이 됩니다. 「왜 NXDOMAIN 만 2점인가요?」 라는 질문에는 「정상 사용자는 없는 이름을 거의 묻지 않아서, 다른 지표보다 의심의 근거가 강하다」 고 답합니다.

---

### ✍️ 문제 6-2 · 점수 함수 만들기 (`dga_score.py`)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — VS Code 에서 `dga_score.py` 만들기 → 터미널에서 `python dga_score.py` 실행

6.1 의 규칙대로 점수와 **걸린 규칙 이름**을 돌려주는 함수를 완성하시오. 비어 있는 두 규칙만 채웁니다.

```python
# ── 강사용: 정답을 채운 코드입니다 ──
CHEAP_TLD = ["top", "xyz", "tk"]                  # 값싼 TLD


def score(name, rcode):                           # 이름과 답을 받아 점수 · 이유를 돌려준다
    parts = name.split(".")
    label = parts[-2]                             # TLD 앞 조각
    tld = parts[-1]                               # TLD
    points = 0                                    # 합계 점수
    why = []                                      # 걸린 규칙 이름
    if len(label) >= 10:                          # 규칙 ① 길이
        points = points + 1
        why.append("길이")
    digits = 0
    vowels = 0
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

**파일을 만들고 실행합니다**

1. VS Code 왼쪽 목록에서 `network_zt` 폴더를 오른쪽 클릭 › **New File** › 이름 `dga_score.py` 를 입력하고 Enter 를 누릅니다.
2. 위 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 로 복사해 파일에 붙여 넣은 뒤, 번호 주석 아래를 채웁니다. 저장은 자동입니다.
3. 터미널에 아래 명령을 입력합니다. 터미널의 줄 위에 `…/network_zt` 가 보여야 합니다. 아니면 먼저 `cd network_zt` 를 입력합니다.

```bash
python dga_score.py
```

4. 고친 뒤에는 같은 명령을 다시 입력합니다. 터미널에서 **↑(위 화살표)** 를 누르면 방금 입력한 명령이 다시 나옵니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `{'points': 0, 'why': []}` · `{'points': 5, 'why': ['숫자', '모음', 'TLD', 'NXDOMAIN']}` |

**💡 힌트**

1. 1번은 `if vowels / len(label) < 0.25:` 아래 두 줄입니다 — 위 규칙 ②와 같은 모양.
2. 2번은 2점입니다.
3. `why` 에 쌓인 이름이 7교시 보고서의 「근거」 칸이 됩니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 6-2</mark>

(코드는 위 문제 칸에 채워 두었습니다.)

💻 **터미널에 입력합니다.** `python dga_score.py`

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `{'points': 0, 'why': []}` · `{'points': 5, 'why': ['숫자', '모음', 'TLD', 'NXDOMAIN']}`</mark>

**왜** — `kxq3vz9a` 는 8글자라 길이 규칙만 빠지고, 숫자 · 모음 · TLD 각 1점에 NXDOMAIN 2점이 더해져 5점입니다. `why` 에 걸린 규칙 이름이 차례로 쌓입니다.

**자주 틀리는 곳** — NXDOMAIN 에 `points + 1` 을 써서 4점이 나오는 경우가 많습니다. 이 규칙만 2점입니다.

**관제에서는** — 점수와 함께 `why` 를 남겨야 경보를 받은 분석가가 어떤 근거로 걸렸는지 바로 봅니다.

**강사 메모** — `kxq3vz9a` 가 8글자라 길이 규칙이 빠지고 `why` 에 `'길이'` 가 없다는 점을 화면에서 같이 확인합니다. 「`why` 리스트는 왜 따로 두나요?」 라는 질문에는 「점수만 있으면 어떤 규칙에 걸렸는지 모르므로, 7교시 보고서의 근거 줄에 그대로 쓴다」 고 답합니다. 학생 화면에 4점이 나오면 NXDOMAIN 줄의 `+ 1` 부터 봅니다.

---

### ✍️ 문제 6-3 · 로그 12건 판정하기 (`judge.py`)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — VS Code 에서 `judge.py` 만들기 → 터미널에서 `python judge.py` 실행

6-2 의 `score` 를 불러와 로그 12건을 **문턱값 3** 으로 판정하시오.

```python
# ── 강사용: 정답을 채운 코드입니다 ──
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
    result = score(name, rcode)
    # 1. judged 에 result["points"] 가 THRESHOLD 이상이면 "의심", 아니면 "정상" 을 담으세요
    if result["points"] >= THRESHOLD:             # 기준을 넘으면
        judged = "의심"
    else:
        judged = "정상"
    print(name, f"{result['points']}점", judged, f"(실제 {truth})")
```

**파일을 만들고 실행합니다**

1. VS Code 왼쪽 목록에서 `network_zt` 폴더를 오른쪽 클릭 › **New File** › 이름 `judge.py` 를 입력하고 Enter 를 누릅니다.
2. 위 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 로 복사해 파일에 붙여 넣은 뒤, 번호 주석 아래를 채웁니다. 저장은 자동입니다.
3. 터미널에 아래 명령을 입력합니다. 터미널의 줄 위에 `…/network_zt` 가 보여야 합니다. 아니면 먼저 `cd network_zt` 를 입력합니다.

```bash
python judge.py
```

4. 고친 뒤에는 같은 명령을 다시 입력합니다. 터미널에서 **↑(위 화살표)** 를 누르면 방금 입력한 명령이 다시 나옵니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | 열두 줄. `xn--3e0b707e.kr 3점 의심 (실제 정상)` 과 `qwrtpzkx7v.com 2점 정상 (실제 의심)` · `bnk-secure-login.xyz 2점 정상 (실제 의심)` 이 **틀린 줄**이다 |

**💡 힌트**

1. 두 갈래 값 고르기는 `if` · `else` 로 `judged` 를 정합니다.
2. `dga_score.py` 와 같은 폴더에서 실행해야 `import` 가 됩니다.
3. 틀린 줄 세 개가 6-4 의 오탐 1 · 미탐 2 입니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 6-3</mark>

(코드는 위 문제 칸에 채워 두었습니다.)

💻 **터미널에 입력합니다.** `python judge.py`

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 열두 줄. `xn--3e0b707e.kr 3점 의심 (실제 정상)` 과 `qwrtpzkx7v.com 2점 정상 (실제 의심)` · `bnk-secure-login.xyz 2점 정상 (실제 의심)` 이 **틀린 줄**입니다.</mark>

**왜** — `result["points"] >= THRESHOLD` 한 줄이 판정을 정합니다. `qwrtpzkx7v.com` 은 실제로 등록돼 NOERROR 라 NXDOMAIN 2점을 못 받았고, `bnk-secure-login` 은 모음이 충분해 길이 · TLD 2점에 그쳤습니다.

**자주 틀리는 곳** — `>=` 대신 `>` 를 쓰면 3점인 `xn--3e0b707e.kr` 이 정상으로 바뀌어 틀린 줄 수가 달라집니다.

**관제에서는** — 규칙이 틀린 줄을 하나씩 열어 보고 왜 틀렸는지 찾는 것이 탐지 룰을 고치는 출발점입니다.

**강사 메모** — `dga_score.py` 와 `judge.py` 가 같은 폴더에 있어야 한다는 점을 실행 전에 확인시킵니다 — `ModuleNotFoundError` 가 나면 폴더가 다른 경우입니다. 「`import` 했는데 6-2 의 시험 `print` 두 줄이 같이 나와요」 라는 질문에는 「`if __name__ == "__main__":` 아래로 들여 썼는지 본다」 고 답합니다. 틀린 줄 세 개를 반 전체가 같이 찾게 한 뒤 6-4 로 넘어갑니다.

---

### ✍️ 문제 6-4 · 맞힘 · 오탐 · 미탐 세기 (`evaluate.py`)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — VS Code 에서 `evaluate.py` 만들기 → 터미널에서 `python evaluate.py` 실행

6-3 의 판정을 **정답지(실제)와 비교해** 맞힘 · 오탐 · 미탐 수를 세시오.

```python
# ── 강사용: 정답을 채운 코드입니다 ──
from dga_score import score

LOG = [
    ("www.naver.com", "NOERROR", "정상"), ("mail.google.com", "NOERROR", "정상"),
    ("update.microsoft.com", "NOERROR", "정상"), ("e6030.a.akamaiedge.net", "NOERROR", "정상"),
    ("cdn.jsdelivr.net", "NOERROR", "정상"), ("xn--3e0b707e.kr", "NOERROR", "정상"),
    ("kxq3vz9a.top", "NXDOMAIN", "의심"), ("p0w8rk2mzq.xyz", "NXDOMAIN", "의심"),
    ("qwrtpzkx7v.com", "NOERROR", "의심"), ("zzx9q2lk.top", "NXDOMAIN", "의심"),
    ("bnk-secure-login.xyz", "NOERROR", "의심"), ("www.example.com", "NOERROR", "정상"),
]
THRESHOLD = 3
hit = 0                                           # 맞힘 — 의심을 의심으로
false_alarm = 0                                   # 오탐 — 정상을 의심으로
missed = 0                                        # 미탐 — 의심을 정상으로

for name, rcode, truth in LOG:
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

**파일을 만들고 실행합니다**

1. VS Code 왼쪽 목록에서 `network_zt` 폴더를 오른쪽 클릭 › **New File** › 이름 `evaluate.py` 를 입력하고 Enter 를 누릅니다.
2. 위 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 로 복사해 파일에 붙여 넣은 뒤, 번호 주석 아래를 채웁니다. 저장은 자동입니다.
3. 터미널에 아래 명령을 입력합니다. 터미널의 줄 위에 `…/network_zt` 가 보여야 합니다. 아니면 먼저 `cd network_zt` 를 입력합니다.

```bash
python evaluate.py
```

4. 고친 뒤에는 같은 명령을 다시 입력합니다. 터미널에서 **↑(위 화살표)** 를 누르면 방금 입력한 명령이 다시 나옵니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `맞힘 3 · 오탐 1 · 미탐 2` |

**💡 힌트**

1. 세 개 모두 `and` 로 두 조건을 잇습니다.
2. `judged` 를 정하는 네 줄은 6-3 에서 쓴 것과 같아 미리 채워 두었습니다.
3. 6.2 표의 네 칸 가운데 세 칸을 세는 것입니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 6-4</mark>

(코드는 위 문제 칸에 채워 두었습니다.)

💻 **터미널에 입력합니다.** `python evaluate.py`

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `맞힘 3 · 오탐 1 · 미탐 2`</mark>

**왜** — `and` 로 판정과 실제를 함께 봅니다. 맞힘은 NXDOMAIN 세 개, 오탐은 한글 도메인 `xn--3e0b707e.kr`, 미탐은 `qwrtpzkx7v.com` · `bnk-secure-login.xyz` 입니다.

**자주 틀리는 곳** — 조건을 `judged == "의심"` 하나만 쓰면 맞힘과 오탐이 섞여 맞힘이 4 로 나옵니다.

**관제에서는** — 오탐이 많으면 분석가가 헛경보에 시간을 쓰고, 미탐이 있으면 공격을 놓치므로 둘을 따로 세어 룰을 평가합니다.

**강사 메모** — 6.2 표를 화면에 띄워 놓고 세 변수가 표의 어느 칸인지 하나씩 짚으면서 풉니다. 「표의 네 번째 칸(정상을 정상으로)은 왜 안 세나요?」 라는 질문에는 「규칙을 평가할 때 문제가 되는 것은 오탐과 미탐이라서이고, 세려면 같은 모양으로 한 줄 더 쓰면 6건이 나온다」 고 답합니다. 반에 「오탐과 미탐 중 무엇이 더 위험할까요?」 를 물어 짧게 의견을 듣습니다.

---

### ✍️ 문제 6-5 · 예외 목록으로 오탐 줄이기 (`dga_score.py` 고치기)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — VS Code 에서 앞 문제의 `dga_score.py` 열어 고치기 → 터미널에서 `python dga_score.py` 실행

오탐 `xn--3e0b707e.kr` 은 **한글 도메인**을 영문으로 바꾼 모양(퓨니코드 · Punycode)이라 무작위처럼 보입니다. `dga_score.py` 의 `score` 맨 앞에 **`xn--` 로 시작하는 조각은 0점**으로 돌려보내는 줄을 넣고, 6-4 를 다시 실행하시오.

**파일을 만들고 실행합니다**

1. 왼쪽 목록에서 앞 문제에서 만든 `dga_score.py` 를 엽니다.
2. 아래 힌트대로 `label = parts[-2]` 바로 아래에 예외 두 줄을 넣습니다. 새 코드를 붙여 넣지 않고 **있는 파일을 고칩니다.** 저장은 자동입니다.
3. 터미널에 아래 명령을 입력합니다. 터미널의 줄 위에 `…/network_zt` 가 보여야 합니다. 아니면 먼저 `cd network_zt` 를 입력합니다.

```bash
python dga_score.py
```

4. 고친 뒤에는 같은 명령을 다시 입력합니다. 터미널에서 **↑(위 화살표)** 를 누르면 방금 입력한 명령이 다시 나옵니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | 6-4 를 다시 실행하면 `맞힘 3 · 오탐 0 · 미탐 2` |

**💡 힌트**

1. 넣을 곳은 `label = parts[-2]` 바로 아래입니다.
2. `label.startswith("xn--")` 이면 `return {"points": 0, "why": ["한글 도메인 예외"]}`.
3. 예외는 **근거가 분명할 때만** 넣습니다. 예외가 많아지면 공격자가 그 틈으로 숨습니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 6-5</mark>

`dga_score.py` 의 `label = parts[-2]` 바로 아래에 두 줄을 넣습니다.

```python
CHEAP_TLD = ["top", "xyz", "tk"]                  # 값싼 TLD

def score(name, rcode):                           # 이름과 답을 받아 점수 · 이유를 돌려준다
    parts = name.split(".")
    label = parts[-2]                             # TLD 앞 조각
    if label.startswith("xn--"):                  # 한글 도메인을 영문으로 바꾼 모양이면
        return {"points": 0, "why": ["한글 도메인 예외"]}
    tld = parts[-1]                               # TLD
    points = 0                                    # 합계 점수
    why = []                                      # 걸린 규칙 이름
    if len(label) >= 10:                          # 규칙 ① 길이
        points = points + 1
        why.append("길이")
    digits = 0
    vowels = 0
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
    if rcode == "NXDOMAIN":                       # 규칙 ⑤ 없는 이름
        points = points + 2
        why.append("NXDOMAIN")
    return {"points": points, "why": why}

if __name__ == "__main__":                        # 직접 실행할 때만 시험한다
    print(score("www.naver.com", "NOERROR"))
    print(score("kxq3vz9a.top", "NXDOMAIN"))
```

💻 **터미널에 입력합니다.** 고친 뒤 `python evaluate.py` → `맞힘 3 · 오탐 0 · 미탐 2`

```bash
python dga_score.py
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 6-4 를 다시 실행하면 `맞힘 3 · 오탐 0 · 미탐 2`</mark>

**왜** — `label.startswith("xn--")` 이면 점수를 세기 전에 0점으로 돌려보내므로, 한글 도메인 하나가 오탐에서 빠집니다. 다른 이름의 점수는 그대로입니다.

**자주 틀리는 곳** — 두 줄을 `return {"points": points, …}` 바로 앞(맨 끝)에 넣으면 이미 점수를 다 센 뒤라 소용이 없습니다. `label = parts[-2]` 바로 아래에 넣습니다.

**관제에서는** — 예외는 근거가 분명한 것만 넣고 보고서에 적어 둡니다. 예외가 늘면 공격자가 그 틈으로 숨습니다.

**강사 메모** — 고친 뒤 `python dga_score.py` 의 출력은 그대로이고, 숫자가 바뀌는 것은 `python evaluate.py` 라는 점을 분명히 말해 줍니다. 「예외를 넣으면 공격자가 `xn--` 로 시작하는 이름을 쓰면 되지 않나요?」 라는 질문에는 「그렇다. 그래서 예외는 근거와 함께 보고서에 적고 따로 점검한다」 고 답합니다. 학생 화면에서 오탐이 여전히 1 이면 두 줄을 넣은 위치부터 봅니다.

---

### ⭐ 도전 6-6 · 문턱값을 바꾸면 (`threshold.py`, 선택)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — VS Code 에서 `threshold.py` 만들기 → 터미널에서 `python threshold.py` 실행

6-5 를 고친 `score` 로 문턱값 **2 · 3 · 4** 마다 맞힘 · 오탐 · 미탐을 세어 표로 출력하시오.

```python
# ── 강사용: 정답을 채운 코드입니다 ──
from dga_score import score

LOG = [
    ("www.naver.com", "NOERROR", "정상"), ("mail.google.com", "NOERROR", "정상"),
    ("update.microsoft.com", "NOERROR", "정상"), ("e6030.a.akamaiedge.net", "NOERROR", "정상"),
    ("cdn.jsdelivr.net", "NOERROR", "정상"), ("xn--3e0b707e.kr", "NOERROR", "정상"),
    ("kxq3vz9a.top", "NXDOMAIN", "의심"), ("p0w8rk2mzq.xyz", "NXDOMAIN", "의심"),
    ("qwrtpzkx7v.com", "NOERROR", "의심"), ("zzx9q2lk.top", "NXDOMAIN", "의심"),
    ("bnk-secure-login.xyz", "NOERROR", "의심"), ("www.example.com", "NOERROR", "정상"),
]
print("| 문턱값 | 맞힘 | 오탐 | 미탐 |")
print("|---|---|---|---|")
# 1. 문턱값 2, 3, 4 를 하나씩 꺼내 6-4 처럼 세고, 한 줄씩 표로 출력하세요
for threshold in [2, 3, 4]:                       # 문턱값을 하나씩
    hit = 0
    false_alarm = 0
    missed = 0
    for name, rcode, truth in LOG:
        if score(name, rcode)["points"] >= threshold:
            judged = "의심"
        else:
            judged = "정상"
        if judged == "의심" and truth == "의심":
            hit = hit + 1
        if judged == "의심" and truth == "정상":
            false_alarm = false_alarm + 1
        if judged == "정상" and truth == "의심":
            missed = missed + 1
    print(f"| {threshold} | {hit} | {false_alarm} | {missed} |")
```

**파일을 만들고 실행합니다**

1. VS Code 왼쪽 목록에서 `network_zt` 폴더를 오른쪽 클릭 › **New File** › 이름 `threshold.py` 를 입력하고 Enter 를 누릅니다.
2. 위 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 로 복사해 파일에 붙여 넣은 뒤, 번호 주석 아래를 채웁니다. 저장은 자동입니다.
3. 터미널에 아래 명령을 입력합니다. 터미널의 줄 위에 `…/network_zt` 가 보여야 합니다. 아니면 먼저 `cd network_zt` 를 입력합니다.

```bash
python threshold.py
```

4. 고친 뒤에는 같은 명령을 다시 입력합니다. 터미널에서 **↑(위 화살표)** 를 누르면 방금 입력한 명령이 다시 나옵니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `\| 2 \| 5 \| 0 \| 0 \|` · `\| 3 \| 3 \| 0 \| 2 \|` · `\| 4 \| 3 \| 0 \| 2 \|` |

**💡 힌트**

1. 6-4 의 반복을 문턱값 반복 **안에** 넣습니다. 세는 변수는 문턱값마다 0 에서 시작합니다.
2. 예외(6-5)를 넣었기 때문에 문턱값 2 에서도 오탐이 0 입니다.
3. 오늘 데이터에서는 2 가 가장 좋아 보이지만, 데이터 12건으로 정한 값은 믿기 어렵습니다 — 7교시 「한계」에 적습니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 6-6</mark>

(코드는 위 문제 칸에 채워 두었습니다.)

💻 **터미널에 입력합니다.** `python threshold.py`

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `| 2 | 5 | 0 | 0 |` · `| 3 | 3 | 0 | 2 |` · `| 4 | 3 | 0 | 2 |`</mark>

**왜** — 미탐 두 건(`qwrtpzkx7v.com` · `bnk-secure-login.xyz`)이 모두 2점이라 문턱값 2 에서만 잡힙니다. 정상 이름은 예외 덕분에 가장 높은 것이 1점(`akamaiedge`)이라 오탐은 계속 0 입니다.

**자주 틀리는 곳** — `hit = 0` 같은 세 줄을 바깥 `for` 밖에 두면 문턱값마다 숫자가 이어 쌓여 `| 3 | 8 | …` 처럼 나옵니다.

**관제에서는** — 문턱값을 낮추면 미탐은 줄고 오탐이 늘 수 있어, 더 많은 로그로 다시 재 보고 정합니다.

**강사 메모** — 문턱값 2 에서 맞힘 5 · 오탐 0 · 미탐 0 이 나오는 것은 예외를 넣은 뒤 정상 이름이 모두 0 · 1점이기 때문이라는 점을 짚습니다. 「그럼 문턱값을 2 로 바꾸면 되나요?」 라는 질문에는 「12건에서만 맞춘 값이라 다른 로그에서는 오탐이 늘 수 있다」 고 답합니다. 바깥 `for` 안에 세 변수를 0 으로 두는 줄이 있는지 학생 코드에서 먼저 봅니다.

### 6교시 한눈에

| 하려는 일 | 쓰는 것 |
|---|---|
| 지표를 점수로 | 규칙마다 `+1` · NXDOMAIN `+2` · 합 ≥ 문턱값 |
| 규칙을 재기 | 맞힘 · 오탐 · 미탐 |
| 오탐 줄이기 | 근거 있는 예외 — `xn--` |
| 문턱값 정하기 | 낮추면 미탐 ↓ 오탐 ↑ |

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">7교시 (16:00–16:50) · 3일 차 DNS 분석서 완성</mark>

### 왜 필요한가

1. 규칙을 만든 사람만 아는 규칙은 쓸 수 없습니다. **무엇을 · 왜 · 얼마나 맞았나**를 문서로 남겨야 다른 사람이 쓰고 고칩니다.
2. 강의계획서의 평가 기준이 바로 「합리적 근거」와 「판단 기준 문서화」입니다.
3. 마지막으로 판정이 맞는지 `nslookup` 으로 한 번 더 확인합니다.

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

### ✍️ 문제 7-1 · 무엇이 보일까요

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 실행하지 않고 머리로 예상합니다

아래 코드를 실행하면 무엇이 보일지 적어 보세요.

```python
result = {"points": 5, "why": ["숫자", "모음", "TLD", "NXDOMAIN"]}
print(f"| kxq3vz9a.top | {result['points']} | {', '.join(result['why'])} |")
```

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답</mark>

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `| kxq3vz9a.top | 5 | 숫자, 모음, TLD, NXDOMAIN |`</mark>

**왜** — `', '.join(...)` 이 리스트 네 개를 쉼표와 빈칸으로 이어 글자 하나로 만듭니다. 앞뒤의 `|` 덕분에 마크다운 표의 한 줄이 됩니다.

**자주 틀리는 곳** — 리스트 모양 그대로 `['숫자', '모음', …]` 이 찍힌다고 예상하는 경우가 많습니다. `join` 을 거치면 대괄호와 따옴표가 사라집니다.

**관제에서는** — 걸린 규칙 이름을 근거로 함께 적어 두어야 다른 분석가가 왜 의심인지 바로 확인합니다.

**강사 메모** — f-string 안에서 바깥은 큰따옴표, 안쪽 `', '` 와 `['points']` 는 작은따옴표를 쓴다는 점을 짚어 줍니다. 「따옴표를 둘 다 큰따옴표로 쓰면 안 되나요?」 라는 질문에는 「바깥 따옴표와 같으면 글자가 거기서 끝난 것으로 읽혀 에러가 날 수 있으니 서로 다르게 쓴다」 고 답합니다. 이 한 줄이 7-2 판정표의 한 줄과 같은 모양이라고 말하고 넘어갑니다.

---

### ✍️ 문제 7-2 · 판정표 만들기 (`report_table3.py`)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — VS Code 에서 `report_table3.py` 만들기 → 터미널에서 `python report_table3.py` 실행 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day03_dns_analysis.md` 의 **3절**

로그 12건의 **점수 · 판정 · 근거**를 마크다운 표로 출력해 보고서 3절에 붙이시오. 근거가 없으면 `-` 로 적습니다.

```python
# ── 강사용: 정답을 채운 코드입니다 ──
from dga_score import score

LOG = [
    ("www.naver.com", "NOERROR"), ("mail.google.com", "NOERROR"), ("update.microsoft.com", "NOERROR"),
    ("e6030.a.akamaiedge.net", "NOERROR"), ("cdn.jsdelivr.net", "NOERROR"), ("xn--3e0b707e.kr", "NOERROR"),
    ("kxq3vz9a.top", "NXDOMAIN"), ("p0w8rk2mzq.xyz", "NXDOMAIN"), ("qwrtpzkx7v.com", "NOERROR"),
    ("zzx9q2lk.top", "NXDOMAIN"), ("bnk-secure-login.xyz", "NOERROR"), ("www.example.com", "NOERROR"),
]
print("| 이름 | 답 | 점수 | 판정 | 근거 |")
print("|---|---|---|---|---|")

for name, rcode in LOG:
    result = score(name, rcode)
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

**파일을 만들고 실행합니다**

1. VS Code 왼쪽 목록에서 `network_zt` 폴더를 오른쪽 클릭 › **New File** › 이름 `report_table3.py` 를 입력하고 Enter 를 누릅니다.
2. 위 코드 상자 안을 마우스로 끌어 선택하고 `Ctrl + C` 로 복사해 파일에 붙여 넣은 뒤, 번호 주석 아래를 채웁니다. 저장은 자동입니다.
3. 터미널에 아래 명령을 입력합니다. 터미널의 줄 위에 `…/network_zt` 가 보여야 합니다. 아니면 먼저 `cd network_zt` 를 입력합니다.

```bash
python report_table3.py
```

4. 고친 뒤에는 같은 명령을 다시 입력합니다. 터미널에서 **↑(위 화살표)** 를 누르면 방금 입력한 명령이 다시 나옵니다.

| | |
|---|---|
| 🎯 나와야 하는 결과 | `\| www.naver.com \| NOERROR \| 0 \| 정상 \| - \|` 로 시작하는 열두 줄 — `xn--3e0b707e.kr` 은 `0 \| 정상 \| 한글 도메인 예외` |

**💡 힌트**

1. 바로 위 문법 상자의 `", ".join(…)` 입니다.
2. 비어 있는지는 `if reason == "":` 로 봅니다.
3. 6-5 를 고친 `dga_score.py` 를 불러오므로 한글 도메인은 예외로 나옵니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 7-2</mark>

(코드는 위 문제 칸에 채워 두었습니다.)

💻 **터미널에 입력합니다.** `python report_table3.py`

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — `| www.naver.com | NOERROR | 0 | 정상 | - |` 로 시작하는 열두 줄 — `xn--3e0b707e.kr` 은 `0 | 정상 | 한글 도메인 예외`</mark>

**왜** — `", ".join(result["why"])` 가 걸린 규칙을 한 칸에 이어 붙이고, 아무 규칙에도 안 걸려 빈 글자면 `-` 로 바꿉니다.

**자주 틀리는 곳** — `if result["why"] == "":` 처럼 리스트를 빈 글자와 비교하면 늘 거짓이라 `-` 가 나오지 않습니다. `join` 한 뒤의 `reason` 을 비교합니다.

**관제에서는** — 판정마다 근거가 있어야 보고서를 읽는 사람이 판정을 다시 확인할 수 있습니다.

**강사 메모** — 6-5 에서 고친 `dga_score.py` 를 불러오므로 `xn--3e0b707e.kr` 이 0점 · 한글 도메인 예외로 나와야 한다는 점을 확인합니다. 「출력을 보고서에 붙이니 표가 깨져요」 라는 질문에는 「머리 두 줄(`| 이름 | …` 과 `|---|…`)까지 함께 복사했는지 본다」 고 답합니다. 학생 화면에서 `xn--3e0b707e.kr` 이 3점으로 나오면 6-5 를 고치지 않은 파일을 불러온 것입니다.

---

### ✍️ 문제 7-3 · 판정을 `nslookup` 으로 확인하기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 터미널에서 명령 실행 → 화면을 사진으로 저장 → 보고서에 넣기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day03_dns_analysis.md` 의 `## 실습 기록` 에 사진 한 줄

규칙이 「정상」이라고 한 CDN 이름과, 지어낸 무작위 이름을 각각 물어 **있는 이름인지** 확인하시오.

```bash
nslookup e6030.a.akamaiedge.net
nslookup qzkx7wp2v.invalid
```

**사진 남기기** — 결과 화면에서 두 명령의 결과(IP 가 나온 것 · `Non-existent domain`)가 함께 보이게 잘라 `nslookup_check.png` 로 `network_zt` 폴더에 저장하고, `## 실습 기록` 에 `- 7-3: ![있는 이름 · 없는 이름](nslookup_check.png)` 한 줄을 넣으시오. 자르고 저장하는 법은 10/12 오후 7-2 와 같습니다(`Win + Shift + S`).

| | |
|---|---|
| 🎯 나와야 하는 결과 | 첫째는 IP 가 나온다(있는 이름). 둘째는 `Non-existent domain`(없는 이름) (나오는 IP 는 실행할 때마다 다를 수 있습니다) |

**💡 힌트**

1. 겉모습만으로는 둘 다 무작위처럼 보입니다. **실제로 물어보는 것**이 가장 확실한 근거입니다. `.invalid` 는 「절대 존재하지 않는 이름」으로 정해 둔 TLD 라 시험용으로 씁니다(`example.com` 은 아무 하위 이름에도 답하도록 돼 있어 쓰지 않습니다 — 실측).
2. 실무에서는 여기에 「언제 처음 등록됐나」, 「위협 정보 사이트에 올라 있나」를 더 봅니다.
3. 의심 도메인에 **브라우저로 접속하지 않습니다.** `nslookup` 은 이름만 묻고 접속하지 않습니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 7-3</mark>

💻 **터미널에 입력합니다.**

```bash
nslookup e6030.a.akamaiedge.net
nslookup qzkx7wp2v.invalid
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 첫째는 `Address` 에 IP 가 나오고(있는 이름), 둘째는 `Non-existent domain`(없는 이름)입니다. IP 는 실행할 때마다 다를 수 있습니다.</mark>

**왜** — 둘 다 겉모습은 무작위지만, `nslookup` 은 DNS 에 실제로 물어 답(NOERROR · NXDOMAIN)을 받아 옵니다. `.invalid` 는 존재하지 않도록 정해 둔 TLD 입니다.

**자주 틀리는 곳** — 확인하려고 의심 이름을 브라우저 주소창에 넣는 경우가 있습니다. 접속하지 않고 `nslookup` 으로 묻기만 합니다.

**관제에서는** — 규칙의 판정을 실제 조회 결과와 등록일 · 위협 정보 사이트로 한 번 더 확인한 뒤 차단을 정합니다.

**강사 메모** — 의심 도메인에 브라우저로 접속하지 않는다는 점을 이 문제에서 한 번 더 말합니다. 「`kxq3vz9a.top` 같은 로그의 이름을 물어보면 안 되나요?」 라는 질문에는 「수업용으로 지어낸 이름이라 결과가 정해져 있지 않으므로, 없도록 정해 둔 `.invalid` 를 쓴다」 고 답합니다. 첫째 이름의 IP 는 옆 사람과 다를 수 있다고 미리 말해 둡니다.

---

### ✍️ 문제 7-4 · 판단 기준과 한계 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 명령 없이 생각해서 → 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day03_dns_analysis.md` 의 **4절**

보고서 4절에 아래 틀을 붙여 채우시오. 코드는 쓰지 않습니다.

```markdown
## 4. 판단 기준

- TLD 앞 조각 10글자 이상 (+1) — 근거(왜 의심스러운지): 
- 숫자 2개 이상 (+1) — 근거: 
- 모음 비율 0.25 미만 (+1) — 근거: 
- 값싼 TLD — top · xyz · tk (+1) — 근거: 
- NXDOMAIN (+2) — 근거: 
- 예외 — xn-- 로 시작 (0점) — 근거: 한글 도메인을 영문으로 바꾼 모양

- 문턱값: 3 (합이 3 이상이면 의심)
- 결과: 맞힘 (  ) · 오탐 (  ) · 미탐 (  )

## 5. 한계와 다음에 할 일
- 놓친 것: (6-3 의 미탐 두 건과 이유)
- 데이터가 12건뿐이라: (한 줄)
- 더 넣고 싶은 지표: (예: 등록일 · 같은 PC 의 NXDOMAIN 횟수)
```

| | |
|---|---|
| 🎯 나와야 하는 결과 | 근거 줄이 모두 찼고, 결과 · 한계가 숫자와 함께 적혀 있다 |

**💡 힌트**

1. 근거는 5.1 표의 「왜」 칸을 내 말로 다시 씁니다.
2. 미탐 `bnk-secure-login.xyz` 는 DGA 가 아니라 **사칭**이라 이 규칙으로는 못 잡습니다 — 5-4 같은 다른 규칙이 필요합니다.
3. 한계를 숨기지 않는 것이 좋은 보고서입니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 7-4</mark>

보고서 4 · 5절의 예 — 근거: 「길이 — 사람이 지은 이름은 짧고 뜻이 있다」, 「NXDOMAIN — DGA 는 대부분 등록하지 않은 이름을 묻는다」. 결과: 맞힘 3 · 오탐 0 · 미탐 2. 한계: 「`qwrtpzkx7v.com` 은 실제로 등록돼 NOERROR 라 2점에 그쳤다 · `bnk-secure-login.xyz` 는 사칭이라 DGA 규칙으로 못 잡는다 · 12건으로 정한 문턱값은 믿기 어렵다」.

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 근거 줄이 모두 찼고, 결과 · 한계가 숫자와 함께 적혀 있습니다. 결과는 예외를 넣은 뒤 숫자인 `맞힘 3 · 오탐 0 · 미탐 2` 입니다.</mark>

**왜** — 규칙마다 「왜 의심스러운가」를 적어야 다른 사람이 규칙을 이해하고 고칩니다. 미탐 두 건의 이유가 곧 다음에 넣을 지표입니다.

**자주 틀리는 곳** — 결과 칸에 6-4 의 `오탐 1` 을 그대로 적는 경우가 많습니다. 6-5 에서 예외를 넣은 뒤라 오탐은 0 입니다.

**관제에서는** — 탐지 룰 문서에 한계를 함께 적어 두어야 어떤 공격은 이 룰로 안 잡히는지 팀이 압니다.

**강사 메모** — 결과 칸에 6-4 의 숫자가 아니라 6-5 이후 숫자(`맞힘 3 · 오탐 0 · 미탐 2`)를 적는지 돌아다니며 확인합니다. 「한계를 적으면 보고서 점수가 깎이지 않나요?」 라는 질문에는 「평가 기준이 판단 기준의 문서화라서, 무엇을 못 잡는지 적는 것이 오히려 근거가 된다」 고 답합니다. 미탐 두 건의 이유가 서로 다르다(등록된 DGA · 사칭)는 점을 반 전체에 짚어 줍니다.

---

### ✍️ 문제 7-5 · 분석서 완성하고 올리기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — 보고서 파일 마무리 → 깃허브에 올리기(웹 화면 또는 `git push`)

`day03_dns_analysis.md` 에 아래 3절을 4절 **앞에** 넣고 채운 뒤 깃허브에 올리시오.

```markdown
## 3. 의심 도메인 판정
(report_table3.py 의 표를 붙입니다)

- NXDOMAIN 이 많은 PC: (5-5 결과)
- 사칭 의심: (5-4 결과)
- nslookup 확인: (7-3 결과 두 줄)
```

| | |
|---|---|
| 🎯 나와야 하는 결과 | 깃허브의 `network_zt/day03_dns_analysis.md` 에 1~5절과 사진 두 장(`nslookup_example.png` · `nslookup_check.png`)이 모두 보인다 |

**💡 힌트**

1. 절 순서는 1 조회 결과 → 2 계층 → 3 판정 → 4 기준 → 5 한계입니다.
2. 표는 코드가 낸 것을 그대로 붙입니다.
3. 올리기는 `git add network_zt` → `git commit -m "…"` → `git push`.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 7-5</mark>

보고서를 채운 뒤, **터미널(`security-agent-toolkit` 폴더)에 입력합니다.**

```bash
git status
git add network_zt
git commit -m "Add day 3 DNS analysis"
git push
```

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 깃허브의 `network_zt/day03_dns_analysis.md` 에 1~5절과 사진 두 장(`nslookup_example.png` · `nslookup_check.png`)이 모두 보입니다.</mark>

**왜** — `git add network_zt` 가 과목 폴더의 바뀐 파일을 담고, `commit` 이 기록하고, `push` 가 깃허브로 올립니다. 그래서 `security-agent-toolkit` 폴더에서 실행합니다.

**자주 틀리는 곳** — 3절을 4절 **뒤에** 붙여 절 순서가 1 · 2 · 4 · 5 · 3 이 되는 경우가 많습니다. 3절은 4절 앞에 넣습니다.

**관제에서는** — 판정표와 판단 기준을 한 문서로 남겨 두어야 다음 근무자가 같은 기준으로 이어서 봅니다.

**강사 메모** — 명령은 `network_zt` 가 아니라 `security-agent-toolkit` 폴더에서 친다는 점을 실행 전에 확인시킵니다. 「`git push` 가 안 돼요」 라는 질문에는 「웹 화면(Add file › Upload files)으로 `day03_dns_analysis.md` 를 올려도 된다」 고 답합니다. 끝난 학생에게는 깃허브 화면에서 1~5절이 순서대로 보이는지 직접 열어 보게 합니다.

---

### ⭐ 도전 7-6 · 내가 고른 이름으로 시험하기 (선택)

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**어디서**</mark> — VS Code 에서 판정 파일의 `LOG` 고치기 → 터미널에서 실행 → 다른 점을 보고서에 적기

<mark style="background:#bbdefb; color:#1a1a1a; padding:0 4px; border-radius:3px">**적는 곳**</mark> — `day03_dns_analysis.md` 의 **5절**

평소 자주 쓰는 사이트 이름 **세 개**와, 내가 지어낸 **무작위 이름 두 개**를 `LOG` 에 더해 판정하고, 결과가 예상과 다르면 왜 그런지 보고서 5절에 한 줄 적으시오.

| | |
|---|---|
| 🎯 나와야 하는 결과 | 다섯 줄이 더해진 판정표와 「예상과 달랐던 것」 한 줄 |

**💡 힌트**

1. 지어낸 이름은 `nslookup` 으로 물어 NXDOMAIN 인지 먼저 확인하고, 그 답을 `rcode` 칸에 적습니다.
2. 짧은 무작위 이름(예: `qz7.top`)은 점수가 낮게 나올 수 있습니다 — 길이 규칙 때문입니다.
3. 결과를 보고 규칙을 고치고 싶어지면, 그 생각이 곧 「다음에 할 일」입니다.

#### <mark style="display:block; background:#fff59d; color:#1a1a1a; padding:4px 12px; border-radius:4px; text-decoration:underline">정답 7-6</mark>

자주 쓰는 이름 세 개와 지어낸 이름 두 개를 `nslookup` 으로 물어 `rcode` 를 정한 뒤 `LOG` 에 더해 7-2 를 다시 실행합니다. 예상과 다른 결과(예: 짧은 무작위 이름이 낮은 점수)를 5절에 한 줄 적습니다.

<mark style="background:#fff59d; color:#1a1a1a; text-decoration:underline; padding:0 4px; border-radius:3px">**결과** — 다섯 줄이 더해진 판정표와 「예상과 달랐던 것」 한 줄</mark>

**왜** — 같은 `score` 를 새 이름에 돌려 보면 규칙의 빈틈이 드러납니다. 예를 들어 `qz7.top` 같은 짧은 무작위 이름은 길이 · 숫자 규칙에 안 걸려 점수가 낮게 나올 수 있습니다.

**자주 틀리는 곳** — 지어낸 이름의 `rcode` 를 `nslookup` 으로 확인하지 않고 `NOERROR` 로 적으면 NXDOMAIN 2점이 빠져 판정이 달라집니다.

**관제에서는** — 실제 로그에 없던 이름으로 룰을 시험해 보는 것이 룰을 배포하기 전에 빈틈을 찾는 방법입니다.

**강사 메모** — 지어낸 이름은 먼저 `nslookup` 으로 물어 `rcode` 를 정한다는 순서를 강조합니다. 「`qz7.top` 은 NXDOMAIN 이면 몇 점인가요?」 라는 질문에는 「모음 · TLD 1점씩에 NXDOMAIN 2점이 더해져 4점으로 의심이지만, NOERROR 였다면 2점으로 정상이 된다」 고 답합니다. 선택 문제이므로 7-5 까지 올린 학생에게만 권합니다.

### 7교시 한눈에

| 보고서 절 | 무엇 | 만든 곳 |
|---|---|---|
| 1 · 2 | 조회 결과 · 계층 | 오전 |
| 3 | 의심 도메인 판정표 | 7-2 · 5-4 · 5-5 · 7-3 |
| 4 | 판단 기준 | 7-4 |
| 5 | 한계와 다음에 할 일 | 7-4 · ⭐7-6 |

---

## 오늘 마무리

| 확인 | 문제 |
|---|---|
| DGA · 사칭 · 터널링의 지표를 말할 수 있다 | 5교시 |
| 오탐과 미탐의 차이를 숫자로 설명할 수 있다 | 6-4 |
| 분석서 1~5절이 깃허브에 있다 | 7-5 |

---
