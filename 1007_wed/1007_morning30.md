# 아침 과제 6 · 내 폴더를 깃허브 저장소와 연결하기

10월 7일 (수) · 아침 과제

**오늘 하는 일:** `cd ..` 로 폴더를 오르내리는 법을 익히고, 깃허브의 `security-agent-toolkit` 저장소를 **내 PC 로 내려받아(clone)** 그 폴더에서 작업하도록 바꿉니다.

지금까지는 PC 의 폴더와 깃허브 저장소가 **따로** 있었습니다. 그래서 파일을 웹 화면에서 하나씩 올렸습니다. 오늘부터는 **깃허브와 연결된 폴더**에서 작업합니다. 명령어로 올리는 것은 다음 시간에 합니다.

**오늘 못 끝냈으면 오후 5시 이후에 마무리합니다.** 단, **7번(가상환경)은 2교시 전에** 끝내야 오늘 노트북을 실행할 수 있습니다.

막히면 혼자 오래 붙잡지 말고 강사를 부릅니다.

---

## 1. 왜 이걸 하는지 찾아봅니다

먼저 **왜 필요한지**를 직접 찾아보고 한두 줄로 적습니다.

| 질문 | 검색어 예시 |
|---|---|
| 개발자는 왜 파일을 웹에서 하나씩 올리지 않고 `git` 으로 올릴까요? | `git 이란`, `git 쓰는 이유`, `git clone 이란` |

정답을 맞히는 과제가 아닙니다. **찾은 내용을 자기 말로 적는 것**이 과제입니다.

---

## 2. 이 말들이 무슨 뜻인지 찾아봅니다

검색해서 읽고 자기 말로 한 줄씩 적습니다.

| 찾아볼 말 | 무엇을 알아 오면 되나 (힌트) |
|---|---|
| 저장소 (repository) | 깃허브에 있는 저장소와 내 PC 의 폴더는 어떤 관계인가 |
| clone (클론) | 무엇을 어디로 가져오는 명령인가 |

오른쪽은 **힌트일 뿐입니다.** 뜻은 직접 찾아서 자기 말로 적습니다.

---

## 3. `cd ..` 로 위 폴더로 올라가 봅니다

1. VS Code 에서 지금 쓰는 `security-agent-toolkit` 폴더를 엽니다.
2. 왼쪽 파일 목록에서 **`agent_core` 폴더를 오른쪽 클릭**하고 **Open in Integrated Terminal**(통합 터미널에서 열기)을 누릅니다.
3. 아래를 한 줄씩 입력하고, `pwd` 의 결과가 어떻게 바뀌는지 봅니다.

```
$ pwd
$ cd ..
$ pwd
$ cd agent_core
$ cd ../..
$ pwd
```

| 명령 | 뜻 |
|---|---|
| `cd ..` | 한 칸 위 폴더로 갑니다 |
| `cd ../..` | 두 칸 위 폴더로 갑니다 |

마지막 `pwd` 의 결과를 **메모장에 적어 둡니다.** `security-agent-toolkit` 폴더가 들어 있는 곳입니다. 예를 들면 `/c/Users/이름/Documents` 입니다(사람마다 다릅니다). 5번에서 씁니다.

---

## 4. 내 이름과 이메일을 git 에 알려 줍니다

git 은 파일을 올릴 때마다 **누가 올렸는지**를 함께 남깁니다. 그래서 이름과 이메일을 한 번 적어 둡니다. 이 PC 에서 **한 번만** 하면 됩니다.

```
$ git config --global user.name "내 이름"
$ git config --global user.email "깃허브에 가입한 이메일"
```

- 따옴표 안을 자기 것으로 바꿉니다. 따옴표는 그대로 둡니다.
- 확인합니다. 방금 적은 이름과 이메일이 나오면 됩니다.

```
$ git config --global user.name
$ git config --global user.email
```

---

## 5. 지금 쓰던 폴더를 보관용으로 이름을 바꿉니다

지금 폴더는 **지우지 않습니다.** 이름만 바꿔서 보관합니다. 6번에서 같은 이름의 새 폴더를 받기 때문입니다.

1. VS Code 에서 **File › Close Folder**(파일 › 폴더 닫기)를 누릅니다. 폴더가 열려 있으면 이름을 바꿀 수 없습니다.
2. **Terminal › New Terminal** 로 터미널을 엽니다.
3. 3번에서 적어 둔 곳으로 이동합니다. `cd` 뒤에 적어 둔 경로를 그대로 붙입니다.

```
$ cd /c/Users/이름/Documents
$ ls
```

목록에 `security-agent-toolkit` 이 보이면 됩니다.

4. 이름을 바꿉니다.

```
$ mv security-agent-toolkit security-agent-toolkit_old
$ ls
```

목록에 `security-agent-toolkit_old` 가 보이면 됩니다.

`Device or resource busy` 또는 `Permission denied` 가 나오면 그 폴더를 쓰는 창이 남아 있는 것입니다. VS Code 를 **완전히 닫고** 다시 연 뒤 2번부터 다시 합니다.

---

## 6. 깃허브 저장소를 내려받습니다 (clone)

1. 브라우저에서 내 저장소 `security-agent-toolkit` 을 엽니다.
2. 초록색 **Code** 버튼을 누르고, **HTTPS** 탭의 주소 옆 복사 버튼을 누릅니다. 주소는 이런 모양입니다.

```
https://github.com/내아이디/security-agent-toolkit.git
```

3. 터미널에 `git clone` 뒤에 복사한 주소를 붙여 넣습니다. 터미널에 붙여 넣기는 **마우스 오른쪽 클릭** 또는 `Ctrl+Shift+V` 입니다.

```
$ git clone https://github.com/내아이디/security-agent-toolkit.git
$ ls
```

목록에 `security-agent-toolkit` 과 `security-agent-toolkit_old` 가 **둘 다** 보이면 됩니다.

4. 새 폴더로 들어가 안을 봅니다.

```
$ cd security-agent-toolkit
$ ls -a
```

`.git` 이라는 폴더가 보이면 **깃허브와 연결된 폴더**입니다. 웹에서 올린 파일들도 보입니다.

---

## 7. 필요한 파일을 옮기고, 가상환경을 다시 만듭니다

### ① 키 파일과 `.gitignore` 를 옮깁니다

`.env` 는 깃허브에 올리지 않았으므로 새 폴더에 없습니다. 보관 폴더에서 복사해 옵니다.

```
$ cp ../security-agent-toolkit_old/.env .
$ cp ../security-agent-toolkit_old/.gitignore .
$ ls -a
```

| 명령 | 뜻 |
|---|---|
| `cp 원래파일 옮길곳` | 파일을 복사합니다 |
| 맨 끝의 `.` | 「지금 이 폴더」입니다 |

`.gitignore` 가 없다고 나오면 10/6 아침 과제의 6번을 새 폴더에서 다시 합니다.

### ② `.gitignore` 에 한 줄을 더합니다

1. VS Code 에서 **File › Open Folder** 로 **새** `security-agent-toolkit` 폴더를 엽니다. `_old` 가 아닙니다.
2. 왼쪽 목록에서 `.gitignore` 를 열고, 맨 아래에 한 줄을 더해 두 줄로 만듭니다.

```
.env
.venv
```

`.venv` 는 가상환경 폴더입니다. 크고, 사람마다 달라서 깃허브에 올리지 않습니다.

### ③ 가상환경을 새 폴더에 다시 만듭니다

가상환경은 9/30 에 **예전 폴더 안에** 만들었습니다. 새 폴더에서는 다시 만들어야 합니다.

1. 왼쪽 목록에서 `agent_core` 안의 노트북 하나를 엽니다.
2. 오른쪽 위 **Select Kernel**(커널 선택) › **Create Python Environment** › **Venv** 를 고릅니다. 파이썬 버전을 물으면 목록 맨 위의 것을 고릅니다.
3. 새로 만든 가상환경이 커널로 선택된 것을 확인합니다.
4. 새 코드 셀에 아래 줄을 입력하고 실행합니다.

```python
%pip install requests flask schedule
```

5. 설치가 끝나면 그 셀을 지웁니다.

### ④ 아직 웹에 올리지 않은 파일을 옮깁니다

보관 폴더의 `agent_core` 에만 있는 파일이 있으면 새 폴더의 `agent_core` 로 복사합니다. 터미널이 새 `security-agent-toolkit` 폴더에 있어야 합니다.

```
$ cp -r ../security-agent-toolkit_old/agent_core/* agent_core/
$ ls agent_core
```

`-r` 은 폴더 안의 것까지 모두 복사한다는 뜻입니다. `docs` 폴더도 같은 방법으로 옮깁니다.

---

## 8. 연결된 폴더인지 확인합니다

터미널이 새 `security-agent-toolkit` 폴더에 있는지 `pwd` 로 본 뒤 입력합니다.

```
$ git status
```

- 목록에 **`.env` 와 `.venv` 가 없어야** 합니다. 있으면 7번 ②의 `.gitignore` 를 다시 확인합니다.
- 4번에서 옮긴 파일들은 빨간 글씨로 보입니다. 「아직 깃허브에 올리지 않은 파일」이라는 뜻입니다. 올리는 것은 다음 시간에 합니다.

---

## 9. 오늘 한 것을 파일로 남깁니다

새 폴더의 `docs` 에 `2026-10-07.md` 를 만들고 아래를 채웁니다. VS Code 왼쪽 목록에서 `docs` 를 오른쪽 클릭 › **New File** 로 만듭니다.

```markdown
# 2026-10-07 (수)

## 오늘 새로 쓴 명령
cd .., cd ../.., git config, mv, git clone, cp, git status

## 찾아보고 알게 된 것
저장소와 내 폴더는

## 막힌 것

## 다음에 확인할 것
```

---

## 10. 확인합니다

- [ ] `cd ..` 와 `cd ../..` 로 위 폴더로 올라가 봤다
- [ ] `git config --global user.name` 과 `user.email` 이 내 것으로 나온다
- [ ] 예전 폴더는 `security-agent-toolkit_old` 로 남아 있다
- [ ] 새 `security-agent-toolkit` 폴더 안에 `.git` 이 있다
- [ ] 새 폴더에 `.env` 가 있고, `.gitignore` 에 `.env` 와 `.venv` 두 줄이 있다
- [ ] 새 폴더의 가상환경을 커널로 골라 `%pip install` 을 마쳤다
- [ ] `git status` 목록에 `.env` 와 `.venv` 가 없다

예전 폴더(`_old`)는 일주일쯤 두고, 새 폴더에 빠진 것이 없으면 그때 지웁니다.

---

## ⭐ 다 한 사람만 합니다

새 폴더에서 아래를 입력해 봅니다.

```
$ git log --oneline
```

9/30 부터 웹에서 올린 기록이 한 줄씩 보입니다. 맨 위가 가장 최근입니다. 웹에서 올린 것도 git 기록으로 남아 있었다는 뜻입니다.
