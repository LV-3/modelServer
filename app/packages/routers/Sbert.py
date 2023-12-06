import numpy as np
import pandas as pd
import faiss
from transformers import AutoModel, AutoTokenizer
import pickle
import random


class Sbert:
    def __init__(self):

        self.index = faiss.read_index('app/resources/Union_SMRY_RoBERTa_emb_v2.index')

        with open('app/resources/FaissIndex2Content_id.pickle','rb') as pickle_file:
            self.FaissIndex2Content_id = pickle.load(pickle_file)

        self.model = AutoModel.from_pretrained('BM-K/KoDiffCSE-RoBERTa')
        self.tokenizer = AutoTokenizer.from_pretrained('BM-K/KoDiffCSE-RoBERTa')


    def embedding(self, query: str):
        
        inputs = self.tokenizer(query, padding=True, truncation=True, return_tensors="pt")
        embeddings, _ = self.model(**inputs, return_dict=False)

        return embeddings[0][0].tolist()

    def ContentId2FaissIndex(self, content_id: int) -> np.ndarray:
        faiss_index = self.FaissIndex2Content_id.get(content_id)
        emb = self.index.reconstruct(faiss_index)
        emb_np = np.array(emb).reshape(1, -1)
        return emb_np
    
    def search(self, query: dict) -> list[str]:
        
        content_id_list = [int(item.content_id) for item in query]
        print("content_id_list: ",content_id_list)
        query_list = []

        for content_id in content_id_list:
            query = self.ContentId2FaissIndex(content_id)
            query_list.append(query)

        query_array = np.vstack(query_list)

        k = 21
        D, I = self.index.search(query_array, k)

        index_list = I.flatten().tolist()
        index_list = random.sample(index_list, 21)

        recommend_content_id = [str(self.FaissIndex2Content_id.get(key)) for key in self.FaissIndex2Content_id.keys() if key in index_list]

        return recommend_content_id

   
