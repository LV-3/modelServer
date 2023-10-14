# https://fastapi.tiangolo.com/deployment/docker/

FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 두 줄은 배포할 때 주석 해제하고 실행
#COPY ./app /code/app
#CMD ['uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8080']