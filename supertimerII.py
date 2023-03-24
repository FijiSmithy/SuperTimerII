import serial,math
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def get_spreadsheet_id():
    #ask user form input to provide ID of spreadsheet
    spreadsheet_id = input("What is the id of the spreadsheet: ")
    sheet_range = input("What is the range of the sheet to read: ")
    return spreadsheet_id,sheet_range

def get_google_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_supertrackII.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def read_google_sheet(creds):
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet_id, sheet_range = get_spreadsheet_id()
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id,
                                    range=sheet_range).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return None

        return values
    except HttpError as err:
        print(err)
        return None

RaceIsOn = False

def start_race():
    #Sets the value of RaceIsOn to True
    global RaceIsOn
    RaceIsOn = True
    print("Race has Started")

def stop_race():
    #Sets the value of RaceIsOn to False
    global RaceIsOn
    RaceIsOn = False
    print("Race has stopped")

def run_race():
    global RaceIsOn
    ser = serial.Serial('/dev/tty.usbserial-10')
    while RaceIsOn: 
        line = ser.readline()
        str_line = line.decode("utf-8")
        str_line = str_line.replace("\r","").replace("\n","").replace(" ","")

def calc_race_and_runs(number_of_cars):
    lanes = 4
    #Find the exponent from an exponential value with a base of 4
    print("Based on the number of cars registered...")
    print("You should run "+str(math.floor(math.log(number_of_cars)))+" times and")
    print("each run will need "+str(math.ceil(number_of_cars/lanes))+" races")
    