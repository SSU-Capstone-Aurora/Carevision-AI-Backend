class CameraNotFound(Exception):
    def __init__(self, message="카메라 정보를 찾을 수 없습니다."):
        super().__init__(f"환자의 {message}")