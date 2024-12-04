
from sentence_transformers import SentenceTransformer
from util.env_manager import *


def get_embedding_model():
    model_name = get_sentence_transformer_model()
    return SentenceTransformer(model_name)

