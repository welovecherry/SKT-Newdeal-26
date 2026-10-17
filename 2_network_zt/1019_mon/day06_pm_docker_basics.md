# 10/19(월) 오후 · Docker ① — 왜 도커인가 · 설치 · nginx 서버 켜고 읽기 · 내 페이지 연결 — 실습

오전에는 접속 요청을 점수로 판단하고(PDP), 판단과 집행을 나누는 구조(PEP)를 배웠습니다. 오후에는 그 구조를 직접 눈으로 보는 데 쓸 도구, **Docker**(도커)를 시작합니다. 오늘은 **서버 하나를 켜고(5 · 6교시), 내 페이지를 올려 보고, 접속 기록을 읽는 것(6 · 7교시)** 까지 합니다. 화요일에는 서버 여러 개를 파일 하나로 켜고 끄고, 서버 상태를 읽는 연습을 합니다.

## 시작하기

**오후에 받은 파일 두 개를 `network_zt` 폴더로 옮깁니다.** VS Code 왼쪽 목록의 `network_zt` 폴더로 끌어다 놓거나, 탐색기(맥북은 Finder)로 옮깁니다.

- `day06_pm_docker_basics.md` (이 파일) — 오후 실습 안내. 읽기만 합니다.
- `day06_pm_report.md` — **오후 보고서.** 5 · 6 · 7교시 답을 여기에 적습니다.

1. **[VS Code]** 이 파일을 열고 `Ctrl + Shift + V`(맥북은 `Cmd + Shift + V`)를 누릅니다 — 왼쪽.
2. **[VS Code]** `day06_pm_report.md` 를 오른쪽 클릭 › **Open to the Side** — 오른쪽. 질문마다 `쓸 내용:` 을 보고 `답:` 뒤에 씁니다.
3. 문제는 **할 일 → 순서**대로 합니다. 순서 앞의 `[창 이름]` 이 지금 쓸 창이고, `[창 이름]` 이 없는 단계는 안내를 읽고 생각하는 단계입니다. 막히면 문서 맨 아래 「정답」을 봅니다.

> 오늘 명령은 모두 **터미널**에서 칩니다(윈도에서는 Git Bash). 명령 아래에 「맥북:」 줄이 있으면 맥북에서만 그 줄을 칩니다. 도식 안의 이름은 영어로 쓰고, 한글 설명은 도식 아래에 적습니다. 학원에서 같이 쓰는 내려받기 한도가 있어서 **이미지를 지우지 않습니다**(`docker rmi` 를 치지 않습니다). 오늘 명령에 나오는 이름과 숫자는 연습용입니다.

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">5교시 (14:00–14:50) · 왜 도커인가 · 이미지와 컨테이너 · 같이 설치하기</mark>

> 📨 **오늘 들어온 일**
> A사 보안 담당이 보낸 메시지: 「관제 도구를 서버마다 직접 설치했더니 버전이 달라서 결과도 다르게 나옵니다. 같은 환경을 어느 PC에서나 똑같이 띄울 방법이 없을까요?」
> - 이 교시에서 하는 일: 도커가 왜 필요한지 알고, 이미지와 컨테이너의 차이를 익히고, 도커를 설치해 첫 컨테이너를 실행합니다.
> - 끝나면 쓰는 것: **보고서 한 줄**(보안 담당에게 보낼 답 한 문장)

### 왜 필요한가

1. 프로그램을 PC에 직접 설치하면 PC마다 버전과 설정이 달라지고, 지우고 나서도 파일이 남습니다. 「내 PC에서는 되는데 다른 PC에서는 안 된다」가 여기서 생깁니다.
2. 관제 현장에서는 로그 서버, 탐지 도구, 테스트 서버를 여러 대에 똑같이 띄웁니다. 도커는 **프로그램과 필요한 파일을 한 묶음으로 만들어 어디서나 똑같이 실행**하게 해 줍니다.
3. 이번 주에 배우는 도커는 4과목(이상탐지)에서 접속 로그를 모으고, 5과목(자동 대응)에서 대응 대상 서버를 켜고 끄고, 캡스톤에서 시연 환경을 한 번에 켜는 데 다시 씁니다.

### 5.1 도커 없이 설치하는 것과 도커로 실행하는 것

```
[WITHOUT DOCKER]
PC-A: install nginx 1.18 --> setting differs
PC-B: install nginx 1.24 --> setting differs     ==> results differ per PC
PC-C: install nginx 1.18 + old files left

[WITH DOCKER]
PC-A, PC-B, PC-C: pull the same image nginx:1.28
                  run it                        ==> same server on every PC
```

- PC마다 설치하면 버전이 다를 수 있고, 지워도 파일이 남을 수 있습니다.
- 도커는 같은 **이미지**를 받아서 실행하므로 어느 PC에서나 같은 서버가 됩니다. 지울 때도 컨테이너 하나를 지우면 끝납니다.

### 5.2 이미지와 컨테이너 · Docker Hub · 엔진

- **이미지**(image · 이미지)
  - 실행할 프로그램과 필요한 파일을 한 묶음으로 만들어 둔 것
  - 읽기만 할 수 있다
  - 이름은 `nginx:1.28` 처럼 `이름:태그`(태그는 버전)
- **컨테이너**(container · 컨테이너)
  - 이미지를 실제로 실행한 것
  - 같은 이미지로 컨테이너를 여러 개 만들 수 있다
- **레지스트리**(registry · 레지스트리) 와 **Docker Hub**(도커 허브)
  - 레지스트리: 이미지를 모아 두고 내려받게 해 주는 서버
  - Docker Hub: 가장 널리 쓰는 공개 레지스트리
  - 이미지를 받을 때 일어나는 일
    - `registry-1.docker.io` 같은 **이름을 DNS 로 IP 로 바꾼다**(3일 차)
    - 그 IP 로 인터넷을 거쳐 이미지를 내려받는다
- **엔진**(engine · 엔진)
  - 이미지를 받고 컨테이너를 만들어 실행하는 도커의 핵심 프로그램
  - 윈도에서는 **Docker Desktop**(도커 데스크톱)이 엔진을 설치하고 켜 준다
  - Docker Desktop 은 WSL 2(윈도 안에서 리눅스를 돌리는 기능) 위에서 엔진을 돌린다

```
Docker Hub (internet)            MY PC
+--------------------+  pull  +-----------------------------+
| IMAGE nginx:1.28   | -----> | IMAGE nginx:1.28 (read only)|
+--------------------+        |   |            |            |
                              |   v run        v run        |
                              | CONTAINER-1   CONTAINER-2   |
                              +-----------------------------+
```

- 이미지는 한 번 받아 두면 같은 이미지로 컨테이너를 몇 개든 만들 수 있습니다.
- 컨테이너를 지워도 이미지는 남아서 다음에 바로 다시 켤 수 있습니다.

### 5.3 nginx 기반이란?

이번 주 연습은 모두 **`nginx`**(엔진엑스) 이미지로 합니다.

- **nginx** 는 웹 서버 프로그램입니다. 브라우저가 요청하면 파일을 응답하고, 접속 기록을 남깁니다. 설정에 따라 요청을 다른 서버로 넘겨 주는 중간 서버(프록시)로도 쓰입니다.
- 코드를 새로 만들지 않고도 **서버를 켜고 · 기록을 읽고 · 끄는 일**을 연습할 수 있어서 도커를 배우는 재료로 알맞습니다. 실무에서도 가장 흔한 서버 중 하나입니다.
- 이미지 하나(`nginx:1.28`)만 받으면 돼서 학원 망의 내려받기 한도에도 맞습니다.
- nginx 의 접속 기록은 4과목 이상탐지에서 분석할 로그가 됩니다.

### 5.4 같이 설치하기

설치가 진행되는 동안 5.1 ~ 5.3 을 읽습니다. 학원 PC는 **계정별로 설치**되므로, 내 계정에 설치합니다.

1. **[브라우저]** `https://docs.docker.com/desktop/setup/install/windows-install/` 를 열고 **Docker Desktop for Windows** 다운로드 단추를 눌러 `Docker Desktop Installer.exe` 를 받습니다. 대부분의 PC는 AMD64(x86) 용입니다.
2. **[탐색기]** `Docker Desktop Installer.exe` 를 두 번 눌러 실행하고, 설치 방식에서 **WSL 2** 를 고르고 끝까지 진행합니다. 다시 시작하라는 안내가 나오면 다시 시작합니다.
3. **[터미널]** 「WSL 이 없다」는 안내가 나오면 터미널에서 아래를 입력합니다. 100% 까지 올라가고 「요청한 작업이 잘 실행되었습니다」가 나오면 윈도를 다시 시작한 뒤 2번을 이어서 합니다.
   ```bash
   wsl --install
   ```
4. **[윈도]** 시작 메뉴에서 **Docker Desktop** 을 실행합니다. 약관에 동의하고, 사용 목적을 묻는 화면에서 **Personal** 을 고르고, 로그인 화면에서 **Skip**(건너뛰기)이 보이면 건너뜁니다.
5. 창 아래쪽에 고래 모양과 함께 **Engine running**(초록색)이 보일 때까지 기다립니다. 처음에는 몇 분 걸릴 수 있습니다. **Docker Desktop 을 끄지 말고 켜 둡니다.**

설치가 안 될 때는 아래를 봅니다.

| 증상 | 이유 | 해결 |
|---|---|---|
| 「가상화가 꺼져 있다」는 안내 | BIOS/UEFI 에서 가상화가 꺼져 있음 | 작업 관리자 › 성능 › CPU 에서 「가상화」를 확인하고, 꺼져 있으면 알려 줍니다 |
| 「WSL 2 가 설치되지 않았다」 | WSL 이 없거나 오래됨 | 3번의 `wsl --install` 후 다시 시작. 이미 있으면 `wsl --update` |
| `docker: command not found` | 터미널이 설치 전에 열렸거나 Docker Desktop 이 꺼짐 | Docker Desktop 이 켜져 있는지 보고 **터미널을 모두 닫았다가 다시 엽니다** |
| 「You are not allowed to use Docker」 | 모든 사용자용으로 설치됐는데 내 계정이 허용 그룹에 없음 | 알려 주세요 |
| Engine 이 계속 노란색 | 처음 시작은 오래 걸림 | 몇 분 기다리고, 계속 안 되면 Docker Desktop 을 종료했다가 다시 실행 |

### 5.5 `docker run hello-world` 가 하는 일

설치가 끝나면 이 한 줄로 도커의 전체 흐름을 한 번에 봅니다.

```
[TERMINAL] docker run hello-world
     |
     | (1) ask
     v
[DOCKER CLIENT] --> [DOCKER ENGINE] --(2) no image? pull--> [DOCKER HUB]
                          |  <------------ image ----------------
                          | (3) create and start container
                          v
                 [CONTAINER hello-world] --(4) print text--> [TERMINAL]
```

① 터미널의 `docker` 명령(클라이언트)이 엔진에 요청하고, ② 엔진이 이미지가 PC에 없으면 Docker Hub 에서 받고, ③ 받은 이미지로 컨테이너를 만들어 실행하고, ④ 컨테이너가 글자를 출력하면 터미널로 돌아옵니다.

### ✍️ 문제 5-1 · 설치를 확인하고 첫 컨테이너 실행하기

**📍 이런 상황이 있습니다**

- A사 보안 담당이 「도커가 제대로 설치됐는지 팀원 PC마다 확인해 달라」고 합니다. 담당자는 버전을 확인하고, 첫 컨테이너를 실행하고, 이미지와 컨테이너가 각각 어디에 남는지 봐야 합니다.
- 현업에서는 새 서버나 PC에 도구를 올린 뒤 가장 먼저 이 확인을 합니다.

**🎯 할 일**

1. <mark>`docker --version`</mark> 으로 버전을 확인합니다.
2. <mark>`docker run hello-world`</mark> 를 실행하고 출력이 5.5 의 네 단계와 맞는지 읽습니다.
3. <mark>`docker images`</mark> 와 <mark>`docker ps -a`</mark> 로 이미지와 컨테이너가 각각 남아 있는지 봅니다.

**순서**

1. **[터미널]** 버전을 확인합니다. 숫자가 나오면 됩니다.
   ```bash
   docker --version
   ```
   예: `Docker version 29.8.2, build 7fc2dff` (학원 PC에서 나온 값입니다. 숫자는 다를 수 있습니다)
2. **[터미널]** 첫 컨테이너를 실행합니다. 처음에는 이미지를 내려받는 줄(`Unable to find image ... locally` → `Pulling from library/hello-world`)이 먼저 나옵니다. **Docker Hub 에서 받는 것이므로 한 번만 칩니다.**
   ```bash
   docker run hello-world
   ```
   아래처럼 나오면 성공입니다.
   ```
   Hello from Docker!
   This message shows that your installation appears to be working correctly.

   To generate this message, Docker took the following steps:
    1. The Docker client contacted the Docker daemon.
    2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
       (amd64)
    3. The Docker daemon created a new container from that image which runs the
       executable that produces the output you are currently reading.
    4. The Docker daemon streamed that output to the Docker client, which sent it
       to your terminal.
   ```
   - 영어 문장의 네 단계가 5.5 의 ① ~ ④ 와 같은 순서입니다
   - `daemon`(데몬)은 엔진과 같은 말로, 뒤에서 계속 돌며 요청을 처리하는 프로그램입니다
3. **[터미널]** 이미지가 어디에 남았는지 봅니다. `hello-world` 줄이 보입니다.
   ```bash
   docker images
   ```
4. **[터미널]** 컨테이너가 어디에 남았는지 봅니다. `hello-world` 컨테이너가 `Exited` 로 보입니다. 글자를 한 번 출력하고 끝났기 때문입니다.
   ```bash
   docker ps -a
   ```
5. **[보고서]** `day06_pm_report.md` 의 `## 5교시` › `### 문제 5-1` 아래를 채웁니다.
   - (가) `docker --version` 으로 나온 값을 적어 주세요.
   - (나) 🔍 `docker run hello-world` 출력이 말하는 일의 순서를 5.5 그림의 번호(① ~ ④)에 맞춰 설명해 주세요.
   - (다) 🔍 `docker images` 에 보인 것과 `docker ps -a` 에 보인 것은 각각 이미지와 컨테이너 중 무엇이고, 어떻게 다른가요?

### ✍️ 문제 5-2 · Docker Hub 에서 이미지 이름 읽고 없는 이미지 받아 보기

**📍 이런 상황이 있습니다**

- A사 보안 담당이 「웹 서버 이미지를 Docker Hub 에서 찾아 써 보고 싶다」고 합니다. 담당자는 이미지 이름과 태그를 읽을 줄 알아야 하고, 이름을 잘못 쓰면 어떻게 되는지도 알아야 합니다.
- 현업에서는 이름이나 태그를 잘못 적어 엉뚱한 이미지를 받거나, 받지 못하는 일이 흔합니다.

**🎯 할 일**

1. 브라우저로 <mark>Docker Hub 의 nginx 페이지</mark>를 열어 이미지 이름과 태그를 읽습니다.
2. 없는 이름(`nginxx`)을 일부러 받아 보고 <mark>오류 문구</mark>를 읽습니다.
3. 이름과 태그가 각각 <mark>무엇을 정하는지</mark> 설명합니다.

**순서**

1. **[브라우저]** `https://hub.docker.com/_/nginx` 를 열고, 페이지 위쪽에 **Docker Official Image**(도커 공식 이미지)라고 적혀 있는지 봅니다. 「Tags」 목록에서 `1.28` 이 들어간 태그를 찾습니다.
2. **[터미널]** 이름을 일부러 틀리게 써서 받아 봅니다. 오타 이름은 내려받기 한도에 들어가지 않습니다.
   ```bash
   docker pull nginxx
   ```
   `pull access denied for nginxx, repository does not exist or may require 'docker login'` 처럼 나옵니다. 오류 아래에 「What's next: Debug … with Gordon」 같은 광고 문구가 붙으면 무시합니다.
3. **[보고서]** `### 문제 5-2` 아래를 채웁니다.
   - (가) `nginx:1.28` 에서 `nginx` 와 `1.28` 이 각각 무엇을 정하는지 적어 주세요.
   - (나) 🔍 `docker pull nginxx` 를 쳤을 때 나온 오류 문구와 그 뜻을 적어 주세요.
   - (한 줄) 보안 담당에게 보낼 답을 한 문장으로 적어 주세요.
   - 이 교시에서 새로 알게 된 것 하나를 적어 주세요.

### 5교시 한눈에

| 하려는 일 | 명령 · 말 |
|---|---|
| 설치 확인 | `docker --version` |
| 첫 컨테이너 | `docker run hello-world` |
| 내려받은 이미지 보기 | `docker images` |
| 컨테이너 기록 보기 | `docker ps -a` |
| 이미지 이름 읽기 | `이름:태그` (예: `nginx:1.28`) |

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">6교시 (15:00–15:50) · nginx 서버 켜고 접속 기록 읽기</mark>

> 📨 **오늘 들어온 일**
> A사 보안 담당이 보낸 메시지: 「웹 서버 하나를 켜서 접속하면 기록이 남는지 확인하고 싶습니다. 서버를 어떻게 켜고, 안에는 무엇이 들어 있고, 어떻게 끄나요?」
> - 이 교시에서 하는 일: nginx 서버를 켜서 브라우저로 접속하고, 접속 기록을 읽고, 컨테이너 안을 들여다본 뒤 끄고 지웁니다.
> - 끝나면 쓰는 것: **보고서 한 줄**(보안 담당에게 보낼 답 한 문장)

### 왜 필요한가

1. 서버를 켜 두었는데 접속이 안 될 때, 어디부터 볼지 알아야 합니다. 이번 교시의 명령 `ps` · `logs` · `exec` 는 그때 가장 먼저 쓰는 명령입니다.
2. 컨테이너는 기본적으로 **밖에서 접속할 수 없게 막혀 있습니다.** 내 PC의 포트와 컨테이너의 포트를 연결해야 브라우저가 닿습니다. 1일 차에서 배운 포트가 여기서 다시 쓰입니다.
3. 서버가 남기는 접속 기록은 관제의 원자료입니다. 누가 · 언제 · 무엇을 요청했는지가 한 줄에 들어 있어서 4과목 이상탐지에서 그대로 분석합니다.

### 6.1 포트를 연결해야 접속이 된다

```
BROWSER   http://127.0.0.1:8080
   |
   v   port 8080 of MY PC
+------------------ MY PC -----------------------+
|  8080  ===== -p 8080:80 =====>  +-------------+ |
|                                 | CONTAINER   | |
|                                 | nginx  :80  | |
|                                 +-------------+ |
+------------------------------------------------+
```

- 컨테이너 안의 nginx 는 컨테이너 안의 **80번 포트**를 듣고 있습니다. 내 PC의 8080번 포트로 온 요청을 그 80번으로 넘기도록 **연결**하는 것이 `-p 8080:80`(`-p 내PC포트:컨테이너포트`)입니다. 1 · 2일 차의 `IP:포트` 접속과 같고, 포트 포워딩(한 포트로 온 요청을 다른 포트로 넘김)이라고도 부릅니다.
- 이 연결이 없으면 컨테이너는 켜져 있어도 브라우저가 닿을 길이 없습니다. 아래에서 직접 확인합니다.

### 6.2 접속 기록 한 줄 읽기

nginx 는 요청을 처리할 때마다 한 줄씩 기록합니다. `docker logs` 로 보면 아래와 같은 모양입니다(주소와 시각은 PC마다 다릅니다).

```
172.17.0.1 - - [19/Oct/2026:14:31:05 +0000] "GET / HTTP/1.1" 200 615 "-" "Mozilla/5.0 ..."
```

| 부분 | 뜻 |
|---|---|
| `172.17.0.1` | 요청을 보낸 쪽의 주소(내 PC에서 컨테이너로 올 때 도커가 붙인 사설 주소, 2일 차 사설 주소) |
| `[19/Oct/2026:14:31:05 +0000]` | 요청을 받은 시각 |
| `"GET / HTTP/1.1"` | 요청: 방법(`GET`) · 주소(`/`) · 프로토콜 |
| `200` | 응답 번호. `200` 은 성공 |
| `615` | 응답으로 보낸 글자 수 |

- 응답 번호는 서버가 요청에 답하며 붙이는 번호입니다(`200` 성공, `404` 없는 주소). 오늘은 `200` 만 봅니다.

### 6.3 이번 교시의 명령 — 필요한 상황에서 하나씩

| 명령 | 필요한 상황 | 달라지는 점 |
|---|---|---|
| `docker run -d --name web -p 8080:80 nginx:1.28` | 서버를 켜고 이름을 붙이고 포트를 연결하고 싶다 | 컨테이너가 켜지고 브라우저로 접속된다 |
| `docker ps` | 켜 둔 서버가 살아 있는지, 포트가 연결됐는지 | 실행 중인 컨테이너 목록과 `PORTS` 열 |
| `docker logs web` | 접속이 들어왔는지, 어떤 요청인지 | 접속 기록 한 줄씩 |
| `docker exec -it web sh` | 컨테이너 안에 무엇이 있는지 직접 보고 싶다 | 컨테이너 안의 터미널이 열린다 |
| `docker stop web` | 서버를 끄고 싶다 | 컨테이너가 멈춘다 |
| `docker rm web` | 같은 이름을 다시 쓰고 싶다 | 멈춘 컨테이너가 지워진다 |

- `-d`(detach · 디태치)는 컨테이너를 **백그라운드**로 켜서 터미널을 계속 쓰게 합니다. `--name` 은 이름을 붙여서 뒤에 `web` 으로 부를 수 있게 합니다. `-p` 는 포트 연결입니다. 마지막 `nginx:1.28` 이 이미지 이름입니다.
- `-it` 는 컨테이너 안의 터미널(`sh`)을 키보드로 쓰게 합니다. 안에서 나올 때는 `exit` 를 칩니다.

### ✍️ 문제 6-1 · 포트 없이 켜 보고, 포트를 연결해 접속하고, 기록 읽기

**📍 이런 상황이 있습니다**

- A사 보안 담당이 웹 서버 하나를 켜서 접속 기록이 남는지 확인하려고 합니다. 먼저 포트를 연결하지 않고 켜면 어떻게 되는지, 연결하면 무엇이 달라지는지 봐야 합니다.
- 현업에서는 「서버는 켜졌는데 접속이 안 된다」의 흔한 원인이 포트 연결 빠뜨림입니다.

**🎯 할 일**

1. <mark>포트 없이</mark> nginx 를 켜서 접속해 보고 안 되는 것을 확인합니다.
2. 지우고 <mark>`-p 8080:80`</mark> 으로 다시 켜서 브라우저로 접속합니다.
3. <mark>`docker ps`</mark> 의 PORTS 열과 <mark>`docker logs`</mark> 의 접속 기록 한 줄을 읽습니다.

**순서**

1. **[터미널]** 포트 없이 nginx 를 켭니다. 이미지가 PC에 없으면 먼저 내려받는 줄이 나옵니다(한 번만 받습니다).
   ```bash
   docker run -d --name web nginx:1.28
   ```
2. **[브라우저]** `http://127.0.0.1:8080` 을 엽니다. **접속이 안 되는 것**을 확인합니다. 연결할 수 없다는 오류가 나옵니다.
3. **[터미널]** 컨테이너는 켜져 있는데 접속이 안 되는 상태를 `ps` 로 봅니다. `PORTS` 열에 `80/tcp` 만 있고 `->` 가 없습니다.
   ```bash
   docker ps
   ```
4. **[터미널]** 이 컨테이너를 지우고(`-f` 는 켜져 있어도 지우는 옵션) 포트를 연결해 다시 켭니다.
   ```bash
   docker rm -f web
   docker run -d --name web -p 8080:80 nginx:1.28
   ```
5. **[브라우저]** `http://127.0.0.1:8080` 을 엽니다. **Welcome to nginx!** 가 보이면 성공입니다. 새로 고침을 두세 번 눌러 접속 기록을 만듭니다.
6. **[터미널]** `ps` 에서 이번에는 `PORTS` 열이 `0.0.0.0:8080->80/tcp` 처럼 `->` 로 이어진 것을 봅니다.
   ```bash
   docker ps
   ```
7. **[터미널]** 접속 기록을 읽습니다. 새로 고침을 누른 횟수만큼 `GET / HTTP/1.1" 200` 줄이 쌓입니다.
   ```bash
   docker logs web
   ```
8. **[보고서]** `day06_pm_report.md` 의 `## 6교시` › `### 문제 6-1` 아래를 채웁니다.
   - (가) 포트 없이 켠 `web` 에 접속했을 때 어떻게 되었는지 적어 주세요.
   - (나) 🔍 `-p 8080:80` 이 하는 일을 내 PC의 포트와 컨테이너의 포트로 나눠 설명해 주세요.
   - (다) 🔍 `docker logs web` 의 접속 기록 한 줄에서 접속자 주소 · 시각 · 요청 · 응답 번호를 찾아 적어 주세요.

### ✍️ 문제 6-2 · 컨테이너 안을 들여다보고, 끄고, 지우기

**📍 이런 상황이 있습니다**

- 보안 담당이 「이 서버 안에 실제로 무슨 파일이 있는지, 끈 서버는 어떻게 정리하는지」 묻습니다. 담당자는 컨테이너 안에 들어가 파일을 확인하고, 끈 컨테이너가 어디에 남는지, 같은 이름으로 다시 켜면 어떻게 되는지 알아야 합니다.
- 현업에서는 끈 컨테이너를 지우지 않아 같은 이름이나 포트를 다시 쓰지 못하는 일이 흔합니다.

**🎯 할 일**

1. <mark>`docker exec -it web sh`</mark> 로 컨테이너 안에 들어가 nginx 가 응답하는 파일을 봅니다.
2. <mark>`docker stop`</mark> 으로 끄고, `ps` 와 `ps -a` 의 차이를 봅니다.
3. 같은 이름으로 다시 켜면 나오는 <mark>오류</mark>를 읽고, `docker rm` 으로 지웁니다.

**순서**

1. **[터미널]** 컨테이너 안의 터미널을 엽니다. 프롬프트가 `#` 로 바뀝니다.
   ```bash
   docker exec -it web sh
   ```
2. **[컨테이너 안]** nginx 가 응답하는 폴더의 파일을 봅니다. `index.html` 이 보입니다. 브라우저에서 본 **Welcome to nginx!** 가 이 파일입니다. 보고 나서 컨테이너 밖으로 나옵니다.
   ```bash
   ls /usr/share/nginx/html
   exit
   ```
3. **[터미널]** 서버를 끕니다.
   ```bash
   docker stop web
   ```
4. **[브라우저]** `http://127.0.0.1:8080` 을 새로 고쳐 접속이 안 되는 것을 확인합니다.
5. **[터미널]** 끈 뒤의 목록을 두 가지로 봅니다. `docker ps` 에는 `web` 이 안 보이고, `docker ps -a` 에는 `Exited` 로 보입니다.
   ```bash
   docker ps
   docker ps -a
   ```
6. **[터미널]** 같은 이름으로 다시 켜 봅니다. 오류가 나는 것이 정상입니다. 컨테이너가 `Exited` 로 남아 있어서 같은 이름을 쓸 수 없습니다.
   ```bash
   docker run -d --name web -p 8080:80 nginx:1.28
   ```
   `Conflict. The container name "/web" is already in use` 처럼 나옵니다.
7. **[터미널]** 끈 컨테이너를 지우고 다시 켜서 이번에는 켜지는 것을 확인합니다.
   ```bash
   docker rm web
   docker run -d --name web -p 8080:80 nginx:1.28
   docker ps
   ```
8. **[보고서]** `### 문제 6-2` 아래를 채웁니다.
   - (가) 컨테이너 안에서 `ls /usr/share/nginx/html` 로 본 파일 이름을 적어 주세요.
   - (나) 🔍 `docker stop web` 뒤에 `docker ps` 와 `docker ps -a` 에 각각 `web` 이 보이나요? 차이를 설명해 주세요.
   - (다) 🔍 같은 이름으로 다시 `run` 했을 때 나온 오류 문구와, `docker rm` 이 필요한 이유를 적어 주세요.
   - (한 줄) 보안 담당에게 보낼 답을 한 문장으로 적어 주세요.
   - 이 교시에서 새로 알게 된 것 하나를 적어 주세요.

### 6교시 한눈에

| 하려는 일 | 명령 |
|---|---|
| 서버 켜기 | `docker run -d --name 이름 -p 내PC포트:컨테이너포트 이미지:태그` |
| 켜진 것 보기 | `docker ps` (끈 것까지는 `docker ps -a`) |
| 접속 기록 보기 | `docker logs 이름` |
| 컨테이너 안에 들어가기 | `docker exec -it 이름 sh` (나올 때 `exit`) |
| 끄기 · 지우기 | `docker stop 이름` · `docker rm 이름` (켜진 채로 지우기 `docker rm -f 이름`) |

---

# <mark style="display:block; background:#c8e6c9; color:#1a1a1a; padding:6px 12px; border-radius:4px">7교시 (16:00–16:50) · 내 페이지 연결 · 두 서버 · 올리기</mark>

> 📨 **오늘 들어온 일**
> A사 보안 담당이 보낸 메시지: 「서버 화면에 우리 회사 안내 문구를 넣고 싶습니다. 문구 파일은 컨테이너 안이 아니라 제 PC 에 두고 서버가 그걸 쓰게 할 수 있나요? 서버를 두 대 띄우는 것도 해 주세요.」
> - 이 교시에서 하는 일: 컨테이너 안에서 바꾼 파일이 사라지는 것을 확인하고, 내 폴더를 연결해 내 페이지를 띄우고, 서버를 두 대 켠 뒤 오늘 만든 것을 올립니다.
> - 끝나면 쓰는 것: **보고서 한 줄**(보안 담당에게 보낼 답 한 문장)

### 왜 필요한가

1. 컨테이너 안에서 고친 파일은 컨테이너를 지우면 같이 사라집니다. 서버의 설정이나 페이지 파일을 안전하게 두려면 **파일은 내 PC에 두고 컨테이너가 그것을 읽게** 해야 합니다.
2. 서버를 여러 대 켤 때는 **포트 번호가 서버를 구분**합니다(1일 차). 한 PC에서 두 서버를 켜려면 포트를 다르게 연결합니다.
3. 읽기만 하게 연결(`:ro`)하면 컨테이너가 내 파일을 바꾸지 못합니다. 필요한 권한만 주는 최소권한과 같은 생각입니다(6일 차).

### 7.1 컨테이너 안의 변경은 사라진다

```
STEP 1: edit inside container          STEP 2: remove container, run again
+-----------+                          +-----------+
| nginx     |  index.html changed      | nginx     |  index.html is the original
| index.html| --- (remove) --- X       | index.html|  (the change is gone)
+-----------+                          +-----------+
```

컨테이너는 이미지에서 새로 만들어집니다. 지웠다 다시 켜면 이미지에 들어 있던 원래 파일로 돌아갑니다. 바꾼 내용을 지키려면 컨테이너 밖에 파일을 두어야 합니다.

### 7.2 `-v` 로 내 폴더를 연결한다

```
MY PC                                        CONTAINER (nginx)
day06_docker/site-one/index.html  <==(-v)==> /usr/share/nginx/html/index.html (read only)
```

- **`-v`**(volume · 볼륨, 여기서는 바인드 마운트(bind mount) 방식) 는 `내 PC의 폴더:컨테이너 안의 폴더` 를 서로 연결합니다. 내 PC에서 파일을 고치면 서버가 바로 새 파일을 보여 줍니다.
- 끝에 붙인 **`:ro`**(read-only · 리드 온리) 는 컨테이너가 이 폴더를 읽기만 하게 합니다.
- ⚠ **Git Bash 에서는 `-v` 앞에 `MSYS_NO_PATHCONV=1 ` 을 붙입니다.** Git Bash 가 `-v` 뒤 글자를 윈도 경로로 멋대로 바꿔서, 오류 없이 연결만 안 되고 기본 화면이 나옵니다.

```
YOU TYPE:   -v "/c/.../site-one:/usr/share/nginx/html:ro"
GIT BASH CHANGES THE CONTAINER PATH:
            /usr/share/nginx/html --> C:/Program Files/Git/usr/share/nginx/html
RESULT:     no error, but the folder is not connected --> "Welcome to nginx!"
FIX:        put  MSYS_NO_PATHCONV=1  in front of docker run
```

- 맥북에서는 `MSYS_NO_PATHCONV=1 ` 을 붙이지 않아도 됩니다.

### 7.3 서버 두 대, 포트 두 개

```
BROWSER :8080 --> MY PC 8080 ==> CONTAINER web-one (site-one)
BROWSER :8081 --> MY PC 8081 ==> CONTAINER web-two (site-two)
```

두 서버 모두 컨테이너 안에서는 80번 포트를 쓰지만, 내 PC에서는 8080 · 8081 로 나누어 연결하므로 주소의 포트 번호로 서버를 구분합니다.

### 7.4 파일 만들기

작업 폴더 `day06_docker` 를 `network_zt` 안에 만듭니다.

```bash
pwd
mkdir -p day06_docker/site-one day06_docker/site-two
cd day06_docker
pwd
```

- 첫 `pwd` 결과가 `…/network_zt` 로 끝나지 않으면 `cd network_zt` 로 이동한 뒤 다시 합니다. 마지막 `pwd` 가 `…/network_zt/day06_docker` 로 끝나면 됩니다.
- 이 폴더에서 `site-one/index.html` 과 `site-two/index.html` 두 파일을 만듭니다.

### ✍️ 문제 7-1 · 컨테이너 안의 변경이 사라지는 것을 보고, 내 폴더를 연결하기

**📍 이런 상황이 있습니다**

- 보안 담당이 「안내 문구를 서버 안에서 직접 고쳤는데 서버를 다시 켜니 원래대로 돌아갔다」고 합니다. 담당자는 왜 그런지 확인하고, 문구 파일을 내 PC에 두고 서버가 읽게 만들어야 합니다.
- 현업에서는 이렇게 컨테이너 안에서 고친 설정이 날아가는 일이 처음 쓰는 사람의 흔한 사고입니다.

**🎯 할 일**

1. 컨테이너 안에서 <mark>`index.html` 을 바꿔</mark> 화면이 바뀌는 것을 봅니다.
2. 컨테이너를 지우고 다시 켜서 <mark>원래 화면으로 돌아가는 것</mark>을 봅니다.
3. 내 PC에 <mark>`site-one/index.html`</mark> 을 만들고 `-v` 로 연결해 내 페이지를 띄웁니다. 먼저 `MSYS_NO_PATHCONV=1` 을 빼고 해 보고, 그다음 붙여서 해 봅니다.

**순서**

1. **[터미널]** 6교시의 `web` 이 켜져 있는지 봅니다. 없으면 켭니다.
   ```bash
   docker ps
   docker run -d --name web -p 8080:80 nginx:1.28
   ```
   `web` 이 이미 있다고 오류가 나면 이미 켜져 있는 것이니 다음으로 갑니다.
2. **[터미널]** 컨테이너 안으로 들어가 페이지 파일을 바꿉니다. 안에서는 아래 한 줄을 치고 `exit` 로 나옵니다.
   ```bash
   docker exec -it web sh
   ```
   ```bash
   echo '<h1>inside</h1>' > /usr/share/nginx/html/index.html
   exit
   ```
3. **[브라우저]** `http://127.0.0.1:8080` 을 새로 고쳐 **inside** 로 바뀐 것을 확인합니다.
4. **[터미널]** 컨테이너를 지우고 같은 명령으로 다시 켭니다.
   ```bash
   docker rm -f web
   docker run -d --name web -p 8080:80 nginx:1.28
   ```
5. **[브라우저]** `http://127.0.0.1:8080` 을 새로 고쳐 어떤 화면인지 확인합니다. 바꾼 내용이 사라지고 원래 화면으로 돌아갑니다.
6. **[터미널]** 이 컨테이너를 지우고 내 페이지 파일을 만듭니다. 7.4 의 폴더 안(`day06_docker`)에서 `site-one/index.html` 을 만듭니다. 아래 둘 중 **하나만** 고릅니다.
   ```bash
   docker rm -f web
   ```
   - **vim**: `vim site-one/index.html` → `i` → 글 입력 → `Esc` → `:wq` Enter
   - **touch**: `touch site-one/index.html` → VS Code 에서 파일을 열어 글 입력

   파일 내용입니다.
   ```html
   <meta charset="utf-8">
   <h1>site-one</h1>
   <p>첫 번째 서버입니다</p>
   ```
7. **[터미널]** 먼저 `MSYS_NO_PATHCONV=1` **없이** 연결해 봅니다. 오류는 안 나지만 연결이 안 됩니다.
   ```bash
   docker run -d --name web-one -p 8080:80 -v "$(pwd)/site-one:/usr/share/nginx/html:ro" nginx:1.28
   ```
8. **[브라우저]** `http://127.0.0.1:8080` 을 열어 **Welcome to nginx!** 가 나오는 것을 확인합니다. 내 파일이 연결되지 않은 것입니다. 이제 지우고 이번에는 앞에 `MSYS_NO_PATHCONV=1 ` 을 붙여 다시 켭니다. 맥북은 첫 줄을 건너뛰고 바로 두 번째 줄만 칩니다.
   ```bash
   docker rm -f web-one
   MSYS_NO_PATHCONV=1 docker run -d --name web-one -p 8080:80 -v "$(pwd)/site-one:/usr/share/nginx/html:ro" nginx:1.28
   ```
9. **[브라우저]** `http://127.0.0.1:8080` 을 새로 고쳐 **site-one** 이 보이는지 확인합니다.
10. **[보고서]** `day06_pm_report.md` 의 `## 7교시` › `### 문제 7-1` 아래를 채웁니다.
    - (가) 컨테이너 안에서 바꾼 뒤 `docker rm -f web` 으로 지우고 다시 켰을 때 화면이 어떻게 되었는지 적어 주세요.
    - (나) 🔍 컨테이너 안에서 바꾼 내용이 사라진 이유와, `-v` 로 폴더를 연결하면 무엇이 달라지는지 적어 주세요.
    - (다) 🔍 `MSYS_NO_PATHCONV=1` 없이 `-v` 를 실행했을 때 화면에 무엇이 나왔고 왜 그랬는지 적어 주세요.

### ✍️ 문제 7-2 · 두 번째 서버를 켜고, 파일을 고쳐 새로고침하고, 정리하기

**📍 이런 상황이 있습니다**

- 보안 담당이 「두 번째 안내 페이지도 다른 포트로 띄우고, 문구를 고치면 바로 반영되는지 보여 달라」고 합니다. 담당자는 서버 두 대를 한 PC에 켜고, 파일을 고쳐 새로 고쳤을 때 반영되는지, 정리까지 확인해야 합니다.
- 현업에서는 같은 서버 이미지로 서비스를 나눠 띄우고, 포트로 구분합니다.

**🎯 할 일**

1. <mark>`site-two/index.html`</mark> 을 만들고 8081 포트로 두 번째 서버를 켭니다.
2. `docker ps` 의 <mark>PORTS 열 두 줄</mark>을 읽습니다.
3. <mark>`site-one/index.html` 을 고치고</mark> 새로 고쳐 반영되는 것을 봅니다.
4. 두 서버를 <mark>정리</mark>합니다.

**순서**

1. **[터미널]** `site-two/index.html` 을 만듭니다. 아래 둘 중 **하나만** 고릅니다.
   - **vim**: `vim site-two/index.html` → `i` → 글 입력 → `Esc` → `:wq` Enter
   - **touch**: `touch site-two/index.html` → VS Code 에서 파일을 열어 글 입력

   파일 내용입니다.
   ```html
   <meta charset="utf-8">
   <h1>site-two</h1>
   <p>두 번째 서버입니다</p>
   ```
2. **[터미널]** 두 번째 서버를 8081 포트로 켭니다. 맥북은 `MSYS_NO_PATHCONV=1 ` 을 빼고 칩니다.
   ```bash
   MSYS_NO_PATHCONV=1 docker run -d --name web-two -p 8081:80 -v "$(pwd)/site-two:/usr/share/nginx/html:ro" nginx:1.28
   ```
3. **[브라우저]** `http://127.0.0.1:8080` 에서 **site-one**, `http://127.0.0.1:8081` 에서 **site-two** 가 보이는지 확인합니다.
4. **[터미널]** 두 서버를 한 번에 봅니다. `PORTS` 열의 포트 번호가 서로 다른 것을 읽습니다.
   ```bash
   docker ps
   ```
5. **[터미널]** `site-one/index.html` 의 `<p>` 줄을 다른 문구로 고쳐 저장합니다(vim 이면 `vim site-one/index.html`).
6. **[브라우저]** `http://127.0.0.1:8080` 을 새로 고쳐 바뀐 문구가 바로 보이는지 확인합니다. 컨테이너를 다시 켜지 않아도 반영됩니다.
7. **[터미널]** 두 서버를 정리합니다. `docker ps -a` 에 `hello-world` 만 남으면 됩니다.
   ```bash
   docker rm -f web-one web-two
   docker ps -a
   ```
8. **[보고서]** `### 문제 7-2` 아래를 채웁니다.
   - (가) 두 주소(`8080` · `8081`)에서 보이는 화면을 각각 적어 주세요.
   - (나) 🔍 `docker ps` 의 PORTS 열에서 두 서버를 구분해 주는 것은 무엇인가요?
   - (다) 🔍 `:ro` 는 무슨 뜻이고, 왜 읽기 전용으로 연결하나요?
   - (한 줄) 보안 담당에게 보낼 답을 한 문장으로 적어 주세요.
   - 이 교시에서 새로 알게 된 것 하나를 적어 주세요.

### ✍️ 문제 7-3 · 오늘 만든 것을 깃허브에 올리기

**📍 이런 상황이 있습니다**

- 팀장이 「오늘 만든 서버 페이지와 보고서를 저장소에 남겨 달라」고 합니다. 올리기 전에 올라갈 파일을 확인하고, 비밀 키 파일(`.env`)이 섞이지 않았는지 봐야 합니다.

**🎯 할 일**

1. 터미널에서 <mark>`git status`</mark> 로 올라갈 파일을 확인합니다.
2. <mark>`git add .` → `git commit` → `git push`</mark> 순서로 올립니다.
3. 깃허브에서 <mark>`day06_docker` 폴더와 보고서 두 개</mark>가 보이는지 확인합니다.

**순서**

1. **[터미널]** `security-agent-toolkit` 폴더로 옮기고 위치를 확인합니다. 결과가 `…/security-agent-toolkit` 으로 끝나야 합니다.
   ```bash
   cd ../..
   pwd
   ```
2. **[터미널]** 무엇이 바뀌었는지 먼저 봅니다. 빨간 목록에 `.env` 나 `.venv` 가 보이면 올리지 않고 멈춥니다.
   - `.env` 가 보이면: VS Code 왼쪽 목록에서 `security-agent-toolkit` 바로 아래의 `.gitignore` 를 열어 맨 아래에 `.env` 한 줄을 적고 저장한 뒤 `git status` 를 다시 칩니다. `.venv` 도 같은 방법으로 합니다.
   - `Untracked files:` 나 `modified:` 아래에 나오는 줄이 올라갈 파일입니다. 오늘 만든 `site-one` · `site-two` 폴더와 보고서 파일이 보여야 합니다.
   ```bash
   git status
   ```
3. **[보고서]** `### 문제 7-3` 아래를 채웁니다. 올리기 전에 채워야 깃허브에 빈칸 없이 올라갑니다.
   - (가) `git status` 를 쳤을 때 빨간 목록에 줄이 몇 개였는지, 그 가운데 `.env` · `.venv` 가 있었는지 적어 주세요.
4. **[터미널]** 바뀐 파일을 모두 담고(`add`), 기록하고(`commit`), 올립니다(`push`).
   ```bash
   git add .
   git commit -m "Add day 6 docker practice pages and report"
   git push
   ```
   - `git push` 가 거절(`rejected`)되면 `git pull` 을 입력해 받아 온 뒤 `git push` 를 다시 합니다
   - 편집기 화면이 뜨면 `Esc` 를 누르고 `:wq` 를 입력한 뒤 `Enter` 를 누릅니다
5. **[브라우저]** 깃허브의 내 저장소를 새로 고쳐 `network_zt` 폴더 안에 `day06_docker` 폴더와 오전 · 오후 보고서가 있는지 확인합니다.

### 7교시 한눈에

| 하려는 일 | 명령 |
|---|---|
| 내 폴더를 서버에 연결 | `MSYS_NO_PATHCONV=1 docker run -d --name 이름 -p 포트:80 -v "$(pwd)/폴더:/usr/share/nginx/html:ro" nginx:1.28` |
| 컨테이너 안에서 바꾼 것 | 컨테이너를 지우면 사라진다 → 파일은 내 PC에 두고 `-v` 로 연결 |
| 서버 두 대 | 내 PC 포트를 다르게 연결(8080 · 8081) |
| 읽기만 연결 | `:ro` |
| 한꺼번에 정리 | `docker rm -f 이름1 이름2` |

---

## 오늘 마무리

| 확인 | 문제 |
|---|---|
| Docker 가 설치되고 `hello-world` 가 실행됐다 | 5-1 |
| 이미지와 컨테이너의 차이를 `images` · `ps -a` 로 구분했다 | 5-1 |
| 포트를 연결해야 접속된다는 것을 직접 확인했다 | 6-1 |
| 접속 기록 한 줄을 읽었다 | 6-1 |
| 컨테이너 안을 들여다보고, 끄고, 지웠다 | 6-2 |
| 컨테이너 안의 변경이 사라지는 것을 보고 `-v` 로 내 폴더를 연결했다 | 7-1 |
| 서버 두 대를 포트로 구분해 켰다 | 7-2 |
| 오늘 만든 파일과 보고서를 깃허브에 올렸다 | 7-3 |

내일(10/20(화)) 오후에는 이미지를 직접 만들고(Dockerfile), 서버 여러 개를 파일 하나로 켜고(compose), 서버가 안 열릴 때 어디를 볼지 읽는 연습을 합니다.

---

# 정답 · 먼저 풀어 본 뒤에 봅니다

설명하는 답은 한 예이고, 핵심이 같으면 맞습니다.

---

### 정답 5-1

💻 **터미널에 입력합니다.**

```bash
docker --version
docker run hello-world
docker images
docker ps -a
```

**결과**

- (가) 한 예: `Docker version 29.8.2, build 7fc2dff`. 숫자는 내려받은 시기에 따라 다릅니다.
- (나) ① 터미널의 `docker` 명령(클라이언트)이 엔진(데몬)에 요청합니다(출력의 1번). ② 엔진이 `hello-world` 이미지가 PC에 없어서 Docker Hub 에서 받습니다(2번, `Pulling from library/hello-world`). ③ 받은 이미지로 컨테이너를 만들어 실행합니다(3번). ④ 컨테이너가 만든 글자를 엔진이 터미널로 보내 화면에 `Hello from Docker!` 가 나옵니다(4번).
- (다) `docker images` 에 보인 `hello-world` 는 **이미지**입니다. 받아 둔 읽기 전용 묶음이고 컨테이너를 지워도 남습니다. `docker ps -a` 에 보인 `hello-world` 는 **컨테이너**입니다. 그 이미지를 실행한 것이고 글자를 출력한 뒤 끝나서 `Exited` 로 남습니다.

**왜** — 이미지는 받아 둔 묶음이고 컨테이너는 그것을 실행한 결과입니다. 둘을 나누어 보면 「지운다」가 무엇을 지우는지 헷갈리지 않습니다.

**자주 틀리는 곳** — `hello-world` 를 여러 번 쳐서 컨테이너가 여러 개 쌓이는 경우가 많습니다. 같은 이미지에서 컨테이너가 여러 개 생기는 것은 정상입니다. 터미널을 설치 전에 열어 둔 채로 `docker: command not found` 가 나오는 경우도 많습니다. 터미널을 모두 닫았다가 다시 엽니다.

**관제에서는** — 새 서버나 PC에 도구를 올린 뒤 `--version` 과 `hello-world` 로 동작을 확인하는 것이 첫 점검입니다.

---

### 정답 5-2

💻 **터미널에 입력합니다.**

```bash
docker pull nginxx
```

**결과**

- (가) `nginx` 는 **이미지 이름**(어떤 프로그램인가)을 정하고, `1.28` 은 **태그**(어느 버전인가)를 정합니다. 태그를 안 쓰면 `latest`(최신)가 선택돼 시기마다 버전이 달라질 수 있어서, 같은 서버를 만들려면 `nginx:1.28` 처럼 태그를 씁니다.
- (나) `pull access denied for nginxx, repository does not exist or may require 'docker login'` 입니다. 뜻은 「`nginxx` 라는 이미지는 Docker Hub 에 없거나, 있어도 로그인해야 받을 수 있다」입니다. 이름의 오타이므로 `nginx` 로 고쳐 씁니다.
- (한 줄) 예: 「도커는 같은 이미지를 받아 실행하므로 어느 PC에서나 같은 서버를 똑같이 띄울 수 있고, 이미지 이름과 태그를 정확히 써야 합니다.」

**왜** — 이미지 이름과 태그가 곧 서버의 종류와 버전입니다. 같은 이름과 태그면 어디서나 같은 서버가 됩니다.

**자주 틀리는 곳** — 태그 없이 `nginx` 만 쓰면 매번 같은 서버가 된다고 오해하는 경우가 많습니다. 오타 오류를 「인터넷이 안 된다」로 읽는 경우도 있습니다. 오류 문구에 `repository does not exist` 가 있으면 이름 문제입니다.

**관제에서는** — 이미지 이름과 태그가 정확히 같은지 확인하는 것이 같은 환경을 재현하는 첫 단계입니다. 출처가 불분명한 이미지는 쓰지 않고 공식 이미지를 씁니다.

---

### 정답 6-1

💻 **터미널에 입력합니다.**

```bash
docker run -d --name web nginx:1.28
docker ps
docker rm -f web
docker run -d --name web -p 8080:80 nginx:1.28
docker ps
docker logs web
```

**결과**

- (가) 브라우저에서 `http://127.0.0.1:8080` 에 접속하면 연결할 수 없다는 오류가 나옵니다. 컨테이너는 켜져 있지만(`docker ps` 에서 `Up`) 내 PC의 8080 포트와 연결돼 있지 않아서 브라우저가 닿을 길이 없습니다. `PORTS` 열에 `80/tcp` 만 있고 `->` 가 없습니다.
- (나) `-p 8080:80` 은 **내 PC의 8080 포트**로 온 요청을 **컨테이너 안의 80 포트**로 넘기게 연결합니다. 앞의 숫자는 내 PC 쪽(브라우저가 접속하는 곳), 뒤의 숫자는 컨테이너 쪽(nginx 가 듣는 곳)입니다. 연결이 되면 `PORTS` 열에 `0.0.0.0:8080->80/tcp` 로 나옵니다.
- (다) 한 예: `172.17.0.1 - - [19/Oct/2026:14:31:05 +0000] "GET / HTTP/1.1" 200 615 "-" "Mozilla/5.0 ..."` 에서 접속자 주소는 `172.17.0.1`, 시각은 `19/Oct/2026:14:31:05`, 요청은 `GET /`(주소 `/` 를 달라는 요청), 응답 번호는 `200`(성공)입니다. 접속자 주소는 PC마다 다르게 보입니다.

**왜** — 컨테이너는 기본적으로 밖에서 접속할 수 없게 막혀 있어서, 접속하게 하려면 포트를 연결해야 합니다. 이 연결이 서버를 어디까지 열지를 정하는 출발점입니다(화요일에 이어서 봅니다).

**자주 틀리는 곳** — 앞뒤 숫자를 바꿔 `-p 80:8080` 으로 쓰는 경우가 많습니다. 앞이 내 PC, 뒤가 컨테이너입니다. 컨테이너가 켜져 있으니 접속된다고 생각하는 경우도 많은데, 켜진 것과 접속되는 것은 다릅니다. `docker rm -f web` 없이 같은 이름으로 다시 켜서 이름 충돌이 나는 경우도 있습니다.

**관제에서는** — 「서버는 켜졌는데 접속이 안 된다」가 오면 먼저 `docker ps` 의 `PORTS` 열을 봅니다. 접속 기록은 `logs` 로 보고, 요청 주소 · 시각 · 응답 번호가 분석할 원자료입니다.

---

### 정답 6-2

💻 **터미널에 입력합니다.**

```bash
docker exec -it web sh
ls /usr/share/nginx/html
exit
docker stop web
docker ps
docker ps -a
docker run -d --name web -p 8080:80 nginx:1.28
docker rm web
docker run -d --name web -p 8080:80 nginx:1.28
```

**결과**

- (가) `50x.html` 과 `index.html` 두 개가 보입니다. `index.html` 이 브라우저의 **Welcome to nginx!** 화면입니다. 파일 이름은 이미지 버전에 따라 조금 다를 수 있습니다.
- (나) `docker ps` 는 **실행 중인** 컨테이너만 보여 주므로 `web` 이 안 보입니다. `docker ps -a` 는 멈춘 것까지 모두 보여 주므로 `web` 이 `Exited` 로 보입니다. 끈 컨테이너는 지워지는 것이 아니라 멈춘 채로 남습니다.
- (다) `Conflict. The container name "/web" is already in use` 처럼 나옵니다. 끈 `web` 이 `Exited` 로 남아 있어서 같은 이름을 쓸 수 없다는 뜻입니다. `docker rm web` 으로 지워야 같은 이름으로 다시 만들 수 있습니다.
- (한 줄) 예: 「nginx 서버는 `docker run -d --name web -p 8080:80 nginx:1.28` 로 켜고, 접속 기록은 `docker logs web` 으로 확인하고, 끌 때는 `stop` 뒤 `rm` 으로 지워야 같은 이름을 다시 쓸 수 있습니다.」

**왜** — 켜고 · 보고 · 끄고 · 지우는 흐름을 한 번 돌려 봐야, 이름이나 포트가 막혔을 때 무엇을 정리할지 압니다.

**자주 틀리는 곳** — `docker ps` 에 안 보이니 지워졌다고 생각하는 경우가 가장 많습니다. `exit` 를 안 치고 새 명령을 쳐서 컨테이너 안에서 명령이 실행되는 경우도 있습니다. 프롬프트가 `#` 이면 아직 컨테이너 안입니다.

**관제에서는** — 정리하지 않은 멈춘 컨테이너가 쌓이면 이름과 포트가 막히고 어떤 것이 쓰이는 것인지 알기 어렵습니다. `ps -a` 로 점검하고 필요 없는 것은 지웁니다.

---

### 정답 7-1

💻 **터미널에 입력합니다.**

```bash
docker exec -it web sh
docker rm -f web
docker run -d --name web -p 8080:80 nginx:1.28
docker rm -f web
docker run -d --name web-one -p 8080:80 -v "$(pwd)/site-one:/usr/share/nginx/html:ro" nginx:1.28
docker rm -f web-one
MSYS_NO_PATHCONV=1 docker run -d --name web-one -p 8080:80 -v "$(pwd)/site-one:/usr/share/nginx/html:ro" nginx:1.28
```

**결과**

- (가) 컨테이너 안에서 바꾼 뒤 `docker rm -f web` 으로 지우고 같은 명령으로 다시 켜면, 화면이 바꾼 **inside** 에서 원래의 **Welcome to nginx!** 로 돌아갑니다.
- (나) 컨테이너는 이미지에서 새로 만들어지고, 지우면 컨테이너 안에서 바꾼 파일도 같이 사라지기 때문입니다. 다시 켜면 이미지에 들어 있던 원래 파일로 시작합니다. `-v` 로 내 PC의 폴더를 연결하면 파일은 **내 PC에** 있고 컨테이너는 그것을 읽기만 합니다. 컨테이너를 지웠다 다시 켜도 내 파일은 그대로이고, 내 PC에서 고치면 서버에 바로 반영됩니다.
- (다) `MSYS_NO_PATHCONV=1` 없이 실행하면 오류는 나지 않고 **Welcome to nginx!** 기본 화면이 나옵니다. Git Bash 가 `-v` 뒤의 컨테이너 쪽 경로(`/usr/share/nginx/html`)를 윈도 경로(`C:/Program Files/Git/usr/share/nginx/html`)로 바꿔서 연결이 엉뚱한 곳에 됐기 때문입니다. 앞에 `MSYS_NO_PATHCONV=1` 을 붙이면 경로를 바꾸지 않아 내 폴더가 연결됩니다.

**왜** — 컨테이너 안의 변경은 일시적이고, 지킬 파일은 컨테이너 밖에 두어야 합니다. 오류 없이 연결만 안 되는 경우는 겉으로 성공한 것처럼 보여서 더 찾기 어렵습니다.

**자주 틀리는 곳** — 화면에 **Welcome to nginx!** 가 나오는데 내 파일이 연결됐다고 생각하는 경우가 많습니다. 내 파일 문구가 보여야 연결된 것입니다. `$(pwd)` 위치가 `day06_docker` 가 아니어서 `site-one` 폴더를 못 찾는 경우도 많습니다. `pwd` 로 위치를 확인합니다. `web` 을 지우지 않고 같은 8080 포트로 켜서 `port is already allocated` 가 나는 경우도 있습니다.

**관제에서는** — 컨테이너에는 설정과 데이터를 넣지 않고 밖에 두어 연결합니다. 연결이 제대로 됐는지는 화면이 아니라 내 파일의 내용이 나오는지로 확인합니다.

---

### 정답 7-2

💻 **터미널에 입력합니다.**

```bash
MSYS_NO_PATHCONV=1 docker run -d --name web-two -p 8081:80 -v "$(pwd)/site-two:/usr/share/nginx/html:ro" nginx:1.28
docker ps
docker rm -f web-one web-two
docker ps -a
```

**결과**

- (가) `http://127.0.0.1:8080` 에는 **site-one** 과 「첫 번째 서버입니다」(또는 고친 문구)가, `http://127.0.0.1:8081` 에는 **site-two** 와 「두 번째 서버입니다」가 보입니다.
- (나) `PORTS` 열의 **내 PC 쪽 포트 번호**입니다. 한 줄은 `0.0.0.0:8080->80/tcp`, 다른 줄은 `0.0.0.0:8081->80/tcp` 로 나옵니다. 컨테이너 안은 둘 다 80번이지만 내 PC에서는 8080 · 8081 로 나뉘어 있어서, 주소의 포트 번호로 어느 서버인지 구분합니다.
- (다) `:ro` 는 **read-only**(읽기 전용)입니다. 컨테이너가 연결된 폴더를 읽기만 하고 바꾸지 못하게 합니다. 서버에 문제가 생기거나 공격을 받아도 내 PC의 원본 파일을 지우거나 바꿀 수 없어서, 필요한 권한(읽기)만 주는 최소권한과 같은 생각입니다.
- (한 줄) 예: 「안내 페이지 파일은 내 PC에 두고 `-v ... :ro` 로 연결해 서버 두 대를 8080 · 8081 포트로 띄웠고, 파일을 고치면 서버를 다시 켜지 않아도 반영됩니다.」

**왜** — 포트가 서버를 구분하고, 읽기 전용으로 연결하면 컨테이너가 내 파일을 건드리지 못합니다. 같은 이미지로 서버를 여러 대 띄워도 파일과 포트만 다르게 하면 됩니다.

**자주 틀리는 곳** — 두 서버를 같은 포트(예: 둘 다 8080)로 켜서 `port is already allocated` 가 나는 경우가 많습니다. 파일을 고쳤는데 반영이 안 된다며 컨테이너를 다시 켜는 경우도 있는데, `-v` 로 연결했으면 새로 고침만으로 반영됩니다. 브라우저가 이전 화면을 보여 줄 때는 `Ctrl + F5` 로 새로 고칩니다.

**관제에서는** — 한 PC에서 여러 서버를 돌릴 때 `docker ps` 의 `PORTS` 열로 어느 포트가 어느 서버인지, 어느 포트가 열려 있는지 확인하는 것이 점검의 기본입니다.

---

### 정답 7-3

💻 **터미널에 입력합니다.**

```bash
cd ../..
pwd
git status
git add .
git commit -m "Add day 6 docker practice pages and report"
git push
```

**결과**

- (가) 한 예: 「줄이 3개였고(`day06_docker/` 폴더, 오후 보고서 `day06_pm_report.md`, 안내 문서 등), `.env` · `.venv` 는 없었다」. 줄 수와 이름은 학생마다 다를 수 있습니다. `.env` 나 `.venv` 가 보였다면 `.gitignore` 에 한 줄을 적고 `git status` 를 다시 쳤다고 적습니다.

**왜** — 올리기 전에 올라갈 파일을 확인해야 비밀 키가 섞이지 않습니다. 저장소에 남기면 누가 언제 무엇을 했는지 기록이 남고 다음 사람이 이어받을 수 있습니다.

**자주 틀리는 곳** — `.env` 가 보이는데 그대로 `git add .` 를 하는 실수가 가장 위험합니다. 멈추고 `.gitignore` 를 확인합니다. 올린 뒤 브라우저에서 확인하지 않으면 올라갔는지 알 수 없습니다.

**관제에서는** — 작업 결과와 설정을 저장소에 남기면 사고 때 같은 환경을 다시 만들 수 있습니다. 비밀 키는 저장소에 올리지 않습니다.
