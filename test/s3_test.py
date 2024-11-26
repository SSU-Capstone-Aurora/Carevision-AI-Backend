import boto3

from src.camera_stream.stream_sendto_kafka import stream_rtsp_and_send_to_kafka

s3 = boto3.client('s3')
bucket_name = 'carevision-bucket'

def s3_test():
    file_name = 'example.txt'
    data = b"Hello, this is a test file!"

    s3.put_object(Bucket=bucket_name, Key=file_name, Body=data)


async def s3_save_video_test():
    print("1. set up===================")
    await stream_rtsp_and_send_to_kafka("seoul_hospital",1)
    print("5. save ==================")
