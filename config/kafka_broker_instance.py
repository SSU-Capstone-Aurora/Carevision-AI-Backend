from faststream import FastStream
from faststream.kafka import KafkaBroker

broker = KafkaBroker("kafka-faststream:9092")
kafka_app = FastStream(broker)
