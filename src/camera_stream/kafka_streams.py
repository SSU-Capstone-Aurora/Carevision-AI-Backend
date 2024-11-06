import asyncio

from src.config.kafka_broker_instance import broker

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
        print("subscriber 동작 중...")

        await send_to_topic("tmp_topic", msg)
        print("subscriber 동작 완료")


# Kafka로 메시지 전송
async def send_to_topic(topic_name, msg):
    @broker.publisher(topic_name)
    async def send_processed_result(msg):
        print(f"Kafka에 {topic_name}로 메시지 전송 완료: {msg}")

    await send_processed_result(msg)