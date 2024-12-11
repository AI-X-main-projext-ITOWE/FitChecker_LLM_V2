import os
import fitz
from transformers import LayoutLMTokenizer, LayoutLMForTokenClassification
import torch
from util.env_manager import *

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

class AdvertisementsOperator():
    def __init__(self):
        self.model_name = get_detect_ad_model()
        self.layoutlm_tokenizer = LayoutLMTokenizer.from_pretrained(self.model_name)
        self.layoutlm_model = LayoutLMForTokenClassification.from_pretrained(self.model_name).to(device)
    def extract_text_from_pdf(self, folder_path):
        """Extract text and bounding boxes from all PDF files in a folder using PyMuPDF."""
        all_texts = []
        all_coordinates = []

        for filename in os.listdir(folder_path):
            if filename.lower().endswith(".pdf"):
                pdf_path = os.path.join(folder_path, filename)
                pdf_document = fitz.open(pdf_path)

                for page_num in range(len(pdf_document)):
                    page = pdf_document[page_num]
                    blocks = page.get_text("dict")["blocks"]

                    for block in blocks:
                        if "lines" not in block:
                            continue

                        for line in block["lines"]:
                            for span in line["spans"]:
                                if span["text"].strip():  # 빈 텍스트 제외
                                    all_texts.append(span["text"])
                                    all_coordinates.append((
                                        span["bbox"][0],  # left
                                        span["bbox"][1],  # top
                                        span["bbox"][2] - span["bbox"][0],  # width
                                        span["bbox"][3] - span["bbox"][1]   # height
                                    ))

                pdf_document.close()

        return all_texts, all_coordinates
    
    def detect_advertisements(self, texts, coordinates):
        """Detect advertisements using LayoutLM."""
        if not texts:  # 텍스트가 비어 있는 경우 처리
            print("No texts detected for advertisement detection.")
            return []

        # Tokenize texts for LayoutLM
        inputs = self.layoutlm_tokenizer(texts, return_tensors="pt", truncation=True, padding=True, is_split_into_words=True).to(device)
        outputs = self.layoutlm_model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=-1)

        # 광고로 예측된 인덱스 확인
        ad_indices = []
        for i, label in enumerate(predictions[0]):
            # 모델 라벨링 기준에 따라 광고 라벨(예: label == 1)을 확인
            if i < len(coordinates) and label == 1:
                ad_indices.append(i)

        # 광고 텍스트 추출
        ad_texts = [texts[i] for i in ad_indices]

        return ad_texts
    
    def process_pdf_for_ads_only(self, pdf_path):
        """Process PDF and return only advertisement texts."""
        # Step 1: Extract text and coordinates directly from PDF
        print(f"Extracting text and coordinates from {pdf_path}...")
        texts, coordinates = self.extract_text_from_pdf(pdf_path)

        if not texts:
            print("No texts found in the PDF.")
            return []

        # Step 2: Detect advertisement texts
        print("Detecting advertisement texts...")
        ad_texts = self.detect_advertisements(texts, coordinates)
        print(f"Advertisement texts detected: {ad_texts}")

        return ad_texts