import os
import sys
import json
import logging
from Settings import Settings

## Fix for requests
import requests

from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)

# Auth route
@app.route('/auth', methods=['GET'])
def authUser():
    return "Auth page", 200

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == Settings.get("VERIFY_TOKEN"):
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    #message_text = messaging_event["message"]["text"]  # the message's text

                    send_message(sender_id, "Received")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_login_button(recipient_id):
    log("sending login button")
    params = {
        "access_token": Settings.get("PAGE_ACCESS_TOKEN")
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "buttons": {
            "type": "account_link",
            "url": "https://work-record-fb-bot.appspot.com/auth"
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    bot = Bot(Settings.get("PAGE_ACCESS_TOKEN"))
    bot.send_message(recipient_id, message_text)
    log("Message sent")


def log(message):  # simple wrapper for logging to stdout on heroku
    logging.getLogger().setLevel(logging.DEBUG)
    logging.info(message)
