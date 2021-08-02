# Raven Discord - Barebones

This is an ultra-lightweight barebones version of NLCA (Natural Language Cognitive Architecture) using only CURIE (GPT-3) and SQLITE. Consider this the training-wheels version. Since this will use CURIE the prompts should be portable to other technologies like GPT-J. This version uses SQLITE and CURIE so as to be as light and cheap as possible at the cost of intelligence. This version also lacks a KB (knowledge base) for now.

## Architecture

![Discord Architecture](https://github.com/daveshap/RavenDiscord3/blob/main/Discord%20Architecture%203.png)

## Shared DB Service

### Fields (Schema)

- type
- content
- time (created time)
- last_access
- access_count
- uuid
- parent
- vector?
- summary?

# Legal

Raven is based upon Natural Language Cognitive Architecture ("NLCA"). NLCA is based upon MARAGI. All of the above are Open Source Software released under the MIT license starting in 2018. See below for a list of related repositories. These repositories, having been publicly posted in a version controlled platform, serve as "prior art" - a legal term meaning they cannot be patented.

- https://github.com/daveshap/maragi_message_broker
- https://github.com/daveshap/maragi_sensor_audio
- https://github.com/daveshap/maragi_sensor_video
- https://github.com/daveshap/maragi_model_speech_gpu
- https://github.com/daveshap/maragi_exec_wh_question_v1
- https://github.com/daveshap/maragi_action_speech_v1
- https://github.com/daveshap/dialog_act_service
- https://github.com/daveshap/maragi
- https://pypi.org/project/maragi/
- https://github.com/daveshap/CoreObjectiveFunctions

Therefore any and all technologies, methods, techniques, and inventions herein described are unpatentable under [35 U.S.C. 102](https://www.uspto.gov/web/offices/pac/mpep/mpep-9015-appx-l.html)

And yes, GitHub can serve as prior art!