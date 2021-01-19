import requests
import json
import random
import db
from datetime import datetime, timedelta

# Word lists
negative_phrases = ['sad', 'upset', 'depressed', 'depression']

list_of_encouragements = [
    'Hang in there, champ!', 
    'Things will get better soon',
    'Our lives are a wise balance of good and bad, such is the way of life.',
    'Don\'t you worry child, this too shall pass', 
    'This too shall pass'
]

you_should_be_working_responses = [
    'Kindly get back to work', 'Sweat now, enjoy later',
    'I believe you should be working right now? ',
    'The only place success comes before work is in the dictionary ',
    'You ought to working on something, younge one ',
    'No, not under my watch. Get back to work, child',
    'Stay on the task at hand young one, you must be better.',
    'The texts can wait, your future can\'t, back on track - now!'
]

work_phrases_whitelist = [
    '-p',
    '!p',
    '-r',
    '!r',
    '-dc',
    '-stop',
    '-loop'
]
working_users = {}
working_users_hardcore = {}



# Input should be of type - timdelta
def formatTimeDelta(delta):
    times = {}
    delta = str(delta)
    if('day' in delta):
        deltaSplit = delta.split(' ')
        times['days'] = int(deltaSplit[0])
        delta = deltaSplit[2]
    times['hours'] = int(delta.split(':')[0])
    times['minutes'] = int(delta.split(':')[1])
    try:
        times['seconds'] = int(delta.split(':')[2])
    except:
        pass
        # Seconds tends to break at times, I do not understand why
    return times

def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    jsonData = json.loads(response.text)
    quote = jsonData[0]['q']
    return quote

def get_blessing(message):
    if (message.mentions):
        mentions = message.mentions
        return blessing

    blessing = 'May the gods shine fortune upon you today, {user}'.format(
        user=message.author.mention)
    return blessing


def get_advice():
    response = requests.get('https://api.adviceslip.com/advice')
    jsonData = json.loads(response.text)
    return jsonData['slip']['advice']

# Adding an encouragement
def add_encouragement(phrase):
    item = db.Encouragement(phrase=phrase)
    db.add(item)

def delete_encouragement(phrases):
    for phrase in phrases:
        statement = db.Encouragement.__table__.delete().where(db.Encouragement.phrase == phrase)
        db.engine.execute(statement)
        # item = db.session.query(db.Encouragement).filter(db.Encouragement.phrase==phrase).first()

def get_encouragements():
    encouragements = db.get_all(db.Encouragement)
    returnList = []
    for encourage in encouragements:
        returnList.append(encourage.phrase)
    return returnList
    
# Adding user to working list
def add_working(user, time):
    currentTime = datetime.now()
    endTime = currentTime + timedelta(minutes=time)
    working_users[user] = endTime
    return True

def add_working_hardcore(message):
    
    if(message.author in working_users_hardcore):
        return
    user = message.author
    minutes = float(message.content.split(' ')[3])
    currentTime = datetime.now()
    endTime = currentTime + timedelta(minutes=minutes)
    working_users_hardcore[user] = endTime
    return user, minutes

# Checking if user should still be working
def check_working(user, bracket):
    endTime = bracket[user]
    if (datetime.now() < endTime):
        return True
    return False


def update_working_users():
    if (working_users):
        for user in working_users:
            if not (check_working(user)):
                del working_users[user]


# Shows all currently working users
# UNDER CONSTRUCTION
def show_working():
    update_working_users()
    if bool(working_users):
        text = "Work status:"
        for user, endTime in working_users.items():
            try:
                timeRemaining = formatTimeDelta(endTime - datetime.now())
            except:
                return 'Facing trouble getting timeRemaining'
            timeString = ''
            if('days' in timeRemaining.keys()):
                days = timeRemaining['days']
                timeString = timeString + f'{days} days, '
            if(timeRemaining['hours'] > 0):
                hours = timeRemaining['hours']
                timeString = timeString + f'{hours} hrs '
            if(timeRemaining['minutes'] > 0):
                minutes = timeRemaining['minutes']
                timeString = timeString + f'{minutes} mins '
            elif(timeRemaining['seconds'] > 0):
                seconds = timeRemaining['seconds']
                timeString = timeString + f'{seconds} secs '
            if(user.nick == None):
                text = text + "\n{user} will be working for another {time}".format(user=user.name, time=timeString)
            else:
                text = text + "\n{user} will be working for another {time}".format(user=user.nick, time=timeString)
        return text
    return "No one is currently working"
