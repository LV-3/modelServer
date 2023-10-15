from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from gensim.models.doc2vec import Doc2Vec,TaggedDocument


# TODO conda activate lv3_fastapi

# TODO BE에서 오는 데이터 모델로 보내기
# TODO BE랑 모델 서버랑 연결




  # TODO. 모델 joblib으로 저장하고 불러오는 방식으로 만들기
    # '''
    # loaded_model = joblib.load('d2v_model.joblib')

    # #불러온 모델을 사용
    # vector = loaded_model.infer_vector(~)
    # '''


app = FastAPI()

DB =[]


@app.get('/')
def read_root():
    return {'hello': 'World'}



class Model(BaseModel):
  genre1: str
  genre2: str
  genre3: str

@app.get('/get_data')
async def get_rs_data():

    return DB

@app.post('/input_data')
async def contents_based_rs(data:Model):
  # 문서 샘플 데이터 (TaggedDocument 형식으로 작성)
  documents = [
      TaggedDocument(words=["commedy", "action", "crime", "first", "detective"], tags=["극한직업"]),
      TaggedDocument(words=["animation", "drama", "melodrama", "romance"], tags=["너의 이름은"]),
      TaggedDocument(words=["action", "crime",'drama'], tags=["더 배트맨"]),
  ]




  # Doc2Vec 모델 학습
  model = Doc2Vec(vector_size=20, window=2, min_count=1, workers=4, epochs=100)

  model.build_vocab(documents)

  model.train(documents, total_examples=model.corpus_count, epochs=model.epochs)

  # 문서 벡터 검색
  inferred_vector = model.infer_vector([data.genre1, data.genre2, data.genre3])
#   print("Inferred Vector:", inferred_vector)

  # 유사한 문서 찾기
  similar_documents = model.dv.most_similar([inferred_vector])
  print("Similar Documents:", similar_documents)
  RecommendedList=[]
  for elm in similar_documents:
    RecommendedList.append(elm[0])

  print(RecommendedList)

  global DB
  DB = RecommendedList
  return RecommendedList