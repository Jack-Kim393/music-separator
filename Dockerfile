# Python 런타임 환경 설정
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# FFmpeg 설치
RUN apt-get update && apt-get install -y ffmpeg

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



# 소스 코드 복사
COPY . .

# 모델 경로 환경변수 설정
ENV MODEL_PATH /app/pretrained_models
