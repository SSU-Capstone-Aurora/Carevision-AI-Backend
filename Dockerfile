FROM python:3.9-slim

WORKDIR /app-ai

COPY requirements.txt /app-ai/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app-ai

ENV PORT=5001

EXPOSE 5001 5002

# sh -c를 사용하여 환경 변수를 참조
CMD ["sh", "-c", "uvicorn app-ai:app --host 0.0.0.0 --port ${PORT}"]
