import os
import sys
import json
import logging
from AppSettings import AppSettings
from AppLogger import AppLogger

## Fix for requests
import requests

from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)

# Auth route
@app.route('/auth', methods=['GET'])
def authUser():
    log("Auth page")
    return "Auth page", 200

# Google Callback link
@app.route("/OAuthCallback", methods=['POST'])
def OAuthCallback():
    return "Google Callback", 200

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == AppSettings.get("VERIFY_TOKEN"):
            log("{} != {}".format(request.args.get("hub.verify_token"), AppSettings.get("VERIFY_TOKEN")))
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
                    message_text = messaging_event["message"]["text"]  # the message's text

                    send_login_button(sender_id)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_login_button(recipient_id):
    log("sending login button")
    bot = Bot(AppSettings.get("PAGE_ACCESS_TOKEN"))
    buttons = [{
        "type": "account_link",
        "url": "https://4c8bde1f.ngrok.io/auth"
    }]
    result = bot.send_button_message(recipient_id, "Login", buttons)
    log(result) # For debugging


def send_message(recipient_id, message_text):
    '''
        Send a message to the receipient
    '''
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    bot = Bot(AppSettings.get("PAGE_ACCESS_TOKEN"))
    response = bot.send_text_message(recipient_id, message_text)

def log(message):  # simple wrapper for logging to stdout on heroku
    AppLogger.log(message)
