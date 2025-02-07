# Untis to google calendar transfer tool

This tool transfers your untis calendar to a specified google calendar.

It utilizes a publicly accessibale UNTIS API to retrieve all important Information about lessons and budles them into calendar entries.
A calendar entry is built as follows:

```
    'summary': [CHANGED|CANCELLED]Subject name,
    'location': roomnumber,
    'description': period Text,
    'color': [purple:regular|yellow:changed|red:cancelled]
```

**Advantages of this tool**
- See all the most recent changes in your untis schedule mirrored in your calendar 🪞
- Additive procedure (No entries are deleted, previous versions of the lessons are preserved) ➕
- Configuration for The Information added to the calendar🖋️


---

# Configuration ⚙️

- group: [A|B]
- classID: ID found in the untis API as string
- color-scheme:
  - primary: google calendar color code as string
  - cancelled: google calendar color code as string
  - changed: google calendar color code as string
- weeksAhead: number of weeks to look ahead as string

**Defaults:**

```
"group": "B",
  "classID": "3306",
  "color-scheme": {
    "primary": "1",
    "cancelled": "11",
    "changed": "5"
  },
  "weeksAhead": 1
```

**color codes** 🖍️

| colorID | Name                  | hexCode |
| ------- | --------------------- | ------- |
| 1       | Lavender              | #A4BDFC |
| 2       | Sage                  | #7AE7BF |
| 3       | Grape                 | #DBADFF |
| 4       | Flamingo              | #FF887C |
| 5       | Banana                | #FBD75B |
| 6       | Tangerine             | #FFB878 |
| 7       | Peacock               | #46D6DB |
| 8       | Graphite              | #E1E1E1 |
| 9       | Blueberry             | #5484ED |
| 10      | Basil                 | #51B749 |
| 11      | Tomato                | #DC2127 |
| None    | Color of the calendar |         |

---

# Endpoints 🔌

- https://erato.webuntis.com/WebUntis/api/public/timetable/weekly/data
- https://www.googleapis.com/auth/calendar

---

# Modules 🧩

- google_cal_connector.py
  Handles all communication with the google calendar API
- untis_connector.py
  Retrieves all data from the public untis API
- configReader.py
  Reads all configs and does a regex validation
- runner.py
  Executes the script

---

# Setup 🛠️

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
7. Configure a cron job to run runner.py (Alternatively it can be ran manually)


⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
** When you run the script for the first time, you need to login with Googles OAuth provider! So a Webbrowser is needed. Alternatively the script can be ran on your computer at first and the token can be transferred to your server!**
