from typing import Union
from fastapi import FastAPI, Body
from pydantic import BaseModel
from app.Kafka.KafkaProcessor import KafkaProcessor
from packages.routers import Sbert, Doc2VecModel
from typing import Union, List

# TODO. 모델 joblib으로 저장하고 불러오는 방식으로 만들기
  # '''
  # loaded_model = joblib.load('d2v_model.joblib')

  # #불러온 모델을 사용
  # vector = loaded_model.infer_vector(~)
  # '''

# main.py
# https://github.com/lsjsj92/fast-api-tutorial/blob/main/main.py


app = FastAPI()


@app.get('/')
def read_root():
    return {'h': 'i'}


# spring - fe에서 Get 요청을 받아서 request로 보냄.
# 리턴 값으로 받는 것은 모델 당 21개 추천 컨텐츠 데이터.
class MoodDataItem(BaseModel):
    content_id: str
    mood: List[str]


class DescriptionDataItem(BaseModel):
    content_id: str
    description: str


class DataItem(BaseModel):
    modelName: str
    responseData: List[Union[MoodDataItem, DescriptionDataItem]]


class RequestData(BaseModel):
    data: List[DataItem]


@app.post('/prcs_models')
def process_multiple_models(request_data: RequestData = Body()):
    try:
        
        d2v = Doc2VecModel()
        sbert = Sbert()
        
        request_d2v_data = request_data.data[0]
        request_sbert_data = request_data.data[1]

        mood_subsr_json_data = d2v.contents_based_rs(request_d2v_data)
        desc_subsr_json_data = sbert.simular_description(request_sbert_data)
        
        append_json_data = mood_subsr_json_data + desc_subsr_json_data
        return append_json_data
    except Exception as e:
        print(e)

#################################################################
# Kafka 사용

# @app.on_event('startup')
# async def start_func():
#     await received_data()

# async def received_data():
#     consumer_config_file = '../config/kafka_cons_config.yaml'
#     producer_config_file = '../config/kafka_prod_config.yaml'
#     config_file = '../config/config.yaml'

#     processor = KafkaProcessor(consumer_config_file, producer_config_file, config_file)
#     await processor.cons_messages()
