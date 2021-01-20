import discord, requests, json, random, os

from discord.ext import commands
from datetime import datetime, timedelta
from functions import *

from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix="tree ")

# BOT EVENTS
@bot.event
async def on_ready():
    print('The Tree of Eridarra is now live, rejoice!\n')

@bot.event
async def on_message(message):
    # Checking for negative phrases
    if(any(word in message.content.lower().split() for word in negative_phrases)):
        encouragement = random.choice(list_of_encouragements+get_phrases(db.Encouragement))
        await message.channel.send(content=encouragement)

    # # Checking if user in working
    # if(message.author in working_users):
    #     if(check_working(message.author, working_users)):
    #         await message.channel.send(content="{main} {user}".format(main=you_should_be_working_responses[random.randrange(len(you_should_be_working_responses))], user=message.author.mention))
    #         return
    #     else:
    #         del working_users[message.author]
    
    await bot.process_commands(message)

# BOT COMMANDS
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
    response = requests.get('https://zenquotes.io/api/random')
    jsonData = json.loads(response.text)
    inspiration = jsonData[0]['q']
    await ctx.send(inspiration)

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
    response = requests.get('https://api.adviceslip.com/advice')
    jsonData = json.loads(response.text)
    advice = jsonData['slip']['advice']
    await ctx.send(advice)

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
            add_phrase(db.Encouragement, phraseToAdd)
            await ctx.send('"{added}"\thas been added to the list of encouragements'.format(added=phraseToAdd))
    elif option == "show":
        # 'show' lists custom encouragements from db in format
        #   1. encouragement1
        #   2. encouragement2
        await ctx.send(makeList('List of Encouragements', get_phrases(db.Encouragement)))

    elif option == "delete":
        # user deletes phrase(s) from db based on index numbers from 'show'
        delete_phrases(db.Encouragement, indexesToBeDeleted = args[1:])
        await ctx.send("Deleted {indexes} phrase(s) from DB".format(indexes=len(args[1:])))
    
@bot.command(
    name='suggest',
    brief="Suggest improvements",
    help=
    """
    Add a suggestion:
    tree suggest add "<you suggestion here>"
    
    View all suggestions:
    tree suggest view
    """
)
async def suggest(ctx, *args):
    option = args[0]
    if option=='add':
        # args[1] contains the suggestion
        add_phrase(db.Suggestion, args[1])
        await ctx.send("Thanks for your suggestion {user}!".format(user=ctx.author.mention))
    elif option=='view':
        await ctx.send(makeList('Suggestions:', get_phrases(db.Suggestion)))

# FUNCTIONS
def printit():
    print('hello')
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

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)