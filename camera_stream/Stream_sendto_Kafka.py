import os
import zlib
import cv2
import asyncio
from dotenv import load_dotenv
from config.kafka_broker_instance import broker

load_dotenv()
camera_id = os.environ.get("CAMERA_ID")
camera_pw = os.environ.get("CAMERA_PASSWORD")
camera_ip = os.environ.get("CAMERA_IP")
url = f"rtsp://{camera_id}:{camera_pw}@{camera_ip}/cam/realmonitor?channel=1&subtype=0"

async def stream_rtsp_and_send_to_kafka(kafka_topic, user_id):
    frame_counter = 0
    frame_interval = 270  # 10초마다 처리
    retry_attempts = 5

    while True:
        # RTSP 스트림 열기
        cap = cv2.VideoCapture(url)

        if not cap.isOpened():
            print("카메라 스트림을 열 수 없습니다.")
            await asyncio.sleep(3)
            continue

        while True:
            try:
                ret, frame = cap.read()
                if not ret:
                    print("프레임을 가져올 수 없습니다. 스트림 재시도 중...")
                    cap.release()
                    await asyncio.sleep(3)
                    break

                frame_counter += 1
                if frame_counter % frame_interval == 0:
                    ret, buffer = cv2.imencode('.jpg', frame)
                    if not ret:
                        print("프레임 인코딩 실패")
                        continue

                    compressed_frame = zlib.compress(buffer)

                    for attempt in range(retry_attempts):
                        try:
                            await broker.publish(compressed_frame, kafka_topic, key=user_id)
                            print("Kafka에 메시지 전송 성공")
                            break
                        except Exception as e:
                            print(f"Kafka 전송 실패: {e}, 재시도 중...")
                            await asyncio.sleep(2 ** attempt)
                    else:
                        print("Kafka 전송 최종 실패")

            except Exception as e:
                print(f"오류 발생: {e}")
                break

        # 자원 해제 및 루프 재시작
        cap.release()
        await asyncio.sleep(3)

    cv2.destroyAllWindows()
