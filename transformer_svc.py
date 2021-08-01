import flask
from flask import request
import logging
import json
import openai
import emoji
from time import time


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = flask.Flask('gpt3')
with open('openaiapikey.txt', 'r') as infile:
    open_ai_api_key = infile.read()
openai.api_key = open_ai_api_key


def gpt3_completion(prompt, prompt_name, engine='curie', temp=0.5, top_p=0.5, tokens=100, freq_pen=0.5, pres_pen=0.5, stop=['<<END>>', '\n\n']):
    response = openai.Completion.create(
        engine=engine,
        prompt=emoji.demojize(prompt),
        temperature=temp,
        max_tokens=tokens,
        top_p=top_p,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop)
    text = emoji.demojize(response['choices'][0]['text'].strip())
    filename = '%s_%s.txt' % (time(), prompt_name)
    with open('gpt3_logs/%s' % filename, 'w') as outfile:
        outfile.write('Prompt: ' + prompt + '\n\nResult: ' + text)
    return text


def gpt3_answer(question, docs, model='curie', search='ada', tokens=60, temp=0.3, max_rerank=10, top_p=0.9, stop=['<<END>>', '\n\n']):
    #api = 'https://api.openai.com/v1/answers'
    #headers = {'Content-Type':'application/json', 'Authorization': 'Bearer %s' % open_ai_api_key}
    examples = [['What are the symptoms of malaria?', 'The symtpoms of malaria are fever, tiredness, vomiting, and headaches. It can cause yellow skin, seizures, coma, and death in severe cases.<<END>>'],['What is the Tigris River?', 'I do not know what the Tigris River is.<<END>>'],['How long does malaria resistance last?', 'Malaria can recur after months if not treated properly. Partial resistance lasts only a few months without ongoing exposure.<<END>>']]
    ex_context = 'Malaria is a mosquito-borne infectious disease that affects humans and other animals. Malaria causes symptoms that typically include fever, tiredness, vomiting, and headaches. In severe cases, it can cause yellow skin, seizures, coma, or death. Symptoms usually begin ten to fifteen days after being bitten by an infected mosquito. If not properly treated, people may have recurrences of the disease months later. In those who have recently survived an infection, reinfection usually causes milder symptoms. This partial resistance disappears over months to years if the person has no continuing exposure to malaria.'
    response = openai.Answer.create(
        search_model=search,
        model=model,
        question=question,
        documents=docs,
        examples_context=ex_context,
        examples=examples,
        max_rerank=max_rerank,
        max_tokens=tokens,
        temperature=temp,
        top_p=top_p,
        stop=stop)
    return response['answers'][0]


@app.route('/completion', methods=['POST'])
def completion():
    try:
        payload = request.json
        print('\n\nPayload:', payload)
        text = gpt3_completion(payload)
        print('\n\nResponse:', text)
        return text
    except Exception as oops:
        print('ERROR in RECALL/completion:', oops)
        return json.dumps({'success':False, 'error':oops}), 500, {'ContentType':'application/json'}


if __name__ == '__main__':
    print('Starting Transformer Svc')
    app.run(host='0.0.0.0', port=7777)