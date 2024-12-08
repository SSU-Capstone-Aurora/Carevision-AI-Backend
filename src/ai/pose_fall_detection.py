import base64

import cv2
import mediapipe as mp
import numpy as np

from src.config.kafka_broker_instance import broker

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# For static images:
IMAGE_FILES = []
BG_COLOR = (192, 192, 192)  # gray

fps = 30  #  초당 30프레임으로 설정
wait_time = 1000 // fps  # 밀리초로 변환

# 영상 데이터를 바이트로 변환하는 함수
def encode_image(image):
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')


async def pose_fall_detection(topic, user_id, url):
    kafka_topic = topic+"-alarm"

    with mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.5) as pose:
        for idx, file in enumerate(IMAGE_FILES):
            image = cv2.imread(file)
            image_height, image_width, _ = image.shape
            # Convert the BGR image to RGB before processing.
            results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            if not results.pose_landmarks:
                continue
            print(
                f'Nose coordinates: ('
                f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
                f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height})'
            )

            annotated_image = image.copy()
            # Draw segmentation on the image.
            # To improve segmentation around boundaries, consider applying a joint
            # bilateral filter to "results.segmentation_mask" with "image".
            condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
            bg_image = np.zeros(image.shape, dtype=np.uint8)
            bg_image[:] = BG_COLOR
            annotated_image = np.where(condition, annotated_image, bg_image)
            # Draw pose landmarks on the image.
            mp_drawing.draw_landmarks(
                annotated_image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
            # Plot pose world landmarks.
            mp_drawing.plot_landmarks(
                results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

    try:
        cap = cv2.VideoCapture(url)
    except cv2.error as e:
        print(f"Error opening video stream: {e}")
        return

    cnt = 0  # 카운트

    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            results = pose.process(image)

            keypoints = []
            if results.pose_landmarks:
                for data_point in results.pose_landmarks.landmark:
                    keypoints.append({
                        'X': data_point.x,
                        'Y': data_point.y,
                        'Z': data_point.z,
                        'Visibility': data_point.visibility,
                    })

                a = keypoints[10]['Y']
                b = keypoints[24]['Y']

                diff = abs(b - a)

                if diff < 0.1:
                    cnt += 1
                    print(f'{cnt}번 쓰러짐 감지!, 넘어진듯')

                    # 첫번 째만 출력되게 - 알람을 보내는 용
                    if cnt == 1:
                        await broker.publish(message=user_id.encode('utf-8'), topic=kafka_topic, key=user_id.encode('utf-8'))
                    # 랜드마크 그리기
                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    mp_drawing.draw_landmarks(
                        image,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

                    # 이미지를 base64로 변환해서 Kafka로 전송
                    encoded_image = encode_image(image).encode('utf-8')
                    message = {"key": user_id.encode('utf-8'), "data": encoded_image}
                    await broker.publish(message=message, topic=topic, key=user_id.encode('utf-8'))
                else:
                    cnt=0
            # 30 FPS로 대기
            if cv2.waitKey(wait_time) & 0xFF == 27:
                break

    cap.release()


