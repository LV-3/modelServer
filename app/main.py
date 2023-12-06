from typing import Union
from fastapi import FastAPI, Body
from pydantic import BaseModel
from .packages.routers import Sbert, Doc2VecModel, DeepFM
from typing import Union, List
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException
import json
import time




class MoodDataItem(BaseModel):
    content_id: str
    mood: Union[List[str], None]


class DescriptionDataItem(BaseModel):
    content_id: str
    description: str


class PersonalDataItem(BaseModel):
    subsr: int
    content_id: int
    liked: int
    ct_cl: str
    genre_of_ct_cl: str
    template_A_TopGroup: Union[List[str], None]
    template_B_TopGroup: Union[List[str], None]
    template_C_TopGroup: Union[List[str], None]


class RequestData(BaseModel):
    mood_data: List[MoodDataItem]
    description_data: List[DescriptionDataItem]
    personal_data: List[PersonalDataItem]
    

class ResponseData(BaseModel):
    description_data: List[str]
    mood_data: List[str]
    personal_data: List[str]


app = FastAPI()


@app.get('/')
def read_root():
    return {'h': 'i'}

@app.get('/test')
def test(data):
    return data

@app.post('/prcs_models')
def process_multiple_models(request_data: RequestData = Body()):
    try:
        ST = time.time()
        d2v = Doc2VecModel()
        ED = time.time()
        print('d2v 모델 초기화 시간: ', ED-ST)

        ST = time.time()
        sbert = Sbert()
        ED = time.time()
        print('bert 모델 초기화 시간: ', ED-ST)
        
        ST = time.time()
        deepfm = DeepFM()
        ED = time.time()
        print('fm 모델 초기화 시간: ', ED-ST)
        
        
        request_d2v_data = request_data.mood_data
        request_sbert_data = request_data.description_data
        request_deepfm_data = request_data.personal_data

        print('sucess receive data')

        ST = time.time()
        mood_subsr_json_data = d2v.get_contents_based_rs(request_d2v_data)
        ED = time.time()
        print('d2v 모델 연산 시간: ', ED-ST)
        print('mood done.', mood_subsr_json_data)

        ST = time.time()
        desc_subsr_json_data = sbert.search(request_sbert_data)
        ED = time.time()
        print('bert 모델 연산 시간: ', ED-ST)
        print('desc done.', desc_subsr_json_data)

        ST = time.time()
        pers_subsr_json_data = deepfm.get_request_data_2_Rs(request_deepfm_data)
        ED = time.time()
        print('fm 모델 연산 시간: ', ED-ST)
        print('pers done.', pers_subsr_json_data)

        response_data = ResponseData(
            description_data = desc_subsr_json_data,
            mood_data = mood_subsr_json_data,
            personal_data = pers_subsr_json_data
        )

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


