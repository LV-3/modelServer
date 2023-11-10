import yaml
import json
from confluent_kafka import Consumer, KafkaError
from packages.routers.d2v_router import get_similar_movies
from producer.kafka_producer import init_producer, send_message_confluent


consumer = None
producer = None

# consumer init
def init_consumer(config_file_path):
    global consumer
    with open(config_file_path, 'r') as config_file:
        cons_config = yaml.safe_load(config_file)
    consumer = Consumer(cons_config)
    print('Consumer config')

# producer과 consumer init
def init_global_producer(producer_config_file, topic):
    global producer
    producer = init_producer(producer_config_file, topic)
    print('Producer config')

async def cons_messages():
    consumer_config_file = '../config/kafka_cons_config.yaml'
    producer_config_file = '../config/kafka_prod_config.yaml'
    
    # 토픽은 먼저 생성해놓고 실행해야 함.
    topic = 'kafka-test'
    
    init_consumer(consumer_config_file)
    init_global_producer(producer_config_file, topic)

    # 토픽을 subscribe할 뿐 토픽이 없으면 오류 발생함.
    # KafkaError{code=UNKNOWN_TOPIC_OR_PART,val=3,str="Subscribed topic not available: example_topic: Broker: Unknown topic or partition"}
    # 통신 전에 토픽을 먼저 생성.

    # 구독
    consumer.subscribe([topic])

    try:
        while True:

            # 1.0초 동안 기다린 후 producer한테서 요청이 없으면 continue
            msg = consumer.poll(1)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print('Error while consuming message: {}'.format(msg.error()))
                    break
            
            # 추천 영화 리스트를 가져 옴
            recommended_list = await process_message(msg.value())
            
            print(f"Sending message to topic {topic}: {recommended_list}")
            
            send_message_confluent(producer, 'producing_test', json.dumps(recommended_list))

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

# 데이터가 들어왓을 때 실행되는 함수

async def process_message(message: str):
    print('start process_message')
    try:

        data = json.loads(message)

        # content_id = data.get('content_id')
        # description = data.get('description')
        # genre = data.get('genre')

        # model_input = {
        #     'content_id': content_id,
        #     'description': description,
        #     'genre': genre
        # }


        print(data)

        # TEST
        genre1 = data.get('genre1')
        genre2 = data.get('genre2')
        genre3 = data.get('genre3')

        model_input_test = {
            'genre1': genre1,
            'genre2': genre2,
            'genre3': genre3,
        }

        try:
            # dict 자료형을 넣을 땐 매개변수 앞에 **
            model_output = await get_similar_movies(**model_input_test)
        except Exception as e:
            print(str(e))

        return model_output

    except:
        pass