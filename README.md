# Untis to google calendar transfer tool

This tool transfers your untis calendar to a specified google calendar.

# Endpoints

- https://erato.webuntis.com/WebUntis/api/public/timetable/weekly/data
- https://www.googleapis.com/auth/calendar

# Setup

1. Clone this repository
2. Register a google project
3. Enable the google calendar api
   https://developers.google.com/calendar/api/quickstart/python?hl=de
4. Download your secret and add it to credentials.json in the rood directory of the project
5. Create a environment.json file containing your calendar ID like:

   ```
   {
       "calendarID":"<calendar id>"
   }

   ```

6. Install all python libraries needed for the google API
   ```
   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```
7. Configure a cron job to run runner.py
