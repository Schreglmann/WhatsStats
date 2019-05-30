import re

users = []
total=0
emojis = ["😂", "👍", "🙈", "😅"
# , "💪", "🙄", "😬", "😏", "🤔", "😱", "🤨", "😉", "😭", "🤤"
 ]

def addEmojis(user):
    for emoji in emojis:
        user[emoji] = 0 

def getPercent(users, currentuser, key):
    ges = 0
    for user in users:
        ges += user[key]

    if(ges is not 0):
        return str(round(currentuser[key]/ges*100, 2))+"%" 
    else:
        return str(0)+"%"

def createUser(text):
    if(text.find("Nachrichten an diese Gruppe sind jetzt mit Ende-zu-Ende", 0, len(text)) is -1):
        result = (re.search('] (.*): ', text))
        if result:
            user = result.group(1)
            if not any(d['Name'] == user for d in users):
                if user.count(':') is 0:
                    users.append({
                        "Name": user,
                        "Nachrichten": 0,
                        "GIFs": 0,
                        "Bilder": 0,
                    })
                    addEmojis(users[-1])


def getUser(text):
    createUser(text)
    global total
    for user in users:
        if(text.find("[", 0, len(text)) is not -1):
            if(text.find(user["Name"], 0, len(text)) is not -1):
                user["Nachrichten"]+=1
                total+=1
                for emoji in user:
                    if(emoji is not "Name" and emoji is not "GIFs" and emoji is not "Bilder" and emoji is not "Nachrichten"):
                        if(text.find(emoji, 0, len(text)) is not -1):
                            user[emoji]+=text.count(emoji) 

                if(text.find("Bild weggelassen", 0, len(text)) is not -1):
                    user["Bilder"]+=1
                if(text.find("GIF weggelassen", 0, len(text)) is not -1):
                    user["GIFs"]+=1

   

with open('_chat.txt') as text:
    for line in text:          
        getUser(line)
    print("Gesamte Nachrichten: ",total,"\n")

    for user in users:
        for key, value in user.items():
            if(key is "Name"):
                print('{: <15}{: <10}'.format(key, value))
                print()
            else:
                print('{: <15}{: <10}{: <10}'.format(key, value, getPercent(users, user, key)))
        print()
        print()