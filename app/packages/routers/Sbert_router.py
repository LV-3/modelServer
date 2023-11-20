import os

from fastapi import APIRouter
from pydantic import BaseModel, Field

import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
from typing import List
from fastapi.responses import JSONResponse


# 10월 데이터
movie = pd.read_pickle('resource/movie.pickle')

description_list = movie['description'].to_list()


model_args ={
    'sbert_klue' : 'snunlp/KR-SBERT-V40K-klueNLI-augSTS',
    'sbert_sts':'jhgan/ko-sbert-sts',
    'sroberta':'jhgan/ko-sroberta-multitask',
    'albert':'bongsoo/albert-small-kor-sbert-v1.1'
}

model = SentenceTransformer(model_args['sroberta'])

encoded_data = model.encode(description_list)

# faiss 인덱스 생성
index = faiss.IndexIDMap(faiss.IndexFlatIP(768))

# 데이터 id 배열
index.add_with_ids(encoded_data, np.array(range(0, len(description_list))))


def search(query: str) -> dict:
   query_vector = model.encode([query]) 
   k = 21
   D,I = index.search(query_vector, k)
   sorted_indices = np.argsort(D,axis=1)
   D_sorted = np.take_along_axis(D, sorted_indices, axis=1)
   I_sorted = np.take_along_axis(I, sorted_indices, axis=1)
   dict_movie = movie.loc[I_sorted[0].tolist()].to_dict(orient='records') # 하나의 줄거리 - 21 append 105

   return dict_movie


def parse_dict(query: dict) -> list:
  desc_list = []
  res = query.get('responseData')
  desc_list = [item.get('description') for item in res]
  return desc_list


##########################################################



s_bert = APIRouter(prefix='/s_bert')

@s_bert.get('/',tags=['S_bert'])
async def HereIs():
    return {'msg':'s_bert경로'}

@s_bert.post('/predict',tags=['S_bert'])
def simular_description(query: dict) -> JSONResponse:
    desc_list = parse_dict(query)
    prediction = search(desc_list)
    
    return JSONResponse(content=prediction)