from elasticsearch import Elasticsearch
from util.env_manager import *

def elastic_creator():
    host = get_elasticsearch_url()
    return Elasticsearch(host)

        