from uuid import uuid4
from datetime import datetime
from time import time, sleep
import json
import logging
from functions import *

'''
chronology example:
Theme: Where is the coffee pot?
[datetime]: Dave says he lost the coffee pot and is looking for it
[datetime]: Dave found the coffee pot and said he's making coffee
[datetime]: Dave brewed coffee and seems happy

Default questions:
What's next if anything, or is this sequence complete?
What lessons can be learned from this sequence?
What inferences can we make from this sequence of events?
COF questions
'''


default_sleep = 20  # time between inner loop cycles


def get_score(uuid, searchlist):
    for i in searchlist:
        if i['uuid'] == uuid:
            return i['score']
    return 0.0


def calculate_scores(sourcelist):
    result = list()
    score = 1.0
    for i in sourcelist:
        i['score'] = score
        score = score - 0.01
        result.append(i)
    return result


def get_uuids(sourcelist):
    result = list()
    for i in sourcelist:
        result.append(i['uuid'])
    return result


def find_uuid_from_lists(uuid, list1, list2, list3):
    for i in list1:
        if i['uuid'] == uuid:
            return i
    for i in list2:
        if i['uuid'] == uuid:
            return i
    for i in list3:
        if i['uuid'] == uuid:
            return i
    return None


def kernel_search():
    # fetch top memories from database
    time_signal = select_from_db('corpus', 'time', 'DESC', 100)
    count_signal = select_from_db('corpus', 'access_count', 'ASC', 100)
    access_signal = select_from_db('corpus', 'last_access', 'ASC', 100)
    # calculate signal score for each memory
    time_scores = calculate_scores(time_signal)
    count_scores = calculate_scores(count_signal)
    access_scores = calculate_scores(access_signal)
    # enumerate all UUIDs in all 3 lists
    all_uuids = get_uuids(time_scores)
    all_uuids += get_uuids(count_scores)
    all_uuids += get_uuids(access_scores)
    all_uuids = list(set(all_uuids))
    # accumulate score for all UUIDs
    aggregate_scores = list()
    for i in all_uuids:
        score = 0.0
        score += get_score(i, time_scores)
        score += get_score(i, count_scores)
        score += get_score(i, access_scores)
        aggregate_scores.append({'uuid': i, 'score': score})
    aggregate_scores = sorted(aggregate_scores, key=lambda i: i['score'], reverse=True)
    top_uuid = aggregate_scores[0]['uuid']    # warning: if Raven has no memories, this will break (but that should pretty much never happen)
    selected_memory = find_uuid_from_lists(top_uuid, time_signal, count_signal, access_signal)
    print('KERNEL SEARCH:', selected_memory)
    return selected_memory


def extract_themes(corpus):
    prompt = make_prompt_default('p_extract_themes.txt', corpus['content'])
    themes = transformer_completion({'prompt': prompt, 'prompt_name': 'p_extract_themes'}).splitlines()
    print('THEMES:', themes)
    return themes


def build_chronology(theme, corpuses):
    # see chronology example at the top
    corpuses = sorted(corpuses, key=lambda i: i['time'])
    chronology = 'Theme: %s\n' % theme
    for corpus in corpuses:
        prompt = make_prompt_default('p_summarize_theme.txt', corpus['content'])
        prompt = prompt.replace('<<THEME>>', theme)
        summary = transformer_completion({'prompt': prompt, 'prompt_name': 'p_summarize_theme'})
        date = datetime.utcfromtimestamp(corpus['time']).strftime('%Y-%m-%d %H:%M:%S')
        chronology += '%s: %s\n' % (date, summary)
    return chronology.strip()


def ask_default_questions(chronology):
    prompts = ['p_inner_next.txt', 'p_inner_lessons.txt', 'p_inner_inferences.txt', 'p_inner_cof1.txt', 'p_inner_cof2.txt', 'p_inner_cof3.txt']
    # TODO add constitution
    # TODO add self/project/task e.g. "What was I doing? Why was I doing it?"
    answers = list()
    for i in prompts:
        prompt = make_prompt_default(i, chronology)
        answer = transformer_completion({'prompt': prompt, 'prompt_name': i.replace('.txt', '')})
        answers.append(answer)
    return answers


def compose_dossier(corpus, chronology, answers):
    chronology += '\n\nThoughts: '
    for answer in answers:
        chronology += answer + ' '
    chronology = chronology.strip()
    result = dict()
    # type,time,content,last_access,access_count,uuid,parent
    result['content'] = chronology
    result['type'] = 'dossier'
    result['time'] = time()
    result['last_access'] = 0.0
    result['access_count'] = 0
    result['uuid'] = str(uuid4())
    result['parent'] = corpus['uuid']
    return result


if __name__ == '__main__':
    while True:
        top_corpus = kernel_search()                                   # select corpuses 3 times (by time descending, access count ascending, last access ascending) (select corpus that is highest in all 3 stacks)
        themes = extract_themes(top_corpus)                            # theme could be something like "where is the coffee pot" or "fire alarm on Wednesday, June 28, 2092"
        for theme in themes:                                           # there might be only 1 theme and that's okay (probably limit to 3 themes per corpus)
            corpuses = search_db_keywords(theme.split())               # get all other memories related to top corpus
            corpuses = [i for i in corpuses if i['type'] == 'corpus']  # filter only corpuses from memories
            #corpuses = [i for i in corpuses if i['score'] > 1]         # filter out low score corpuses (nullified by removing stopwords)
            chronology = build_chronology(theme, corpuses)             # summarize all documents as they relate to the theme in chronological order (deduplicate as well)
            answers = ask_default_questions(chronology)                # ask boilerplate questions
            dossier = compose_dossier(top_corpus, chronology, answers) # 'Theme: %s\nChronology:\n%s\n\nEvaluations:\n%s' % (theme, chronology, answers) etc
            print('DOSSIER:', dossier)
            save_to_shared_db(dossier)                                 # exactly what it says on the tin
        sleep(default_sleep)