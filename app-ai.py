from fastapi import FastAPI

from camera_stream.stream_sendto_kafka import stream_rtsp_and_send_to_kafka
from test.api_test import router

app = FastAPI()
app.include_router(router)

@app.get('/ai-health')
def health_check():
    return {"I'm healthy!!!"}

@app.get("/video/{user_id}")
def stream_video(topic: str, user_id: str):
    return stream_rtsp_and_send_to_kafka(topic, user_id) #병원을 토픽으로, 환자 key, data값으로 저장