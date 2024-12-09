import httpx
from util.env_manager import *
import requests


async def send_to_firebase(data):
    firebase_url = get_firebase_url()
    print(f"Firebase로 전송하는 데이터: {data}")
    # Firebase로 데이터 전송
    # response = await requests.post(firebase_url, json=data)

    # Firebase로 데이터 전송
    async with httpx.AsyncClient() as client:
        response = await client.post(firebase_url, json=data)


    # 상태 코드 확인
    if response.status_code != 200:
        print(f"Firebase 요청 실패: {response.status_code}, 응답: {response.text}")
        raise ValueError(f"Firebase 요청 실패: {response.status_code}")

    # 응답을 JSON으로 파싱
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"Firebase 응답이 JSON 형식이 아님: {response.text}")
        raise ValueError("Firebase 응답이 JSON 형식이 아님")
