import os

import uvicorn
from fastapi import FastAPI

from src.camera_stream.kafka_streams import connect_broker
from src.camera_stream.stream_sendto_kafka import stream_rtsp_and_send_to_kafka
from src.config.kafka_broker_instance import kafka_app
from src.controller.video_controller import video_router
from test.api_test import router

app = FastAPI()
app.include_router(router)
app.include_router(video_router)

# @app.on_event("startup")
# async def startup_event():
#     await connect_broker()
#
#     # FastStream 애플리케이션 실행
#     asyncio.create_task(kafka_app.run())

@app.get('/ai-health')
def health_check():
    return {"I'm healthy!!!"}

@app.get("/video/{user_id}")
def stream_video(topic: str, user_id: str):
    return stream_rtsp_and_send_to_kafka(topic, user_id) #병원을 토픽으로, 환자 key, data값으로 저장


def main():
    # FastAPI 서버 실행
    uvicorn.run(
        "app-ai:app",  # FastAPI 애플리케이션 경로 (파일명:변수명)
        host="0.0.0.0",  # 모든 네트워크 인터페이스에서 수신
        port=int(os.getenv("PORT", 5000)),  # 환경 변수 PORT 사용, 기본값은 8000
        reload=True  # 코드 변경 시 자동 재시작 (개발 환경에서 유용)
    )

if __name__ == "__main__":
    main()