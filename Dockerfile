FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /work

# 시스템 종속성 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# pip 업그레이드
RUN pip install --upgrade pip

# requirements.txt 복사
COPY requirements.txt .

# PyTorch 패키지를 추가 인덱스로 설치 (requirements.txt에서 이미 설정한 경우 필요 없음)
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# 나머지 애플리케이션 파일 복사
COPY . /work/

# FastAPI 애플리케이션 실행
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
