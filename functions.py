import requests
from time import sleep

def post_to_outer_loop(payload)
    resp = requests.request(method='POST', url='http://127.0.0.1:9999/', json=payload, timeout=45)
    return resp.json()


def transformer_completion(payload):
    resp = requests.request(method='POST', url='http://127.0.0.1:7777/completion', json=payload, timeout=15)
    return resp.json()


def save_to_shared_db(payload):
    resp = requests.request(method='POST', url='http://127.0.0.1:8888/', json=payload)
    return resp.json()


def search_db_keywords(keywords):
    records = list()
    for i in keywords.split():
        resp = requests.request(method='GET', url='http://127.0.0.1:8888/', json={'query': i}, timeout=45)
        records = resp.json()
        # TODO concatenate records cleanly (deduplicate by UUID)
    return records
    


def make_prompt_default(filename, content):
    with open(filename, 'r') as infile:
        prompt = infile.read()
    prompt = prompt.replace('<<TEXT>>', content)
    return prompt