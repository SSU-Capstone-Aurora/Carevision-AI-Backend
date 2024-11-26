import os

import requests
from dotenv import load_dotenv

# .env 파일 로딩
load_dotenv()
api_url = os.getenv("API_URL")


def send_alarm_request(patient_id):
    url = f"{api_url}{patient_id}"

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}
