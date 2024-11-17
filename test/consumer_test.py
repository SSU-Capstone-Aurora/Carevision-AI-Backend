from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

kafka_bootstrap_servers = 'kafka-faststream:9092',
kafka_topic = "tmp_topic"


async def produce_messages():
    producer = AIOKafkaProducer(bootstrap_servers=kafka_bootstrap_servers)
    await producer.start()
    try:
        for i in range(10):
            await producer.send_and_wait(kafka_topic, f"메시지 {i}".encode('utf-8'))
            print(f"Kafka에 메시지 전송: 메시지 {i}")
    finally:
        await producer.stop()


async def consume_messages():
    consumer = AIOKafkaConsumer(
        kafka_topic,
        bootstrap_servers=kafka_bootstrap_servers,
        group_id="my-group",
        enable_auto_commit=False,
    )
    await consumer.start()
    try:
        async for message in consumer:
            print(f"메시지 수신: {message.value.decode('utf-8')}")
            # 수동 커밋
            await consumer.commit()
    finally:
        await consumer.stop()
