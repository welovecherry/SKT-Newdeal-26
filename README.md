# SKT K-뉴딜 아카데미 · 대전 C반 수업 자료

**아침 과제와 실습 노트북**입니다. 이 페이지 하나만 저장해 두시면 됩니다. 날짜를 찾아 들어가면 그날 자료가 다 있습니다.

## 날짜 목차

### 1과목 · AI·자동화 기초 — 폴더 `agent_core`

| 날짜 | 아침 과제 | 오전 | 오후 |
|---|---|---|---|
| 9/22 (월) | — | [변수 · 자료형 · 리스트 · 딕셔너리](https://colab.research.google.com/github/welovecherry/SKT-Newdeal-26/blob/main/260922_variables_and_lists.ipynb) | — |
| 9/23 (수) | — | [조건문 · 반복문 · 집합 · Counter](https://colab.research.google.com/github/welovecherry/SKT-Newdeal-26/blob/main/260923_am_conditions_loops_counting.ipynb) · [도전 문제](https://colab.research.google.com/github/welovecherry/SKT-Newdeal-26/blob/main/260923_extra_challenges.ipynb) | [함수 · 모듈 · 파일 · CSV](https://colab.research.google.com/github/welovecherry/SKT-Newdeal-26/blob/main/260923_pm_functions_files_csv.ipynb) |
| 9/28 (월) | [1 · 깃배시 설치와 폴더 확인](0928_mon/0928_morning30.md) | [예외처리 · 로깅](https://colab.research.google.com/github/welovecherry/SKT-Newdeal-26/blob/main/0928_mon/01_0928_am_exceptions_logging.ipynb) | [중첩 자료 · JSON](https://colab.research.google.com/github/welovecherry/SKT-Newdeal-26/blob/main/0928_mon/02_0928_pm_nested_json.ipynb) |
| 9/29 (화) | [2 · 폴더 만들기와 경로 이동](0929_tue/0929_morning30.md) | [정규표현식 · 탐지 룰](https://colab.research.google.com/github/welovecherry/SKT-Newdeal-26/blob/main/0929_tue/01_0929_am_regex_detection_rules.ipynb) | [탐지 룰 · API](https://colab.research.google.com/github/welovecherry/SKT-Newdeal-26/blob/main/0929_tue/02_0929_pm_rules_api.ipynb) |
| 9/30 (수) | [3 · requests 준비 · 깃허브에 노트북 올리기](0930_wed/0930_morning30.md) | [requests · API 클라이언트](https://colab.research.google.com/github/welovecherry/SKT-Newdeal-26/blob/main/0930_wed/01_0930_am_requests_api_client.ipynb) | *(다른 강사 수업)* |
| 10/2 (금) | [4 · VS Code 에서 수업 실행 준비](1002_fri/1002_morning30.md) | [웹훅 · CLI](1002_fri/261002_am_webhook_cli.ipynb) | [트리거 · 스케줄러](1002_fri/261002_pm_trigger_scheduler.ipynb) · [복습](1002_fri/261002_review.ipynb) |
| 10/6 (화) | [5 · Gemini API 키 발급 · 보관](1006_tue/1006_morning30.md) | [LLM 호출 · 프롬프트](1006_tue/261006_am_llm_prompt.ipynb) | [AI 에이전트 · 도구 호출](1006_tue/261006_pm_agent_tools.ipynb) |
| 10/7 (수) | [6 · 내 폴더를 깃허브 저장소와 연결하기](1007_wed/1007_morning30.md) | [보고서 형식 · 묶음 요약 · 위험도 정렬](1007_wed/261007_am_report_summary.ipynb) | [총평 · 보고서 틀 · 조건부 경고](1007_wed/261007_pm_report_generator.ipynb) |
| 10/8 (목) | [7 · 명령어로 깃허브에 올리기](1008_thu/1008_morning30.md) | [설정 분리 · 알림 연동 · 하나로 잇기](1008_thu/261008_am_config_pipeline.ipynb) | [코드 리뷰 · 테스트 · 디버깅 · 회고](1008_thu/261008_pm_review_debug_retro.ipynb) |

### 2과목 · 네트워크·ZT 운영 — 폴더 `network_zt`

| 날짜 | 아침 과제 | 오전 | 오후 |
|---|---|---|---|
| 10/12 (월) | [8 · 로그에서 필요한 줄만 골라내기](1012_mon/1012_morning30.md) | 준비 중 | 준비 중 |
| 10/13 (화) | [9 · 파일 옮기고 복사하기 — `mv` · `cp`](1013_tue/1013_morning30.md) | 준비 중 | 준비 중 |
| 10/14 (수) | [10 · VS Code 를 내 것으로 꾸미기](1014_wed/1014_morning30.md) | 준비 중 | 준비 중 |

9/30 까지는 Colab 으로, **10/2 부터는 VS Code** 로 노트북을 엽니다.

## 노트북 쓰는 법 (10/2 부터)

1. 표에서 주제 이름을 누르고, 깃허브 화면 오른쪽 위의 **다운로드** 버튼으로 `.ipynb` 파일을 받습니다.
2. 받은 파일을 `security-agent-toolkit` 안의 **그날 과목 폴더**(1과목은 `agent_core`)에 넣습니다.
3. VS Code 에서 `security-agent-toolkit` 폴더를 열고, 왼쪽 목록에서 노트북을 엽니다.
4. 오른쪽 위 **Select Kernel**(커널 선택)에서 **각자 만든 가상환경**을 고릅니다. 이름에 `.venv` 처럼 가상환경 이름이 붙은 항목입니다.
5. 맨 위 **위치 확인 셀**부터 실행합니다. 셀 실행은 **Shift + Enter** 입니다.
6. 셀은 **위에서 아래로** 차례로 실행합니다. `NameError` 가 나오면 위쪽 셀을 건너뛴 것입니다.
7. 막히면 문제 아래 **💡 힌트**를 보고, 그래도 안 되면 노트북 맨 아래 **정답**을 봅니다.

## 아침 과제 쓰는 법

1. 표에서 **아침 과제** 칸을 누릅니다. 그날 과제 문서가 열립니다.
2. 명령어 정답이 적혀 있지 않은 부분은 **직접 검색해서** 찾습니다. 찾는 것까지가 과제입니다.
3. 아침에 못 끝냈으면 오후 5시 이후에 마무리합니다.
4. 그날 공부한 것은 `docs/날짜.md` 로 남기고, 10/8 부터는 `git push` 로 올립니다.

## 기본 문제 제작 원칙 (강사용)

- 긴 코드는 기능별로 나누고 `# 1. …`, `# 2. …`처럼 번호가 붙은 주석 힌트를 제공합니다.
- 반복되는 코드는 미리 제공하거나 준비 셀의 함수로 묶습니다. 학생은 그 문제에서 **가장 중요한 부분만** 직접 완성합니다.
- 미리 채워 둔 줄 · 준비 셀 · 정답 칸에는 짧은 주석을 답니다. 출력을 예상하는 문제에는 달지 않습니다.
- 전체 흐름을 스스로 설계하는 연습은 ⭐도전 문제로 분리합니다.
- 교시당 문제 수는 고정하지 않습니다. 그 교시의 주제와 난이도에 따라 정합니다.

## 파일 이름 규칙 (강사용)

```
1006_tue/                            MMDD_요일세글자
  1006_morning30.md                  아침 과제 문서
  261006_am_llm_prompt.ipynb         YYMMDD_am|pm_영문주제
  261006_pm_agent_tools.ipynb
```

9/22 ~ 9/30 파일은 이미 배포한 링크를 살리려고 예전 이름 그대로 둡니다.
