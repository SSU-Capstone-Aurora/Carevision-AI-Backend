import base64
import time

import cv2
import numpy as np

from src.video.s3_upload import s3_upload

frames = []

async def image_handler(msg):
    image_data = base64.b64decode(msg.data)

    # 이미지를 numpy 배열로 변환
    np_image = np.frombuffer(image_data, dtype=np.uint8)
    image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    if image is not None:
        frames.append(image)

    # 10개의 프레임을 모은 후, MP4 파일로 저장
    if len(frames) >= 20:
        print("10개의 프레임이 모였으므로, 영상을 저장합니다.")

        # 영상 저장을 위한 출력 설정
        # todo: 저장 파일 이름 수정 필요
        video_filename = f"output_{int(time.time())}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(video_filename, fourcc, 10, (image.shape[1], image.shape[0]))

        # 프레임을 영상으로 합치기
        for frame in frames:
            video_writer.write(frame)

        # 영상 저장 완료 후, S3에 업로드
        video_writer.release()
        s3_upload(video_filename)

        # 프레임 리스트 초기화
        frames.clear()
