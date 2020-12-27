import discord
import random
import os

from replit import db
from functions import *
from keep_alive import keep_alive


client = discord.Client()
init()


@client.event
async def on_ready():
    print('The Tree of Eridarra is now alive, rejoice! ')
    print('Welcome,', client.user)


@client.event
async def on_message(message):
    if(message.author == client.user):
        return

    if(message.content.startswith('tree')):
        try:
            phrase = message.content.split('tree ')[1]
            command = phrase.split(' ', maxsplit=1)[0]

            # For contributors,
            # Add more commands here
            # Then redirect to a function at functions.py
            if(command == 'help'):
                await message.channel.send(get_help(phrase))
            if(command == 'inspire'):
                await message.channel.send(get_quote())
            if(command == 'bless'):
                await message.channel.send(get_blessing(message))
            if(command == 'advice'):
                await message.channel.send(get_advice())
            if(command == 'show-en'):
                await message.channel.send(get_encouragements())
            if(command == 'del-en'):
                try:
                    index = int(phrase.split(' ', maxsplit=1)[1].strip())
                    del_encouragements(index)
                    await message.channel.send('Phrase has been removed from the list of encouragements')
                except:
                    await message.channel.send('I am facing trouble adjusting my memory, sorry')
            if(command == 'add-en'):
                try:
                    phraseToAdd = phrase.split(' ', maxsplit=1)[1]
                    add_encouragements(phraseToAdd)
                    await message.channel.send('"{added}"\thas been added to the list of encouragements'.format(added=phraseToAdd))
                except:
                    await message.channel.send('I am facing trouble adjusting my memory, sorry')
        except:
            await message.channel.send('Please use "tree help" for more info on commands')

    if(any(word in message.content.lower() for word in negative_phrases)):
        await message.channel.send(content=encouragements[random.randrange(len(encouragements))])
        return

keep_alive()
client.run(os.getenv('TOKEN'))