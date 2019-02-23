from __future__ import print_function

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

def upload_photo():
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
    FILES = (
        ('testImage.jpg',None),
        ('testImage.jpg', 'application/vnd.google-apps.photo'),
    )
    for filename, mimeType in FILES:
        metadata = {'name':filename}
        if mimeType:
            metadata['mimeType'] = mimeType
        res = DRIVE.files().create(body=metadata, media_body = filename).execute()
        if res:
            print('Uploaded "%s" (%s)' % (filename, res['mimeType']))


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