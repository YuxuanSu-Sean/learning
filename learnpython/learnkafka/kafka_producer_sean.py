from kafka import KafkaProducer
import json

#kafka地址
bootstrap_servers = ['localhost:9092']

#创建生产者
producer_sean = KafkaProducer(
    bootstrap_servers = bootstrap_servers,
    #消息序列化
    value_serializer = lambda v: json.dumps(v).encode('utf-8')
)

#定义消息
message = {'key': 'value', 'message': 'hello kafka!'}

#定义主题
topic = '0415-topic'


try:
    #发送消息到主题
    future = producer_sean.send(topic, value = message)
    #等待消息结果
    result = future.get(timeout=10)
    print(f'消息发送成功，分区: {result.partition}, 偏移量: {result.offset}')
except Exception as e:
    print(f'消息发送失败: {e}')
finally:
    producer_sean.close()