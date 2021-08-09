import flask
import json
from flask import request
import logging
from functions import *


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = flask.Flask('QA')
max_memory_count = 10


def get_all_keywords(payload):  # payload should contain elements 'question' and 'context'
    # keywords from context
    prompt = make_prompt_default('p_keywords.txt', payload['context'])
    context = transformer_completion({'prompt': prompt, 'prompt_name': 'p_keywords'}).split()
    # keywords from question
    prompt = make_prompt_default('p_keywords.txt', payload['question'])
    question = transformer_completion({'prompt': prompt, 'prompt_name': 'p_keywords'}).split()
    # concatenate and deduplicate
    keywords = context + question
    keywords = list(dict.fromkeys(keywords))
    return keywords


def answer_from_memory(question, records):
    # try to answer question starting with top memory and working way downward
    # TODO test self-explication (maybe specifically need self-explication prompt?)
    records = sorted(records, key = lambda i: i['score'], reverse=True)  # sort records descending by score
    try_count = 0
    for r in records:
        try_count +=1
        if try_count >= max_memory_count:  # limit to max_memory_count retries
            return "I don't know"
        prompt = make_prompt_default('p_answer_memory.txt', r['content'])
        prompt = prompt.replace('<<QUESTION>>', question)
        answer = transformer_completion({'prompt': prompt, 'prompt_name': 'p_answer_memory'}).split()  # TODO figure out best temp and penalties
        if "I don't know" not in answer:
            u = update_db_access(r['uuid'])
            return answer
    return "I don't know"


@app.route('/', methods=['POST'])
def api():
    #try:
        payload = request.json
        print('\n\nPayload received:', payload)
        # try factual answer first (is this just a fact that we can confabulate?)
        prompt = make_prompt_default('p_answer_factual.txt', payload['question'])
        factual_answer = transformer_completion({'prompt': prompt, 'prompt_name': 'p_answer_factual'})  # TODO figure out best temp and penalties
        if "I don't know" not in factual_answer:
            print(factual_answer)
            return factual_answer
        # if factual answer not possible, try querying memory
        keywords = get_all_keywords(payload)
        records = search_db_keywords(keywords)
        records = score_db_results(records, keywords)
        answer = answer_from_memory(payload['question'], records)
        if "I don't know" not in answer:
            print(answer)
            return answer
        print(factual_answer)
        return factual_answer  # if gets this far, factual_answer will say something specific like "I don't know the airspeed velocity of a laden swallow."
    #except Exception as oops:
    #    err_msg = 'ERROR in QA service: ' + str(oops)
    #    print(err_msg)
    #    return err_msg


if __name__ == '__main__':
    print('Starting QA')
    app.run(host='0.0.0.0', port=9998)