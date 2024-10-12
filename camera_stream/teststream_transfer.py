import cv2
import os
from kafka import KafkaProducer
import json
import numpy as np

def stream_rtsp_and_send_to_kafka(url, output_path, kafka_server, kafka_topic, codec='mp4v', fps=30, frame_size=(640, 480)):

    # Kafka Producer 생성
    producer = KafkaProducer(bootstrap_servers=[kafka_server],
                             value_serializer=lambda x: x.tobytes())  # 데이터를 바이트로 전송

    # RTSP 스트림 열기
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        print("카메라 스트림을 열 수 없습니다.")
        return

    # 저장할 비디오 파일 경로 설정
    fourcc = cv2.VideoWriter_fourcc(*codec)  # 코덱 설정 (MP4용 mp4v)
    out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

    if not out.isOpened():
        print("비디오 파일을 저장할 수 없습니다.")
        cap.release()
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("프레임을 가져올 수 없습니다.")
            break

        # 화면에 프레임 출력
        cv2.imshow("RTSP 스트림", frame)

        # 프레임을 파일에 저장
        out.write(frame)

        # 프레임을 Kafka 서버로 전송 (바이트 형태로 전송)
        producer.send(kafka_topic, value=frame)

        # 'q'를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 모든 작업 종료 후 자원 해제
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    producer.close()

# RTSP URL
url = "rtsp://admin:L2CFB0FD@192.168.35.64/cam/realmonitor?channel=1&subtype=0"

# 저장할 파일 경로, 삭제해도 상관 없음
output_folder = r"C:\VideoStream"
output_file = os.path.join(output_folder, 'stream_output.mp4')

frame_size = (1920, 1080)

# Kafka 서버 정보
kafka_server = 'localhost:9092'  # 실제 Kafka 서버 주소
kafka_topic = 'video-stream'

stream_rtsp_and_send_to_kafka(url, output_file, kafka_server, kafka_topic, codec='mp4v', fps=30, frame_size=frame_size)
