from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pandas as pd
from app.main import MoodDataItem


class Doc2VecModel:
    def __init__(self):
        self.documents = pd.read_pickle('app/resources/tagged_documents.pickle')
        self.model = Doc2Vec(vector_size=20, window=2, min_count=1, workers=4, epochs=100)
        self.model.build_vocab(self.documents)
        self.model.train(self.documents, total_examples=self.model.corpus_count, epochs=self.model.epochs)

        
    def tagging_words(self, mood_df: pd.DataFrame) -> TaggedDocument:
        tagged_documents = [TaggedDocument(words = row['extend_template'], tags=[row['title']]) for _, row in mood_df.iterrows()]


    def get_similar_movies(self, mood_list: list[str]) -> list[str]:
        inferred_vector = self.model.infer_vector(mood_list)
        similar_documents = self.model.dv.most_similar([inferred_vector], topn=21)
        recommended_list = [str(elm[0]) for elm in similar_documents]

        return recommended_list


    def get_contents_based_rs(self, request_data: MoodDataItem) -> list[str]:
        md_list = []
        
        for item in request_data:
            if item.mood is not None:
                md_list.append(item.mood)
        flat_md_list = [item for sublist in md_list for item in sublist]
        
        res_md_list = self.get_similar_movies(flat_md_list)

        return res_md_list
