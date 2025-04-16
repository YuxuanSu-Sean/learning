from kafka import KafkaConsumer
import json

# Kafka 地址
bootstrap_servers = ['localhost:9092']

# 定义主题
topic = '0415-topic'

# 创建消费者
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap_servers,
    # 自动提交偏移量
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    auto_commit_interval_ms=1000,
    # 消息反序列化
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

try:
    # 消费消息
    for message in consumer:
        print(f"收到消息：分区={message.partition}, 偏移量={message.offset}, 键={message.key}, 值={message.value}")
except KeyboardInterrupt:
    print("用户手动停止消费。")
finally:
    # 关闭消费者
    consumer.close()