#!/bin/bash

CURRENT_PORT=$(cat /home/ec2-user/service_ai_url.inc | grep -Po '(?<=:)\d+(?=;)')
TARGET_PORT=0

echo "> Current port of running WAS is ${CURRENT_PORT}."

if [ ${CURRENT_PORT} -eq 5001 ]; then
  TARGET_PORT=5002
elif [ ${CURRENT_PORT} -eq 5002 ]; then
  TARGET_PORT=5001
else
  echo "> No WAS is connected to nginx"
fi

TARGET_PID=$(lsof -Fp -i TCP:${TARGET_PORT} | grep -Po 'p[0-9]+' | grep -Po '[0-9]+')
echo "> TARGET_PID is ${TARGET_PID}."

if [ -n "${TARGET_PID}" ]; then
  echo "> Kill WAS running at ${TARGET_PORT}."
  sudo kill ${TARGET_PID}
else
  echo "> No running WAS found at ${TARGET_PORT}."
fi

# 포트 종료까지 기다리기
while lsof -i :${TARGET_PORT}; do
    echo "> Port ${TARGET_PORT} is already in use. Waiting..."
    sleep 2
done

# 가상환경 경로
VENV_DIR="/home/ec2-user/carevision-ai/venv"

# 가상환경이 없으면 생성
if [ ! -d "${VENV_DIR}" ]; then
  python3 -m venv "${VENV_DIR}"
fi

# 가상환경 활성화
source "${VENV_DIR}/bin/activate"

# PYTHONPATH 설정
export PYTHONPATH=/home/ec2-user/carevision-ai

# 종속성 설치
pip install -r /home/ec2-user/carevision-ai/requirements.txt

# Gunicorn으로 애플리케이션 실행
nohup gunicorn -b 0.0.0.0:${TARGET_PORT} app:app > /home/ec2-user/nohup-ai.out 2>&1 &
echo "> Now new WAS runs at ${TARGET_PORT}."
exit 0
