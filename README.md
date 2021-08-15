# NLCA Discord - Barebones

This is an ultra-lightweight barebones version of NLCA (Natural Language Cognitive Architecture) using only CURIE (GPT-3) and SQLITE. Consider this the training-wheels version. Since this will use CURIE the prompts should be portable to other technologies like GPT-J. This version uses SQLITE and CURIE so as to be as light and cheap as possible at the cost of intelligence. This version also lacks a KB (knowledge base) for now. This version of NLCA is very dumb. Please set your expectations accordingly. 

# Architecture

![Discord Architecture](https://github.com/daveshap/RavenDiscord3/blob/main/Discord%20Architecture%203.png)

# Setup

## Discord Bot

You'll need to open a Discord Developer account and create a bot. This process is pretty simple. Check it out here:

1. Setup your bot here: https://discord.com/developers/applications
2. Get your API key and put in into this repo as `discordkey.txt`
3. Don't worry about accidentally sharing this - this file is excluded in `.gitignore`
4. Update the guild and channel information in `discord_svc.py`

## OpenAI Key

For this version you will also need access to OpenAI GPT-3. 

1. Go get an account at https://beta.openai.com/
2. Create your API key and put into this repo as `openaiapikey.txt`
3. Don't worry about accidentally sharing this - this file is excluded in `.gitignore`

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
- https://maragi.io/
- https://github.com/daveshap/CoreObjectiveFunctions
- https://github.com/daveshap/maragi-camera
- https://ravenagi.io/

Therefore any and all technologies, methods, techniques, and inventions herein described are unpatentable under [35 U.S.C. 102](https://www.uspto.gov/web/offices/pac/mpep/mpep-9015-appx-l.html)

And yes, GitHub can serve as prior art!