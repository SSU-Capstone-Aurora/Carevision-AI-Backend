import asyncio

from fastapi import FastAPI

from src.camera_stream.kafka_streams import connect_broker
from src.camera_stream.stream_sendto_kafka import stream_rtsp_and_send_to_kafka
from src.config.kafka_broker_instance import kafka_app
from test.api_test import router

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    await connect_broker()

    # FastStream 애플리케이션 실행
    asyncio.create_task(kafka_app.run())

@app.get('/ai-health')
def health_check():
    return {"I'm healthy!!!"}

@app.get("/video/{user_id}")
def stream_video(topic: str, user_id: str):
    return stream_rtsp_and_send_to_kafka(topic, user_id) #병원을 토픽으로, 환자 key, data값으로 저장