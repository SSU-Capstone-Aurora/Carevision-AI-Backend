import os

from dotenv import load_dotenv

from src.database.database import get_user_and_camera

# .env 파일 로딩
load_dotenv()
url_format = os.getenv("URL_FORMAT")


def get_rtsp_url(patient_id):
    camera_ip, camera_pw = get_user_and_camera(patient_id)
    url = url_format.format(camera_pw=camera_pw, camera_ip=camera_ip)
    return url
