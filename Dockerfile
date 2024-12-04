# Python 3.10 버전으로 시작
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# pip 업그레이드
RUN pip install --upgrade pip

# 필요한 파일들 복사
COPY . /app/

# 의존성 설치 (networkx 버전 수정)
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 애플리케이션 실행
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]