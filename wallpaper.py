#!/usr/bin/env python3

from oauth2client.client import SignedJwtAssertionCredentials
from httplib2 import Http
import config

p12 = open("wallpaper.p12", 'rb').read()

credentials = SignedJwtAssertionCredentials(config.account_email, p12, 'https://picasaweb.google.com/data/')

http = Http()

credentials.authorize(http)

resp, content = http.request("https://picasaweb.google.com/data/feed/api/user/" + config.picasa_user_id)

print(content)
