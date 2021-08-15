import requests
import discord
from time import time
import emoji
from functions import *


messages = list()
cur_guild = 'RavenAGI'
cur_channel = 'general'
with open('discordkey.txt', 'r') as infile:
    discordkey = infile.read()


def time_to_respond_gpt(context):
    prompt = make_prompt_default('p_next_speaker.txt', context)  # CURIE is not intelligent enough for this
    result = transformer_completion({'prompt':prompt, 'prompt_name': 'p_next_speaker'})
    print('Next:', result)
    if 'raven' in result.lower():
        return True
    else:
        return False


def time_to_respond(context):
    try:
        lines = context.lower().splitlines()
        if 'raven:' in lines[-1]:  # Raven just spoke
            return False
        if 'raven' in lines[-1] and '?' in lines[-1]:  # someone asked raven a question or a question about raven
            return True
        if 'raven' not in lines[-1] and 'raven' not in lines[-2]:  # Raven hasn't said anything in a minute
            return True
        if 'raven:' in lines[-2] and '?' in lines[-1]:  # someone just asked a follow-up question
            return True
        return False
    except:
        return False


def build_context(messages):
    recent = messages[-10:]  # TODO make this a bit smarter?
    result = ''
    for i in recent:
        result += '%s: %s\n' % (i['author'], i['content'])
    return result.strip().replace('RavenAGI', 'Raven')


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        global messages
        content = emoji.demojize(message.content)
        msg = {'author': message.author.name, 'channel': message.channel.name, 'guild': message.guild.name, 'content': content, 'time': time()}  # message.author.discriminator
        if msg['channel'] != cur_channel or msg['guild'] != cur_guild:
            return
        messages.append(msg)
        print('\n\nMESSAGE:', msg)
        context = build_context(messages)
        respond = time_to_respond(context)  # only DAVINCI is smart enough for this
        print('RESPOND:', respond)
        if respond:
            response = post_to_outer_loop({'context':context})
            print('OUTPUT:', response)
            await message.channel.send(emoji.emojize(response['output']))
            #await message.channel.send('this is only a test')


if __name__ == '__main__':
    print('Starting Discord Receiver')
    client = MyClient()
    client.run(discordkey)