import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

load_dotenv()

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')
url_format = os.getenv('URL_FORMAT')

# SQLAlchemy 엔진 생성
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')

# 세션 생성
Session = sessionmaker(bind=engine)

def save_video_in_db(patient_id, link, name):
    created_at = datetime.now()

    query = """
    INSERT INTO video (created_at, deleted_at, modified_at, patient_id, link, name) VALUES (:created_at, NULL, NULL, :patient_id, :link, :name);
    """

    params = {
        "created_at": created_at,
        "patient_id": patient_id,
        "link": link,
        "name": name,
    }

    # 세션을 사용하여 쿼리 실행
    with Session() as session:
        session.execute(text(query), params)  # 쿼리 실행
        session.commit()  # 변경사항 커밋

    print("Data inserted successfully.")