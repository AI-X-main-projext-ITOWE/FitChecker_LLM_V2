import re

def preprocess_text(raw_text):
    """
    텍스트 전처리 함수
    """
    # 1. Null 문자 제거
    cleaned_text = raw_text.replace("\u0000", "")

    # 2. 중복 줄바꿈 및 공백 정리
    cleaned_text = re.sub(r"\n+", "\n", cleaned_text)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)

    # 3. 특수문자 제거
    cleaned_text = re.sub(r"[^\w\s\.,!?]", "", cleaned_text)

    # 4. 앞뒤 공백 제거
    cleaned_text = cleaned_text.strip()

    return cleaned_text


def preprocess_results(results):
    """
    딕셔너리 리스트 형태의 데이터를 전처리하고 같은 형식으로 반환
    """
    processed_results = []
    for item in results:
        score = item["score"]  # 점수는 그대로 유지
        text = item["text"]    # 텍스트를 전처리
        cleaned_text = preprocess_text(text)
        processed_results.append({
            "score": score,
            "text": cleaned_text
        })
    return processed_results
