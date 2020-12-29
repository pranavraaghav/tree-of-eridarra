import discord
import random
import os
from datetime import datetime, timedelta

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

    # Avoiding other bot commands (saving computational resources)
    if(message.content.startswith(whitelisted) for whitelisted in work_phrases_whitelist):
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
                return
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
            if(command == 'startwork'):
                try:
                    user, minutes = add_working(message)
                    await message.channel.send("{user} has started working and will continue to work for another {minutes} minutes".format(user=user.mention, minutes=minutes))
                    return
                except:
                    await message.channel.send('Kindly check if you have used the command properly (refer to "tree help")')
            # UNDER CONSTRUCTION
            if(command == 'seework'):
                try:
                    output = show_working()
                    await message.channel.send(output)
                    return
                except:
                    await message.channel.send('This command troubles me at times, I owe it to the incompetence of my creator...')
                    return 
            if(command == 'stopwork'):
                try:
                    del working_users[message.author]
                    await message.channel.send('{user} has finished/stopped working!'.format(user=message.author.mention))
                except:
                    await message.channel.send("You haven't even begun working, lazy one")
        except:
            await message.channel.send('Please use "tree help" for more info on commands')

    if(message.author in working_users):
        if(check_working(message.author)):
            await message.channel.send(content="{main} {user}".format(main=you_should_be_working_responses[random.randrange(len(you_should_be_working_responses))], user=message.author.mention))
        else:
            del working_users[message.author]

    if(any(word in message.content.lower() for word in negative_phrases)):
        encouragement = get_encouragement()
        await message.channel.send(content=encouragement)
        return

keep_alive()
client.run(os.getenv('TOKEN'))