from mysql_message import MySQLManager
from kafka_producer import KafkaMessageProducer
from kafka_consumer import KafkaMessageConsumer

# MySQL 配置
mysql_user = 'root'
mysql_password = '123456'
mysql_host = 'localhost'
mysql_database = 'learning-test'

# Kafka 配置
bootstrap_servers = ['localhost:9092']
topic = 'test-topic'

# 初始化 MySQL 管理器
mysql_manager = MySQLManager(mysql_user, mysql_password, mysql_host, mysql_database)

# 插入消息到 MySQL
message = {'key': 'value', 'message': 'hello kafka!'}
mysql_manager.insert_message(topic, message)

# 插入主题配置
mysql_manager.insert_topic_config(topic, 3, 2)

# 获取主题配置
config = mysql_manager.get_topic_config(topic)
if config:
    partitions, replication_factor = config
    print(f"主题: {topic}, 分区数: {partitions}, 副本因子: {replication_factor}")
else:
    print("未找到主题配置信息。")

# 初始化 Kafka 生产者
producer = KafkaMessageProducer(bootstrap_servers)

# 从 MySQL 读取消息并发送到 Kafka
messages = mysql_manager.read_messages()
for topic, message in messages:
    producer.send_message(topic, message)

# 初始化 Kafka 消费者
consumer = KafkaMessageConsumer(bootstrap_servers, topic)

# 消费消息
consumer.consume_messages()

# 关闭连接
mysql_manager.close()
producer.close()
consumer.close()