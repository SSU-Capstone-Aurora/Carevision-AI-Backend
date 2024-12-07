import asyncio
import base64
import os
import time

import cv2
import numpy as np

from src.video.s3_upload import s3_upload

frames = []
last_data_time = time.time()  # 마지막 데이터 수신 시간

async def image_handler(data, key):
    global last_data_time
    last_data_time = time.time()

    image_data = base64.b64decode(data)

    # 이미지를 numpy 배열로 변환
    np_image = np.frombuffer(image_data, dtype=np.uint8)
    image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    if image is not None:
        frames.append(image)

    await check_for_idle_time(key)

async def check_for_idle_time(key):
    global last_data_time
    idle_time_limit = 3  # 3초 동안 데이터가 없으면 저장

    while True:
        await asyncio.sleep(1)  # 매 초마다 체크
        if time.time() - last_data_time > idle_time_limit:
            if len(frames) > 0:
                print(f"{idle_time_limit}초 동안 데이터가 없어, 영상을 저장합니다.")

                # 영상 저장을 위한 출력 설정
                video_filename = f"output_idle_{int(time.time())}.mp4"
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                video_writer = cv2.VideoWriter(video_filename, fourcc, 10, (frames[0].shape[1], frames[0].shape[0]))

                # 프레임을 영상으로 합치기
                for frame in frames:
                    video_writer.write(frame)

                # 영상 저장 완료 후, S3에 업로드
                video_writer.release()
                s3_upload(video_filename, key)

                # 로컬 파일 삭제
                if os.path.exists(video_filename):
                    os.remove(video_filename)

                # 프레임 리스트 초기화
                frames.clear()

            # 타이머 초기화
            last_data_time = time.time()