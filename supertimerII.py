import serial,math
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

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

def race_range(sheet_range,run,race):
    # Split the range into sheet name and range
    sheet_name, range_str = sheet_range.split("!")

    # Get the column indexes
    start_col, end_col = range_str.split(":")
    end_col_idx = ord(end_col) - 64  # Convert the column letter to index

    # Increase the end column index by 1
    new_start_col_idx = end_col_idx + (2*run+1)
    new_end_col_idx = end_col_idx + (2*run+2)

    # Convert the new end column index back to letter
    new_end_col = chr(new_end_col_idx + 64)
    new_start_col = chr(new_start_col_idx + 64)
    start_idx=str(4*race+1)
    end_idx=str(4*race+4)

    # Construct the new range string
    new_range_str = f"{new_start_col}{start_idx}:{new_end_col}{end_idx}"

    # Combine the sheet name and new range to get the updated range string
    updated_range = f"{sheet_name}!{new_range_str}"
    return updated_range


def read_google_sheet(creds,sheet_id, sheet_range):
    try:
        service = build('sheets', 'v4', credentials=creds)
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

def update_google_sheet(creds,spreadsheet_id, sheet_range, values):
    try:
        service = build('sheets', 'v4', credentials=creds)
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=sheet_range, valueInputOption="USER_ENTERED", body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

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

def connect_to_track():
    ser = serial.Serial('/dev/tty.usbserial-10')
    return ser

def run_race(creds,cars,runs,spreadsheet_id):
    global RaceIsOn
    ser = serial.Serial('/dev/tty.usbserial-10')
    while RaceIsOn: 
        line = ser.readline()
        str_line = line.decode("utf-8")
        str_line = str_line.replace("\r","").replace("\n","").replace(" ","")

def calc_race_and_runs(number_of_cars):
    lanes = 4
    runs = math.floor(math.log(number_of_cars))
    races = math.ceil(number_of_cars/lanes)
    print("Based on the number of cars registered...")
    print("You should run "+str(runs)+" times and")
    print("each run will need "+str(races)+" races")
    return runs,races
