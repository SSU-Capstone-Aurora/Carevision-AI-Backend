from fastapi import APIRouter

from test.stream_test import send_example

router = APIRouter()

@router.get('/test')
async def test_send():
    await send_example()
    print("send_example 함수 실행 완료")

