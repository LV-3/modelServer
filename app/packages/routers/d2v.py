from gensim.models.doc2vec import Doc2Vec, TaggedDocument

class Doc2VecModel:
    def __init__(self):
        # tagged_documents = [ TaggedDocument(words=row['words'], tags=[row['tags']]) for _, row in df.iterrows() ]

        self.documents = [
            TaggedDocument(words=["comedy", "action", "crime", "first", "detective"], tags=["극한직업"]),
            TaggedDocument(words=["animation", "drama", "melodrama", "romance"], tags=["너의 이름은"]),
            TaggedDocument(words=["action", "crime", "drama"], tags=["더 배트맨"]),
        ]
        self.model = Doc2Vec(vector_size=20, window=2, min_count=1, workers=4, epochs=100)
        self.model.build_vocab(self.documents)
        self.model.train(self.documents, total_examples=self.model.corpus_count, epochs=self.model.epochs)

        
    # def tagging_words(self, mood_df) -> TaggedDocument:
        # tagged_documents = [TaggedDocument(words = row['words'], tags=[row['tags']]) for _, row in mood_df.iterrows()]


    def get_similar_movies(self, mood_list) -> list:
        inferred_vector = self.model.infer_vector(mood_list)
        similar_documents = self.model.dv.most_similar([inferred_vector])
        recommended_list = [elm[0] for elm in similar_documents]
        return recommended_list


    def get_contents_based_rs(self, request_data) -> list: # 변경 예정
        md_list = [item.mood for item in request_data]
        flat_md_list = [item for sublist in md_list for item in sublist]
        
        res_md_list = self.get_similar_movies(flat_md_list)
        return res_md_list