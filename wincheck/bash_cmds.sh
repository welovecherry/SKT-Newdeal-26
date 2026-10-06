# .git 만 옮겨 옛 폴더를 저장소로 만드는 방법을 Windows Git Bash 에서 실측한다
set -x
git --version
git config --show-origin --get core.autocrlf
cd "$RUNNER_TEMP"; rm -rf t; mkdir t; cd t
# 1) 깃허브 저장소 흉내 — 웹 업로드처럼 바이트 그대로(CRLF md · LF ipynb) 커밋
mkdir origin; cd origin; git init -q; git config core.autocrlf false
git config user.email a@b.c; git config user.name t
mkdir -p agent_core docs
printf '# 2026-10-02\r\n\r\n- 한 줄\r\n' > docs/2026-10-02.md
printf '{\n "cells": []\n}\n' > agent_core/nb.ipynb
printf 'print("hi")\r\n' > agent_core/llm_client.py
git add -A; git commit -qm web; cd ..
# 2) 학생 PC 의 옛 폴더 — 같은 파일 + 아직 안 올린 파일 + .env + .venv
mkdir -p stk/agent_core stk/docs stk/.venv/Scripts
cp origin/docs/2026-10-02.md stk/docs/; cp origin/agent_core/nb.ipynb origin/agent_core/llm_client.py stk/agent_core/
printf 'GEMINI_API_KEY=x\r\n' > stk/.env; printf '.env\r\n' > stk/.gitignore; echo x > stk/.venv/Scripts/python.exe
printf 'new\r\n' > stk/docs/2026-10-06.md
# 3) 기본 설정(autocrlf=true)으로 임시 이름에 clone → .git 만 옮김
git -c core.autocrlf=true clone -q origin temp_clone
mv temp_clone/.git stk/; rm -rf temp_clone
cd stk
echo "== status (system default autocrlf)"; git status --short
echo "== status autocrlf=true"; git -c core.autocrlf=true status --short
echo "== status after adding .venv to .gitignore"; printf '.env\r\n.venv\r\n' > .gitignore; git status --short
echo "== diff of nb.ipynb"; git diff --stat; git diff agent_core/nb.ipynb | head -20
echo "== after git reset"; git reset -q; git status --short
