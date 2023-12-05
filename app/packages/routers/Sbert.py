import numpy as np
import pandas as pd
import faiss
# from sentence_transformers import SentenceTransformer

import torch
from transformers import AutoModel, AutoTokenizer

import pickle

# content_id, description


class Sbert:
    def __init__(self):
        # ... (commented out code)

        # self.model = SentenceTransformer(self.model_args['sroberta'])

        # self.encoded_data = self.model.encode(self.description_list)

        # # faiss 인덱스 생성 
        # # 임베딩한 값을 faiss 인덱스에 저장함.
        # self.index = faiss.IndexIDMap(faiss.IndexFlatIP(768))


        self.index = faiss.read_index('app/resource/Union_SMRY_RoBERTa_emb.index')


        # { faiss_index : content_id } 파일 불러오기
        with open('app/resource/FaissIndex2Content_id.pickle','rb') as pickle_file:
            self.FaissIndex2Content_id = pickle.load(pickle_file)

        self.model = AutoModel.from_pretrained('BM-K/KoDiffCSE-RoBERTa')
        self.tokenizer = AutoTokenizer.from_pretrained('BM-K/KoDiffCSE-RoBERTa')



    def embedding(self, query: str):
        
        # 문장 임베딩 임베딩
        inputs = self.tokenizer(query, padding=True, truncation=True, return_tensors="pt")
        embeddings, _ = self.model(**inputs, return_dict=False)

        return embeddings[0][0].tolist()

        # # 데이터 id 배열
        # self.index.add_with_ids(self.encoded_data, np.array(range(0, len(self.description_list))))



    def search(self,query:str) -> list[int]:
        query_vector = self.embedding(query)
        query_vector_np = np.array(query_vector).reshape(1,-1)

        k = 21

        D,I = self.index.search(query_vector_np,k)
        index_list = I.flatten().tolist()

        # faiss index로 반환된 I의 값을, content_id로 맵핑해서 reommend_content_id에 담김
        recommend_content_id = [self.FaissIndex2Content_id.get(key) for key in self.FaissIndex2Content_id.keys() if key in index_list]


        return recommend_content_id

    # def search(self, query: str) -> dict:
    #     # query_vector = self.model.encode([query]) 

    #     query_vector = self.embedding(query)  # Fix: call the embedding method on the object

    #     k = 21
    #     D, I = self.index.search(query_vector, k)
    #     sorted_indices = np.argsort(D, axis=1)
    #     D_sorted = np.take_along_axis(D, sorted_indices, axis=1)
    #     I_sorted = np.take_along_axis(I, sorted_indices, axis=1)
    #     dict_movie = self.movie.loc[I_sorted[0].tolist()].to_dict(orient='records')  # Fix: add self. before movie

    #     return dict_movie

    # def get_simular_description(self, request_data: dict) -> list:
    #     desc_list = [item.description for item in request_data]

    #     prediction = self.search(desc_list)
    #     subsr_list = [str(item.get('content_id')) for item in prediction]
    #     return subsr_list
    
    # def save(self):
    #     faiss.write_index(self.index, 'resource/save_index.index')