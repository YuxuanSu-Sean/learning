from kafka import KafkaConsumer
import json


class KafkaMessageConsumer:
    def __init__(self, bootstrap_servers, topic):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            auto_commit_interval_ms=1000,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

    def consume_messages(self):
        try:
            for message in self.consumer:
                print(f"收到消息：分区={message.partition}, 偏移量={message.offset}, 键={message.key}, 值={message.value}")
        except KeyboardInterrupt:
            print("用户手动停止消费。")

    def close(self):
        self.consumer.close()