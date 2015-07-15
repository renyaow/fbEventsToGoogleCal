#fbEventsToGoogleCal

The project is to export user's fb events to google calendar so they won't miss out. 

Three main parts:
1. Get user's fb events using FB Graph API
2. GUI shows the events and user can choose what events to add to google cal
3. Add these events to gcal using Google Calendar API

Instructions to run:
Packages:
Google Calendar Python Client Library: 
     pip install --upgrade google-api-python-client

Before running: make sure you have following four files
1. main.py: the main file to run
2. googleAuth.py: it runs authentication for gcal
3. client_secret.json: for gcal authentication (Not included)
4. fb_info: stores fb token and user id


Before running, user should obtain fb user id and access token. You can run python3 main.py and it gives instructions on how to get those information and how to store them in fb_info file. 

To obtain client_secret.json, go to Google Developer Console and create a new application. Follow this to setup: https://developers.google.com/api-client-library/python/apis/calendar/v3

First time using, google will prompt you to authorize usage by opening a default browser. Click accept so the app can access your calendars. 



Run: python3 main.py


References:
The Google API authtication code is taken from the Google Calendar API example   
