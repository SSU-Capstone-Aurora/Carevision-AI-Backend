import asyncio

from src.alarm.send_alarm import send_alarm_request
from src.config.kafka_broker_instance import broker
from src.video.s3_video import image_handler


async def connect_broker():
    try:
        print("Kafka 브로커 연결 시도 중...")
        await broker.connect()
        print("Kafka 브로커 연결 완료")

        print("topic 구독 중...")
        alarm_to_topic("aurora-alarm")
        subscribe_to_topic("aurora")
        print("topic 구독 완료")

    except Exception as e:
        print(f"Kafka 브로커 연결 실패: {e}")
        await asyncio.sleep(3) # 3초 대기 후 재시도
        await connect_broker()

# Kafka에서 구독
def subscribe_to_topic(topic_name):
    @broker.subscriber(topic_name)
    async def handle_video(msg):
        print("subscriber 동작 중...")

        key = msg.get("key")
        data = msg.get("data")

        await image_handler(data,key)
        print("subscriber 동작 완료")


# Kafka로 메시지 전송
async def send_to_topic(topic_name, msg):
    @broker.publisher(topic_name)
    async def send_processed_result(msg):
        print(f"Kafka에 {topic_name}로 메시지 전송 완료: {msg}")

    await send_processed_result(msg)


# 알림 전용 consumer
def alarm_to_topic(topic_name):
    @broker.subscriber(topic_name)
    async def handle_alarm(msg):
        print("subscriber 동작 중...")
        await send_alarm_request(msg)
        print("subscriber 동작 완료")