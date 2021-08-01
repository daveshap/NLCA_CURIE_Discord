import requests

def post_to_corpus(payload)
    resp = requests.request(method='POST', url='http://127.0.0.1:9999/', json=payload, timeout=45)
    return resp.json()


def transformer_completion(payload):
    resp = requests.request(method='POST', url='http://127.0.0.1:7777/completion', json=payload)
    return resp.json()


def add_to_recall(payload):
    resp = requests.request(method='POST', url='http://127.0.0.1:8888/add', json=payload)
    return resp.json()


def recall_answer(payload):
    resp = requests.request(method='POST', url='http://127.0.0.1:8888/answer', json=payload)
    return resp.json()