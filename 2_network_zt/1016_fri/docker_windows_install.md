# Docker Desktop 윈도 설치 — 월요일 오후 수업 준비

월요일(10/19(월)) 오후부터 Docker 를 씁니다. 이 문서는 **윈도 PC 에 Docker Desktop 을 내려받아 설치하고, 잘 설치됐는지 확인**하는 순서입니다. 설치는 한 번만 하면 됩니다.

- **Docker Desktop**(도커 데스크톱)
  - 윈도에서 Docker 를 쓰게 해 주는 프로그램. 설치하면 터미널에서 `docker` 명령을 칠 수 있다
- **WSL 2**(Windows Subsystem for Linux 2 · 더블유에스엘 투)
  - 윈도 안에서 리눅스를 돌리는 기능. Docker Desktop 이 이 위에서 컨테이너를 실행한다(기본 방식)
- 확인한 내용은 Docker 공식 문서(`docs.docker.com/desktop/setup/install/windows-install/`)와 Microsoft 공식 문서(`learn.microsoft.com/windows/wsl/install`)에서 가져왔습니다.

---

## 1. 설치 전에 확인합니다

| 확인할 것 | 필요한 조건 | 확인하는 법 |
|---|---|---|
| 윈도 버전 | Windows 10 **22H2**(빌드 19045) 이상, 또는 Windows 11 **23H2**(빌드 22631) 이상. 64비트. 공식 문서에 적힌 에디션은 Pro · Enterprise · Education | `Win + R` 을 누르고 `winver` 입력 → Enter |
| 메모리 | 8GB 이상 | 설정 › 시스템 › 정보 |
| 가상화 | 켜져 있어야 함(BIOS/UEFI 설정) | 작업 관리자(`Ctrl + Shift + Esc`) › 성능 › CPU › 「가상화: 사용」 |

- 가상화가 「사용 안 함」이면 BIOS/UEFI 에서 켜야 합니다. 학원 PC 는 설정을 바꿀 수 없을 수 있으니, 그때는 이 문서 아래 「막힐 때」를 봅니다.
- 에디션이 Home 이면 위 공식 문서에는 나오지 않습니다. 설치 중 막히면 막힌 화면 그대로 알려 주세요.

## 2. 설치 파일을 내려받습니다

1. **[브라우저]** Docker 공식 문서 `https://docs.docker.com/desktop/setup/install/windows-install/` 를 엽니다.
2. **[브라우저]** 페이지의 **Docker Desktop for Windows** 다운로드 단추를 눌러 `Docker Desktop Installer.exe` 를 받습니다. 대부분의 PC 는 AMD64(x86) 용입니다.
3. 내려받은 파일이 `다운로드` 폴더에 있는지 확인합니다.

## 3. 설치합니다

1. **[탐색기]** `Docker Desktop Installer.exe` 를 두 번 눌러 실행합니다.
2. 설치 방식을 묻는 화면이 나옵니다.
   - **WSL 2** 를 고릅니다(기본값, 공식 문서가 권장). 이 방식은 관리자 권한이 없어도 설치할 수 있다고 공식 문서에 적혀 있습니다(계정별 설치).
3. 설치 마법사의 안내를 따라 끝까지 진행합니다.
4. 설치가 끝나면 **윈도를 다시 시작**하라는 안내가 나올 수 있습니다. 다시 시작합니다.

### WSL 이 없다고 나오면

수업 때 쓰는 **터미널**(VS Code 에서 여는 그 터미널)에서 그대로 합니다. 학원 PC 에서 이렇게 해서 설치되는 것을 확인했습니다.

1. **[터미널]** 아래 명령을 입력하고 Enter 를 누릅니다. 진행 막대(`%`)가 100% 까지 올라가고 「요청한 작업이 잘 실행되었습니다. 시스템을 다시 시작하면 변경 사항이 적용됩니다.」가 나오면 성공입니다. 글자가 조금 섞여 보여도 괜찮습니다. (Windows 10 2004 이상 또는 Windows 11 에서 쓰는 명령입니다)
   ```bash
   wsl --install
   ```
2. **윈도를 다시 시작**합니다. 다시 시작해야 변경 사항이 적용됩니다.
3. 다시 시작한 뒤 위 3번 설치를 이어서 합니다.

- 「권한이 없다」는 오류가 나면, 시작 메뉴에서 PowerShell 을 **오른쪽 클릭 › 관리자 권한으로 실행**해 같은 명령 `wsl --install` 을 입력합니다. (Microsoft 문서는 관리자 권한에서 실행하라고 안내합니다)

## 4. Docker Desktop 을 처음 켭니다

1. **[윈도]** 시작 메뉴에서 **Docker Desktop** 을 검색해 실행합니다.
2. 처음에는 **Docker Subscription Service Agreement**(구독 서비스 약관) 동의 화면이 나옵니다. 동의해야 실행됩니다. 개인 · 교육 · 소규모 회사는 무료라고 공식 문서에 적혀 있습니다.
3. 창 아래쪽에 고래 모양과 함께 **Engine running**(초록색)이 보일 때까지 기다립니다. 처음에는 몇 분 걸릴 수 있습니다.
4. 작업 표시줄 오른쪽 아래에 고래 아이콘이 생깁니다. 이 아이콘이 있어야 `docker` 명령이 동작합니다. **Docker Desktop 을 끄지 말고 켜 둔 채로** 아래를 확인합니다.

## 5. 잘 설치됐는지 확인합니다

수업 때 쓰는 터미널(Git Bash)에서 확인합니다.

1. **[터미널]** 버전을 확인합니다. 숫자가 나오면 됩니다.
   ```bash
   docker --version
   ```
   예: `Docker version 28.x.x, build ...` (숫자는 내려받은 시기에 따라 다릅니다)
2. **[터미널]** 첫 컨테이너를 실행해 봅니다. `hello-world` 는 설치가 잘 됐는지 확인하는 연습용 컨테이너입니다.
   ```bash
   docker run hello-world
   ```
3. 처음에는 이미지를 내려받는 줄(`Unable to find image ... locally` → `Pulling from library/hello-world`)이 나온 뒤, 아래 문장이 나오면 성공입니다.
   ```
   Hello from Docker!
   This message shows that your installation appears to be working correctly.
   ```
4. **[터미널]** 방금 실행한 컨테이너 기록을 봅니다. `hello-world` 줄이 보이면 됩니다.
   ```bash
   docker ps -a
   ```

## 6. 설치가 끝났는지 체크합니다

| 확인 | 됐으면 ✔ |
|---|---|
| Docker Desktop 창에 **Engine running** 이 보인다 | |
| `docker --version` 에 버전이 나온다 | |
| `docker run hello-world` 에 `Hello from Docker!` 가 나온다 | |
| `docker ps -a` 에 `hello-world` 줄이 보인다 | |

---

## 막힐 때

| 증상 | 이유 | 해결 |
|---|---|---|
| 「가상화가 꺼져 있다」는 안내, 또는 Docker Desktop 이 시작되지 않는다 | BIOS/UEFI 에서 가상화가 꺼져 있다 | 작업 관리자 › 성능 › CPU 에서 「가상화」를 확인합니다. 꺼져 있으면 BIOS/UEFI 설정이 필요합니다 |
| 「WSL 2 가 설치되지 않았다」는 안내 | WSL 이 없거나 오래됐다 | 위 「WSL 이 없다고 나오면」의 `wsl --install` 을 관리자 PowerShell 에서 실행하고 재시작합니다. 이미 설치돼 있으면 `wsl --update` 를 해 봅니다 |
| `docker: command not found` (Git Bash) | Docker Desktop 이 꺼져 있거나, 터미널이 설치 전에 열렸다 | Docker Desktop 이 켜져 있는지 보고, **터미널을 모두 닫았다가 다시 엽니다** |
| 설치 중 관리자 권한을 요구하거나 권한 오류가 난다 | 모든 사용자용 설치를 골랐다 | 계정별 설치(WSL 2)를 고릅니다. 모든 사용자용으로 설치했는데 일반 계정이면 관리자가 `net localgroup docker-users 사용자이름 /add` 를 실행해야 합니다 |
| Engine 이 계속 시작 중(노란색)이다 | 처음 시작에는 오래 걸린다 | 몇 분 기다립니다. 계속 안 되면 Docker Desktop 을 종료했다가 다시 실행합니다 |

- 어디서 막혔는지 알려 줄 때는 **화면 그대로**(오류 문구가 보이는 창)를 같이 보내 주세요.

## 설치한 뒤에는

- Docker Desktop 은 **월요일 수업 전에 켜 두지 않아도** 됩니다. 수업 때 시작 메뉴에서 실행하면 됩니다.
- 월요일 오후에는 nginx 라는 웹 서버를 `docker run` 으로 띄우고, `docker ps` · `docker logs` · `docker stop` 으로 상태를 보는 것을 합니다.
