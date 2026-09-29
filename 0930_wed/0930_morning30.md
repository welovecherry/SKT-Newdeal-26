# 아침 과제 3 · requests를 준비하고 GitHub에 노트북 올리기

9월 30일 (수) · 아침 과제

**오늘 하는 일:** Windows용 VS Code 노트북에서 `requests`를 준비하고, GitHub 웹 화면에서 security-agent-toolkit 리포지토리를 만들어 9/29까지 배운 실습 노트북을 올립니다.

터미널이나 명령 프롬프트에는 명령어를 입력하지 않습니다. `requests` 설치 명령은 VS Code 노트북의 **코드 셀**에서 실행합니다. 리포지토리와 폴더 만들기·파일 업로드는 GitHub 웹 화면에서 합니다.

**오늘 못 끝냈으면 10/2(금) 아침에 이어서 합니다.** 오늘 오후는 다른 강사님 수업입니다.

---

## 1. Windows용 VS Code 노트북에서 requests를 설치합니다

Python이 없다면 [Python 공식 Windows 다운로드 페이지](https://www.python.org/downloads/windows/)에서 Python 3.12.x를 설치합니다. VS Code가 없다면 먼저 설치하고, 확장 프로그램에서 Microsoft의 **Python**과 **Jupyter**를 설치합니다. 작업할 폴더가 없다면 새 폴더를 하나 만든 뒤, VS Code에서 **File > Open Folder**로 그 폴더를 엽니다. 수업 노트북 `01_0930_am_requests_api_client.ipynb`도 이 폴더에 저장하고 엽니다.

노트북을 연 뒤 아래 순서대로 진행합니다.

1. 노트북 **오른쪽 위의 Select Kernel**을 누릅니다.
2. **Create Python Environment**를 선택하고 **Quick Create**를 누릅니다.
3. 만들어진 **`.venv (Python 3.x)`**를 커널로 선택합니다. 셀을 실행할 때 `ipykernel` 설치 안내가 나오면 **Install**을 누릅니다.
4. 새 코드 셀에 아래 줄을 입력하고 왼쪽의 ▶ 버튼을 눌러 실행합니다.

   ```python
   %pip install requests
   ```

5. 설치가 끝나면 새 코드 셀에서 아래 줄을 실행합니다.

   ```python
   import requests
   ```

오류 없이 셀이 끝나면 준비된 것입니다. `import requests` 셀에는 출력이 없어도 정상입니다. `ModuleNotFoundError`가 나오면 같은 `.venv` 커널이 선택되어 있는지 확인하고 `%pip install requests` 셀을 다시 실행합니다.

**같은 작업 폴더에서는 `.venv`와 `requests`를 한 번만 준비하면 됩니다.** 다음에 그 폴더에서 새 노트북을 열면 오른쪽 위 **Select Kernel**에서 기존 `.venv`를 선택하세요. 새 프로젝트 폴더를 만들어 별도 환경을 쓰면 그 환경에는 다시 설치해야 합니다.

---

## 2. GitHub 웹 화면에서 리포지토리를 만듭니다

1. GitHub에 로그인합니다.
2. 오른쪽 위의 **＋** 버튼을 누르고 **New repository**를 선택합니다.
3. **Repository name**에 security-agent-toolkit을 입력합니다.
4. 공개 여부에서 **Public**을 선택합니다.
5. **Add a README file**에 체크합니다.
6. **Create repository**를 누릅니다.

만들고 나면 주소가 이런 모양입니다.

https://github.com/<내 아이디>/security-agent-toolkit

---

## 3. 배운 내용에 맞는 폴더를 만듭니다

지금까지 배운 1과목 자료를 담을 agent_core/와 학습 기록을 담을 docs/를 만듭니다. 아직 배우지 않은 과목 폴더는 만들지 않습니다.

GitHub 웹 화면에서 **Add file → Create new file**을 누르고 파일 이름 칸에 다음 경로를 입력합니다.

- agent_core/README.md
- docs/2026-09-30.md

파일을 만들고 커밋하면 해당 폴더도 함께 생깁니다. GitHub에는 빈 폴더만 따로 저장되지 않습니다.

---

## 4. 9/29까지의 실습 노트북을 올립니다

Run of Show에서 안내한 다음 노트북을 VS Code에서 준비합니다.

- 260922_variables_and_lists.ipynb
- 260923_am_conditions_loops_counting.ipynb
- 260923_pm_functions_files_csv.ipynb
- 01_0928_am_exceptions_logging.ipynb
- 02_0928_pm_nested_json.ipynb
- 01_0929_am_regex_detection_rules.ipynb
- 02_0929_pm_rules_api.ipynb

GitHub 웹 화면에서 agent_core/ 폴더를 열고 **Add file → Upload files**를 누릅니다. 위 노트북 파일들을 끌어다 놓고 **Commit changes**를 누릅니다.

.env 파일이나 API 키가 들어 있는 파일은 올리지 않습니다.

---

## 5. 오늘 공부한 것을 기록합니다

docs/2026-09-30.md에 오늘 한 일을 적고 커밋합니다.

    # 2026-09-30 (수)

    ## 내 리포지토리 주소
    https://github.com/          /security-agent-toolkit

    ## requests 설치 및 실행

    ## 오늘 만든 폴더

    ## 올린 노트북

    ## 찾아보고 알게 된 것

    ## 막힌 것

    ## 다음에 확인할 것

---

## 6. 확인합니다

- [ ] 내 리포지토리 주소가 github.com/<내 아이디>/security-agent-toolkit입니다
- [ ] agent_core/와 docs/ 폴더가 보입니다
- [ ] 9/29까지의 실습 노트북 7개가 agent_core/에 있습니다
- [ ] 노트북 파일을 눌러 내용이 보입니다
- [ ] docs/2026-09-30.md에 오늘 기록이 있습니다
- [ ] VS Code에서 `.venv` 커널을 선택하고 `%pip install requests`를 실행했습니다
- [ ] 새 코드 셀에서 `import requests`가 오류 없이 실행됩니다

---

## ⭐ 다 한 사람만 합니다

노트북 하나를 리포지토리에서 열어 변경 이력을 찾아봅니다. 누가 언제 파일을 올렸는지 확인해 보세요.
