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

if [ ! -z ${TARGET_PID} ]; then
  echo "> Kill WAS running at ${TARGET_PORT}."
  sudo kill ${TARGET_PID}
fi

nohup java -jar -Dserver.port=${TARGET_PORT} /home/ec2-user/carevision-ai/build/libs/* > /home/ec2-user/nohup-ai.out 2>&1 &
echo "> Now new WAS runs at ${TARGET_PORT}."
exit 0