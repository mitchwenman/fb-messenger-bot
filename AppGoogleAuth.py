from oauth2client import client
from oauth2client.contrib.dictionary_storage import DictionaryStorage
from AppLogger import AppLogger
from flask import url_for

import json

def GetUserCredientialsFromFile(user_fb_id):
    cred_dict = LoadCredentialsFile()
    storage = DictionaryStorage(cred_dict, user_fb_id)
    return storage.get()

def SaveUserCredentials(user_fb_id, user_gauth_code):
    cred_dict = LoadCredentialsFile()
    storage = DictionaryStorage(cred_dict, user_fb_id)
    credentials = GetFlow().step2_exchange(user_gauth_code)
    storage.locked_put(credentials)
    SaveCredentialsFile(storage._dictionary)

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

def LoadCredentialsFile():
    with open('Credentials.json', 'r') as f:
        raw_contents = f.read()
        if not raw_contents:
            return {}
        return json.loads(raw_contents)

def SaveCredentialsFile(data):
    with open('Credentials.json', 'w') as f:
        json.dump(data, f)
