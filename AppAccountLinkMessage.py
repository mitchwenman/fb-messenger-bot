from AppMessage import AppMessage
from pymessenger.bot import Bot
import AppGoogleAuth

class AppAccountLinkMessage(AppMessage):
    """docstring for AppAccountLinkMessage."""
    def __init__(self, messaging_event, page_access_token):
        super(AppAccountLinkMessage, self).__init__(messaging_event, page_access_token)

    def handle_message(self):
        auth_code = self._received_message['account_linking'].get('authorization_code')
        if auth_code:
            AppGoogleAuth.SaveUserCredentials(self._sender_id, auth_code)
            bot = Bot(self._page_access_token)
            bot.send_text_message(self._sender_id, "Success! Thanks for linking your Drive account")
        else:
            super.handle_message()
