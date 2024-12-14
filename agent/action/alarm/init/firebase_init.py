# firebase_init.py
from util.env_manager import *
import firebase_admin
from firebase_admin import credentials, db

# 환경 변수 로드

# Firebase 초기화 확인 후 초기화
def initalize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(get_firebase_credentials())
        firebase_admin.initialize_app(cred, {
            'databaseURL': get_firebase_url()
        })
