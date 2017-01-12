from AppMessage import AppMessage
from pymessenger.bot import Bot
import AppGoogleAuth
import AppMessaging

class AppAccountLinkMessage(AppMessage):
    """docstring for AppAccountLinkMessage."""
    def __init__(self, messaging_event, page_access_token):
        super(AppAccountLinkMessage, self).__init__(messaging_event, page_access_token)

    def handle_message(self):
        bot = Bot(self._page_access_token)
        auth_code = self._received_message['account_linking'].get('authorization_code')
        if auth_code:
            AppGoogleAuth.SaveUserCredentials(self._sender_id, auth_code)
            bot.send_text_message(self._sender_id, "Success! Thanks for linking your Drive account")
        else:
            bot.send_text_message(self._sender_id, "Hmmm...something went wrong. Let's try that again.")
            AppMessaging.send_login_button(self._page_access_token, self._sender_id, "auth")
