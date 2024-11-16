import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

from src.error import camera_error

# 환경 변수 로드
load_dotenv()

# 환경 변수에서 데이터베이스 설정 가져오기
host = "host.docker.internal"
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')

# SQLAlchemy 엔진 생성
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')


def get_user_and_camera(patient_id):
    query = f"""
        SELECT c.ip, c.password
        FROM patient p
        JOIN camera c ON p.patient_id= c.patient_id
        WHERE p.patient_id = {patient_id}
    """

    df = pd.read_sql(query, engine)

    if not df.empty:
        camera_ip = df.iloc[0]['ip']
        camera_password = df.iloc[0]['password']
        return camera_ip, camera_password
    else:
        raise camera_error.CameraNotFound(patient_id)
