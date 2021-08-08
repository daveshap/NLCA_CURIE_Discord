from datetime import datetime
import concurrent.futures
from time import time
import flask
import json
from flask import request
import logging
from functions import *


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = flask.Flask('outer loop')


def generate_corpus(payload):
    # define all parallel thought patterns
    parallel = [('p_summary.txt', 'summary'), ('p_sentiment.txt', 'sentiment'), ('p_intent.txt', 'intent'), ('p_questions.txt', 'questions')]
    # NOTE: Max temp and max penalty seems to be great for some of these...
    async_executors = list()
    # run concurrent executor pool
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # spool up parallel thought patterns and execute
        for i in parallel:
            prompt = make_prompt_default(i[0], payload['context'])
            f = executor.submit(transformer_completion, {'prompt': prompt, 'prompt_name': i[1]})
            async_executors.append((f, i[1]))
        # fetch results from executors
        results = dict()
        for i in async_executors:
            results[i[1]] = i[0].result()
        # answer questions
        # NOTE: medium penalties with high temp seem to work better for generating questions
        questions = results['questions'].splitlines()
        answers_executors = list()
        for q in questions:
            f = executor.submit(qa_answer, {'question': q, 'context': payload['context']})
            answers_executors.append((q, f))
        # fetch answers to questions
        answers = ''
        for a in answers_executors:
            answers += '% %\n' % (q, f.result())
    # compile corpus
    with open('corpus_template.txt', 'r', encoding='utf-8') as infile:
        corpus = infile.read()
    corpus = corpus.replace('<<TIME>>', str(datetime.now()))
    corpus = corpus.replace('<<SUMMARY>>', results['summary'])
    corpus = corpus.replace('<<SENTIMENT>>', results['sentiment'])
    corpus = corpus.replace('<<INTENT>>', results['intent'])
    corpus = corpus.replace('<<QUESTIONS>>', answers.strip())    
    # constitution (and censorship?)
    prompt = make_prompt_default('p_constitution.txt', corpus)
    constitution = transformer_completion(prompt, 'constitution')
    corpus += '\n\nConstitution: %s' % constitution
    return corpus


def generate_output(corpus):
    prompt = make_prompt_default('p_output.txt', corpus)  # TODO work on output
    output = transformer_completion(prompt, 'output')
    return output


@app.route('/', methods=['POST'])
def api():
    try:
        payload = request.json
        print('\n\nPayload received:', payload)
        corpus = generate_corpus(payload)
        output = generate_output(corpus)
        result = {'output': output}  # TODO flesh this out (time, type, uuid, etc)
        return flask.Response(json.dumps(result), mimetype='application/json')
    except Exception as oops:
        err_msg = 'ERROR in svc_corpus/api: ' + str(oops)
        print(err_msg)
        result = {'output': err_msg}
        return flask.Response(json.dumps(result), mimetype='application/json')


if __name__ == '__main__':
    print('Starting Outer Loop')
    app.run(host='0.0.0.0', port=9999)