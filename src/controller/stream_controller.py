from fastapi import APIRouter

from src.camera_stream.stream_sendto_kafka import stream_rtsp_and_send_to_kafka

stream_router = APIRouter()


@stream_router.get("/video/{user_id}")
async def stream_video(topic: str, user_id: str):
    return await stream_rtsp_and_send_to_kafka(topic, user_id)  # 병원을 토픽으로, 환자 key, data값으로 저장
