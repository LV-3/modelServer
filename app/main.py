from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

# TODO conda activate lv3_fastapi

# TODO BE에서 오는 데이터 모델로 보내기
# TODO BE랑 모델 서버랑 연결

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get('/')
def read_root():
    return {'hello_havi_1555': 'World'}

@app.get('/items/{item_id}')
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q":q}

@app.put('/items/{item_id}')
def update_item(item_id: int, item: Item):
    return {'item_name' : item.name, 'item_id': item_id}