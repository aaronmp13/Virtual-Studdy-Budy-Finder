from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def createMeeting(group_name, emails, date, startTime, endTime):
    #group_name will be a string
    #emails will be a list of strings
    #date will be a string in yyyy-mm-dd format
    #starttime will be in hh:mm:ss
    #timezone will awlays be eastern

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('virtualstuddybuddy/token.pickle'):
        with open('virtualstuddybuddy/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'virtualstuddybuddy/oldCredentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': group_name + " meeting",
        'attendees':[{'email':str(e)} for e in emails],
        'start':{
            'dateTime': str(date)+"T"+str(startTime),
            'timeZone': 'America/New_York'
        },
        'end':{
            'dateTime': str(date)+"T"+str(endTime),
            'timeZone': 'America/New_York'
        },
        'conferenceData':{
            'createRequest':{
                "conferenceSolutionKey": {
                    "type": "hangoutsMeet"
                },
                "requestId": group_name,
            }
        }
    }

    event = service.events().insert(calendarId='primary', sendUpdates = "all", body=event, conferenceDataVersion = 1).execute()

g = "vsb test"
emails = ["mtmenon123@gmail.com", "mtmenon1234@gmail.com","mtmenon12345@gmail.com",]
date = "2020-11-14"
startTime = "10:00:00"
endTime = "14:00:00"
createMeeting(g, emails, date, startTime, endTime)