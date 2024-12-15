import httpx
from util.env_manager import *
import requests
from firebase_admin import messaging
import asyncio
from datetime import datetime, timezone
from agent.action.alarm.scheduler.setup.scheduler_setup import scheduler


async def send_to_firebase(user_id, data):
    
    print(f"Firebase로 전송하는 데이터: {data}")
    # Firebase로 데이터 전송
    # response = await requests.post(firebase_url, json=data)
    firebase_url = f"{get_firebase_url()}/alarms/{user_id}.json"

    # Firebase로 데이터 전송
    async with httpx.AsyncClient() as client:
        response = await client.post(firebase_url, json=data)

    try:
    # 상태 코드 확인
        if response.status_code != 200:
            print(f"Firebase 요청 실패: {response.status_code}, 응답: {response.text}")
            raise ValueError(f"Firebase 요청 실패: {response.status_code}")

    # 응답을 JSON으로 파싱
    
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"Firebase 응답이 JSON 형식이 아님: {response.text}")
        raise ValueError("Firebase 응답이 JSON 형식이 아님")

def schedule_alarm(alarm_id, alarm_time_str, alarm_text, response, fcm_token):
    """
    알람 시간을 기반으로 FCM 알림을 스케줄링합니다.
    """
    # 알람 시간을 datetime 객체로 변환 (ISO 8601 형식 예상)
    try:
        alarm_time = datetime.fromisoformat(alarm_time_str)
    except ValueError as e:
        print(f'알람 시간 형식 오류: {alarm_time_str}, 오류: {e}')
        return
    
    
    if alarm_time.tzinfo is None:
        alarm_time = alarm_time.replace(tzinfo=timezone.utc)
    else:
        alarm_time = alarm_time.astimezone(timezone.utc)
    
    
    now = datetime.now(timezone.utc)
    
    if alarm_time <= now:
        print(f'알람 {alarm_id} 시간이 이미 지났습니다.')
        return
    
    # 스케줄링
    scheduler.add_job(
        lambda: asyncio.create_task(send_fcm_notification(fcm_token, alarm_text, response)),#run
        'date',
        run_date=alarm_time,
        id=alarm_id  # 고유한 alarm_id로 작업 ID 설정
    )
    print(f'알람 {alarm_id} 스케줄링 완료: {alarm_time}')


async def send_fcm_notification(fcm_token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=fcm_token,
    )
    try:
        response = messaging.send(message)
        print(f'알림 전송 성공: {response}')
    except Exception as e:
        print(f'알림 전송 실패: {e}')
