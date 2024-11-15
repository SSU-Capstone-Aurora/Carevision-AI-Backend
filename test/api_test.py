from fastapi import APIRouter

from test.ffmpeg_test import ffmpeg_test
from test.stream_test import send_example

router = APIRouter()


@router.get('/test')
async def test_send():
    await send_example()
    print("send_example 함수 실행 완료")


@router.get('/test/stream')
def test_ffmpeg():
    print("ffmpeg 테스트 실행")
    ffmpeg_test()
