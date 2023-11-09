import os

from fastapi import APIRouter
from pydantic import BaseModel

import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer

import os
print(os.getcwd())
########################################################
import os

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
index.add_with_ids(encoded_data,np.array(range(0,len(description_list))))


def search(query:str) -> dict:
   query_vector = model.encode([query])
   k = 5
   D,I = index.search(query_vector, k)
   sorted_indices = np.argsort(D,axis=1)
   D_sorted = np.take_along_axis(D, sorted_indices, axis=1)
   I_sorted = np.take_along_axis(I, sorted_indices, axis=1)
   dict_movie = movie.loc[I_sorted[0].tolist()].to_dict(orient='records')

   return dict_movie


##########################################################



s_bert = APIRouter(prefix='/s_bert')

@s_bert.get('/',tags=['S_bert'])
async def HereIs():
    return {'msg':'s_bert경로'}


class Model(BaseModel):
    description: str



@s_bert.post('/predict',tags=['S_bert'])
async def simular_description(query:Model) -> dict:
    print(query.description)

    prediction = search(query.description)
    print(prediction)
    return prediction
