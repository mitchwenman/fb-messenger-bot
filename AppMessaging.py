from pymessenger.bot import Bot
import json
from flask import url_for

'''
A module to collect a bunch of useful, generic messages to send to users.
'''

def send_login_button(page_token, receipient_id, login_link):
    bot = Bot(page_token)
    bot.send_message(receipient_id, json.dumps({
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
                                    "url": url_for(login_link, _external=True)
                        }]
                    }]
                }
            }
    }))
