from faststream.kafka import KafkaBroker

from camera_stream.kafka_streams import send_to_topic, startup_event

broker = KafkaBroker("kafka-faststream:9092")  # Kafka 브로커 주소 설정

async def send_example():
    await startup_event()

    print("send_example 함수 호출")

    send_processed_result = await send_to_topic("test")
    await send_processed_result("hello")

    print("send_to_topic 함수 실행 완료")