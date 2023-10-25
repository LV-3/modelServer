from fastapi import APIRouter
from pydantic import BaseModel





deepfm = APIRouter(prefix='/deepfm')


@deepfm.get('/',tags=['DeepFM'])
async def HereIsDeepFM():
    return {'msg':'deepfm경로'}


# @deepfm.post('/predict',tags=['deepfm'])
# async def ~