FROM python:3.9-slim

WORKDIR /app-ai

COPY requirements.txt /app-ai/

RUN pip install --no-cache-dir -r requirements.txt

# 영상 처리에 필요한 시스템 라이브러리 설치
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# FFmpeg 설치
RUN apt-get install -y ffmpeg

# 어플리케이션 코드 복사
COPY . /app-ai

ENV PORT=5001

EXPOSE 5001 5002

# sh -c를 사용하여 환경 변수를 참조
CMD ["sh", "-c", "uvicorn app-ai:app --host 0.0.0.0 --port ${PORT}"]
