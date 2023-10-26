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
# https://github.com/lsjsj92/fast-api-tutorial/blob/main/main.py

from app.packages.routers import d2v_router  # d2v 모듈을 불러옴
from app.packages.routers import Sbert_router
from app.packages.routers import DeepFM_router

import importlib

app = FastAPI()


# d2v_router.py에서 d2v라우터 가져오기
app.include_router(d2v_router.d2v)
app.include_router(Sbert_router.s_bert)
app.include_router(DeepFM_router.deepfm)

DB = []

@app.get('/')
def read_root():
    return {'hello': 'main'}

# class Model(BaseModel):
#     genre1: str
#     genre2: str
#     genre3: str

# @app.get('/get_data')
# async def get_rs_data():
#     return DB

# @app.post('/input_data')
# async def contents_based_rs(data: Model):
#     recommended_list = d2v.get_similar_movies(data.genre1, data.genre2, data.genre3)
#     global DB
#     DB = recommended_list
#     return recommended_list