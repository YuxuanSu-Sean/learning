import mysql.connector
import json


class MySQLManager:
    def __init__(self, user, password, host, database):
        self.mysql_config = {
            'user': user,
            'password': password,
            'host': host,
            'database': database
        }
        self.conn = mysql.connector.connect(**self.mysql_config)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        # 创建消息表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS kafka_messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                topic VARCHAR(255),
                message TEXT
            )
        ''')
        # 创建主题配置表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS kafka_topics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                topic_name VARCHAR(255),
                partitions INT,
                replication_factor INT
            )
        ''')
        self.conn.commit()

    def insert_message(self, topic, message):
        sql = "INSERT INTO kafka_messages (topic, message) VALUES (%s, %s)"
        val = (topic, json.dumps(message))
        self.cursor.execute(sql, val)
        self.conn.commit()

    def read_messages(self):
        self.cursor.execute("SELECT topic, message FROM kafka_messages")
        messages = self.cursor.fetchall()
        return [(topic, json.loads(msg)) for topic, msg in messages]

    def insert_topic_config(self, topic_name, partitions, replication_factor):
        sql = "INSERT INTO kafka_topics (topic_name, partitions, replication_factor) VALUES (%s, %s, %s)"
        val = (topic_name, partitions, replication_factor)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def get_topic_config(self, topic_name):
        sql = "SELECT partitions, replication_factor FROM kafka_topics WHERE topic_name = %s"
        val = (topic_name,)
        self.cursor.execute(sql, val)
        result = self.cursor.fetchone()
        return result

    def close(self):
        self.cursor.close()
        self.conn.close()