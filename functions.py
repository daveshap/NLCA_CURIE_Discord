import requests

def post_to_outer_loop(payload)
    resp = requests.request(method='POST', url='http://127.0.0.1:9999/', json=payload, timeout=45)
    return resp.json()


def transformer_completion(payload):
    resp = requests.request(method='POST', url='http://127.0.0.1:7777/completion', json=payload, timeout=15)
    return resp.json()


def add_to_recall(payload):
    resp = requests.request(method='POST', url='http://127.0.0.1:8888/add', json=payload)
    return resp.json()


def qa_answer(question):
    resp = requests.request(method='POST', url='http://127.0.0.1:8888/answer', json={'question': question}, timeout=45)
    return resp.json()
    


def make_prompt_default(filename, content):
    with open(filename, 'r') as infile:
        prompt = infile.read()
    prompt = prompt.replace('<<TEXT>>', content)
    return prompt