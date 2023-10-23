from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from gensim.models.doc2vec import Doc2Vec,TaggedDocument


# TODO conda activate lv3_fastapi

# TODO BE에서 오는 데이터 모델로 보내기
# TODO BE랑 모델 서버랑 연결




  # TODO. 모델 joblib으로 저장하고 불러오는 방식으로 만들기
    # '''
    # loaded_model = joblib.load('d2v_model.joblib')

    # #불러온 모델을 사용
    # vector = loaded_model.infer_vector(~)
    # '''


# main.py

from .rs_models import d2v  # d2v 모듈을 불러옴

app = FastAPI()

DB = []

@app.get('/')
def read_root():
    return {'hello': 'World'}

class Model(BaseModel):
    genre1: str
    genre2: str
    genre3: str

@app.get('/get_data')
async def get_rs_data():
    return DB

@app.post('/input_data')
async def contents_based_rs(data: Model):
    recommended_list = d2v.get_similar_movies(data.genre1, data.genre2, data.genre3)
    global DB
    DB = recommended_list
    return recommended_list



