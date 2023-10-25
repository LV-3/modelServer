
# d2v_router.py 
# 1. models 디렉토리에서 모델 가져오고
# 2. 라우터 설정
#   * post, predict(결과값 산출)
# 3. main.py 에는 d2v_router의 경로를 추가해주기

from fastapi import APIRouter
from pydantic import BaseModel

#TODO 모델 가져오기 코드

d2v = APIRouter(prefix='/d2v')

# router 경로 설정
@d2v.get('/',tags=['d2v_model'])
async def start_d2v():
    return {"msg":'d2v위치'}


class Model(BaseModel):
    genre1: str
    genre2: str
    genre3: str

from gensim.models.doc2vec import Doc2Vec, TaggedDocument

# 문서 샘플 데이터 (TaggedDocument 형식으로 작성)
documents = [
    TaggedDocument(words=["comedy", "action", "crime", "first", "detective"], tags=["극한직업"]),
    TaggedDocument(words=["animation", "drama", "melodrama", "romance"], tags=["너의 이름은"]),
    TaggedDocument(words=["action", "crime", "drama"], tags=["더 배트맨"]),
]

# Doc2Vec 모델 학습
model = Doc2Vec(vector_size=20, window=2, min_count=1, workers=4, epochs=100)
model.build_vocab(documents)
model.train(documents, total_examples=model.corpus_count, epochs=model.epochs)

def get_similar_movies(genre1, genre2, genre3):
    inferred_vector = model.infer_vector([genre1, genre2, genre3])
    similar_documents = model.dv.most_similar([inferred_vector])
    recommended_list = [elm[0] for elm in similar_documents]
    return recommended_list




@d2v.post('/predict',tags=['d2v_model'])
async def contents_based_rs(data: Model):
    recommended_list = get_similar_movies(data.genre1, data.genre2, data.genre3)
    global DB
    DB = recommended_list
    return recommended_list





