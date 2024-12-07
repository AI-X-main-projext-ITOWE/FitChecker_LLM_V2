from transformers import VisionEncoderDecoderModel, DonutProcessor
import json
import fitz # type: ignore
from util.env_manager import *
from PIL import Image

# 모델과 프로세서 로드
model_name = get_pdf_ocr_model()
model = VisionEncoderDecoderModel.from_pretrained(model_name)
processor = DonutProcessor.from_pretrained(model_name)


folder_path = get_pdf_folder_path()

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

def extract_pdf_sentence(folder_path, use_ocr=False):
    """
    PDF 텍스트 추출 함수.
        Args:
        folder_path (str): PDF 파일이 있는 폴더 경로.
        use_ocr (bool): True면 OCR(Donut 모델)을 사용하여 텍스트를 추출.
        Returns:
        str: 추출된 모든 PDF 텍스트.
    """
    pdf_data = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            try:
                doc = fitz.open(pdf_path)
                text = ""

                if use_ocr:  # OCR 방식으로 텍스트 추출
                    for page_num in range(len(doc)):
                        page = doc.load_page(page_num)
                        pix = page.get_pixmap()
                        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        
                        # OCR 수행
                        pixel_values = processor(image, return_tensors="pt").pixel_values
                        generated_ids = model.generate(pixel_values)
                        page_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
                        
                        text += page_text + "\n\n"
                else:  # 기본 텍스트 추출
                    for page in doc:
                        text += page.get_text()

                pdf_data.append(text)
            except Exception as e:
                print(f"Error processing file {pdf_path} : {e}")

    return " ".join(pdf_data)

    

