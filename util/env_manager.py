import os
from dotenv import load_dotenv

load_dotenv()

def get_elasticsearch_url():
    return os.getenv("ELASTICSEARCH_URL")

def get_youtube_api_key():
    return os.getenv("YOUTUBE_API_KEY")

def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY")

def get_cors_origins():
    return os.getenv("CORS_ORIGINS")

def get_pdf_folder_path():
    return os.getenv("PDF_FOLDER_PATH")

def get_json_folder_path():
    return os.getenv("JSON_FOLDER_PATH")

def get_sentence_transformer_model():
    return os.getenv("SENTENCE_TRANSFORMER_MODEL")

def get_pdf_ocr_model():
    return os.getenv("PDF_OCR_MODEL")

def get_huggingface_token():
    return os.getenv("HUGGINFACE_TOKEN")