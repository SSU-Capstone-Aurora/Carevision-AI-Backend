import asyncio

from config.kafka_broker_instance import broker

async def connect_broker():
    try:
        print("Kafka 브로커 연결 시도 중...")
        await broker.connect()
        print("Kafka 브로커 연결 완료")
    except Exception as e:
        print(f"Kafka 브로커 연결 실패: {e}")
        await asyncio.sleep(3) # 3초 대기 후 재시도
        await connect_broker()

# Kafka에서 구독
def subscribe_to_topic(topic_name):
    @broker.subscriber(topic_name)
    async def handle_video(msg):
        #내부 처리 로직 필요
        print("handle_video" + msg)

# Kafka로 메시지 전송
async def send_to_topic(topic_name):
    @broker.publisher(topic_name)
    async def send_processed_result(result):
        print(f"send_processed_result 실행됨, 메시지: {result}")  # 로그 추가
        await broker.publish(result, topic_name)
        print(f"Kafka에 {topic_name}로 메시지 전송 완료: {result}")  # 메시지 전송 완료 로그

    return send_processed_result  # 비동기 함수 반환