from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import logging

# https://github.com/googleapis/google-api-python-client/issues/299
logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'


def moisture_to_google(moisture_data, spreadsheet_id):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    try:
        store = file.Storage('google/token.json')
    except:
        print("Problem with token.json")
        return False

    try:
        creds = store.get()
    except:
        print("problem with creds")
        return False

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('google/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    service = build('sheets', 'v4', http=creds.authorize(Http()))

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

