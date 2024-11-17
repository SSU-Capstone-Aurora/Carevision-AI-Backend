import os
import subprocess

import cv2
from dotenv import load_dotenv

# .env 파일 로딩
load_dotenv()
camera_id = os.environ.get("CAMERA_ID")
camera_pw = os.environ.get("CAMERA_PASSWORD")
camera_ip = os.environ.get("CAMERA_IP")
stream_ip = os.environ.get("STREAM_IP")
stream_port = os.environ.get("STREAM_PORT")

# input url
url = f"rtsp://{camera_id}:{camera_pw}@{camera_ip}/cam/realmonitor?channel=1&subtype=0"

# output url
output_url = f"rtsp://{stream_ip}:{stream_port}/output_stream"


def ffmpeg_test():
    # RTSP 스트림 열기
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        print("입력 스트림을 열 수 없습니다.")
        return

    ffmpeg_command = [
        'ffmpeg', '-y',
        '-f', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', f"{int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}",
        '-r', str(int(cap.get(cv2.CAP_PROP_FPS))),
        '-i', '-',
        '-c:v', 'libx264',
        '-preset', 'ultrafast',
        '-f', 'rtsp',
        output_url
    ]

    process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

    print("ffmpeg open done")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("프레임을 더 이상 읽을 수 없습니다.")
                break
            process.stdin.write(frame.tobytes())
    except Exception as e:
        print(f"error: {e}")
    finally:
        cap.release()
        process.stdin.close()
        process.wait()
