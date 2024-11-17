import os
import zlib
import cv2
from dotenv import load_dotenv
from Crypto.Cipher import AES
from src.config.kafka_broker_instance import broker

# .env 파일 로딩
load_dotenv()
camera_id = os.environ.get("CAMERA_ID")
camera_pw = os.environ.get("CAMERA_PASSWORD")
camera_ip = os.environ.get("CAMERA_IP")
url = f"rtsp://{camera_id}:{camera_pw}@{camera_ip}/cam/realmonitor?channel=1&subtype=0"

# AES 암호화에 사용할 키와 IV 로딩
aes_key = os.environ.get("AES_KEY").encode()  # 32바이트 키 (256비트)
aes_iv = os.environ.get("AES_IV").encode()    # 16바이트 IV (nonce)

# AES GCM 암호화 함수
def encrypt_data_gcm(data):
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=aes_iv)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return ciphertext, tag

# 병원을 토픽으로, 환자 key, data 값으로 저장
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

        # 설정된 프레임마다 분석 작업 실행
        if frame_counter % frame_interval == 0:
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("프레임 인코딩 실패")
                continue

            # JPEG 데이터를 zlib로 압축
            compressed_frame = zlib.compress(buffer)

            # 압축된 프레임을 AES GCM 암호화
            encrypted_frame, tag = encrypt_data_gcm(compressed_frame)

            # Kafka로 암호화된 데이터 전송 (nonce와 tag 포함)
            await broker.publish(encrypted_frame + aes_iv + tag, kafka_topic, key=user_id)

    # 모든 작업 종료 후 자원 해제
    cap.release()
    cv2.destroyAllWindows()
