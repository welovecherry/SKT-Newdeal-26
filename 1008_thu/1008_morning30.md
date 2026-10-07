# 아침 과제 7 · 명령어로 깃허브에 올리기

10월 8일 (목) · 아침 과제

**오늘 하는 일:** 어제 깃허브와 연결한 폴더에서, 파일을 **명령어로** 깃허브에 올립니다. 웹 화면에서 하나씩 올리던 것을 오늘로 끝냅니다.

오늘 새로 쓰는 명령은 **네 개**입니다 — `git config` · `git add` · `git commit` · `git push`.

**오늘 못 끝냈으면 오후 5시 이후에 마무리합니다.**

막히면 혼자 오래 붙잡지 말고 강사를 부릅니다.

---

## 1. 왜 이걸 하는지 찾아봅니다

| 질문 | 검색어 예시 |
|---|---|
| git 으로 올릴 때는 왜 `add` · `commit` · `push` 세 단계로 나눌까요? | `git add commit push 차이`, `git 커밋 이란` |

정답을 맞히는 과제가 아닙니다. **찾은 내용을 자기 말로 적는 것**이 과제입니다.

---

## 2. 이 말들이 무슨 뜻인지 찾아봅니다

| 찾아볼 말 | 무엇을 알아 오면 되나 (힌트) |
|---|---|
| commit (커밋) | 무엇을 남기는 것인가. 왜 메시지를 함께 적나 |
| push (푸시) | 내 PC 의 무엇을 어디로 보내는 것인가 |

오른쪽은 **힌트일 뿐입니다.** 뜻은 직접 찾아서 자기 말로 적습니다.

---

## 3. 터미널을 저장소 폴더에서 엽니다

1. VS Code 에서 어제 깃허브와 연결한 `security-agent-toolkit` 폴더를 엽니다.
2. 왼쪽 목록의 빈 곳을 오른쪽 클릭 › **Open in Integrated Terminal** 을 누릅니다.
3. 위치를 확인합니다.

```
$ pwd
```

결과가 `…/security-agent-toolkit` 으로 끝나면 됩니다.

---

## 4. 내 이름과 이메일을 git 에 알려 줍니다 (한 번만 세팅하면 됨. 이미 세팅한 사람은 다음으로 넘어갑니다)

git 은 올릴 때마다 **누가 올렸는지**를 함께 남깁니다. 이 PC 에서 **한 번만** 하면 됩니다.

```
$ git config --global user.name "Hong Gildong"
$ git config --global user.email "깃허브에 가입한 이메일"
```

- 따옴표 안을 자기 것으로 바꿉니다. 따옴표는 그대로 둡니다.
- ⚠ **이름은 영어로 적습니다**(예: `Hong Gildong`). 한글로 적으면 터미널 · 깃허브 기록에서 글자가 깨져 보일 수 있습니다.
- 확인합니다. 방금 적은 이름과 이메일이 나오면 됩니다.

```
$ git config --global user.name
$ git config --global user.email
```

---

## 5. 무엇이 바뀌었는지 봅니다 — `git status`

```
$ git status
```

- 빨간 글씨는 「깃허브에 아직 없는 파일 · 바뀐 파일」입니다. 어제 옮긴 파일들이 보입니다. 제목을 읽는 법은 바로 아래 5-1 에 있습니다.
- ⚠ 목록에 **`.env` 나 `.venv` 가 있으면 멈춥니다.** `.gitignore` 에 두 줄(`.env` · `.venv`)이 있는지 먼저 고칩니다. 키가 깃허브에 올라가면 지워도 기록에 남습니다.

---

## 5-1. `git status` 가 보여 주는 세 가지 상태 — untracked · tracked · staged

`git status` 의 결과는 영어 제목 아래에 파일을 나눠 보여 줍니다. 제목은 **세 가지**입니다. 이 셋만 읽을 줄 알면 「지금 무엇이 올라가고 무엇이 안 올라가는지」를 알 수 있습니다.

### 세 가지 상태

| 상태 | 읽는 법 · 뜻 | `git status` 의 제목 | 색 | 이 파일은 지금 |
|---|---|---|---|---|
| **untracked** | 언트랙트 · 추적하지 않는 | `Untracked files:` | 빨강 | git 이 **한 번도 기록한 적 없는 새 파일**입니다. 커밋에 들어가지 않습니다 |
| **tracked**, 바뀜 | 트랙트 · 추적하는 | `Changes not staged for commit:` (`modified:`) | 빨강 | 전에 커밋한 파일인데 **그 뒤에 고쳤습니다.** 고친 내용은 아직 커밋에 들어가지 않습니다 |
| **staged** | 스테이지드 · 다음 커밋에 넣기로 고른 | `Changes to be committed:` | 초록 | `git add` 로 고른 파일입니다. **다음 `git commit` 에 이 파일들만** 들어갑니다 |

- **tracked(트랙트)** 는 「git 이 이 파일을 기억하고 있다」는 뜻입니다. 한 번이라도 커밋된 파일은 모두 tracked 입니다. 9/30 부터 웹 화면으로 올린 파일도 tracked 입니다. 그 뒤에 고치면 git 이 알아채고 `modified:`(모디파이드 · 고쳐짐)로 보여 줍니다. 고치지 않았으면 `git status` 에 나오지 않습니다.
- **stage(스테이지)** 는 동사로 「다음 커밋에 넣을 파일로 고른다」는 뜻입니다. `git add` 가 바로 stage 하는 명령입니다. 고른 파일이 모여 있는 자리를 **staging area(스테이징 에어리어)** 라고 부릅니다.

### 실제 화면에서 읽어 보기

새 파일 하나, 고친 파일 하나, `git add` 한 파일 하나가 있을 때의 `git status` 입니다.

```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	new file:   docs/2026-10-08.md

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   agent_core/llm_client.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	agent_core/261007_am_report_summary.ipynb
```

| 파일 | 어느 제목 아래 | 뜻 | 지금 `git commit` 하면 |
|---|---|---|---|
| `docs/2026-10-08.md` | `Changes to be committed` | staged — `git add` 로 골랐다 | **들어간다** |
| `agent_core/llm_client.py` | `Changes not staged for commit` | tracked 인데 고쳤고, 아직 고르지 않았다 | 고친 내용은 안 들어간다 |
| `agent_core/261007_am_report_summary.ipynb` | `Untracked files` | 처음 보는 새 파일이다 | 안 들어간다 |

괄호 안의 `(use "git add <file>..." …)` 줄은 git 이 「이럴 때는 이 명령을 쓰라」고 알려 주는 안내입니다. 파일 이름이 아닙니다.

### 파일 하나가 지나가는 순서

| 순서 | 한 일 | 파일의 상태 |
|---|---|---|
| 1 | 새 파일을 만든다 | untracked (빨강) |
| 2 | `git add 파일` | staged (초록) |
| 3 | `git commit -m "…"` | tracked · 바뀐 것 없음 (`git status` 에 안 나옴) |
| 4 | 파일을 고친다 | tracked · modified (빨강) |
| 5 | `git add 파일` | staged (초록) |
| 6 | `git commit -m "…"` | tracked · 바뀐 것 없음 |

**4 → 5 가 중요합니다.** 한 번 커밋한 파일이라도, 고친 뒤에는 **다시 `git add`** 해야 그 고친 내용이 다음 커밋에 들어갑니다.

### 왜 한 번에 올리지 않고 stage 를 거칠까

- 폴더 안에는 올리면 안 되는 파일(`.env` · 연습하다 만든 파일)과 올릴 파일이 섞여 있습니다.
- `git add` 로 **올릴 것만 골라** stage 하고, 고른 것만 커밋합니다. 커밋하기 전에 `git status` 의 초록 목록으로 한 번 더 확인할 수 있습니다.
- 그래서 순서가 언제나 **`git status`(보기) → `git add`(고르기) → `git status`(초록 확인) → `git commit`(기록) → `git push`(보내기)** 입니다.

### 자주 하는 착각

| 착각 | 실제 |
|---|---|
| `git add` 하면 깃허브에 올라간다 | 아닙니다. 내 PC 안에서 고르기만 합니다. 깃허브로 보내는 것은 `git push` 입니다 |
| 한 번 `add` 한 파일은 고쳐도 자동으로 들어간다 | 아닙니다. 고친 뒤에는 다시 `git add` 합니다 (위 순서 4 → 5) |
| `.gitignore` 에 적은 파일도 빨간 글씨로 보인다 | 아닙니다. `.gitignore` 에 적은 파일은 `git status` 의 **어느 목록에도 나오지 않습니다.** `.env` 가 `Untracked files` 에 보이면 `.gitignore` 가 잘못된 것입니다 |

### 잘못 고른 파일을 빼는 법

초록 목록(`Changes to be committed`)에 올리면 안 되는 파일이 들어갔으면, **커밋하기 전에** 이렇게 뺍니다. 파일 내용은 지워지지 않고, 고른 것만 취소됩니다.

```
$ git restore --staged 파일이름
$ git status
```

그 파일이 다시 빨간 글씨로 돌아가면 된 것입니다. `.env` 가 초록에 들어갔다면 이 명령으로 빼고, `.gitignore` 를 고친 뒤 강사를 부릅니다.

---

## 6. 올릴 파일을 고릅니다 — `git add`

올릴 폴더를 이름으로 적습니다.

```
$ git add agent_core docs
$ git status
```

- 고른 파일은 **초록 글씨**로 바뀝니다. `Changes to be committed` 아래, 곧 **staged** 상태입니다(5-1).
- 초록 글씨에 `.env` 가 있으면 멈추고 강사를 부릅니다.

---

## 7. 기록을 남깁니다 — `git commit`

```
$ git commit -m "Add notebooks and outputs from 10/2 and 10/6"
```

- `-m` 뒤의 따옴표 안이 **커밋 메시지**입니다. 「무엇을 했는지」를 한 줄로 적습니다.
- 메시지는 한국어로 적어도 됩니다.

---

## 8. 깃허브로 보냅니다 — `git push`

```
$ git push
```

- **처음 한 번은 로그인 창**이 뜹니다. **Sign in with your browser** 를 누르고, 브라우저에서 깃허브에 로그인한 뒤 승인합니다.
- 끝에 `main -> main` 이 보이면 올라간 것입니다.
- 브라우저에서 내 저장소를 새로고침해 파일이 올라왔는지 확인합니다.

---

## 9. 오늘 한 것을 기록하고, 한 번 더 올립니다

`docs` 에 `2026-10-08.md` 를 만들고 아래를 채웁니다. VS Code 왼쪽 목록에서 `docs` 를 오른쪽 클릭 › **New File** 로 만듭니다.

```markdown
# 2026-10-08 (목)

## 오늘 새로 쓴 명령
git config, git add, git commit, git push

## 찾아보고 알게 된 것
add 와 commit 과 push 는

untracked · tracked · staged 는

## 막힌 것

## 다음에 확인할 것
```

이 파일도 같은 순서로 올립니다. **↑(위 화살표)** 로 앞에서 친 명령을 불러와 고쳐 쓰면 빠릅니다.

```
$ git status
$ git add docs
$ git commit -m "Add 10/8 study note"
$ git push
```

---

## 10. 확인합니다

- [ ] `git config --global user.name` 과 `user.email` 이 내 것으로 나온다
- [ ] `git add` 전에 `git status` 로 `.env` 가 없는 것을 확인했다
- [ ] `git status` 에서 내 파일이 untracked · modified · staged 중 어디에 있는지 말할 수 있다
- [ ] `git push` 로 올렸고, 브라우저의 저장소에 `agent_core` 와 `docs` 의 파일이 보인다
- [ ] `docs/2026-10-08.md` 도 같은 순서로 한 번 더 올렸다

앞으로 산출물은 **이 순서(`status` → `add` → `commit` → `push`)** 로 올립니다. 웹 화면에서 올리지 않습니다.

---

## ⭐ 다 한 사람만 합니다

```
$ git log --oneline
```

맨 위 두 줄이 오늘 내가 만든 커밋입니다. 그 아래는 9/30 부터 웹에서 올린 기록입니다.
