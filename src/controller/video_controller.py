from fastapi import APIRouter

from src.video.video_service import save_thumbnail

video_router = APIRouter()


@video_router.get('/thumbnail')
def get_thumbnail(url: str, patient_id: int):
    file_url = save_thumbnail(url, patient_id)

    return {"s3_url": file_url}
