#!/bin/bash

# 변수 설정
COMPOSE_PATH="/home/ec2-user/docker-compose.yml"
NGINX_CONF_DIR="/home/ec2-user/nginx"
DELAY=5
NGINX_CONTAINER="nginx"

# 현재 실행 중인 블루 컨테이너 확인
BLUE_API_CONTAINER="$(docker ps --filter "name=carevision-ai-blue" --filter "status=running" | grep -v "CONTAINER ID")"

# 컨테이너 환경 스위칭
if [[ -n "$BLUE_API_CONTAINER" ]]; then
    echo "-----------------------------"
    echo "전환: BLUE => GREEN"
    echo "-----------------------------"

    CURRENT_API_ENV='carevision-ai-blue'
    NEW_API_ENV='carevision-ai-green'

    CURRENT_NGINX_CONF='carevision.blue.conf'
    NEW_NGINX_CONF='carevision.green.conf'
else
    echo "-----------------------------"
    echo "전환: GREEN => BLUE"
    echo "-----------------------------"

    CURRENT_API_ENV='carevision-ai-green'
    NEW_API_ENV='carevision-ai-blue'

    CURRENT_NGINX_CONF='carevision.green.conf'
    NEW_NGINX_CONF='carevision.blue.conf'
fi

# 새로운 이미지 빌드 (캐시 무시)
echo
echo "-----------------------------"
echo i"새로운 환경 이미지 빌드 중: $NEW_API_ENV (캐시 무시)"
sudo docker-compose -f "$COMPOSE_PATH" build --no-cache $NEW_API_ENV
echo "-----------------------------"
echo

# 새로운 컨테이너 시작
echo
echo "-----------------------------"
echo "새로운 환경 시작 중: $NEW_API_ENV"
sudo docker-compose -f "$COMPOSE_PATH" up  -d --no-deps $NEW_API_ENV
echo "-----------------------------"
echo

# 컨테이너 시작 대기
sleep $DELAY

# Nginx 설정 파일 업데이트
echo
echo "-----------------------------"
echo "Nginx 설정 파일 업데이트 중..."
# 현재 Nginx 컨테이너 내부의 conf.d에 새로운 설정 파일을 복사
docker cp "$NGINX_CONF_DIR/$NEW_NGINX_CONF" "$NGINX_CONTAINER:/etc/nginx/conf.d/"
# 현재 설정 파일을 삭제
docker exec "$NGINX_CONTAINER" rm -f "/etc/nginx/conf.d/$CURRENT_NGINX_CONF"
echo "-----------------------------"
echo

# Nginx 리로드
echo
echo "-----------------------------"
echo "Nginx 리로드 중..."
sudo docker-compose -f "$COMPOSE_PATH" exec "$NGINX_CONTAINER" nginx -s reload
echo "-----------------------------"
echo

# 이전 환경 중지 및 제거
echo
echo "-----------------------------"
echo "이전 환경 중지 및 제거 중: $CURRENT_API_ENV"
sudo docker-compose -f "$COMPOSE_PATH" stop "$CURRENT_API_ENV"
sudo docker-compose -f "$COMPOSE_PATH" rm -f "$CURRENT_API_ENV"
echo "-----------------------------"
echo

# 배포 완료 메시지
echo
echo "-----------------------------"
echo "배포가 완료되었습니다!"
echo "-----------------------------"