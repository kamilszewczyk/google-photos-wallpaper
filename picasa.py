import webbrowser
import os
import json
import httplib2
import xml.etree.ElementTree as etree
import urllib.request as urllib

from oauth2client import client


class Picasa:
    current_dir = os.path.dirname(os.path.realpath(__file__))

    def _get_credentials(self):
        # if credentials file exists load it
        if os.path.isfile(self.current_dir + '/credentials.json'):
            credentials_file = open(self.current_dir + '/credentials.json', 'r')
            credentials = client.OAuth2Credentials.from_json(json.load(credentials_file))
        # else create credentials and ask for permission from user
        else:
            flow = client.flow_from_clientsecrets(self.current_dir + '/client_secret.json', scope='https://picasaweb.google.com/data/', redirect_uri='urn:ietf:wg:oauth:2.0:oob')

            auth_uri = flow.step1_get_authorize_url()
            webbrowser.open(auth_uri)
            auth_code = input('Enter the auth code: ')
            credentials = flow.step2_exchange(auth_code)
            # save credentials to file
            credentials_file = open(self.current_dir + '/credentials.json', 'w')
            json.dump(credentials.to_json(), credentials_file)

        return credentials

    def _get_authorized_http(self):
        http = httplib2.Http()
        credentials = self._get_credentials()
        try:
            http = credentials.authorize(http)
            credentials.refresh(http)
        except Exception as ex:
            print(ex)

        return http

    def _request(self, url):
        http = self._get_authorized_http()
        response, content = http.request(url)

        return content.decode("utf-8")

    def get_album_list(self):
        url = "https://picasaweb.google.com/data/feed/api/user/default?v=2.0&fields=entry(id,gphoto:numphotos)"

        tree = etree.fromstring(self._request(url))

        return [{"id": "".join(node[0].text.split("/")[-1:]), "url": node[0].text, "num_photos": int(node[1].text)} for node in tree]

    def get_photos_list(self, album_id):
        url = "https://picasaweb.google.com/data/feed/api/user/default/albumid/" + album_id + "?v=2.0&imgmax=1440u&fields=entry(content(@src))"

        tree = etree.fromstring(self._request(url))

        return [node[0].attrib for node in tree]

    def get_photo(url, path):
        if not os.path.exists(path):
            os.makedirs(path)

        name = "".join(url.split("/")[-1:])
        urllib.urlretrieve(url, path + "/" + name)
