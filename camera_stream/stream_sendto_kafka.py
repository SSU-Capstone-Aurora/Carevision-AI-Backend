import os
import zlib
import cv2
from dotenv import load_dotenv

from config.kafka_broker_instance import broker

# .env 파일 로딩
load_dotenv()
camera_id = os.environ.get("CAMERA_ID")
camera_pw = os.environ.get("CAMERA_PASSWORD")
camera_ip = os.environ.get("CAMERA_IP")
url = f"rtsp://{camera_id}:{camera_pw}@{camera_ip}/cam/realmonitor?channel=1&subtype=0"

# FastStream, Kafka 브로커 설정
broker_env = os.environ.get("BROKER")

# 병원을 토픽으로, 환자 key, data값으로 저장
async def stream_rtsp_and_send_to_kafka(kafka_topic, user_id):
    frame_counter = 0
    frame_interval = 270  # 10초

    # RTSP 스트림 열기
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        print("카메라 스트림을 열 수 없습니다.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("프레임을 가져올 수 없습니다.")
            break

        # 프레임 카운터 증가
        frame_counter += 1

        # 설정 프레임마다 분석 작업 실행
        if frame_counter % frame_interval == 0:
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("프레임 인코딩 실패")
                continue

            # JPEG 데이터를 zlib로 압축
            compressed_frame = zlib.compress(buffer)

            # 프레임을 Kafka 서버로 전송
            await broker.publish(compressed_frame, kafka_topic, key=user_id)

    # 모든 작업 종료 후 자원 해제
    cap.release()
    cv2.destroyAllWindows()
