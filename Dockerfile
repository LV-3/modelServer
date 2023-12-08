# 멀티 스테이지 빌드 - 첫 번째 스테이지
FROM python:3.9-slim-buster as builder

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# 패키지 설치
RUN pip install --no-cache-dir -r /code/requirements.txt

# 두 번째 스테이지 - 최종 이미지
FROM python:3.9-slim-buster

WORKDIR /code

# 이전 스테이지에서 설치한 패키지만 복사
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

COPY ./app /code/app

# CMD는 그대로 유지
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
