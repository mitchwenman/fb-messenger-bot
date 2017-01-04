from pydrive.auth import GoogleAuth

class AppGoogleAuth(object):
    """docstring for GoogleAuth."""

    @staticmethod
    def SaveUserCredentials(user_fb_id, user_gauth_code)
        f = open('client_secrets_authcodes','w')
        f.write(("%s=%s") % (user_fb_id, user_gauth_code))
        
