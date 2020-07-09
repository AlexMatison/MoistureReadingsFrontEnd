from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import logging
import os
import pickle

# https://github.com/googleapis/google-api-python-client/issues/299
logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

# flow = client.flow_from_clientsecrets('MoistureReadingsFrontEnd/google/credentials.json', SCOPES)

def moisture_to_google(moisture_data, spreadsheet_id):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('MoistureReadingsFrontEnd/google/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'MoistureReadingsFrontEnd/google/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Call the Sheets API
    RANGE_NAME = 'Sheet1!A:D'
    print(moisture_data)
    # payload = [
    #     moisture_data.get('id'),
    #     moisture_data.get('location_id'),
    #     moisture_data.get('moisture_reading'),
    #     moisture_data.get('timestamp').strftime("%Y-%m-%d %H:%M:%S")
    # ]
    ### SEND data

    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED'

    # How the input data should be inserted.
    insert_data_option = 'INSERT_ROWS'

    value_range_body = {
        'values': [moisture_data]
        # List of rows, each row has a list of values (columns)
    }

    try:
        request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=RANGE_NAME,
                                                     valueInputOption=value_input_option,
                                                     insertDataOption=insert_data_option, body=value_range_body)
        response = request.execute()
    except:
        print('There was a problem appending values to google sheets')
        return False
    else:
        print('this is the google sheets response:')
        print(response)
        return True


    # TODO: Change code below to process the `response` dict:


    ### GET data
    # result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
    #                                             range=RANGE_NAME).execute()
    # values = result.get('values', [])
    #
    # if not values:
    #     print('No data found.')
    # else:
    #     print('Name, Major:')
    #     for row in values:
    #         # Print columns A and E, which correspond to indices 0 and 4.
    #         print('%s, %s' % (row[0], row[1]))

