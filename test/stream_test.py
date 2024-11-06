from src.config.kafka_broker_instance import broker


async def send_example():
    await broker.publish(message="test", topic="tmp_topic")
    print("tmp_topic에 publish 완료")
