from oauth2client import client
from oauth2client.contrib.dictionary_storage import DictionaryStorage
from AppLogger import AppLogger
from flask import url_for
import os.path

import json

def is_existing_user(user_fb_id):
    return GetUserCredientialsFromFile(user_fb_id) is not None

def GetUserCredientialsFromFile(user_fb_id):
    cred_dict = LoadCredentialsFile()
    if not cred_dict:
        return None
    else:
        storage = DictionaryStorage(cred_dict, user_fb_id)
        return storage.get()

def SaveUserCredentials(user_fb_id, user_gauth_code):
    cred_dict = LoadCredentialsFile()
    if not cred_dict: # Handle non-existent file
        cred_dict = {}
    storage = DictionaryStorage(cred_dict, user_fb_id)
    credentials = GetFlow().step2_exchange(user_gauth_code)
    storage.locked_put(credentials)
    SaveCredentialsFile(storage._dictionary) # XXX: TODO don't use private var here

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
    if not os.path.isfile('Credentials.json'):
        return None
    with open('Credentials.json', 'r') as f:
        if not f:
            return None
        raw_contents = f.read()
        if not raw_contents:
            return {}
        return json.loads(raw_contents)

def SaveCredentialsFile(data):
    with open('Credentials.json', 'w') as f:
        json.dump(data, f)
