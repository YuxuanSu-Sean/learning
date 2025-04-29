from kafka import KafkaProducer
import json


class KafkaMessageProducer:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_message(self, topic, message):
        try:
            future = self.producer.send(topic, value=message)
            result = future.get(timeout=10)
            print(f'消息发送成功，分区: {result.partition}, 偏移量: {result.offset}')
        except Exception as e:
            print(f'消息发送失败: {e}')

    def close(self):
        self.producer.close()