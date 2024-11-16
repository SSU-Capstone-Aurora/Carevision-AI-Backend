from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.camera_stream.patient_camera import get_rtsp_url
from src.error import camera_error

from src.camera_stream.stream_sendto_kafka import stream_rtsp_and_send_to_kafka

stream_router = APIRouter()


@stream_router.get("/video/{user_id}")
async def stream_video(topic: str, user_id: str):
    return await stream_rtsp_and_send_to_kafka(topic, user_id)  # 병원을 토픽으로, 환자 key, data값으로 저장


@stream_router.get("/api/streaming/{patient_id}", tags=["Streaming API"])
def stream_video(patient_id: str):
    try:
        url = get_rtsp_url(patient_id)

        return JSONResponse(
            content={"code": 200, "message": "Success", "data": {"url": url}},
            status_code=200
        )

    except camera_error.CameraNotFound as e:
        return JSONResponse(
            content={"code": 404, "message": str(e)},
            status_code=404
        )
