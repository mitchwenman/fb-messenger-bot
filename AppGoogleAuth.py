from oauth2client import client
from AppLogger import AppLogger
from flask import url_for

import json

def SaveUserCredentials(user_fb_id, user_gauth_code):
    flow = GetFlow()

def GetAuthUrl():
    # Get redirect uri from client secrets
    flow = GetFlow()
    redirect = flow.step1_get_authorize_url(GetRedirectURI())
    return redirect

def GetFlow():
    flow = client.flow_from_clientsecrets("client_secrets.json",
                scope="https://www.googleapis.com/auth/drive",
                redirect_uri=GetRedirectURI())
    return flow

def GetRedirectURI():
    redirect = url_for('OAuthCallback', _external=True)
    return redirect
