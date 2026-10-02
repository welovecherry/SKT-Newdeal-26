# 아침 과제 4 · VS Code 에서 오늘 수업을 실행할 준비하기

10월 2일 (금) · 아침 과제

**오늘 하는 일:** VS Code 에 **확장(extension) 두 개**를 설치하고, 터미널을 **Git Bash** 로 바꾸고, 오늘 쓸 **패키지를 설치**하고, **자동완성을 끕니다**. 마지막에 오늘 노트북의 **확인 셀**을 실행합니다.

오늘 2교시부터 노트북을 VS Code 에서 실행하고, 3교시부터 명령어를 터미널에 입력합니다. **이 과제를 끝내야 수업을 따라올 수 있습니다.**

막히면 혼자 오래 붙잡지 말고 강사를 부릅니다.

---

## 1. 확장(extension) 두 개를 설치합니다

확장은 VS Code 에 기능을 더 붙이는 추가 프로그램입니다.

1. 왼쪽 세로 막대에서 **블록 네 개 모양 아이콘**을 누릅니다. (또는 `Ctrl+Shift+X`)
2. 위 검색창에 이름을 입력합니다.
3. 게시자가 **Microsoft** 인 항목의 **Install** 을 누릅니다.

| 확장 | 검색어 | 왜 설치하나 |
|---|---|---|
| **Python** | `Python` (Microsoft) | VS Code 가 내 PC 의 파이썬을 찾아 쓰게 합니다 |
| **Jupyter** | `Jupyter` (Microsoft) | 노트북(`.ipynb`)을 VS Code 에서 열고 셀을 실행하게 합니다 |

이미 설치되어 있으면 **Install** 대신 톱니바퀴가 보입니다. 그대로 두고 넘어갑니다.

---

## 2. 터미널을 Git Bash 로 바꿉니다

지금까지 배운 `ls` · `cd` 와 오늘 배울 `curl` 은 **Git Bash 에서 쓰는 명령어**입니다. VS Code 터미널이 다른 것으로 열리면 같은 명령어가 다르게 동작합니다.

1. 위 메뉴에서 **Terminal › New Terminal**(터미널 › 새 터미널)을 누릅니다.
2. 아래에 열린 창의 **첫 줄**을 봅니다.

   | 첫 줄 모양 | 지금 상태 |
   |---|---|
   | `PS C:\Users\이름>` | PowerShell 입니다. **아래 3~6 을 합니다** |
   | `이름@PC이름 MINGW64 ~` | 이미 Git Bash 입니다. 바로 「3. 패키지를 설치합니다」로 넘어갑니다 |

3. `Ctrl+Shift+P` 를 누르고 검색창에 `Select Default Profile` 을 입력합니다.
4. **Terminal: Select Default Profile** 을 누르고, 목록에서 **Git Bash** 를 고릅니다.
5. 열려 있던 터미널 창을 닫고(휴지통 모양), 터미널을 다시 엽니다.
6. 첫 줄에 `MINGW64` 가 보이는지 확인합니다.

한 번 바꾸면 다음부터는 계속 Git Bash 로 열립니다. 목록에 Git Bash 가 없으면 강사를 부릅니다.

---

## 3. 패키지를 설치합니다

방금 연 터미널에 아래 두 줄을 차례로 입력합니다. `$` 는 입력하지 않습니다.

```
$ python -m pip install flask requests schedule ipykernel
$ curl --version
```

| 패키지 | 언제 쓰나 |
|---|---|
| `flask` | 2교시 — 서버를 만듭니다 |
| `requests` | 5교시 — 서버에 요청을 보냅니다 |
| `schedule` | 7교시 — 정해진 간격마다 실행합니다 |
| `ipykernel` | VS Code 에서 노트북 셀을 실행할 때 필요합니다 |

- 첫 줄은 마지막에 `Successfully installed …` 또는 `Requirement already satisfied …` 가 나오면 됩니다.
- 둘째 줄은 `curl 8.…` 처럼 버전이 나오면 됩니다.
- `python` 을 찾을 수 없다는 메시지가 나오면 `python` 자리에 `py` 를 넣어 다시 입력합니다. 그래도 안 되면 강사를 부릅니다.

---

## 4. 자동완성을 끕니다

VS Code 는 입력하는 중에 코드를 추천하거나 대신 채워 줍니다. 공부할 때는 **직접 끝까지 입력해야 기억에 남으므로** 꺼 둡니다.

`Ctrl+,` 로 설정을 열고, 위 검색창에 아래 이름을 하나씩 입력해 바꿉니다.

| 검색어 | 바꿀 것 | 꺼지는 기능 |
|---|---|---|
| `quick suggestions` | **Editor: Quick Suggestions** 의 `other` 를 **off** 로 | 입력하는 중에 뜨는 추천 목록 |
| `suggest on trigger` | **Editor: Suggest On Trigger Characters** 체크 해제 | `.` 을 입력했을 때 뜨는 추천 목록 |
| `inline suggest` | **Editor › Inline Suggest: Enabled** 체크 해제 | 회색 글씨로 미리 채워지는 코드 |

- **Copilot(AI 가 코드를 대신 써 주는 기능)도 끕니다.** 같은 설정 검색창에 `disable ai` 를 입력하고 **Chat: Disable AI Features** 에 체크합니다. 오른쪽 아래의 Copilot 아이콘이 사라지면 꺼진 것입니다.
- 추천 목록이 필요할 때는 `Ctrl+Space` 를 누르면 그때만 나옵니다.

---

## 5. 오늘 노트북의 확인 셀을 실행합니다

1. 단톡방에서 받은 `261002_am_webhook_cli.ipynb` 를 `security-agent-toolkit` 의 **`agent_core` 폴더**에 넣습니다.
2. VS Code 에서 `security-agent-toolkit` 폴더를 열고, 왼쪽 목록에서 그 노트북을 누릅니다.
3. 맨 위 **「아침 과제 확인 셀」**의 왼쪽 ▶ 를 누릅니다.
4. 위쪽에 **Select Kernel**(커널 선택)이 나오면 **Python Environments…** 를 누르고, 목록의 **Python** 을 고릅니다.
5. 셀 아래에 `준비 완료` 가 나오면 끝입니다.

`ModuleNotFoundError` 가 나오면 3번의 설치가 다른 파이썬에 된 것입니다. 강사를 부릅니다.

---

## 6. 확인합니다

- [ ] 확장 목록에 **Python** 과 **Jupyter** 가 설치되어 있다
- [ ] VS Code 터미널 첫 줄에 `MINGW64` 가 보인다
- [ ] 터미널에서 패키지 설치가 끝났고, `curl --version` 이 버전을 출력했다
- [ ] 설정에서 자동완성 세 가지를 껐다
- [ ] 노트북의 확인 셀이 `준비 완료` 를 출력했다

오늘 기록(`docs/2026-10-02.md`)은 **오후 수업이 끝난 뒤** 씁니다.

---

## ⭐ 다 한 사람만 합니다

터미널에서 오늘 노트북이 있는 폴더로 이동해 봅니다.

```
$ cd ~/security-agent-toolkit/agent_core
$ ls
```

목록에 `261002_am_webhook_cli.ipynb` 가 보이면 됩니다. 3교시에 이 폴더에서 명령어를 입력합니다.
