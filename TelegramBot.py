import requests
import json
from flask import Flask
from flask import request
from flask import Response
import os


url = "https://api.telegram.org/bot1828699599:AAGvJPcMK8rJKc3lDgk1Fd1lWt7p6dNau-E"

app = Flask(__name__)

def get_all_updates():
    # response = requests.get(url + '/getUpdates')
    try:
        response = requests.get(url + '/getUpdates')
        return response.json()
    except requests.exceptions.ConnectionError:
        requests.status_code = "Connection refused"

def get_last_update(allUpdate):
    return allUpdate['result'][-1]

def get_chat_id(Update):
    if 'edited_message' in Update:
        return Update['edited_message']['chat']['id']
    else:
        return Update['message']['chat']['id']

def send_message(chat_id, text, notif = False):
    sendData = {
        'chat_id' : chat_id,
        'text' : text,
        'disable_notification' : notif
    }
    response = requests.post(url + '/sendMessage', sendData)
    return response

@app.route('/', methods = ['POST', 'GET'])
def index():
    print("hi")
    if request.method == 'POST':
        msg = request.get_json()
        print(msg)
        chat_id = get_chat_id(msg)
        if 'edited_message' in msg:
            text = msg['edited_message'].get('text', '')

        elif 'message' in msg:
            text = msg['message'].get('text', '')
        if text == '/start':
            send_message(chat_id, 'Welcome!')
        elif 'new' in text:    #new sarina 046362
            contacts = read_json()
            username = msg['message']['from']['username']
            print(username)
            if username not in contacts.keys():
                contacts[username] = []
            mokhatab = text.split(maxsplit=1)[1]
            contacts[username].append(mokhatab)
            write_json(contacts)
        elif text == 'list':
            contacts = read_json()
            username = msg['message']['from']['username']
            if username not in contacts.keys():
                send_message(chat_id, "shoma mokhatabi nadarid")
            else:
                for mokhatab in contacts[username]:
                    send_message(chat_id, mokhatab)

        return Response('ok', status=200)

    else:
        return "<h1>salam</h1>"
def write_json(data, filename = "contactlist.json"):
    with open(filename, 'w') as target:
        json.dump(data, target, indent=4, ensure_ascii=False)

def read_json(filename = "contactlist.json"):
    with open(filename, 'r') as target:
        data = json.load(target)
    return data


write_json({})
# app.run(debug=True)
app.run(host='0.0.0.0', port=int(os.environ('PORT', 5000)))
# data = get_all_updates()
# lastUpdate = get_last_update(data)
# sendMessage = send_messae(get_chat_id(lastUpdate), "khoobam!", True)
print()





