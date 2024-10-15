import cv2
import os

def stream_rtsp_and_save(url, output_path, codec='mp4v', fps=30, frame_size=(640, 480)):

    # RTSP 스트림 열기
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        print("카메라 스트림을 열 수 없습니다.")
        return

    # 저장할 비디오 파일 경로 설정
    fourcc = cv2.VideoWriter_fourcc(*codec)  # 코덱 설정 (MP4용 mp4v)
    out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

    if not out.isOpened():
        print("비디오 파일을 저장할 수 없습니다.")
        cap.release()
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("프레임을 가져올 수 없습니다.")
            break

        # 화면에 프레임 출력
        cv2.imshow("RTSP 스트림", frame)

        # 프레임을 파일에 저장
        out.write(frame)

        # 'q'를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 모든 작업 종료 후 자원 해제
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# RTSP URL
url = "rtsp://admin:L2CFB0FD@192.168.35.64/cam/realmonitor?channel=1&subtype=0"

# 저장할 파일 경로
output_folder = r"C:\VideoStream"
output_file = os.path.join(output_folder, 'stream_output.mp4')

# 프레임 크기 (카메라에 따라 변경 필요)
frame_size = (1920, 1080)

# RTSP 스트림을 받아 실시간 저장 및 화면 출력
stream_rtsp_and_save(url, output_file, codec='mp4v', fps=30, frame_size=frame_size)
