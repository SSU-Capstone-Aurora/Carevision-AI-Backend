import os
from datetime import datetime

import boto3
import cv2
import numpy as np
from dotenv import load_dotenv
from fastapi import HTTPException

from src.db.database_service import save_video_in_db

load_dotenv()
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region_name = os.getenv("AWS_REGION")
bucket_name = os.getenv("S3_BUCKET_NAME")

# S3 클라이언트 설정
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
                  region_name=region_name)


def s3_upload(video_filename,key):
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    s3_key = f"video/{key}/{current_time}.mp4"
    s3.upload_file(video_filename, bucket_name, s3_key)
    print(f"{video_filename} 업로드 완료")

    file_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
    save_video_in_db(key,file_url,s3_key)
    print("done")


def upload(frame: np.ndarray,patient_id) -> str:
    _, buffer = cv2.imencode('.jpg', frame)
    file_data = buffer.tobytes()

    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    s3_key = f"thumbnail/{patient_id}/{current_time}.jpg"

    try:
        s3.put_object(Bucket=bucket_name, Key=s3_key, Body=file_data, ContentType='image/jpeg')

        file_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
        return file_url

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"S3 업로드 중 오류가 발생했습니다: {str(e)}")