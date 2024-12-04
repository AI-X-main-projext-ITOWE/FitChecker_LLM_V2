import json
import fitz # type: ignore

# 1. JSON 파일 로드
def load_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# 2. JSON 데이터에서 텍스트 추출
def extract_text_from_json(json_data, key="content"):
    texts = []
    for doc in json_data.get("documents", []):
        if key in doc:
            texts.append(doc[key])
    return texts

def extract_pdf_sentence(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

