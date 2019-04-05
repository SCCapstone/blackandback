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
    
    #media = discovery.MediaFileUpload(imgName, mimetype='image/png',chunksize=-1)
    #credentials = None
    #flow = client.flow_from_clientsecrets('client_secrets.json',SCOPE)
    #flow.redirect_uri = '/upload.html'

    
    #storage = Storage('storage.json')

    #credentials = tools.run_flow(flow,storage)
    #storage.put(credentials)
    #credentials = storage.get()

    if not credentials or credentials.invalid:
        #flow = client.flow_from_clientsecrets('client_id.json', SCOPE)
        flow = client.flow_from_clientsecrets(CLIENT_SECRETS, scope=SCOPE)
        #http = httplib2.Http()
        if flags:
            #credentials = run_flow(flow, STORAGE, http=http)
            credentials = tools.run_flow(flow, STORAGE, flags)
    return credentials
    

    http = httplib2.Http()
    http = credentials.authorize(http)
    drive = build('drive', 'v3', http = http, credentials=credentials)

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


"""
def upload_photo(imgName):
    #SCOPES = 'https://www.googleapis.com/auth/drive.readonly.metadata'
    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
        creds = tools.run_flow(flow, store)
    DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))
    #
    #files = DRIVE.files().list(pageSize=87).execute().get('files', [])
    
    #imgName = 'testImage.jpg'
    FILES = (
        (imgName,None),
        (imgName, 'application/vnd.google-apps.photo'),
    )
    for filename, mimeType in FILES:
        metadata = {'name':filename}
        if mimeType:
            metadata['mimeType'] = mimeType
        res = DRIVE.files().create(body=metadata, media_body = filename).execute()
        if res:
            print('Uploaded "%s" (%s)' % (filename, res['mimeType']))
"""

#for f in files:
#    print(f['name'], f['mimeType'])

'''POST https://www.googleapis.com/upload/drive/v3/files?uploadType=media HTTP/1.1
Content-Type: image/jpeg
Content-Length: [NUMBER_OF_BYTES_IN_FILE]
Authorization: Bearer [YOUR_AUTH_TOKEN]

[JPEG_DATA]'''

'''
file_metadata = {'name': 'photo.jpg'}
media = MediaFileUpload('files/photo.jpg',
                        mimetype='image/jpeg')
file = drive_service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
print ("File ID: %s" % file.get('id'))
'''