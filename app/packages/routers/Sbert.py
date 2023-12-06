import numpy as np
import pandas as pd
import faiss
from transformers import AutoModel, AutoTokenizer
import pickle


class Sbert:
    def __init__(self):

        self.index = faiss.read_index('app/resources/Union_SMRY_RoBERTa_emb.index')

        with open('app/resources/FaissIndex2Content_id.pickle','rb') as pickle_file:
            self.FaissIndex2Content_id = pickle.load(pickle_file)

        self.model = AutoModel.from_pretrained('BM-K/KoDiffCSE-RoBERTa')
        self.tokenizer = AutoTokenizer.from_pretrained('BM-K/KoDiffCSE-RoBERTa')


    def embedding(self, query: str):
        
        inputs = self.tokenizer(query, padding=True, truncation=True, return_tensors="pt")
        embeddings, _ = self.model(**inputs, return_dict=False)

        return embeddings[0][0].tolist()


    def search(self, query: str) -> list[str]:

        desc_list = [item.description for item in query]
        query_vector = self.embedding(desc_list)
        query_vector_np = np.array(query_vector).reshape(1,-1)

        k = 21

        D,I = self.index.search(query_vector_np,k)
        index_list = I.flatten().tolist()

        recommend_content_id = [str(self.FaissIndex2Content_id.get(key)) for key in self.FaissIndex2Content_id.keys() if key in index_list]

        return recommend_content_id

   
