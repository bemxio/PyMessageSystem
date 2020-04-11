import json
from ftplib import FTP
from base64 import b64encode, b64decode
from os import system as call
from platform import system

username = None
password = None
id = None
logstatus = False
database = None
cexit = False

class InternetError(Exception):
    pass
 
def admincheck():
    global logstatus
    global database
    global id
    if not logstatus:
        print('You\'re not logged in!')
        return 1
    if not database[id]['admin'] == 1:
        print('You don\'t have administator rights!')
        return 2
    else:
        return 3
    
def idsearch(n):
    global database
    for i in range(len(database)):
        try:
            if not n == database[str(i)]['username']:
                continue
            else:
                return str(i)
                break
        except:
            return 'err'
        
def command():
    global username
    global password
    global id
    global logstatus
    global database
    global cexit
    global ftp
    syntax = input('> ').split()
    if syntax[0] == 'help':
        print('help - shows this')
        print('register - make your profile')
        print('login - login to your profile')
        print('logoff - logoff from the profile')
        print('friend view|add|remove <name> - view, add or remove someone from your list')
        print('clean - clears the screen')
        print('exit - save the database and exit\n(TYPE IT BEFORE EXITING SHELL ELSE DATABASE WILL NOT BE SAVED!)')
        print('messages read|send|clear - clear, read or send messages')
        command()
    elif syntax[0] == 'register':
        if logstatus:
            print('You can\'t register while you\'re logged in')
            command()
        else:
            b = str(len(database))
            database[b] = {}
            database[b]['username'] = syntax[1]
            passa = b64encode(syntax[2].encode('ascii'))
            database[b]['password'] = passa.decode('ascii')
            database[b]['admin'] = 0
            database[b]['friends'] = []
            database[b]['messages'] = []
            print('Successfully registered! Now you can log in')
            command()
    elif syntax[0] == 'login':
        if logstatus:
            print('You\'re already logged in')
            command()
        else:
            for i in range(len(database)):
                if not syntax[1] == database[str(i)]['username']:
                    continue
                else:
                    username = syntax[1]
                    break
            for i in range(len(database)):
                bass64 = b64decode(database[str(i)]['password'].encode('ascii'))
                bass64 = bass64.decode('ascii')
                if not syntax[2] == bass64 and syntax[1] == username:
                    continue
                else:
                    id = str(i)
                    logstatus = True
                    break
            if logstatus:
                print('Login successful')
                command()
            else:
                print('Login failed, please try again')
                command()
    elif syntax[0] == 'logoff':
        if not logstatus:
            print('You\'re not logged in')
            command()
        else:
            username = None
            password = None
            id = None
            logstatus = False
            print('Successfully logged off')
            command()
    elif syntax[0] == 'friends':
        if syntax[1] == 'add':
            if not logstatus:
                print('You\'re not logged in')
                command()
            aydee = idsearch(syntax[2])
            if aydee == None:
                print('Error: this user doesn\'t exist')
                command()
            else:
                database[id]['friends'].append(database[aydee]['username'])
                lenfriend = len(database[id]['friends']) - 1
                print(database[id]['friends'])
                print('Successfully added ' + syntax[2] + ' to your friend\'s list')
                command()
        elif syntax[1] == 'remove':
            if not logstatus:
                print('You\'re not logged in')
                command()
            else:
                database[id]['friends'].remove(syntax[2])
                print('Successfully removed ' + syntax[2] + ' from your friend\'s list')
                command()
        elif syntax[1] == 'view':
            if not logstatus:
                print('You\'re not logged in')
                command()
            else:
                print(username + '\'s friend list: ')
                for i in database[id]['friends']:
                    print(i)
                command()
    elif syntax[0] == 'clean':
        if system() == 'Windows':
            call('cls')
            command()
        else:
            call('clear')
            command()
    elif syntax[0] == 'debug':
        if syntax[1] == 'database':
            if admincheck() < 3:
                command()
            else:
                print(database)
                command()
        elif syntax[1] == 'user':
            if admincheck() < 3:
                command()
            else:
                print(database[syntax[2]])
                command()
        elif syntax[1] == 'delete':
            if admincheck() < 3:
                command()
            if syntax[2] == 'database':
                if syntax[3] == 'l':
                    dbfile = open('database.json', 'w')
                    dbfile.write('{}')
                    dbfile.close()
                    print('Successfully resetted local database')
                    command()
                elif syntax[3] == 'all':
                    dbfile = open('database.json', 'w')
                    dbfile.write('{}')
                    dbfile.close()
                    ftp.delete('database.json')
                    with open('database.json', 'rb') as storew:
                        ftp.storbinary('STOR database.json', storew)
                    print('Successfully resetted local & online database')
                    exit()
            else:
                if admincheck() < 3:
                    command()
                del database[syntax[2]]
                print('Successfully deleted user ' + syntax[2] + ' from database')
                command()
    elif syntax[0] == 'exit':
        dbfile = open('database.json', 'wb+')
        temp = json.dumps(database).encode('utf-8')
        dbfile.write(b64encode(temp))
        print('Saving database...')
        dbfile.close() 
        ftp.delete('database.json')
        with open('database.json', 'rb') as storew:
            ftp.storbinary('STOR database.json', storew)
        print('Saved!')
        if system() == 'Windows':
            call('del database.json')
        else:
            call('rm database.json')
        print('Exiting...')
        cexit = True
        exit()
    elif syntax[0] == 'messages':
        if syntax[1] == 'read':
            if not logstatus:
                print('You\'re not logged in')
                command()
            if len(database[id]['messages']) == 0:
                print('No messages found')
                command()
            for i in range(len(database[id]['messages'])):
                print('From: ' + database[id]['messages'][i]['from'] + '\n')
                print(str(database[id]['messages'][i]['message']))
                print('-' * 15)
            command()
        elif syntax[1] == 'send':
            if not logstatus:
                print('You\'re not logged in')
                command()
            message = {}
            message['from'] = username
            message['message'] = str(input('Please type the message below:\n'))
            aydee = idsearch(syntax[2])
            if not aydee or aydee == 'err':
                print('Error: this user doesn\'t exist')
                command()
            database[aydee]['messages'].append(message)
            print('Successfully sended message')
            command()
        elif syntax[1] == 'clear':
            if not logstatus:
                print('You\'re not logged in')
                command()
            database[id]['messages'] = []
            print('Successfully cleared all messages')
            command()
    else:
        print('Error: wrong syntax')
        command()

if cexit:
    exit()

print('Loading...')
try:
    ftp = FTP('YOUR_FTP_ADDRESS')
    ftp.login('YOUR_FTP_USERNAME', 'YOUR_FTP_PASSWORD')
except socket.gaierror:
    raise NetworkError('Make sure you\'re connected to the internet')
with open('database.json', 'wb+') as temp:
    ftp.retrbinary('RETR database.json', temp.write)

dbfile = open('database.json', 'rb')
database = b64decode(dbfile.read())
database = json.loads(database.decode('utf-8'))
dbfile.close()
if system() == 'Windows':
    call('del database.json')
else:
    call('rm database.json')
print('Message System by bemxio, ver. online stable 1')
command()