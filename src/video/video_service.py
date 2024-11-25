import cv2
from fastapi import HTTPException

from src.video.s3_upload import upload


def save_thumbnail(url, patient_id):
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        raise HTTPException(status_code=400, detail="카메라 스트림을 열 수 없습니다.")

    ret, frame = cap.read()

    if not ret:
        raise HTTPException(status_code=400, detail="프레임을 가져올 수 없습니다.")

    file_url = upload(frame, patient_id)

    cap.release()

    return file_url
