import asyncio

from fastapi import FastAPI

from src.camera_stream.kafka_streams import connect_broker
from src.config.kafka_broker_instance import kafka_app
from src.controller.stream_controller import stream_router
from test.api_test import router

app = FastAPI()
app.include_router(router)
app.include_router(stream_router)

@app.on_event("startup")
async def startup_event():
    await connect_broker()

    # FastStream 애플리케이션 실행
    asyncio.create_task(kafka_app.run())

@app.get('/ai-health')
def health_check():
    return {"I'm healthy!!!"}
