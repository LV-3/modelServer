import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer

class Sbert:
    def __init__(self):
        # self.movie = movie = pd.read_pickle('resource/movie.pickle')
        self.movie = pd.read_csv('app/resource/final_test_sbert_VODs_1127_1100.csv')
        self.description_list = self.movie['SMRY'].to_list()
        self.model_args ={
            'sbert_klue' : 'snunlp/KR-SBERT-V40K-klueNLI-augSTS',
            'sbert_sts':'jhgan/ko-sbert-sts',
            'sroberta':'jhgan/ko-sroberta-multitask',
            'albert':'bongsoo/albert-small-kor-sbert-v1.1'
            }

        self.model = SentenceTransformer(self.model_args['sroberta'])

        # self.encoded_data = self.model.encode(self.description_list)

        # # faiss 인덱스 생성 
        # # 임베딩한 값을 faiss 인덱스에 저장함.
        # self.index = faiss.IndexIDMap(faiss.IndexFlatIP(768))

        # # 데이터 id 배열
        # self.index.add_with_ids(self.encoded_data, np.array(range(0, len(self.description_list))))
        self.index = faiss.read_index('app/resource/final_test_sbert_VODs_1127_1100.index')


        
    def search(self, query: str) -> dict:
        query_vector = self.model.encode([query]) 
        k = 21
        D,I = self.index.search(query_vector, k)
        sorted_indices = np.argsort(D,axis=1)
        D_sorted = np.take_along_axis(D, sorted_indices, axis=1)
        I_sorted = np.take_along_axis(I, sorted_indices, axis=1)
        dict_movie = self.movie.loc[I_sorted[0].tolist()].to_dict(orient='records') # 하나의 줄거리 - 21 append 105

        return dict_movie

    def get_simular_description(self, request_data: dict) -> list:
        desc_list = [item.description for item in request_data]

        prediction = self.search(desc_list)
        subsr_list = [str(item.get('content_id')) for item in prediction]
        return subsr_list
    
    def save(self):
        faiss.write_index(self.index, 'resource/save_index.index')