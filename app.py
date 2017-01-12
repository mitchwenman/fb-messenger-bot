import os
import sys
import json
import urllib
import logging
from AppSettings import AppSettings
from AppLogger import AppLogger
import AppGoogleAuth

## Fix for requests
import requests

from flask import Flask, request, redirect, session, url_for
from pymessenger.bot import Bot
from oauth2client.contrib.flask_util import UserOAuth2
from AppMessage import AppMessage
from AppAccountLinkMessage import AppAccountLinkMessage

app = Flask(__name__)
app.config['SECRET_KEY'] = AppSettings.get("APP_SECRET_KEY") #secure storage across requests
app.config['GOOGLE_OAUTH2_CLIENT_SECRETS_FILE'] = 'client_secrets.json'
oauth2 = UserOAuth2(app)

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
    log(session)
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
    ''' Messenger webhook '''
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):  # someone sent us a message
                    message = AppMessage(messaging_event, AppSettings.get('PAGE_ACCESS_TOKEN'))
                    message.handle_message()
                if messaging_event.get("account_linking"):
                    link_message = AppAccountLinkMessage(messaging_event, AppSettings.get('PAGE_ACCESS_TOKEN'))
                    link_message.handle_message()
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def log(message):  # simple wrapper for logging to stdout on heroku
    AppLogger.log(message)
