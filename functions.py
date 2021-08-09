import requests
from time import sleep

def post_to_outer_loop(payload):
    resp = requests.request(method='POST', url='http://127.0.0.1:9999/', json=payload, timeout=45)
    return resp.json()


def transformer_completion(payload):
    resp = requests.request(method='POST', url='http://127.0.0.1:7777/', json=payload, timeout=15)
    return resp.text


def save_to_shared_db(payload):
    resp = requests.request(method='POST', url='http://127.0.0.1:8888/', json=payload)
    return resp.json()


def search_db_keywords(keywords):
    records = list()
    for i in keywords.split():
        # there will be 2 types in the shared db: corpus and dossier
        resp = requests.request(method='GET', url='http://127.0.0.1:8888/search', json={'query': i}, timeout=45)
        records = resp.json()
    newlist = list()
    for r in records:
        # check if exists in list
        exists = False
        for n in newlist:
            if n['uuid'] == r['uuid']:
                exists = True
        if exists:
            continue
        # score the record based on number of matches
        score = 0
        for i in keywords.split():
            if i in r['content']:
                score += 1
        newlist.append({'type': r['type'], 
                        'time': r['time'], 
                        'content': r['content'], 
                        'last_access': r['last_access'], 
                        'access_count': r['access_count'], 
                        'uuid': r['uuid'], 
                        'parent': r['parent'], 
                        'score': score})
    return newlist


def score_db_results(records, keywords):
    results = list()
    for record in records:
        count = 0
        for i in keywords:
            if i.lower() in record['content'].lower():
                count += 1
        record['score'] = count / len(keywords)
        results.append(record)
    return results


def select_from_db(typefield, orderby, orderdir, limit):
    payload = {'type': typefield, 'orderby': orderby, 'orderdir': orderdir, 'limit': limit}
    resp = requests.request(method='GET', url='http://127.0.0.1:8888/select', json=payload, timeout=45)
    return resp.json()


def update_db_access(uuid):
    resp = requests.request(method='GET', url='http://127.0.0.1:8888/search', json={'uuid': uuid}, timeout=45)
    return resp.json()


def make_prompt_default(filename, content):
    with open(filename, 'r') as infile:
        prompt = infile.read()
    prompt = prompt.replace('<<TEXT>>', content)
    return prompt