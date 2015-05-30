#!/usr/bin/env python3
import webbrowser
import os
import json
import httplib2
from io import StringIO

from oauth2client import client

picasa_url = "https://picasaweb.google.com/data/feed/api/user/default?v=2.0&kind=photo&max-results=1&imgmax=1440u"

if os.path.isfile('credentials.json'):
    credentials_file = open('credentials.json', 'r')
    credentials = client.OAuth2Credentials.from_json(json.load(credentials_file))
else:
    flow = client.flow_from_clientsecrets('client_secret.json', scope='https://picasaweb.google.com/data/', redirect_uri='urn:ietf:wg:oauth:2.0:oob')

    auth_uri = flow.step1_get_authorize_url()
    webbrowser.open(auth_uri)
    auth_code = input('Enter the auth code: ')
    credentials = flow.step2_exchange(auth_code)
    credentials_file = open('credentials.json', 'w')
    json.dump(credentials.to_json(), credentials_file)

http = httplib2.Http()
try:
    http = credentials.authorize(http)
    response, album_list = http.request(picasa_url, 'GET')
    if response['status'] == '403':
        credentials.refresh(http)
        response, album_list = http.request(picasa_url, 'GET')

    album_list = album_list.decode("utf-8")
    #album_list = StringIO(album_list)
    print(album_list)
except Exception as ex:
    print(ex)

