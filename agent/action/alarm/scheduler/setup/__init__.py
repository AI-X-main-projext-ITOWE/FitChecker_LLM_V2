# firebase_init.py
from util.env_manager import *
import firebase_admin
from firebase_admin import credentials, db

# 환경 변수 로드

# Firebase Admin SDK 초기화
cred = credentials.Certificate(get_firebase_credentials())
firebase_admin.initialize_app(cred, {
    'databaseURL': get_firebase_url()
})
