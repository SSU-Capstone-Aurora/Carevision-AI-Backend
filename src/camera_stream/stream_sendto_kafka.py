import os
import zlib
import time

import cv2
from Crypto.Cipher import AES
from dotenv import load_dotenv
from src.config.kafka_broker_instance import broker
from secrets import token_bytes

load_dotenv()

camera_id = os.environ.get("CAMERA_ID")
camera_pw = os.environ.get("CAMERA_PASSWORD")
camera_ip = os.environ.get("CAMERA_IP")
url = f"rtsp://{camera_id}:{camera_pw}@{camera_ip}/cam/realmonitor?channel=1&subtype=0"

# Global AES Key and IV
aes_key = token_bytes(32)  # 32-byte key
aes_iv = token_bytes(16)   # 16-byte IV
last_key_update = time.time()

# AES GCM 암호화 함수
def encrypt_data_gcm(data):
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=aes_iv)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return ciphertext, tag

# AES 키 업데이트 함수
async def notify_key_update(kafka_topic):
    global aes_key, aes_iv, last_key_update
    aes_key = token_bytes(32)
    aes_iv = token_bytes(16)
    key_update_message = {"type": "key_update", "key": aes_key.hex(), "iv": aes_iv.hex()}
    await broker.publish(key_update_message, kafka_topic)
    last_key_update = time.time()  # 키 업데이트 시간을 갱신


async def stream_rtsp_and_send_to_kafka(kafka_topic, user_id):
    frame_counter = 0
    frame_interval = 270  # 10초

    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        print("카메라 스트림을 열 수 없습니다.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 가져올 수 없습니다.")
            break

        # 10분마다 AES 키 업데이트 및 알림 전송
        if time.time() - last_key_update > 600:  # 10분 = 600초
            await notify_key_update(kafka_topic)

        frame_counter += 1
        if frame_counter % frame_interval == 0:
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("프레임 인코딩 실패")
                continue

            compressed_frame = zlib.compress(buffer)
            encrypted_frame, tag = encrypt_data_gcm(compressed_frame)

            # Kafka로 암호화된 데이터 전송 (nonce와 tag 포함)
            payload = {"type": "frame", "data": encrypted_frame.hex(), "tag": tag.hex(), "iv": aes_iv.hex()}
            await broker.publish(payload, kafka_topic, key=user_id)

    cap.release()
    cv2.destroyAllWindows()
