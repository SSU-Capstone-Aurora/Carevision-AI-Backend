from binascii import unhexlify
import json
from Crypto.Cipher import AES
import zlib

# AES GCM 복호화 함수
def decrypt_data_gcm(encrypted_data, aes_iv, tag, aes_key):
    try:
        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=aes_iv)
        decrypted_data = cipher.decrypt_and_verify(encrypted_data, tag)
        return decrypted_data
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None

# Global AES Key and IV (초기값 설정)
aes_key = None
aes_iv = None

# Kafka 메시지 처리
@broker.subscriber("hospital_topic")
async def handle_message(message):
    global aes_key, aes_iv

    try:
        # JSON 메시지 디코딩
        payload = json.loads(message.value)

        if payload["type"] == "key_update":
            # 키 갱신 알림 처리
            aes_key = unhexlify(payload["key"])
            aes_iv = unhexlify(payload["iv"])
            print("AES 키 갱신됨")
        elif payload["type"] == "frame":
            # 데이터 메시지 처리
            if aes_key is None or aes_iv is None:
                print("AES 키가 설정되지 않았습니다. 복호화 불가")
                return

            encrypted_frame = unhexlify(payload["data"])
            tag = unhexlify(payload["tag"])
            iv = unhexlify(payload["iv"])

            # 복호화
            decompressed_data = decrypt_data_gcm(encrypted_frame, iv, tag, aes_key)
            if decompressed_data:
                frame_data = zlib.decompress(decompressed_data)
                print("Successfully decrypted and decompressed frame")
            else:
                print("Decryption failed")
    except Exception as e:
        print(f"Error processing message: {e}")
