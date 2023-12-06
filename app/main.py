from typing import Union
from fastapi import FastAPI, Body
from pydantic import BaseModel
from .packages.routers import Sbert, Doc2VecModel, DeepFM, DeepFM_V2
from typing import Union, List
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException
import json




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
        
        d2v = Doc2VecModel()
        sbert = Sbert()
        deepfm_v2 = DeepFM_V2()
        
        request_d2v_data = request_data.mood_data
        request_sbert_data = request_data.description_data
        request_deepfm_data = request_data.personal_data

        print('sucess receive data')

        mood_subsr_json_data = d2v.get_contents_based_rs(request_d2v_data)
        print('mood done.', mood_subsr_json_data)
        desc_subsr_json_data = sbert.search(request_sbert_data)
        print('desc done.', desc_subsr_json_data)
        pers_subsr_json_data = deepfm_v2.get_request_data_2_Rs(request_deepfm_data)
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


