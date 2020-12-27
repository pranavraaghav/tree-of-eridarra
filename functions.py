import requests
import json
from replit import db

# Word lists
negative_phrases = [
    'sad',
    'upset',
    'depressed',
    'depression'
]

encouragements = [
    'Hang in there, champ!',
    'Things will get better soon',
    'Our lives are a wise balance of good and bad, such is the way of life.',
    'Don\'t you worry child, this too shall pass',
    'This too shall pass'
]

def init():
    # Initializing encouragments dataset
    global encouragements
    if ('encouragements' in db.keys()):
        encouragements = db['encouragements']
    else:
        db['encouragements'] = encouragements

def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    jsonData = json.loads(response.text)
    quote = jsonData[0]['q']
    return quote

def get_help(phrase):
    try:
        if(phrase.split(' ', maxsplit=1)[1] == 'pro'):
            details = '''__***Pro commands:***__\n```\nshow-en\nadd-en <Phrase>\ndel-en <Index>```'''
            return details
    except:
        details = '''__***Here is what I can do for you, child:***__\n```\ninspire\nbless\nadvice```'''
        return details

def get_blessing(message):
    if(message.mentions):
        mentions = message.mentions
        blessing = 'May the gods shine fortune upon you today, {user}'.format(user=mentions[0].mention)
        return blessing

    blessing = 'May the gods shine fortune upon you today, {user}'.format(user=message.author.mention)
    return blessing
 
def get_advice():
    response = requests.get('https://api.adviceslip.com/advice')
    jsonData = json.loads(response.text)
    return jsonData['slip']['advice']

# Fetches a list of encouragements from the database
def get_encouragements():
    text = '__**List of encouragements**__'
    index = 0
    for phrase in encouragements:
        text = text + '\n{index}. {phrase}'.format(index=index, phrase=phrase)
        index+=1
    return text

# Deletes an entry from the database and updates the database
def del_encouragements(index):
    encouragements = db['encouragements']
    if( len(encouragements) > index):
        del encouragements[index]
    db['encouragements'] = encouragements

# Adding an encouragement
def add_encouragements(phrase):
    encouragements.append(phrase)
    db['encouragements'] = encouragements