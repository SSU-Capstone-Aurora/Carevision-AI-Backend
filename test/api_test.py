from fastapi import APIRouter

from test.stream_test import send_example

router = APIRouter()

@router.get('/test')
async def test_send():  # 이 함수도 비동기 함수로 변경
    await send_example()  # await를 사용하여 비동기 호출
