# 아침 과제 6 · 내 폴더를 깃허브 저장소와 연결하기

10월 7일 (수) · 아침 과제

**오늘 하는 일:** 지금 쓰는 `security-agent-toolkit` 폴더를 **그 자리에서 그대로** 깃허브 저장소와 연결합니다. 내려받기(clone)도, 폴더 옮기기도 하지 않습니다.

지금까지는 PC 의 폴더와 깃허브 저장소가 **따로** 있었습니다. 그래서 파일을 웹 화면에서 하나씩 올렸습니다. 오늘부터는 **깃허브와 연결된 폴더**에서 작업합니다.

오늘은 **명령 여섯 줄을 위에서부터 한 줄씩 붙여 넣습니다.** 뜻은 표로 봅니다. 외울 필요는 없습니다.

**지금 쓰는 폴더는 그대로 씁니다.** `.env` · 가상환경 · 아직 올리지 않은 파일을 **옮기거나 다시 만들 일이 없습니다.**

**아침에는 3번부터 시작합니다.** 1 · 2번 「찾아보기」는 오후 5시 이후 기록 파일(8번)을 쓸 때 합니다. 아침 시간은 **7번까지 2교시 전에** 끝내는 데 씁니다.

막히면 혼자 오래 붙잡지 말고 강사를 부릅니다.

---

## 1. 왜 이걸 하는지 찾아봅니다 (오후에)

먼저 **왜 필요한지**를 직접 찾아보고 한두 줄로 적습니다.

| 질문 | 검색어 예시 |
|---|---|
| 개발자는 왜 파일을 웹에서 하나씩 올리지 않고 `git` 으로 올릴까요? | `git 이란`, `git 쓰는 이유` |

정답을 맞히는 과제가 아닙니다. **찾은 내용을 자기 말로 적는 것**이 과제입니다.

---

## 2. 이 말들이 무슨 뜻인지 찾아봅니다 (오후에)

| 찾아볼 말 | 무엇을 알아 오면 되나 (힌트) |
|---|---|
| 저장소 (repository) | 깃허브에 있는 저장소와 내 PC 의 폴더는 어떤 관계인가 |
| 원격 저장소 (remote) | 내 PC 에서 보면 깃허브 저장소를 무엇이라고 부르는가 |

오른쪽은 **힌트일 뿐입니다.** 뜻은 직접 찾아서 자기 말로 적습니다.

---

## 3. `security-agent-toolkit` 폴더에서 터미널을 엽니다

1. VS Code 에서 지금 쓰는 `security-agent-toolkit` 폴더를 엽니다.
2. 왼쪽 파일 목록의 **빈 곳**(파일이 없는 아래쪽)을 오른쪽 클릭하고 **Open in Integrated Terminal**(통합 터미널에서 열기)을 누릅니다.
3. 아래를 입력합니다.

```
$ pwd
```

- 결과가 `…/security-agent-toolkit` 으로 **끝나야** 합니다. 이 자리에서 끝까지 합니다.
- `…/agent_core` 로 끝나면 `cd ..` 를 한 번 입력합니다. `cd ..` 는 한 칸 위 폴더로 가는 명령입니다.

⚠ `agent_core` 가 아니라 **`security-agent-toolkit`** 에서 합니다. 깃허브 저장소는 `agent_core` · `docs` · `.gitignore` 를 모두 담은 폴더이기 때문입니다.

---

## 4. 저장소 주소를 복사합니다

1. 브라우저에서 내 저장소 `security-agent-toolkit` 을 엽니다.
2. 초록색 **Code** 버튼을 누르고, **HTTPS** 탭의 주소 옆 복사 버튼을 누릅니다. 주소는 `https://github.com/내아이디/security-agent-toolkit.git` 모양입니다.

---

## 5. 명령 여섯 줄로 연결합니다

3번의 터미널에서 **한 줄씩** 붙여 넣고 Enter 를 누릅니다. 둘째 줄의 주소는 4번에서 복사한 내 주소로 바꿉니다. 터미널에 붙여 넣기는 **마우스 오른쪽 클릭** 또는 `Ctrl+Shift+V` 입니다.

```
$ git init -b main
$ git remote add origin https://github.com/내아이디/security-agent-toolkit.git
$ git fetch origin
$ git reset origin/main
$ git branch -u origin/main
$ git status
```

| 줄 | 하는 일 | 내 파일은 |
|---|---|---|
| `git init -b main` | 이 폴더를 git 이 기록하는 폴더로 만듭니다. 숨김 폴더 `.git` 이 생깁니다 | 그대로 |
| `git remote add origin 주소` | 연결할 깃허브 저장소의 주소를 `origin` 이라는 이름으로 등록합니다 | 그대로 |
| `git fetch origin` | 깃허브 저장소의 기록(9/30 부터 웹으로 올린 것)을 받아 옵니다 | 그대로 |
| `git reset origin/main` | 내 폴더를 그 기록에 이어 붙입니다 | **그대로** |
| `git branch -u origin/main` | 내일 `git push` 한 단어로 올릴 수 있게 짝을 정해 둡니다 | 그대로 |
| `git status` | 연결됐는지 확인합니다(7번) | 그대로 |

⚠ 넷째 줄 `git reset origin/main` 은 **적힌 그대로** 입력합니다. 뒤에 다른 말(특히 `--hard`)을 붙이면 내 파일이 깃허브에 있는 옛 파일로 덮어써집니다.

- `error: remote origin already exists` 가 나오면 둘째 줄을 이미 한 것입니다. 셋째 줄부터 이어서 합니다.
- `fatal: repository not found` 가 나오면 주소가 틀린 것입니다. 4번에서 주소를 다시 복사합니다.
- 창이 열리며 깃허브 로그인을 물으면 내 계정으로 로그인합니다.

---

## 6. `.gitignore` 에 한 줄을 더합니다

VS Code 왼쪽 목록에서 `.gitignore` 를 열고, 맨 아래에 한 줄을 더해 두 줄로 만듭니다.

```
.env
.venv
```

`.venv` 는 가상환경 폴더입니다. 크고, 사람마다 달라서 깃허브에 올리지 않습니다. 가상환경 이름이 `.venv` 가 아니면 그 이름을 적습니다.

`.gitignore` 가 없으면 10/6 아침 과제의 6번을 다시 합니다.

---

## 7. 연결된 폴더인지 확인합니다

같은 터미널에서 다시 입력합니다.

```
$ git status
```

| 보이는 것 | 뜻 |
|---|---|
| `On branch main` · `Your branch is up to date with 'origin/main'` | 깃허브 저장소와 연결됐습니다 ✅ |
| 빨간 글씨 파일 (`Untracked files`) | 아직 깃허브에 올리지 않은 파일입니다. 명령어로 올리는 것은 내일 합니다 |
| `modified:` 로 보이는 노트북 | 웹으로 올린 파일이 「바뀜」으로 보일 수 있습니다. 윈도우의 줄바꿈 표시 차이라 내용은 그대로입니다. 괜찮습니다 |

- 목록에 **`.env` 와 `.venv` 가 없어야** 합니다. 있으면 6번의 `.gitignore` 를 다시 확인합니다.
- `fatal: not a git repository` 가 나오면 `security-agent-toolkit` 이 아닌 곳에서 입력한 것입니다. 3번의 `pwd` 를 다시 확인합니다.

---

## 8. 오늘 한 것을 파일로 남깁니다

`security-agent-toolkit` 의 `docs` 에 `2026-10-07.md` 를 만들고 아래를 채웁니다. VS Code 왼쪽 목록에서 `docs` 를 오른쪽 클릭 › **New File** 로 만듭니다.

```markdown
# 2026-10-07 (수)

## 오늘 새로 쓴 명령
git init, git remote add, git fetch, git reset, git branch -u, git status

## 찾아보고 알게 된 것
저장소와 내 폴더는

## 막힌 것

## 다음에 확인할 것
```

---

## 9. 확인합니다

- [ ] `pwd` 의 결과가 `security-agent-toolkit` 으로 끝나는 곳에서 명령을 입력했다
- [ ] 여섯 줄을 순서대로 입력했고, `git reset` 뒤에 아무것도 붙이지 않았다
- [ ] `.gitignore` 에 `.env` 와 `.venv` 두 줄이 있다
- [ ] `git status` 에 `On branch main` 이 나오고, 목록에 `.env` 와 `.venv` 가 없다
- [ ] 노트북을 열면 **어제와 같은 가상환경**이 커널로 골라져 있다

---

## ⭐ 다 한 사람만 합니다

`security-agent-toolkit` 폴더에서 아래를 입력해 봅니다.

```
$ ls -a
$ git log --oneline
```

- `ls -a` 는 숨김 파일까지 보여 줍니다. `.git` 폴더가 보이면 **깃허브와 연결된 폴더**입니다.
- `git log --oneline` 은 9/30 부터 웹에서 올린 기록을 한 줄씩 보여 줍니다. 맨 위가 가장 최근입니다.
