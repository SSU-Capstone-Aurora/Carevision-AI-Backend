import os
import zlib
from dotenv import load_dotenv
from Crypto.Cipher import AES
from src.config.kafka_broker_instance import broker

# .env 파일 로딩
load_dotenv()

# AES 암호화에 사용할 키와 IV 로딩
aes_key = os.environ.get("AES_KEY").encode()  # 32바이트 AES 키
aes_iv = os.environ.get("AES_IV").encode()    # 16바이트 IV (nonce)

# AES GCM 복호화 함수
def decrypt_data_gcm(encrypted_data, tag, nonce):
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(encrypted_data, tag)
    return decrypted_data

# Kafka에서 암호화된 메시지를 수신하고 복호화
async def consume_encrypted_data(kafka_topic):
    async for message in broker.subscribe([kafka_topic]):
        encrypted_message = message.value

        # 암호화된 데이터, nonce(IV), tag 분리
        encrypted_frame = encrypted_message[:-32]  # 데이터
        tag = encrypted_message[-32:-16]           # 인증 태그
        nonce = encrypted_message[-16:]            # IV

        # 복호화 처리
        try:
            decrypted_frame = decrypt_data_gcm(encrypted_frame, tag, nonce)
            # 압축 해제
            decompressed_frame = zlib.decompress(decrypted_frame)

            # 이후 필요한 작업을 수행 (예: 프레임 저장 또는 처리)
            print("복호화된 프레임을 수신하였습니다.")
        except (ValueError, KeyError) as e:
            print(f"복호화 오류: {e}")
