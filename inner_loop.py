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
Is this line of thinking, project, or task complete?
What's next if anything?
What lessons can be learned?
What inferences can we make from this sequence of events?
'''


default_sleep = 10  # time between inner loop cycles


def kernel_search()
    time_signal = select_from_db('corpus', 'time', 'DESC', 100)
    count_signal = select_from_db('corpus', 'access_count', 'ASC', 100)
    access_signal = select_from_db('corpus', 'last_access', 'ASC', 100)
    all_uuids = list()
    for i in time_signal:
        if i['uuid'] not in all_uuids:
            all_uuids.append(i['uuid'])
    for i in count_signal:
        if i['uuid'] not in all_uuids:
            all_uuids.append(i['uuid'])
    for i in access_signal:
        if i['uuid'] not in all_uuids:
            all_uuids.append(i['uuid'])
    scores = list()
    for u in all_uuids:
        # TODO
    


if __name__ == '__main__':
    while True:
        top_corpus = kernel_search()                                   # select corpuses 3 times (by time descending, access count ascending, last access ascending) (select corpus that is highest in all 3 stacks)
        themes = extract_themes(top_corpus)                            # theme could be something like "where is the coffee pot" or "fire alarm on Wednesday, June 28, 2092"
        for theme in themes:                                           # there might be only 1 theme and that's okay (probably limit to 3 themes per corpus)
            dossiers = fetch_db_children(top_corpus['uuid'])           # get all documents that show this memory as parent (maybe exclude dossiers?)
            corpuses = search_db_keywords(theme)                       # get all other memories related to top corpus
            corpuses = [i for i in corpuses if i['type']='corpus']     # filter only corpuses from memories
            # TODO include only n number of related corpuses
            chronology = build_chronology(theme, dossiers + corpuses)  # summarize all documents as they relate to the theme in chronological order (deduplicate as well)
            answers = ask_default_questions(chronology)                # ask boilerplate questions
            dossier = compose_dossier(theme, chronology, answers)      # 'Theme: %s\nChronology:\n%s\n\nEvaluations:\n%s' % (theme, chronology, answers) etc
            save_to_shared_db(dossier)                                 # exactly what it says on the tin
        sleep(default_sleep)