# 10/20(화) 오후 · Docker ② — 내 이미지 만들기 · compose 로 서버 여러 대 · 열린 포트와 증상 읽기 — 실습

어제는 남이 만든 이미지(`nginx:1.28`)를 받아 서버를 켜고, `-v` 로 내 파일을 연결했습니다. 오늘은 세 가지를 합니다.

- **5교시**: 내 파일이 들어 있는 **내 이미지**를 직접 만든다(Dockerfile).
- **6교시**: 어제 길게 치던 옵션을 **파일 하나**에 적고 서버 두 대를 한 줄로 켠다(compose).
- **7교시**: 서버가 **어디까지 열려 있는지** 직접 재 보고, 안 될 때 나오는 **증상 세 가지**를 읽는다.

## 시작하기

**오후에 받은 파일 두 개를 `network_zt` 폴더로 옮깁니다.** VS Code 왼쪽 목록의 `network_zt` 폴더로 끌어다 놓거나, 탐색기(맥북은 Finder)로 옮깁니다.

- `day07_pm_docker_compose.md` (이 파일) — 오후 실습 안내. 읽기만 합니다.
- `day07_pm_report.md` — **오후 보고서.** 5 · 6 · 7교시 답을 여기에 적습니다.

1. **[VS Code]** 이 파일을 열고 `Ctrl + Shift + V`(맥북은 `Cmd + Shift + V`)를 누릅니다 — 왼쪽.
2. **[VS Code]** `day07_pm_report.md` 를 오른쪽 클릭 › **Open to the Side** — 오른쪽. 질문마다 `쓸 내용:` 을 보고 `답:` 뒤에 씁니다.
3. 문제는 **할 일 → 순서**대로 합니다. 순서 앞의 `[창 이름]` 이 지금 쓸 창입니다. 막히면 문서 맨 아래 「정답」을 봅니다.
4. **[터미널]** Docker Desktop 이 켜져 있는지 확인하고, 어제 켠 컨테이너가 남아 있으면 지웁니다. 아래 첫 줄이 에러 없이 표를 보여 주면 켜져 있는 것입니다. 에러가 나면 Docker Desktop 을 실행하고 **Engine running** 이 될 때까지 기다린 뒤 다시 칩니다.
   ```bash
   docker ps -a
   ```
   - `NAMES` 열의 `web` · `web-one` · `web-two` 같은 어제 컨테이너가 보이면 아래 명령으로 지웁니다. 없는 이름에는 `No such container` 가 나와도 괜찮습니다.
   - 이름이 달라도 `PORTS` 열에 `8080` 이나 `8081` 이 보이는 컨테이너는 `docker rm -f 이름` 으로 지웁니다.
   - 지운 뒤 `docker ps -a` 에 `IMAGE` 열이 `hello-world` 인 줄만 남아야 합니다.
   ```bash
   docker rm -f web web-one web-two
   ```

> 오늘도 명령은 모두 **터미널**에서 칩니다(윈도에서는 Git Bash). 어제 배운 `MSYS_NO_PATHCONV=1`(Git Bash 가 경로를 자동으로 바꾸지 못하게 끄는 설정)은 오늘 7-2 의 `broken` 명령 **한 곳에만** 붙입니다. 맥북은 붙이지 않고 칩니다. 이미지는 지우지 않습니다(`docker rmi` 를 치지 않습니다). 오늘 쓰는 `nginx:1.28` 은 어제 받았으므로 새로 받지 않습니다.

작업 폴더는 `network_zt` 안에 `day07_docker` 로 만듭니다.

```bash
pwd
```

- 결과가 `…/network_zt` 로 끝나지 않으면 `cd network_zt` 로 이동한 뒤 다시 `pwd` 를 칩니다.

```bash
mkdir -p day07_docker/site
cd day07_docker
pwd
```

- 마지막 `pwd` 가 `…/network_zt/day07_docker` 로 끝나면 됩니다. 터미널을 새로 열었다면 `network_zt` 로 이동한 뒤 `cd day07_docker` 를 다시 칩니다.

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">5교시 (14:00–14:50) · 내 이미지 만들기 (Dockerfile)</mark>

> 📨 **오늘 들어온 일**
> A사 보안 담당이 보낸 메시지: 「안내 페이지 서버를 다른 PC에도 똑같이 넘기고 싶습니다. 어제처럼 `-v` 로 폴더를 연결하면 폴더도 같이 보내야 하는데, 서버 하나만 통째로 보낼 수는 없나요?」
> - 이 교시에서 하는 일: 안내 페이지 파일이 **안에 들어 있는** 내 이미지를 만들어 서버를 켭니다. 파일을 고치면 이미지를 새로 만들어야 반영된다는 것도 확인합니다.
> - 끝나면 쓰는 것: **보고서 한 줄**(보안 담당에게 보낼 답 한 문장)

### 왜 필요한가

1. 어제 `-v` 방식은 서버를 켜려면 **서버 이미지 + 내 폴더** 두 가지가 필요했습니다. 다른 PC에 넘기려면 폴더도 같이 보내야 하고, 폴더가 빠지면 기본 화면이 나옵니다.
2. 파일을 **이미지 안에 넣어 두면** 이미지 하나만 있으면 어느 PC에서나 같은 화면이 나옵니다. 같은 환경을 재현해야 하는 관제 도구나 테스트 서버를 넘길 때 이 방식을 씁니다.
3. 이미지를 만드는 설명서가 **Dockerfile** 입니다. 5교시에서는 두 줄짜리 Dockerfile 로 시작합니다.

### 5.1 Dockerfile → build → image → run → container

```
Dockerfile (설계도)
   +-- FROM nginx:1.28                                         (바탕 이미지)
   +-- COPY site/index.html /usr/share/nginx/html/index.html   (내 파일을 이미지 안에 넣기)
   |
   | docker build
   v
이미지 my-nginx:1
   |
   | docker run
   v
컨테이너
```

- 위에서 아래로 **설계도(Dockerfile) → 이미지 → 켜진 서버(컨테이너)** 순서입니다. `FROM` 은 바탕 이미지, `COPY` 는 내 파일을 이미지 안에 넣는 줄입니다.

- **Dockerfile**(도커파일): 이미지를 어떻게 만들지 적은 글 파일. 이름은 `Dockerfile`(대문자 D, 확장자 없음)이고, 한 줄에 명령 하나를 씁니다.
- **`docker build`**(빌드): Dockerfile 을 읽어 이미지를 만드는 명령. 이미지 안에 내 파일이 들어갑니다.
- 어제 배운 이미지(읽기 전용 묶음)와 컨테이너(실행한 것)는 그대로입니다. 오늘은 **이미지를 우리가 만드는 쪽**입니다.

### 5.2 Dockerfile 두 줄의 뜻

| 줄 | 형식 | 하는 일 |
|---|---|---|
| `FROM` | `FROM 이미지:태그` | 바탕이 될 이미지를 정한다. 여기에 내 것을 더한다 |
| `COPY` | `COPY 내PC경로 이미지안경로` | 내 PC의 파일을 이미지 안으로 복사해 넣는다 |

- 이미지 안에서 nginx 가 응답하는 파일은 `/usr/share/nginx/html/index.html` 입니다. 어제 `ls` 로 본 그 파일입니다. 여기에 내 파일이 들어가면 기본 화면 대신 내 화면이 나옵니다.
- `COPY` 의 앞쪽 경로는 **Dockerfile 이 있는 폴더 기준**입니다. `site/index.html` 은 `day07_docker/site/index.html` 입니다.

### 5.3 build 명령

```bash
docker build -t my-nginx:1 .
```

| 부분 | 뜻 |
|---|---|
| `docker build` | 이미지를 만든다 |
| `-t my-nginx:1` | 만들 이미지에 `이름:태그` 를 붙인다. 이름은 내 마음대로, `:1` 은 내가 정한 버전 |
| `.` | Dockerfile 이 있는 폴더(= 지금 폴더). 마지막의 점을 빼먹으면 에러가 난다 |

### 5.4 `-v` 방식과 이미지에 넣는 방식

```
어제 (-v)
  내 PC  site-one/index.html  <==== 연결 ====>  컨테이너
  파일을 고치면 -> 서버가 바로 새 파일을 보여 준다

오늘 (이미지 안에 COPY)
  내 PC  site/index.html --COPY (build 할 때)--> 이미지 my-nginx:1 ---> 컨테이너
  파일을 고쳐도 -> 이미 만든 이미지는 그대로다
```

- 위가 어제 방식, 아래가 오늘 방식입니다. 어제는 파일을 연결해 두었고, 오늘은 build 하는 순간 파일을 복사해 이미지에 넣습니다.

| | `-v` 로 연결 | 이미지에 넣기 |
|---|---|---|
| 서버를 넘길 때 | 이미지 + 폴더 | 이미지 하나 |
| 파일을 고치면 | 새로 고침만 | 이미지를 다시 build 해야 반영 |
| 잘 맞는 때 | 자주 고치는 설정 · 페이지 | 고정해서 넘길 서버 |

### ✍️ 문제 5-1 · Dockerfile 두 줄을 써서 내 이미지 만들기

**📍 이런 상황이 있습니다**

- 보안 담당이 「안내 페이지가 들어 있는 서버를 이미지 하나로 넘겨 달라」고 합니다. 담당자는 Dockerfile 을 쓰고, 이미지를 만들고, 그 이미지로 서버를 켜서 내 화면이 나오는지 확인해야 합니다.
- 현업에서는 설정과 페이지를 이미지에 넣어 두면 어느 PC에서 켜도 같은 서버가 되고, 이미지 이름과 태그로 어느 버전인지 구분합니다.

**🎯 할 일**

1. <mark>`site/index.html`</mark> 을 만듭니다.
2. <mark>Dockerfile 두 줄</mark>(`FROM` · `COPY`)을 직접 씁니다.
3. <mark>`docker build`</mark> 로 이미지를 만들고, 그 이미지로 서버를 켜서 접속합니다.

**순서**

1. **[터미널]** 작업 폴더가 `day07_docker` 인지 확인합니다.
   ```bash
   pwd
   ```
2. **[터미널]** `site/index.html` 을 만듭니다. 아래 둘 중 **하나만** 고릅니다.
   - **vim**: `vim site/index.html` → `i` → 글 입력 → `Esc` → `:wq` Enter
   - **touch**: `touch site/index.html` → VS Code 에서 파일을 열어 글 입력

   파일 내용입니다.
   ```html
   <meta charset="utf-8">
   <h1>my-nginx v1</h1>
   <p>이미지 안에 들어 있는 페이지입니다</p>
   ```
3. **[터미널]** `Dockerfile` 을 만듭니다. 아래 둘 중 **하나만** 고릅니다.
   - **vim**: `vim Dockerfile` → `i` → 글 입력 → `Esc` → `:wq` Enter
   - **touch**: `touch Dockerfile` → VS Code 에서 파일을 열어 글 입력
4. **[vim 또는 VS Code]** `Dockerfile` 안에 **아래 뜻대로 두 줄**을 직접 씁니다. 5.2 의 형식 표를 보고 씁니다.
   - 첫 줄: 바탕 이미지는 `nginx:1.28`
   - 둘째 줄: 내 PC의 `site/index.html` 을 이미지 안의 `/usr/share/nginx/html/index.html` 로 복사
5. **[터미널]** 이미지를 만듭니다. 마지막 줄에 `naming to docker.io/library/my-nginx:1 done` 처럼 이름이 보이면 성공입니다.
   ```bash
   docker build -t my-nginx:1 .
   ```
6. **[터미널]** 만든 이미지가 목록에 있는지 봅니다. `my-nginx` 줄의 `TAG` 가 `1` 입니다.
   ```bash
   docker images
   ```
7. **[터미널]** 내 이미지로 서버를 켭니다. 어제와 달리 `-v` 가 없습니다.
   ```bash
   docker run -d --name my-web -p 8080:80 my-nginx:1
   ```
8. **[브라우저]** `http://127.0.0.1:8080` 을 엽니다. **my-nginx v1** 이 보이면 성공입니다.
9. **[보고서]** `day07_pm_report.md` 의 `## 5교시` › `### 문제 5-1` 아래를 채웁니다.
   - (가) 내가 쓴 Dockerfile 두 줄을 붙여 넣어 주세요.
   - (나) 🔍 `FROM` 과 `COPY` 가 각각 하는 일을 적어 주세요.
   - (다) 🔍 어제와 달리 `docker run` 에 `-v` 가 없는데도 내 화면이 나오는 이유는 무엇인가요?

### ✍️ 문제 5-2 · 파일을 고쳐 보고, 이미지를 다시 만들어 반영하기

**📍 이런 상황이 있습니다**

- 보안 담당이 「안내 문구를 바꿨는데 서버에서는 예전 문구가 나온다」고 합니다. 담당자는 파일을 고치고, 반영되지 않는 것을 확인하고, 이미지를 새로 만들어 반영해야 합니다.
- 현업에서는 이미지에 파일을 넣어 두는 방식에서 이 일이 흔합니다. 그래서 이미지에 `:2` 같은 새 태그를 붙여, 어느 버전이 켜져 있는지 구분합니다.

**🎯 할 일**

1. <mark>`site/index.html` 을 고치고</mark> 새로 고쳐도 반영되지 않는 것을 확인합니다.
2. <mark>`my-nginx:2`</mark> 로 이미지를 다시 만들고 서버를 바꿔 켭니다.
3. 이미지가 <mark>`1` 과 `2` 두 개</mark> 있는 것을 봅니다.

**순서**

1. **[vim 또는 VS Code]** `site/index.html` 의 `<h1>` 줄을 `<h1>my-nginx v2</h1>` 로 고쳐 저장합니다. vim 이면 `vim site/index.html` 으로 열고 `i` → 고침 → `Esc` → `:wq` 입니다.
2. **[브라우저]** `http://127.0.0.1:8080` 을 새로 고칩니다. 아직 **v1** 이 나오는 것이 정상입니다. 서버가 쓰는 파일은 이미지 안에 복사된 것이라서 내 PC의 파일을 고쳐도 바뀌지 않습니다.
3. **[터미널]** 같은 Dockerfile 로 태그만 `2` 로 바꿔 이미지를 다시 만듭니다. 이번에는 `COPY` 단계에서 새 파일이 들어갑니다.
   ```bash
   docker build -t my-nginx:2 .
   ```
4. **[터미널]** 켜져 있는 서버를 지우고 `my-nginx:2` 로 다시 켭니다.
   ```bash
   docker rm -f my-web
   docker run -d --name my-web -p 8080:80 my-nginx:2
   ```
5. **[브라우저]** `http://127.0.0.1:8080` 을 새로 고쳐 **v2** 가 나오는지 확인합니다.
6. **[터미널]** 이미지 목록과 실행 중인 목록을 봅니다. 이미지는 `my-nginx:1` 과 `my-nginx:2` 두 개가 있고, 켜진 서버는 `my-nginx:2` 를 씁니다.
   ```bash
   docker images
   docker ps
   ```
7. **[터미널]** 서버를 지웁니다. 이미지는 지우지 않습니다.
   ```bash
   docker rm -f my-web
   ```
8. **[보고서]** `### 문제 5-2` 아래를 채웁니다.
   - (가) 파일을 고친 직후 새로 고침했을 때 화면에 무엇이 나왔나요?
   - (나) 🔍 파일을 고쳤는데도 화면이 바뀌지 않은 이유와, 바꾸려면 무엇을 해야 하는지 적어 주세요.
   - (다) 🔍 어제의 `-v` 방식과 오늘의 이미지에 넣는 방식은 파일을 고쳤을 때 반영되는 방법이 어떻게 다른가요?
   - (한 줄) 보안 담당에게 보낼 답을 한 문장으로 적어 주세요.
   - 이 교시에서 새로 알게 된 것 하나를 적어 주세요.

### 5교시 한눈에

| 하려는 일 | 명령 · 파일 |
|---|---|
| 이미지 설계도 | `Dockerfile` (`FROM` 바탕 이미지 · `COPY` 내 파일 넣기) |
| 이미지 만들기 | `docker build -t 이름:태그 .` |
| 만든 이미지 보기 | `docker images` |
| 내 이미지로 서버 켜기 | `docker run -d --name 이름 -p 포트:80 이름:태그` |
| 파일을 고친 뒤 반영 | 새 태그로 다시 build → 서버 교체 |

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">6교시 (15:00–15:50) · compose 로 서버 두 대 한 줄에 켜기</mark>

> 📨 **오늘 들어온 일**
> A사 보안 담당이 보낸 메시지: 「서버를 두 대 켜려면 긴 명령을 두 번 쳐야 하고, 팀원이 옵션을 하나 빼먹으면 다르게 켜집니다. 서버 구성을 한 파일에 적어 두고 한 줄로 켜고 끌 수는 없나요?」
> - 이 교시에서 하는 일: 서버 두 대의 구성을 파일 하나(`compose.yaml`)에 적고, 한 줄로 켜고 끕니다. 설정 한 줄(환경변수)도 넣어 확인합니다.
> - 끝나면 쓰는 것: **보고서 한 줄**(보안 담당에게 보낼 답 한 문장)

### 왜 필요한가

1. 어제 서버 하나를 켜는 데 `docker run -d --name … -p … -v … 이미지` 를 쳤습니다. 서버가 늘수록 명령도 길어지고, 옵션을 빼먹는 실수도 늘어납니다.
2. 옵션을 **파일에 적어 두면** 누가 켜도 같은 구성이 됩니다. 파일을 저장소에 올려 두면 구성도 기록으로 남습니다.
3. 4과목에서 로그를 모으는 서버, 5과목에서 대응 대상 서버, 캡스톤 시연 환경을 한 번에 켜는 데 이 방식을 다시 씁니다.

### 6.1 docker run 옵션이 compose 파일 항목이 된다

```
docker run -d                      -->  docker compose up -d 가 대신 한다
  --name web-one                   -->  services: 아래의 web-one:
  -p 8080:80                       -->      ports:
                                                - "8080:80"
  -v ./site-one:/usr/share/...:ro  -->      volumes:
                                                - ./site-one:/usr/share/...:ro
  nginx:1.28                       -->      image: nginx:1.28
```

- 왼쪽이 어제 명령에 직접 친 옵션이고, 오른쪽이 오늘 파일에 적는 같은 내용입니다.

- **compose**(컴포즈)는 서버 여러 대의 구성을 파일 하나에 적어 두고 한 번에 켜고 끄는 기능입니다. 명령은 `docker compose` 입니다.
- 어제 옵션 이름과 거의 같아서 새로 외울 것은 파일 모양뿐입니다. 서버를 부르는 이름(`web-one`)은 `services:` 아래에 적습니다.

### 6.2 compose.yaml 읽는 법

```yaml
services:                      # 서버 목록의 시작
  web-one:                     # 서버 이름 (마음대로)
    image: nginx:1.28          # 쓸 이미지
    ports:                     # 포트 연결 목록
      - "8080:80"              # 내PC포트:컨테이너포트
    volumes:                   # 폴더 연결 목록
      - ./site-one:/usr/share/nginx/html:ro
```

- 이 파일 형식을 **YAML**(야믈)이라고 합니다. 규칙은 세 가지입니다.
  - **들여쓰기로 계층을 나눈다.** 이 문서는 **공백 2칸**씩 들여씁니다.
  - **탭 글자를 쓰지 않는다.** 탭이 들어가면 에러가 납니다.
  - **`-` 로 시작하는 줄은 목록의 한 항목**이고, `이름: 값` 은 이름과 값 사이에 공백이 하나 있어야 합니다.
- `./site-one` 의 `./` 는 compose.yaml 이 있는 폴더입니다. 어제는 `$(pwd)/site-one` 으로 쓰던 것을 파일에서는 이렇게 짧게 쓸 수 있고, `MSYS_NO_PATHCONV=1` 도 필요 없습니다.

### 6.3 vim 에서 탭이 공백 2칸이 되게 설정하기

vim 에서 `Tab` 키를 누르면 탭 글자가 들어가서 YAML 이 깨질 수 있습니다. 한 번만 설정해 두면 `Tab` 이 공백 2칸이 됩니다. **[터미널]** 에서 아래 한 줄을 칩니다. 한 번만 치면 되고, 두 번 치면 같은 줄이 두 번 들어갈 뿐 문제는 없습니다.

```bash
echo 'set expandtab shiftwidth=2 softtabstop=2' >> ~/.vimrc
```

- `echo '글자' >> 파일` 은 파일 맨 아래에 그 글자를 한 줄 더합니다. `~/.vimrc` 는 vim 이 시작할 때 읽는 설정 파일입니다.
- 이 설정은 vim 에서만 쓰입니다. VS Code 에서 쓰면 필요 없습니다.

### 6.4 이번 교시의 명령

| 명령 | 필요한 상황 | 달라지는 점 |
|---|---|---|
| `docker compose up -d` | 파일에 적은 서버를 모두 켜고 싶다 | 서버가 한꺼번에 켜진다 |
| `docker compose ps` | 이 파일로 켠 서버만 보고 싶다 | 서버 이름 · 상태 · 포트 |
| `docker compose logs 서버이름` | 한 서버의 접속 기록이 보고 싶다 | 그 서버의 기록만 나온다 |
| `docker compose exec 서버이름 명령` | 켜진 서버 안에서 명령을 실행하고 싶다 | 어제 `exec -it` 와 같고 서버 이름을 쓴다 |
| `docker compose down` | 서버를 모두 끄고 지우고 싶다 | `stop` + `rm` 이 한 번에 된다 |

- 이 명령들은 **compose.yaml 이 있는 폴더**(`day07_docker`)에서 칩니다. 다른 폴더에서 치면 파일을 못 찾습니다.
- 어제 `--name` 으로 붙이던 이름은 compose 에서 `services:` 아래의 **서버 이름**(`web-one`)이 됩니다.
- 켜진 컨테이너의 실제 이름은 compose 가 `폴더이름-서버이름-1`(예: `day07_docker-web-one-1`)로 붙입니다.
- 이름을 쓰는 자리가 다릅니다.
  - `docker compose logs` · `exec` 뒤에는 서버 이름(`web-two`)을 씁니다
  - `docker logs` · `docker rm` 뒤에는 컨테이너 이름(`day07_docker-web-two-1`)을 씁니다

### ✍️ 문제 6-1 · compose.yaml 에 서버 한 대를 더 적고 두 대를 한 줄로 켜기

**📍 이런 상황이 있습니다**

- 보안 담당이 「첫 번째 서버는 이미 적었으니, 두 번째 서버를 같은 방식으로 적어 달라」고 합니다. 담당자는 `compose.yaml` 에 서버를 한 대 더 쓰고, 두 서버가 한 번에 켜지는지, 각각 접속되는지, 어떤 서버의 기록인지 확인해야 합니다.
- 현업에서는 옵션을 한 서버씩 복사해 이름과 포트만 바꾸며 서버를 늘립니다.

**🎯 할 일**

1. <mark>`site-one` · `site-two` 의 `index.html`</mark> 두 파일을 만듭니다.
2. <mark>`compose.yaml`</mark> 에 두 번째 서버의 `ports` · `volumes` 4줄을 직접 씁니다.
3. <mark>`docker compose up -d`</mark> 로 두 서버를 켜고, `ps` 와 `logs` 를 읽습니다.

**순서**

1. **[터미널]** 8080 · 8081 을 쓰는 컨테이너가 남아 있지 않은지 `docker ps -a` 로 봅니다. 있으면 `docker rm -f 이름` 으로 지웁니다. 그리고 6.3 의 vim 설정 한 줄을 아직 안 쳤다면 먼저 칩니다. 이어서 두 폴더를 만듭니다(`day07_docker` 안에서).
   ```bash
   pwd
   mkdir site-one site-two
   ```
2. **[터미널]** `site-one/index.html` 을 만듭니다. 아래 둘 중 **하나만** 고릅니다.
   - **vim**: `vim site-one/index.html` → `i` → 글 입력 → `Esc` → `:wq` Enter
   - **touch**: `touch site-one/index.html` → VS Code 에서 파일을 열어 글 입력

   ```html
   <meta charset="utf-8">
   <h1>site-one</h1>
   <p>compose 의 첫 번째 서버입니다</p>
   ```
3. **[터미널]** `site-two/index.html` 도 같은 방법으로 만듭니다. 아래 둘 중 **하나만** 고릅니다.
   - **vim**: `vim site-two/index.html` → `i` → 글 입력 → `Esc` → `:wq` Enter
   - **touch**: `touch site-two/index.html` → VS Code 에서 파일을 열어 글 입력

   ```html
   <meta charset="utf-8">
   <h1>site-two</h1>
   <p>compose 의 두 번째 서버입니다</p>
   ```
4. **[터미널]** `compose.yaml` 을 만듭니다. 아래 둘 중 **하나만** 고릅니다.
   - **vim**: `vim compose.yaml` → `i` → 코드 붙여넣기 → `Esc` → `:wq` Enter (줄 앞 공백이 줄마다 밀려 있으면 `Esc` → `:q!` 로 나와서 touch 로 다시 만듭니다)
   - **touch**: `touch compose.yaml` → VS Code 에서 파일을 열어 코드 붙여넣기

   ```yaml
   services:
     web-one:
       image: nginx:1.28
       ports:
         - "8080:80"
       volumes:
         - ./site-one:/usr/share/nginx/html:ro
     web-two:
       image: nginx:1.28
       # ← ports: 항목을 쓰세요 (내 PC 8081 → 컨테이너 80)
       # ← volumes: 항목을 쓰세요 (./site-two → nginx 폴더, 읽기 전용)
   ```
5. **[vim 또는 VS Code]** `# ←` 로 시작하는 **두 줄을 지우고**, 그 자리에 `web-one` 의 `ports` · `volumes` 를 보고 **네 줄**을 직접 씁니다(`ports:` · `- "8081:80"` · `volumes:` · `- ./site-two:/usr/share/nginx/html:ro`). 칸 수는 이렇습니다.
   - `ports:` 와 `volumes:` 는 공백 4칸으로 시작합니다(`image:` 와 같은 칸)
   - 그 아래 `-` 줄은 공백 6칸으로 시작합니다
   - 쓴 뒤 `web-one` 의 같은 줄과 글자 시작 위치가 같은지 눈으로 확인합니다
6. **[터미널]** 두 서버를 한 줄로 켭니다. 에러가 나면 에러 문구의 줄 번호가 가리키는 줄의 들여쓰기를 먼저 봅니다.
   ```bash
   docker compose up -d
   ```
   - 아래와 비슷한 줄이 나오고 서버 두 개가 `Started` 로 끝나면 성공입니다(줄 수는 PC마다 다를 수 있습니다).
   ```
    Container day07_docker-web-one-1  Started
    Container day07_docker-web-two-1  Started
   ```
7. **[브라우저]** `http://127.0.0.1:8080` 에서 **site-one**, `http://127.0.0.1:8081` 에서 **site-two** 가 보이는지 확인하고, 각각 새로 고침을 두세 번 눌러 접속 기록을 만듭니다.
8. **[터미널]** compose 로 켠 서버만 봅니다. `SERVICE` 열에 서버 이름 두 개, `PORTS` 열에 `8080` · `8081` 이 보입니다.
   ```bash
   docker compose ps
   ```
9. **[터미널]** `web-two` 의 접속 기록만 봅니다. `GET / HTTP/1.1" 200` 줄을 찾습니다. 브라우저가 따로 요청한 `/favicon.ico` 의 `404` 줄은 무시합니다.
   ```bash
   docker compose logs web-two
   ```
10. **[보고서]** `day07_pm_report.md` 의 `## 6교시` › `### 문제 6-1` 아래를 채웁니다.
    - (가) 내가 쓴 `web-two` 의 네 줄을 붙여 넣어 주세요.
    - (나) 🔍 `docker compose up -d` 한 줄이 어제의 어떤 명령들을 대신했나요? `compose.yaml` 의 `ports` 와 `volumes` 가 어제의 어떤 옵션과 같은가요?
    - (다) 🔍 `docker compose ps` 와 `docker ps` 는 무엇이 다른가요?

### 6.5 환경변수

- **환경변수**(environment variable · 인바이런먼트 베리어블)
  - 프로그램을 켤 때 넘기는 `이름=값` 설정
  - 같은 이미지라도 서버마다 다른 값을 줄 수 있다
- `env`: 서버 안의 환경변수를 모두 보여 주는 명령
- `|` 와 `grep`
  - 앞 명령의 출력에서 글자가 들어 있는 줄만 걸러 낸다
  - 예: `env | grep MY_ROLE` 은 `MY_ROLE` 이 들어 있는 줄만 보여 준다

### ✍️ 문제 6-2 · 환경변수 한 줄을 넣고 서버 안에서 확인한 뒤 한 줄로 끄기

**📍 이런 상황이 있습니다**

- 보안 담당이 「같은 이미지로 켠 서버가 어떤 역할인지 서버마다 표시해 두고 싶다」고 합니다. 담당자는 서버에 `MY_ROLE=web` 이라는 이름표(환경변수)를 달고, 서버 안에서 확인한 뒤, 정리해야 합니다.
- 현업에서는 같은 이미지에 접속 정보나 모드 같은 값을 **환경변수**로 전달해 서버마다 다르게 동작하게 합니다. 이 값은 파일에 적어 두고 한 번에 바꿀 수 있어서 compose 와 같이 씁니다.

**🎯 할 일**

1. `web-one` 에 <mark>`environment` 두 줄</mark>을 직접 씁니다.
2. 설정이 바뀐 서버가 <mark>다시 만들어지는 것</mark>을 읽고, 서버 안에서 값을 확인합니다.
3. <mark>`docker compose down`</mark> 으로 한 번에 정리합니다.

**순서**

1. **[vim 또는 VS Code]** `compose.yaml` 을 열고 `web-one` 의 `- ./site-one…` 줄 **바로 다음 줄**(`web-two:` 줄 위)에 **두 줄**을 직접 씁니다. 환경변수는 `environment:` 아래에 `- 이름=값` 으로 씁니다.
   - `environment:` 는 공백 4칸으로 시작합니다(`image:` 와 같은 칸)
   - 그 아래 `-` 줄은 공백 6칸으로 시작합니다
   - 첫 줄: `environment:`
   - 둘째 줄: 이름이 `MY_ROLE` 이고 값이 `web` 인 항목
2. **[터미널]** 같은 명령으로 다시 켭니다. 이미 켜져 있는 서버의 설정이 바뀌었으면 `web-one` 만 `Recreated` 로 표시되며 새로 만들어집니다.
   ```bash
   docker compose up -d
   ```
3. **[터미널]** 서버 안에서 `MY_ROLE` 을 확인합니다. `MY_ROLE=web` 이 한 줄 나오면 성공입니다. 어제 `exec -it … sh` 는 서버 안의 터미널을 열었고, 이번에는 명령 하나를 실행하고 바로 돌아옵니다.
   ```bash
   docker compose exec web-one env
   ```
   출력이 길면 `docker compose exec web-one env | grep MY_ROLE` 로 한 줄만 봅니다.
4. **[터미널]** 서버를 한 번에 정리하고 남은 컨테이너를 확인합니다. 아래 두 번째 명령에서 `day07_docker-` 로 시작하는 줄이 보이지 않으면 정리된 것입니다.
   ```bash
   docker compose down
   docker ps -a
   ```
5. **[보고서]** `### 문제 6-2` 아래를 채웁니다.
   - (가) 내가 쓴 `environment` 두 줄을 붙여 넣어 주세요.
   - (나) 🔍 `up -d` 를 다시 쳤을 때 `web-one` 만 `Recreated` 가 된 이유와, `web-two` 는 왜 그대로인지 적어 주세요.
   - (다) 🔍 `docker compose down` 은 어제의 `stop` 과 `rm` 중 무엇을 대신하나요? 정리 뒤 `docker ps -a` 에 서버가 남아 있나요?
   - (한 줄) 보안 담당에게 보낼 답을 한 문장으로 적어 주세요.
   - 이 교시에서 새로 알게 된 것 하나를 적어 주세요.

### 6교시 한눈에

| 하려는 일 | 명령 · 파일 |
|---|---|
| 서버 구성을 파일로 | `compose.yaml` (`services:` › 서버 이름 › `image` · `ports` · `volumes` · `environment`) |
| 모두 켜기 | `docker compose up -d` |
| 이 파일의 서버 보기 | `docker compose ps` |
| 한 서버의 기록 | `docker compose logs 서버이름` |
| 서버 안에서 명령 | `docker compose exec 서버이름 명령` |
| 모두 끄고 지우기 | `docker compose down` |

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">7교시 (16:00–16:50) · 서버가 어디까지 열려 있나 · 증상 읽기 · 올리기</mark>

> 📨 **오늘 들어온 일**
> A사 보안 담당이 보낸 메시지: 「서버를 켰는데 우리 PC 안에서만 접속돼야 할 서버가 사내 다른 PC에서도 열리면 안 됩니다. 어느 서버가 밖에서 열려 있는지 확인해 주세요. 그리고 서버가 안 열릴 때 나오는 메시지도 정리해 주세요.」
> - 이 교시에서 하는 일: 같은 서버를 `127.0.0.1:` 이 붙은 것과 안 붙은 것으로 켜서, 내 PC의 IP 주소로 접속해 **누가 열려 있는지** 직접 확인합니다. 그다음 서버가 안 열릴 때 나오는 증상 세 가지를 읽습니다.
> - 끝나면 쓰는 것: **보고서 한 줄**(보안 담당에게 보낼 답 한 문장)

### 왜 필요한가

1. `-p 8080:80` 처럼 `127.0.0.1:` 없이 연결하면 **내 PC의 모든 주소(`0.0.0.0`)로 열립니다.** 같은 네트워크의 다른 PC가 내 PC의 주소로 접속할 수 있다는 뜻이고, 방화벽이 막지 않는다면 그대로 열립니다.
2. 4일 차에서 배운 **방화벽 허용 목록**(필요한 곳만 열어 두는 것)과 같은 생각입니다. 필요한 곳에만 열어 두고 나머지는 닫습니다. 내 PC 안에서만 쓸 서버는 `-p 127.0.0.1:포트:80` 으로 켭니다.
3. 서버가 안 열릴 때는 어디부터 볼지 정해져 있습니다. `docker ps` → `docker ps -a` → `docker logs`. 그 순서와 메시지를 읽는 연습이 관제에서 장애를 보는 첫 단계입니다.

### 7.1 어디까지 열려 있나

```
-p 127.0.0.1:8081:80  (닫힘)
  내 PC 안에서 (127.0.0.1)  : 접속됨
  내 PC 의 IP 주소:8081     : 거부됨
  다른 PC                   : 거부됨

-p 8082:80  (열림)
  내 PC 안에서 (127.0.0.1)  : 접속됨
  내 PC 의 IP 주소:8082     : 접속됨
  다른 PC                   : 접속됨
```

- 위는 닫은 서버로 내 PC 안에서만 접속됩니다. 아래는 연 서버로 내 PC의 IP 주소로도, 다른 PC에서도 접속됩니다.

- `127.0.0.1` 은 내 PC 자신을 가리키는 주소입니다(1일 차). `-p 127.0.0.1:8081:80` 은 그 주소로 온 요청만 서버에 넘깁니다.
- 접두사가 없으면 `0.0.0.0`(모든 주소)입니다. `docker ps` 의 `PORTS` 열에 `127.0.0.1:8081->80/tcp` 로 나오면 닫힌 것이고 `0.0.0.0:8082->80/tcp` 로 나오면 열린 것입니다.
- 오늘은 내 PC의 **IP 주소**(같은 네트워크 안에서 다른 PC가 내 PC를 부르는 주소, 1일 차)로 접속해 봅니다. 다른 PC가 접속하는 것과 같은 경로입니다.

### ✍️ 문제 7-1 · 같은 서버를 닫아서 켜고 열어서 켜서 직접 재 보기

**📍 이런 상황이 있습니다**

- 보안 담당이 「사내 PC에서 접속되면 안 되는 서버가 열려 있는지 확인하라」고 합니다. 담당자는 서버 두 대를 `127.0.0.1:` 이 있는 것과 없는 것으로 켜서, 내 PC의 IP 주소로 접속하고, 어느 쪽이 열려 있는지 판정해야 합니다.
- 현업에서는 켜 두기만 한 개발용 서버가 `0.0.0.0` 으로 열려 있어 사내 다른 PC에서 접속되는 일이 흔하고, 이것을 점검하는 것이 열린 포트 점검입니다.

**🎯 할 일**

1. <mark>닫힌 서버(8081)와 열린 서버(8082)</mark>를 켭니다.
2. 내 PC의 <mark>IP 주소</mark>를 찾아 두 포트에 접속합니다.
3. <mark>`PORTS` 열과 접속 결과</mark>를 짝지어 판정합니다.

**순서**

1. **[터미널]** 6교시에서 `down` 으로 정리했는지 `docker ps -a` 로 확인합니다. `IMAGE` 열이 `hello-world` 인 줄 말고 남은 컨테이너가 있으면 `docker rm -f 이름` 으로 지웁니다. 그다음 서버 두 대를 켭니다. 앞의 서버는 `127.0.0.1:` 이 붙고 뒤의 서버는 붙지 않습니다.
   ```bash
   docker run -d --name closed -p 127.0.0.1:8081:80 nginx:1.28
   docker run -d --name open -p 8082:80 nginx:1.28
   ```
2. **[터미널]** 두 서버의 `PORTS` 열을 읽습니다. `closed` 는 `127.0.0.1:8081->80/tcp`, `open` 은 `0.0.0.0:8082->80/tcp` 로 나옵니다.
   ```bash
   docker ps
   ```
3. **[터미널]** 내 PC의 IP 주소를 찾습니다. 윈도는 아래 첫 줄을 치고, 맥북은 두 번째 줄을 칩니다. 윈도에서 여러 줄이 나오면 `172.17.` · `172.18.` 로 시작하는 줄은 도커용 주소이므로 빼고, 남은 줄이 내 주소입니다. 이 주소를 아래에서 `내주소` 로 부릅니다.
   ```bash
   ipconfig | grep -a "IPv4"
   ```
   맥북:
   ```bash
   ipconfig getifaddr en0
   ```
4. **[터미널]** `내주소` 로 두 포트에 접속합니다. 아래 `내주소` 를 실제 숫자로 바꿔 칩니다. `-m 3` 은 3초 안에 답이 없으면 포기하는 옵션이고, 화면에는 응답 번호만 나옵니다. 앞이 `closed`, 뒤가 `open` 입니다.
   ```bash
   curl -s -m 3 -o /dev/null -w "%{http_code}\n" http://내주소:8081
   curl -s -m 3 -o /dev/null -w "%{http_code}\n" http://내주소:8082
   ```
   - `closed` 는 `000`(연결이 거부돼 응답 번호가 없음)이 나옵니다
   - `open` 은 `200`(성공)이 나옵니다
5. **[터미널]** 같은 `closed` 에 이번에는 `127.0.0.1` 로 접속합니다. 내 PC 안에서는 열려 있어야 합니다.
   ```bash
   curl -s -m 3 -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8081
   ```
6. **[터미널]** 두 서버를 지웁니다.
   ```bash
   docker rm -f closed open
   ```
7. **[보고서]** `day07_pm_report.md` 의 `## 7교시` › `### 문제 7-1` 아래를 채웁니다.
   - (가) `docker ps` 의 `PORTS` 열에서 두 서버가 각각 어떻게 나왔는지 적어 주세요.
   - (나) 🔍 `내주소` 로 접속했을 때 `closed` 와 `open` 의 결과(응답 번호)를 각각 적어 주세요.
   - (다) 🔍 `closed` 는 `127.0.0.1` 로 접속하면 열려 있는데 `내주소` 로는 거부되는 이유는 무엇인가요? 다른 PC가 접속하는 경우와 어떻게 같은가요?
   - (라) 🔍 사내 PC에서 접속되면 안 되는 관리용 서버를 켠다면 `-p` 를 어떻게 쓰고, 이것이 4일 차의 어떤 원칙과 같은가요?

### 7.2 서버가 안 열릴 때 보는 순서

```
서버가 안 열린다
   |
   v
docker ps        <-- 목록에 있나?  (있으면: PORTS 열 확인)
   |  없다
   v
docker ps -a     <-- 목록에 있나?  (Created 또는 Exited 로 있을 수 있다)
   |
   v
docker logs 이름 <-- 에러가 나오나?  (마지막 줄이 원인인 경우가 많다)
```

- 먼저 `docker ps`(켜진 것), 없으면 `docker ps -a`(꺼진 것까지), 그다음 `docker logs 이름`(에러 문구)을 봅니다.

### ✍️ 문제 7-2 · 서버가 안 열릴 때 나오는 증상 세 가지 읽기

**📍 이런 상황이 있습니다**

- 보안 담당이 「서버가 안 열린다는 문의를 세 건 받았는데 메시지가 모두 다르다」며 정리를 부탁합니다. 담당자는 세 증상을 직접 만들어 보고, 메시지에서 원인이 보이는지, 어디서 알 수 있는지 읽어야 합니다.
- 현업에서는 같은 「안 열린다」여도 메시지에 원인이 적혀 있습니다. 메시지를 읽는 순서가 정해져 있어야 빨리 찾습니다.

**🎯 할 일**

1. <mark>포트 충돌</mark>을 만들어 에러 문구를 읽습니다.
2. <mark>없는 주소(404)</mark>로 접속해 기록에서 원인을 읽습니다.
3. <mark>켜지다 바로 꺼지는 서버</mark>를 만들어 `ps` · `ps -a` · `logs` 로 원인을 찾습니다.

**순서**

1. **[터미널]** 먼저 `docker ps -a` 에 8082 를 쓰는 컨테이너가 없는지 봅니다. 있으면 `docker rm -f 이름` 으로 지웁니다. 그다음 같은 포트 8082 로 서버 두 대를 켭니다. 두 번째에서 에러가 나는 것이 정상입니다. 에러 문구의 끝부분을 읽습니다.
   ```bash
   docker run -d --name first -p 8082:80 nginx:1.28
   docker run -d --name second -p 8082:80 nginx:1.28
   ```
   `Bind for 0.0.0.0:8082 failed: port is already allocated` 가 마지막에 나옵니다.
2. **[터미널]** `second` 가 목록에 있는지 두 가지로 봅니다. `docker ps` 에는 `first` 만 있고, `docker ps -a` 에는 `second` 도 보입니다(상태는 `Created` 로 나옵니다).
   ```bash
   docker ps
   docker ps -a
   ```
3. **[터미널]** 두 서버를 지웁니다.
   ```bash
   docker rm -f first second
   ```
4. **[터미널]** 서버를 하나 켜고, **없는 주소**로 접속합니다. 응답 번호 `404` 가 나옵니다.
   ```bash
   docker run -d --name page -p 8082:80 nginx:1.28
   curl -s -m 3 -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8082/nothing
   ```
5. **[터미널]** 접속 기록에서 그 요청을 찾습니다. `"GET /nothing HTTP/1.1" 404` 줄과, 원인을 적은 `[error] … open() "/usr/share/nginx/html/nothing" failed (2: No such file or directory)` 줄이 있습니다.
   ```bash
   docker logs page
   ```
6. **[터미널]** 서버를 지웁니다.
   ```bash
   docker rm -f page
   ```
7. **[터미널]** 켜지자마자 꺼지는 서버를 만듭니다. 이미지 이름 뒤에 쓴 명령은 컨테이너가 켜질 때 실행되는 명령입니다. 마지막 `nginx -c /no/such.conf` 는 일부러 없는 설정 파일로 nginx 를 시작하라는 뜻이라서 서버가 꺼집니다. 맥북은 `MSYS_NO_PATHCONV=1 ` 을 빼고 칩니다.
   ```bash
   MSYS_NO_PATHCONV=1 docker run -d --name broken -p 8083:80 nginx:1.28 nginx -c /no/such.conf
   ```
8. **[터미널]** 목록과 에러를 순서대로 봅니다. `docker ps` 에는 `broken` 이 없고, `docker ps -a` 에는 `Exited (1)` 로 있고, `docker logs broken` 의 마지막 줄에 `[emerg] … open() … failed (2: No such file or directory)` 가 있습니다.
   ```bash
   docker ps
   docker ps -a
   docker logs broken
   ```
9. **[터미널]** 서버를 지웁니다.
   ```bash
   docker rm -f broken
   ```
10. **[보고서]** `### 문제 7-2` 아래를 채웁니다.
    - (가) 포트 충돌에서 나온 에러 문구의 핵심(마지막 부분)과 그 뜻을 적어 주세요.
    - (나) 🔍 404 요청의 접속 기록에서 응답 번호와 원인이 적힌 줄을 각각 찾아 적어 주세요.
    - (다) 🔍 `broken` 은 `docker ps` 에는 없고 `docker ps -a` 에는 있습니다. 상태 값과 원인을 어느 명령에서 알 수 있었는지 적어 주세요.
    - (한 줄) 보안 담당에게 보낼 답을 한 문장으로 적어 주세요.
    - 이 교시에서 새로 알게 된 것 하나를 적어 주세요.

### ✍️ 문제 7-3 · 오늘 만든 것을 깃허브에 올리기

**📍 이런 상황이 있습니다**

- 팀장이 「오늘 만든 이미지 설계도와 compose 파일을 저장소에 남겨 달라」고 합니다. 올리기 전에 올라갈 파일을 확인하고, 비밀 키 파일(`.env`)이 섞이지 않았는지 봐야 합니다.

**🎯 할 일**

1. 터미널에서 <mark>`git status`</mark> 로 올라갈 파일을 확인합니다.
2. <mark>`git add .` → `git commit` → `git push`</mark> 순서로 올립니다.
3. 깃허브에서 <mark>`day07_docker` 폴더와 보고서 두 개</mark>가 보이는지 확인합니다.

**순서**

1. **[터미널]** `security-agent-toolkit` 폴더로 옮기고 위치를 확인합니다. 결과가 `…/security-agent-toolkit` 으로 끝나야 합니다.
   ```bash
   cd ../..
   pwd
   ```
2. **[터미널]** 무엇이 바뀌었는지 먼저 봅니다. 빨간 목록에 `.env` 나 `.venv` 가 보이면 올리지 않고 멈춥니다.
   - `.env` 가 보이면: VS Code 왼쪽 목록에서 `security-agent-toolkit` 바로 아래의 `.gitignore` 를 열어 맨 아래에 `.env` 한 줄을 적고 저장한 뒤 `git status` 를 다시 칩니다. `.venv` 도 같은 방법으로 합니다.
   - `Untracked files:` 나 `modified:` 아래에 나오는 줄이 올라갈 파일입니다. 오늘 만든 `day07_docker` 폴더와 보고서 파일이 보여야 합니다.
   ```bash
   git status
   ```
3. **[보고서]** `### 문제 7-3` 아래를 채웁니다. 올리기 전에 채워야 깃허브에 빈칸 없이 올라갑니다.
   - (가) `git status` 를 쳤을 때 빨간 목록에 줄이 몇 개였는지, 그 가운데 `.env` · `.venv` 가 있었는지 적어 주세요.
4. **[터미널]** 바뀐 파일을 모두 담고(`add`), 기록하고(`commit`), 올립니다(`push`).
   ```bash
   git add .
   git commit -m "Add day 7 docker image and compose practice and report"
   git push
   ```
   - `git push` 가 거절(`rejected`)되면 `git pull` 을 입력해 받아 온 뒤 `git push` 를 다시 합니다
   - 편집기 화면이 뜨면 `Esc` 를 누르고 `:wq` 를 입력한 뒤 `Enter` 를 누릅니다
5. **[브라우저]** 깃허브의 내 저장소를 새로 고쳐 `network_zt` 폴더 안에 `day07_docker` 폴더와 오전 · 오후 보고서가 있는지 확인합니다.

### 7교시 한눈에

| 하려는 일 | 명령 · 값 |
|---|---|
| 내 PC 안에서만 열기 | `-p 127.0.0.1:포트:80` (`PORTS` 열에 `127.0.0.1:…`) |
| 모든 주소로 열기 | `-p 포트:80` (`PORTS` 열에 `0.0.0.0:…`) |
| IP 주소로 접속 확인 | `curl -s -m 3 -o /dev/null -w "%{http_code}\n" http://내주소:포트` |
| 안 열릴 때 보는 순서 | `docker ps` → `docker ps -a` → `docker logs 이름` |
| 포트 충돌 | `port is already allocated` |
| 없는 주소 | 응답 번호 `404` + 기록의 `[error] open() … failed` |
| 켜지다 꺼짐 | `ps -a` 의 `Exited (1)` + `logs` 의 `[emerg]` |

---

## 오늘 마무리

| 확인 | 문제 |
|---|---|
| Dockerfile 두 줄을 쓰고 내 이미지를 만들었다 | 5-1 |
| 파일을 고치면 이미지를 다시 만들어야 한다는 것을 확인했다 | 5-2 |
| `compose.yaml` 에 서버를 한 대 더 쓰고 두 대를 한 줄로 켰다 | 6-1 |
| 환경변수를 넣고 서버 안에서 확인한 뒤 한 줄로 정리했다 | 6-2 |
| `127.0.0.1:` 이 붙은 서버와 아닌 서버의 열림을 직접 쟀다 | 7-1 |
| 포트 충돌 · 404 · 꺼지는 서버의 메시지를 읽었다 | 7-2 |
| 오늘 만든 파일과 보고서를 깃허브에 올렸다 | 7-3 |

내일(10/21(수))은 오전 실습으로 이어갑니다.

---

# 정답 · 먼저 풀어 본 뒤에 봅니다

설명하는 답은 한 예이고, 핵심이 같으면 맞습니다.

---

### 정답 5-1

💻 **Dockerfile 에 쓰는 두 줄입니다.**

```dockerfile
FROM nginx:1.28
COPY site/index.html /usr/share/nginx/html/index.html
```

💻 **터미널에 입력합니다.**

```bash
docker build -t my-nginx:1 .
docker images
docker run -d --name my-web -p 8080:80 my-nginx:1
```

**결과**

- (가) 위의 Dockerfile 두 줄입니다.
- (나) `FROM nginx:1.28` 은 바탕이 될 이미지를 정합니다. 이 이미지 위에 내 것을 더합니다. `COPY site/index.html /usr/share/nginx/html/index.html` 은 내 PC의 `site/index.html` 을 이미지 안의 nginx 가 응답하는 파일 자리로 복사해 넣습니다.
- (다) 내 파일이 `docker build` 때 이미지 안에 복사되어 이미 들어 있기 때문입니다. 어제는 파일이 내 PC에 있고 `-v` 로 연결해야 컨테이너가 볼 수 있었지만, 오늘은 이미지가 파일을 품고 있어서 연결이 필요 없습니다.

**왜** — 파일을 이미지 안에 넣으면 이미지 하나만 넘겨도 같은 서버가 됩니다. 서버를 재현해야 하는 일에 알맞습니다.

**자주 틀리는 곳** — `docker build` 마지막의 점(`.`)을 빼먹는 일이 가장 많습니다. `COPY` 의 앞쪽 경로를 `index.html` 로만 써서 파일을 못 찾는 경우도 많습니다(`site/` 폴더 안에 있습니다). `Dockerfile` 을 소문자 `dockerfile` 로 만들면 못 찾는 경우도 있습니다. 8080 포트를 다른 서버가 쓰고 있으면 `port is already allocated` 가 납니다. 어제 서버를 지웠는지 `docker ps` 로 봅니다.

**관제에서는** — 이미지 이름과 태그가 같은 파일이 같은 내용을 담고 있다는 약속입니다. 서버를 넘길 때 어느 태그인지 함께 남깁니다.

---

### 정답 5-2

💻 **터미널에 입력합니다.**

```bash
docker build -t my-nginx:2 .
docker rm -f my-web
docker run -d --name my-web -p 8080:80 my-nginx:2
docker images
docker ps
docker rm -f my-web
```

**결과**

- (가) 예전 화면인 **my-nginx v1** 이 그대로 나옵니다.
- (나) 서버가 보여 주는 파일은 이미지 안에 복사된 것이고, 내 PC의 `site/index.html` 은 연결돼 있지 않기 때문입니다. 반영하려면 이미지를 다시 만들고(`docker build`, 새 태그 `:2`) 그 이미지로 서버를 다시 켭니다.
- (다) `-v` 방식은 내 PC의 파일을 그대로 보므로 파일을 고치고 새로 고침만 하면 바뀝니다. 이미지에 넣는 방식은 build 때의 파일을 복사해 둔 것이므로 파일을 고친 뒤 이미지를 다시 build 하고 서버를 교체해야 바뀝니다.
- (한 줄) 예: 「안내 페이지를 이미지에 넣어 `my-nginx:1` 로 만들었고, 문구를 바꿀 때는 `my-nginx:2` 로 다시 build 해 서버를 교체하면 됩니다.」

**왜** — 이미지는 만든 순간의 파일을 담아 두는 묶음입니다. 새 태그로 만들면 이전 버전은 그대로 남아 있어서, 문제가 생겼을 때 이전 버전으로 돌아갈 수 있습니다.

**자주 틀리는 곳** — 이미지를 다시 build 하고도 서버를 지우지 않아 예전 이미지로 켜진 서버가 계속 도는 경우가 많습니다. `docker ps` 의 `IMAGE` 열이 `my-nginx:2` 인지 봅니다. 브라우저가 이전 화면을 보여 줄 때는 `Ctrl + F5` 로 새로 고칩니다.

**관제에서는** — 서버에 문제가 생기면 지금 켜진 서버가 어느 이미지(태그)인지부터 확인합니다. 태그가 `latest` 뿐이면 어느 버전인지 알 수 없어서 추적이 어렵습니다.

---

### 정답 6-1

💻 **`compose.yaml` 의 `web-two` 에 쓰는 네 줄입니다.**

```yaml
  web-two:
    image: nginx:1.28
    ports:
      - "8081:80"
    volumes:
      - ./site-two:/usr/share/nginx/html:ro
```

💻 **터미널에 입력합니다.**

```bash
docker compose up -d
docker compose ps
docker compose logs web-two
```

**결과**

- (가) 위 `web-two` 의 `ports:` · `- "8081:80"` · `volumes:` · `- ./site-two:/usr/share/nginx/html:ro` 네 줄입니다.
- (나) 어제 서버마다 따로 친 `docker run -d --name … -p … -v … 이미지` 명령 두 개를 대신합니다(`up -d` 의 `-d` 도 어제와 같은 백그라운드 옵션). `ports` 는 `-p`, `volumes` 는 `-v`, `image` 는 마지막의 이미지 이름, 서버 이름 `web-two` 는 `--name` 과 같습니다.
- (다) `docker compose ps` 는 **이 compose 파일로 켠 서버만** 보여 주고 `SERVICE` 열에 파일의 서버 이름이 나옵니다. `docker ps` 는 이 PC에서 켜진 **모든** 컨테이너를 보여 줍니다.

**왜** — 서버 구성을 파일로 적어 두면 누가 켜도 같은 구성이 되고, 서버가 늘어도 명령은 한 줄입니다.

**자주 틀리는 곳** — 들여쓰기가 한 칸 어긋나서 `yaml: …` 에러가 나는 경우가 가장 많습니다. `ports:` · `volumes:` 는 `image:` 와 같은 칸에서 시작합니다. `- "8081:80"` 에서 `-` 뒤 공백이 없는 경우도 많습니다. `compose.yaml` 이 없는 폴더에서 명령을 쳐서 `no configuration file provided` 가 나오는 경우도 있습니다. 먼저 `pwd` 를 봅니다. 8080 · 8081 포트를 다른 컨테이너가 쓰고 있으면 `port is already allocated` 가 납니다.

**관제에서는** — compose 파일은 서버 구성의 기록입니다. 이 파일 하나로 같은 환경을 다시 켤 수 있어서, 사고 재현과 인수인계에 씁니다.

---

### 정답 6-2

💻 **`compose.yaml` 의 `web-one` 에 쓰는 두 줄입니다.**

```yaml
    environment:
      - MY_ROLE=web
```

💻 **터미널에 입력합니다.**

```bash
docker compose up -d
docker compose exec web-one env
docker compose down
docker ps -a
```

**결과**

- (가) 위 `environment:` 와 `- MY_ROLE=web` 두 줄입니다.
- (나) compose 는 파일과 지금 켜진 서버를 비교해, **설정이 바뀐 서버만** 다시 만듭니다. `web-one` 의 설정(`environment`)이 바뀌었으므로 `Recreated` 가 되고, `web-two` 는 바뀌지 않아서 그대로 둡니다.
- (다) `stop` 과 `rm` 을 한 번에 대신합니다. 켜진 서버를 멈추고 지웁니다. 정리 뒤 `docker ps -a` 에는 compose 로 켠 서버가 남아 있지 않습니다.
- (한 줄) 예: 「서버 구성은 `compose.yaml` 에 적고 `docker compose up -d` 로 켜며, `environment` 로 서버마다 이름표를 달고 `docker compose down` 으로 한 번에 정리합니다.」

**왜** — 환경변수는 이미지를 바꾸지 않고 서버마다 다른 값을 줍니다. 값이 바뀌면 compose 가 그 서버만 새로 만들어 줍니다.

**자주 틀리는 곳** — `environment:` 를 `image:` 와 다른 칸에 써서 에러가 나는 경우가 많습니다. 이름과 값을 `MY_ROLE: web` 처럼 `:` 로 써서 목록 모양이 달라지는 경우도 있습니다. 이 문서는 `- 이름=값` 으로 씁니다. `docker compose exec` 를 compose.yaml 이 없는 폴더에서 치면 서버를 못 찾습니다.

**관제에서는** — 접속 정보나 모드 같은 값은 이미지에 넣지 않고 환경변수로 줍니다. 비밀 값은 파일에 그대로 적어 저장소에 올리지 않습니다.

---

### 정답 7-1

💻 **터미널에 입력합니다.**

```bash
docker run -d --name closed -p 127.0.0.1:8081:80 nginx:1.28
docker run -d --name open -p 8082:80 nginx:1.28
docker ps
curl -s -m 3 -o /dev/null -w "%{http_code}\n" http://내주소:8081
curl -s -m 3 -o /dev/null -w "%{http_code}\n" http://내주소:8082
curl -s -m 3 -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8081
docker rm -f closed open
```

**결과**

- (가) `closed` 는 `127.0.0.1:8081->80/tcp`, `open` 은 `0.0.0.0:8082->80/tcp` 로 나옵니다. 앞에 `127.0.0.1:` 이 붙어 있는지가 다릅니다.
- (나) `closed` 는 `000`(연결 거부), `open` 은 `200` 입니다.
- (다) `closed` 는 `127.0.0.1`(내 PC 자신)로 온 요청만 받도록 연결돼 있어서, 내 PC 안에서 `127.0.0.1` 로 접속하면 `200` 이지만 `내주소` 로 오는 요청은 받지 않아 거부됩니다. 다른 PC가 내 PC의 IP 주소로 접속하는 것도 같은 경로이므로 똑같이 거부됩니다.
- (라) `-p 127.0.0.1:포트:80` 으로 켭니다. 필요한 곳에만 열고 나머지는 닫는 방화벽 허용 목록(4일 차)과 같은 생각입니다.

**왜** — `-p` 에 주소를 쓰지 않으면 서버가 모든 주소로 열립니다. 개발용 · 관리용 서버를 이렇게 켜 둔 채 잊는 것이 열린 포트의 흔한 원인입니다.

**자주 틀리는 곳** — `내주소` 를 글자 그대로 쳐서 에러가 나는 경우가 가장 많습니다. 실제 숫자로 바꿉니다. 맥북에서 `en0` 가 아닌 인터페이스를 쓰고 있어 주소가 비어 나오는 경우도 있습니다. 윈도에서 `172.` 로 시작하는 도커용 주소로 접속해 둘 다 열리는 것처럼 보이는 경우도 있습니다. `내주소` 가 잘못되면 둘 다 거부로 나옵니다. 가장 확실한 판정은 `PORTS` 열입니다.

**관제에서는** — 서버를 켤 때 `docker ps` 의 `PORTS` 열에 `0.0.0.0` 이 있는 서버를 찾는 것이 열린 포트 점검의 첫 단계입니다. 열려 있어도 되는 서버인지 확인하고, 아니면 `127.0.0.1:` 을 붙여 다시 켭니다.

---

### 정답 7-2

💻 **터미널에 입력합니다.**

```bash
docker run -d --name first -p 8082:80 nginx:1.28
docker run -d --name second -p 8082:80 nginx:1.28
docker ps
docker ps -a
docker rm -f first second
docker run -d --name page -p 8082:80 nginx:1.28
curl -s -m 3 -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8082/nothing
docker logs page
docker rm -f page
MSYS_NO_PATHCONV=1 docker run -d --name broken -p 8083:80 nginx:1.28 nginx -c /no/such.conf
docker ps
docker ps -a
docker logs broken
docker rm -f broken
```

**결과**

- (가) `Bind for 0.0.0.0:8082 failed: port is already allocated`. 뜻은 「내 PC의 8082 포트를 이미 다른 컨테이너가 쓰고 있어서 연결할 수 없다」입니다. 다른 포트로 켜거나 먼저 켠 서버를 정리하면 됩니다.
- (나) 응답 번호는 `404` 입니다. 기록의 `"GET /nothing HTTP/1.1" 404 …` 줄에 있고, 원인은 `[error] … open() "/usr/share/nginx/html/nothing" failed (2: No such file or directory)` 줄에 있습니다. 서버 안에 요청한 파일이 없다는 뜻입니다.
- (다) 상태는 `Exited (1)` 입니다. `docker ps` 에는 실행 중인 것만 나오므로 없고, 꺼진 이유는 `docker logs broken` 의 마지막 줄 `[emerg] … open() … failed (2: No such file or directory)` 에서 알 수 있습니다. 설정 파일을 열지 못해서 nginx 가 시작하지 못하고 종료됐다는 뜻입니다.
- (한 줄) 예: 「안 열리면 `docker ps` → `docker ps -a` → `docker logs` 순서로 보고, 포트 충돌은 `port is already allocated`, 없는 주소는 응답 번호 `404`, 켜지다 꺼지는 서버는 `Exited (1)` 와 `[emerg]` 로 원인을 알 수 있습니다.」

**왜** — 안 열리는 이유는 세 곳(포트 · 요청 · 서버 시작)으로 나뉘고, 각 메시지에 원인이 적혀 있습니다. 어디부터 볼지 순서가 있으면 빨리 찾습니다.

**자주 틀리는 곳** — `docker ps` 에 안 보이니 서버가 없다고 단정하는 경우가 가장 많습니다. 꺼진 서버는 `ps -a` 에 있습니다. 404 를 서버 고장으로 읽는 경우도 많은데, 서버는 정상이고 요청한 파일이 없는 것입니다. `broken` 서버에서 `logs` 를 보지 않고 다시 켜 보기만 하는 경우도 있습니다. 윈도에서는 `/no/such.conf` 가 `C:/Program Files/Git/…` 로 바뀌어 `[emerg]` 의 경로가 다르게 보일 수 있습니다. 그래서 `MSYS_NO_PATHCONV=1` 을 붙입니다.

**관제에서는** — 404 가 한꺼번에 많이 쌓이면 존재하지 않는 주소를 훑는 시도일 수 있어서 4과목에서 분석할 대상이 됩니다. 서버가 반복해서 `Exited` 가 되면 `logs` 의 마지막 줄을 먼저 봅니다.

---

### 정답 7-3

💻 **터미널에 입력합니다.**

```bash
cd ../..
pwd
git status
git add .
git commit -m "Add day 7 docker image and compose practice and report"
git push
```

**결과**

- (가) 한 예: 「줄이 3개였고(`day07_docker/` 폴더, 오후 보고서 `day07_pm_report.md`, 안내 문서 등), `.env` · `.venv` 는 없었다」. 줄 수와 이름은 학생마다 다를 수 있습니다. `.env` 나 `.venv` 가 보였다면 `.gitignore` 에 한 줄을 적고 `git status` 를 다시 쳤다고 적습니다.

**왜** — 올리기 전에 올라갈 파일을 확인해야 비밀 키가 섞이지 않습니다. 저장소에 남기면 누가 언제 무엇을 했는지 기록이 남고 다음 사람이 이어받을 수 있습니다.

**자주 틀리는 곳** — `.env` 가 보이는데 그대로 `git add .` 를 하는 실수가 가장 위험합니다. 멈추고 `.gitignore` 를 확인합니다. 올린 뒤 브라우저에서 확인하지 않으면 올라갔는지 알 수 없습니다.

**관제에서는** — `Dockerfile` 과 `compose.yaml` 을 저장소에 남기면 서버 구성이 기록으로 남아 사고 때 같은 환경을 다시 만들 수 있습니다. 비밀 키는 저장소에 올리지 않습니다.
