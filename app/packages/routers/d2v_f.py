# # d2v.py

# from gensim.models.doc2vec import Doc2Vec, TaggedDocument

# # 문서 샘플 데이터 (TaggedDocument 형식으로 작성)
# documents = [
#     TaggedDocument(words=["comedy", "action", "crime", "first", "detective"], tags=["극한직업"]),
#     TaggedDocument(words=["animation", "drama", "melodrama", "romance"], tags=["너의 이름은"]),
#     TaggedDocument(words=["action", "crime", "drama"], tags=["더 배트맨"]),
# ]

# # Doc2Vec 모델 학습
# model = Doc2Vec(vector_size=20, window=2, min_count=1, workers=4, epochs=100)
# model.build_vocab(documents)
# model.train(documents, total_examples=model.corpus_count, epochs=model.epochs)

# def get_similar_movies(genre1, genre2, genre3):
#     inferred_vector = model.infer_vector([genre1, genre2, genre3])
#     similar_documents = model.dv.most_similar([inferred_vector])
#     recommended_list = [elm[0] for elm in similar_documents]
#     return recommended_list