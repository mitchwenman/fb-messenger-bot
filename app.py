import os
import sys
import json
import urllib
import logging
from AppSettings import AppSettings
from AppLogger import AppLogger
import AppGoogleAuth
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
## Fix for requests
import requests

from flask import Flask, request, redirect, session, url_for
from pymessenger.bot import Bot

app = Flask(__name__)
app.secret_key = AppSettings.get("APP_SECRET_KEY") #secure storage across requests

# Auth route
@app.route('/auth', methods=['GET'])
def auth():
    account_linking_token = request.args.get("account_linking_token")
    redirect_uri = request.args.get("redirect_uri")
    session["ACCOUNT_LINKING_TOKEN"] = account_linking_token
    session["REDIRECT_URI"] = redirect_uri
    auth_url = AppGoogleAuth.GetAuthUrl()
    log(("Auth url: %s") % (auth_url))
    return redirect(auth_url)

# Google Callback link
@app.route("/OAuthCallback", methods=['GET'])
def OAuthCallback():
    if request.args.get("error"):
        return "Authentication Error", 403
    else:
        code = request.args.get("code")
        account_linking_token = session["ACCOUNT_LINKING_TOKEN"]
        redirect_uri = session["REDIRECT_URI"]
        data = {
            "authorization_code": code
        }
        url = redirect_uri + '&' + urllib.urlencode(data)
        return redirect(url)

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

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):  # someone sent us a message
                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"].get("text")  # the message's text
                    send_login_button(sender_id)
                if messaging_event.get("account_linking"):
                    sender_id = messaging_event["sender"]["id"]
                    auth_code = messaging_event['account_linking']['authorization_code']
                    AppGoogleAuth.SaveUserCredentials(sender_id, auth_code)
                    send_message(sender_id, "Congratulations, you have successfully linked the Work History bot to your Google Drive account!")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_login_button(recipient_id):
    bot = Bot(AppSettings.get("PAGE_ACCESS_TOKEN"))
    result = bot.send_message(recipient_id, json.dumps({
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        'title': 'Login to Drive',
                        'image_url': 'https://www.google.com/drive/static/images/drive/logo-drive.png'
                    ,
                        "buttons": [{
                                    "type": "account_link",
                                    "url": url_for("auth", _external=True)
                        }]
                    }]
                }
            }
    }))
    log(result)

def send_message(recipient_id, message_text):
    '''
        Send a message to the receipient
    '''
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    bot = Bot(AppSettings.get("PAGE_ACCESS_TOKEN"))
    response = bot.send_text_message(recipient_id, message_text)

def log(message):  # simple wrapper for logging to stdout on heroku
    AppLogger.log(message)
