import requests
import json
import tkinter as tk
import sys
import re
from datetime import datetime, date, time
import googleAuth
from httplib2 import Http
from apiclient.discovery import build
from apiclient import errors
import json


FB_AUTH = 'https://graph.facebook.com/oauth/access_token?'
try:
    with open('fb_info') as filename:
        USER_ID = filename.readline().rstrip()
        ACCESS_TOKEN = filename.read().rstrip()
        print (USER_ID)
        print (ACCESS_TOKEN)
except:
    print ("input correct fb info")
    sys.exit()


class Event():
    def __init__(self, event):
        self.name = event['name']
        self.location = event['location']
        self.start = event['start_time']
        self.start_time = event['start_time']
        if ':' not in self.start_time:
            self.start_time += 'T00:00:00-0400'
        self.start = decomposeTime(self.start)
        if 'end_time' in event:
            self.end = decomposeTime(event['end_time'])
            self.end_time = event['end_time']
            if ':' not in self.end_time:
                self.end_time += 'T23:59:59-0400' 
        else:
            self.end = self.start
            self.end_time = self.start_time

    def __str__(self):
        return "{}, {}, {}-{}".format(self.name, self.location, self.start, self.end)


def decorEvent(func):
    def inner():
        events = func()
        events = [Event(event) for event in events]
        return events
    return inner

# get user events info from FB
@decorEvent
def getEvents():
    FB_GRAPH = 'https://graph.facebook.com/v2.0/' + USER_ID + '/events?access_token='+ACCESS_TOKEN
    response = requests.get(FB_GRAPH)
    if 'error' in response.text:
        print ("Invalid access token. Please provide a valid access token")
        sys.exit()
    events = json.loads(response.text)['data']
    removedEvents = [event for event in events if decomposeTime(event['start_time']) <= datetime.today()]
    for event in removedEvents:
        events.remove(event)
    return events

def decomposeTime(timeStr):
    fmt = '%Y-%m-%d'
    if ':' in timeStr:
        timeStr = timeStr.rsplit('-',1)[0]
        #print (timeStr.rsplit('-',1))[0]
        fmt = '%Y-%m-%dT%H:%M:%S'
    return datetime.strptime(timeStr, fmt)

# GUI
class displayEvents(tk.Frame):

    def __init__(self, events, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.f = tk.Frame(self)
        self.f.grid()

        # handler for toggle button
        def statusHandler(index):
            if status[index]['text'] == 'Add':
                status[index]['text'] = 'Not adding'          
            elif status[index]['text'] == 'Not adding':
                status[index]['text'] = 'Add'

        # handler for adding events
        def addHandler():
            clickedEvents = [event for i, event in enumerate(events) if status[i]['text']=='Add']
            for i in range(0, len(events)):
                if status[i]['text'] == 'Add':
                    status[i]['text'] ='Added'
            addEvents(clickedEvents)
            
        names = [tk.Text(self.f,height=1, width=80) for event in events]
        times = [tk.Text(self.f, height=1, width=40) for event in events]
        status = [tk.Button(self.f, height=1, width=10) for event in events]
        for i, event in enumerate(events):
            names[i].insert(tk.END, event.name)
            names[i].grid(row=i, column=1)
            startTime = event.start
            times[i].insert(tk.END, startTime)
            endTime= event.end
            times[i].insert(tk.END, " - {}".format(endTime))
            times[i].grid(row=i, column=2)
            status[i]['text']='Not adding'
            status[i].grid(row=i, column=3)
            status[i]['command']=lambda number=i:statusHandler(number)
       
        addButton = tk.Button(self.f, height = 1, width =10)
        addButton['text'] = 'Add events'
        addButton.grid(row=len(events)+1,column=1)
        addButton['command']=addHandler
        


"""
add events into google calendar
"""                   
def addEvents(events):
    credentials = googleAuth.get_credentials()
    service = build('calendar', 'v3', http=credentials.authorize(Http()))

    calendar = {
        'summary': 'fbEvents',
        'timeZone': 'America/New_York'
    }
    created_calendar = service.calendars().insert(body=calendar).execute()

    for event in events:
        newEvent = {'summary': event.name,  'location': event.location, 'start': {
    'dateTime': event.start_time
  },
  'end': {
    'dateTime': event.end_time
  }
}   
        try:
            created_event = service.events().insert(calendarId=created_calendar['id'], body=newEvent).execute()
        except errors.HttpError as e:
            print (e.content)

def main():
    print ("To use this, you need to grab your facebook id number and an access token and store it in a file called fb_info.")
    print ("First line should be id and second line should be the token")
    print ('id: https://www.facebook.com/note.php?note_id=91532827198')
    print ('access token: https://developers.facebook.com/tools/explorer')
    events = getEvents()
    root = tk.Tk()
    app = displayEvents(events, master=root)
    app.mainloop()


if  __name__ == '__main__':
    main()



