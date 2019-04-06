from __future__ import print_function

import google.oauth2.credentials
import google_auth_oauthlib.flow
import httplib2

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from google.auth.transport.requests import Request
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

try:
    import argparse
    #flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    flags = tools.argparser.parse_args([])
except ImportError:
    flags = None


CLIENT_SECRETS = 'client_secrets.json'
SCOPE = 'https://www.googleapis.com/auth/drive'
STORAGE = Storage('credentials.storage')

def upload_photo(imgName):

    credentials = STORAGE.get()

    if not credentials or credentials.invalid:
        #flow = client.flow_from_clientsecrets('client_id.json', SCOPE)
        flow = client.flow_from_clientsecrets(CLIENT_SECRETS, scope=SCOPE)
        #http = httplib2.Http()
        flow.redirect_uri = "http://127.0.0.1:8000/upload/"
        if flags:
            #credentials = run_flow(flow, STORAGE, http=http)
            credentials = tools.run_flow(flow, STORAGE, flags)
    #return credentials

    http = httplib2.Http()
    http = credentials.authorize(http)
    drive = discovery.build('drive', 'v3', http = http) #credentials=credentials)

    FILES = (
        (imgName, None),
        (imgName, 'application/vnd.google-apps.photo'),
    )
    for filename, mimeType in FILES:
        metadata = {'name':filename}
        if mimeType:
            metadata['mimeType'] = mimeType
        res = drive.files().create(body=metadata,media_body=filename).execute()
        if res:
            print('Uploaded "%s" (%s)' % (filename, res['mimeType']))