import json

from pymessenger.bot import Bot
import AppGoogleAuth
import AppMessaging
from flask import url_for

class AppMessage(object):
    """docstring for AppMessage."""
    def __init__(self, messaging_event, page_access_token):
        super(AppMessage, self).__init__()
        self._sender_id = messaging_event["sender"]["id"]
        self._received_message = messaging_event
        self._page_access_token = page_access_token
        # Check if user is new or existing
        self._existing_user = AppGoogleAuth.is_existing_user(self._sender_id)

    def handle_message(self):
        ''' Handles messaginga and response logic '''
        bot = Bot(self._page_access_token)
        if not self._existing_user:
            bot.send_text_message(self._sender_id, "Hi there. Welcome! I'll need access to your Google Drive to save your work history.")
            AppMessaging.send_login_button(self._page_access_token, self._sender_id, "auth")
        else:
            bot = Bot(self._page_access_token)
            bot.send_text_message(self._sender_id, "Hi there!")


    def _send_login_button(self):
        bot = Bot(self._page_access_token)
        bot.send_text_message(self._sender_id, "Let's get started! I'll need access to your Google Drive so I can store your work history.")
        bot.send_message(self._sender_id, json.dumps({
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
