import discord
from discord.ext import commands
import random
import os
from datetime import datetime, timedelta
from functions import *

from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix="tree ")

# EVENTS
@bot.event
async def on_ready():
    print('The Tree of Eridarra is now live, rejoice!\n')

@bot.event
async def on_message(message):
    # Checking for negative phrases
    if(any(word in message.content.lower() for word in negative_phrases)):
        encouragement = random.choice(list_of_encouragements+get_encouragements())
        await message.channel.send(content=encouragement)

    # # Checking if user in working
    # if(message.author in working_users):
    #     if(check_working(message.author, working_users)):
    #         await message.channel.send(content="{main} {user}".format(main=you_should_be_working_responses[random.randrange(len(you_should_be_working_responses))], user=message.author.mention))
    #         return
    #     else:
    #         del working_users[message.author]
    
    await bot.process_commands(message)

# COMMANDS
@bot.command(
    brief="say hi!"
)
async def hi(ctx):
    greetings= ['hi', 'hello', 'bonjour', 'hola']
    await ctx.send('{greeting} {user}'.format(greeting=random.choice(greetings),user=ctx.author.mention))

@bot.command(
    brief='get an inspiration'
)
async def inspire(ctx):
    await ctx.send(get_quote())

@bot.command(
    brief='bless another user',
    help=
    """
        tree bless @user
    """
)
async def bless(ctx, *args):
    for user in args:
        blessing = 'May the gods shine fortune upon you today, {user}'.format(user=user)
        await ctx.send(blessing)

@bot.command(
    brief="get some advice"
)
async def advice(ctx):
    await ctx.send(get_advice())

@bot.command(
    name='encouragements',
    brief='add, show & delete custom encouragements',
    help=
    """
    add    - tree encouragements add "A" "B"
            adds "A" and "B" to the custom list of encouragements
    show   - tree encouragements show
            shows a list of encouragements with indexes
    delete - tree encouragements delete 1 4 2
            delete encouragements based on index from "show" command
    """
)
async def encouragements(ctx, *args):
    option = args[0]
    if option == "add":
        for index in range(1, len(args)):
            # args=["hi", "hello"]
            phraseToAdd=args[index]
            add_encouragement(phraseToAdd)
            await ctx.send('"{added}"\thas been added to the list of encouragements'.format(added=phraseToAdd))
    elif option == "show":
        # 'show' lists custom encouragements from db in format
        #   1. encouragement1
        #   2. encouragement2
        text = '__**List of encouragements**__'
        index = 1
        for phrase in get_encouragements():
            text = text + '\n{index}. {phrase}'.format(index=index, phrase=phrase)
            index += 1
        await ctx.send(text)
    elif option == "delete":
        # user deletes phrase(s) from db based on index numbers from 'show'
        delete_encouragements(indexesToBeDeleted = args[1:])
        await ctx.send("Deleted {indexes} phrases from DB".format(indexes=len(indexes)))
    

# @bot.command()
# async def work(ctx, *args):
#     if(args[0]=='start'):
#         if(len(args) < 2):
#             await ctx.send("Need more arguements")
#             return
#         time = int(args[1])
#         result = add_working(user=ctx.author, time=time)
#         if(result):
#             await ctx.send("{user} will be working for {time} minutes".format(ctx.author.name, time))
#         return
#     if(args[0]=='stop'):
#         await ctx.send('stop')
#         return
#     if(args[0]=='see'):
#         await ctx.send(show_working())
#         return


TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)

#             if(command == 'startwork'):
#                 if(phrase.split(' ', maxsplit=1)[1].strip().startswith('hardcore')):
#                     try:
#                         user, minutes = add_working_hardcore(message)
#                         await message.channel.send("{user} has started working and will continue to work for another {minutes} minutes".format(user=user.mention, minutes=minutes))
#                         return
#                     except:
#                         await message.channel.send('You can\'t finesse the HARDCORE mode.')
#                 try:
#                     user, minutes = add_working(message)
#                     await message.channel.send("{user} has started working and will continue to work for another {minutes} minutes".format(user=user.mention, minutes=minutes))
#                     return
#                 except:
#                     await message.channel.send('Kindly check if you have used the command properly (refer to "tree help")')
#                 finally:
#                     return
                
                
#             # UNDER CONSTRUCTION
#             if(command == 'seework'):
#                 try:
#                     output = show_working()
#                     await message.channel.send(output)
#                     return
#                 except:
#                     await message.channel.send('This command troubles me at times, I owe it to the incompetence of my creator...')
#                     return 
#             if(command == 'stopwork'):
#                 try:
#                     del working_users[message.author]
#                     await message.channel.send('{user} has finished/stopped working!'.format(user=message.author.mention))
#                 except:
#                     await message.channel.send("You haven't even begun working, lazy one")
#         except:
#             await message.channel.send('Please use "tree help" for more info on commands')

#     elif(message.author in working_users_hardcore):
#         if(check_working(message.author, working_users_hardcore)):
#             await message.delete()
#             return
#         else:
#             del working_users_hardcore[message.author]
    