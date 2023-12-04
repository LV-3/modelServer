from typing import Union
from fastapi import FastAPI, Body
from pydantic import BaseModel
# from app.Kafka.KafkaProcessor import KafkaProcessor
from packages.routers import Sbert, Doc2VecModel, DeepFM
from typing import Union, List, Dict
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException
import json


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

@app.get('/test')
def test(data):
    return data



# spring - fe에서 Get 요청을 받아서 request로 보냄.
# 리턴 값으로 받는 것은 모델 당 21개 추천 컨텐츠 데이터.
class MoodDataItem(BaseModel):
    content_id: str
    mood: Union[List[str], None]


class DescriptionDataItem(BaseModel):
    content_id: str
    description: str


class PersonalDataItem(BaseModel):
    subsr: str
    content_id: str
    liked: int
    ct_cl: str
    genre_of_ct_cl: str
    template_A: Union[List[str], None]
    template_B: Union[List[str], None]
    template_C: Union[List[str], None]


class RequestData(BaseModel):
    mood_data: List[MoodDataItem]
    description_data: List[DescriptionDataItem]
    personal_data: List[PersonalDataItem]
    

class ResponseData(BaseModel):
    description_data: List[str]
    mood_data: List[str]
    personal_data: List[str]


@app.post('/prcs_models')
def process_multiple_models(request_data: RequestData = Body()):
    try:
        print(request_data)
        # print('###################################################\nReceive data\n', request_data)
        
        d2v = Doc2VecModel()
        sbert = Sbert()
        deepfm = DeepFM()
        
        request_d2v_data = request_data.mood_data
        request_sbert_data = request_data.description_data
        request_deepfm_data = request_data.personal_data

        print('sucess receive data')

        mood_subsr_json_data = d2v.get_contents_based_rs(request_d2v_data)
        # mood_subsr_json_data = [ str(x) for x in range(21)]
        print('mood done.', mood_subsr_json_data)
        desc_subsr_json_data = sbert.get_simular_description(request_sbert_data)
        print('desc done.', desc_subsr_json_data)
        # temp = deepfm.get_request_data(request_deepfm_data)
        pers_subsr_json_data = [ str(x) for x in range(21)]
        print('pers done.', pers_subsr_json_data)

        response_data = ResponseData(
            description_data = desc_subsr_json_data,
            mood_data = mood_subsr_json_data,
            personal_data = pers_subsr_json_data
        )

        print('packing response data...')

        json_encoded_data = jsonable_encoder(response_data)
        return JSONResponse(content=json_encoded_data)

    except Exception as e:
        print('error', e)


@app.post("/items")
async def create_item(request: Request):
    body = await request.body()

    try:
        body_str = body.decode("utf-8")

        json_load_data = json.loads(body_str)
        json_encoded_data = jsonable_encoder(json_load_data)
        return JSONResponse(content=json_encoded_data)   
    
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Invalid UTF-8 encoding" )


@app.post("/deepfm")
def deepfm(request_data: RequestData = Body()):
    deepfm = DeepFM()
    request_deepfm_data = request_data.personal_data
    temp = deepfm.get_request_data(request_deepfm_data)




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
