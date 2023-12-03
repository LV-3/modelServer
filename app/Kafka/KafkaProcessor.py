# import yaml
# import json
# from confluent_kafka import Consumer, KafkaError, Producer
# from packages.routers import Sbert, Doc2VecModel


# class KafkaProcessor:
#     def __init__(self, consumer_config_path: str, producer_config_file: str, config_file: str) -> None:

#         with open(config_file, 'r') as config_file_path:
#             self.config = yaml.safe_load(config_file_path)
#         self.cons_topic = self.config.get('cons_topic')
#         self.prod_topic = self.config.get('prod_topic')

#         self.consumer = self.init_consumer(consumer_config_path)
#         self.producer = self.init_producer(producer_config_file)

#         self.sbert = Sbert()
#         self.d2v = Doc2VecModel()


#     def init_consumer(self, consumer_config_path: str) -> Consumer:

#         with open(consumer_config_path, 'r') as config_file:
#             cons_config = yaml.safe_load(config_file)
#         print('Consumer config success')

#         return Consumer(cons_config)


#     def init_producer(self, producer_config_file: str) -> Producer:

#         with open(producer_config_file, 'r') as config_file:
#             prod_config = yaml.safe_load(config_file)
#         print('Producer config success')

#         return Producer(prod_config)
             

#     async def cons_messages(self) -> None:

#         self.consumer.subscribe([self.cons_topic])

#         try:
#             while True:

#                 # 1.0초 동안 기다린 후 producer한테서 요청이 없으면 continue
#                 msg = self.consumer.poll(1)

#                 if msg is None:
#                     continue
#                 if msg.error():
#                     if msg.error().code() == KafkaError._PARTITION_EOF:
#                         continue
#                     else:
#                         print('Error while consuming message: {}'.format(msg.error()))
#                         break

#                 print('Received message: {}, type: {}'.format(msg.value().decode('utf-8'), type(msg.value())))
                
#                 # match type(msg.value().decode('utf-8')):
#                     # case 'bytes':
#                 # TODO: 각 모델 당 21개씩 3번 - 7개씩 추천 결과를 받은 다음 랜덩으로 보냄. (1-7, 8-14, 15-21)
#                 try:
#                     str_input_data: dict = json.loads(msg.value())
#                     model_name: str = str_input_data['modelName']
#                     print('Model Name: {}. type: {}'.format(model_name, type(model_name)))
#                     if model_name == 'description_data':
#                         response_data: list = str_input_data['responseData']
#                         model_input_data: dict = {item['content_id']: item['description'] for item in response_data}

#                         recommended_list: list = await self.sbert.simular_description(model_input_data)
                    
#                     print(recommended_list)

#                             # elif model_name == 'genre_data'

#                             # self.send_message_confluent(self.producer, self.prod_topic, recommended_list)

#                 except Exception as e:
#                     print('str data error', e)
#                     pass

#                     # bytes 형식은 파싱을 두 번 해야 함 (bytes -> str -> dict)
#                     # case 'bytes21':
#                         # try:
#                         #     bytes_input_data: dict = json.loads(json.loads(msg.value().decode("utf-8")))
#                         #     print("content data: ", bytes_input_data['responseData'][0]['content_id'])
#                         #     recommended_list: list = await self.proc_msg(msg.value())
#                         # except Exception as e:
#                         #     print(e)
#                         #     pass
#                 print('done')
#                 # 추천 영화 리스트를 가져 옴
                
#                 # print(f"Sending message to topic {self.prod_topic}: {recommended_list}")
                
#                 # self.send_message_confluent(self.producer, self.prod_topic, recommended_list)

#         except Exception as e:
#             print(str(e))
#         finally:
#             self.consumer.close()

    
#     async def proc_msg(self, message: str) -> list:
#         print('start process_message')

#         try:
#             data = json.loads(message)
#             print(data)

#             genre1 = data.get('genre1')
#             genre2 = data.get('genre2')
#             genre3 = data.get('genre3')

#             model_input_test = {
#                 'genre1': genre1,
#                 'genre2': genre2,
#                 'genre3': genre3,
#             }

#             try:
#                 model_output = await self.d2v.get_similar_movies(**model_input_test)

#                 return model_output
#             except Exception as e:
#                 print(str(e))
#         except Exception as e:
#             print(str(e))
   

#     def send_message_confluent(self, producer: Producer, prod_topic: str, message: json) -> None:
#         print(f"sending message topic : {prod_topic}, meg : {message}")
#         producer.produce(prod_topic, value=message, callback=self.delivery_report)
#         producer.poll(0)

#         producer.flush()


#     def delivery_report(self, err, msg):
#         """ Called once for each message produced to indicate delivery result.
#             Triggered by poll() or flush(). """
#         if err is not None:
#             print('Message delivery failed: {}'.format(err))
#         else:
#             print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))