import cv2
from kafka import KafkaProducer


def stream_rtsp_and_send_to_kafka(url, kafka_server, kafka_topic, fps=30, frame_size=(640, 480)):

    # Kafka Producer 생성
    producer = KafkaProducer(bootstrap_servers=[kafka_server],
                             value_serializer=lambda x: x.tobytes())  # 데이터를 바이트로 전송

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

        # 화면에 프레임 출력
        cv2.imshow("RTSP 스트림", frame)

        # 프레임을 Kafka 서버로 전송 (바이트 형태로 전송)
        producer.send(kafka_topic, value=frame)

        # 'q'를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 모든 작업 종료 후 자원 해제
    cap.release()
    cv2.destroyAllWindows()
    producer.close()

# RTSP URL 입력
camera_id = "admin"
camera_pw = input("Enter camera pw: ")  # default: L2CFB0FD
camera_ip = input("Enter camera ip: ")  # default: 192.168.35.64
url = "rtsp://" + camera_id + ":" + camera_pw + "@" + camera_ip + "/cam/realmonitor?channel=1&subtype=0"

# Kafka 서버 정보
kafka_server = input("Example = 127.0.0.1:9092, Enter kafka server ip and port : ")  # 실제 Kafka 서버 주소, test default : localhost:9092
kafka_topic = 'video-stream'

stream_rtsp_and_send_to_kafka(url, kafka_server, kafka_topic, fps=30, frame_size=(1920, 1080))
