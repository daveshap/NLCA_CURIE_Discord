import requests
import discord
from time import time
import emoji
from microservice_functions import *
from prompt_functions import *


messages = list()
cur_guild = 'RavenAGI'
cur_channel = 'general'
with open('discordkey.txt', 'r') as infile:
    discordkey = infile.read()


def time_to_respond(context):
    prompt = make_prompt_default('p0_next.txt', context)
    result = transformer_completion({'prompt':prompt})
    if 'raven' in result.lower():
        return True
    else:
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
        respond = time_to_respond(context)
        if respond:
            response = post_to_corpus({'context':context})
            await message.channel.send(emoji.emojize(response['output']))
            #await message.channel.send('this is only a test')


if __name__ == '__main__':
    print('Starting Discord Receiver')
    client = MyClient()
    client.run(discordkey)