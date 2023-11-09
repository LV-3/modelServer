import yaml

# apache-kafka를 사용하는 경우
# from kafka import KafkaProducer

# confluent-kafka를 사용하는 경우 (confluent > apache)
# 서로 호환은 잘 되지만 confluent가 더 큰 범위를 가짐.
from confluent_kafka import Producer
import os

# config 파일을 불러와서 
def init_producer(config_file_path, topic):
    with open(config_file_path, 'r') as config_file:
        kafka_config = yaml.safe_load(config_file)

    topic = topic

    # return KafkaProducer(kafka_config)
    return Producer(kafka_config)

# apache-kafka를 사용하는 경우
# def send_message_apache(producer, topic, message):
    # producer.send(topic, message.encode())
    # print(f"topic : {topic}, meg : {message}")

# confluent-kafka를 사용하는 경우 (confluent > apache)
# 서로 호환은 잘 되지만 confluent가 더 큰 범위를 가짐.
def send_message_confluent(producer, topic, message):
    producer.send(topic, message.encode())
    print(f"topic : {topic}, meg : {message}")