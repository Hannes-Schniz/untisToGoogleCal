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

- 🪞 See all the most recent changes in your untis schedule mirrored in your calendar
- ➕ Additive procedure (No entries are deleted, previous versions of the lessons are preserved)
- 🖋️ Configuration for The Information added to the calendar

---

# ⚙️ Configuration

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
    "changed": "5",
    "exams": "10"
  },
  "weeksAhead": 1
```

🖍️ **color codes**

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

# 🔌 Endpoints

- https://erato.webuntis.com/WebUntis/api/public/timetable/weekly/data
- https://www.googleapis.com/auth/calendar

---

# 🧩 Modules

- google_cal_connector.py
  Handles all communication with the google calendar API
- untis_connector.py
  Retrieves all data from the public untis API
- configReader.py
  Reads all configs and does a regex validation
- runner.py
  Executes the script

---

# 🛠️ Setup

## 📅 Google Calendar Automation Setup ☁️

This guide will walk you through setting up a Google Cloud project, creating a service account, and using the provided Python scripts (`showCalendar.py` and `shareCalendar.py`) to manage your Google Calendar.

### 🛠️ Prerequisites

- A Google account 📧.
- Python 3.6 or later installed 🐍.
- `pip` (Python package installer) 📦.

### ☁️ Setup Google Cloud Project

1.  **Go to the Google Cloud Console:**
    - Open your web browser and navigate to [console.cloud.google.com](https://console.cloud.google.com/) 🌐.
2.  **Create a New Project:**
    - Click on the project selection dropdown at the top of the page 🔽.
    - Click "New Project" ➕.
    - Enter a project name and click "Create" ✅.
3.  **Enable the Google Calendar API:**
    - In the Cloud Console, navigate to "APIs & Services" > "Dashboard" 📊.
    - Click "Enable APIs and Services" ➕.
    - Search for "Google Calendar API" and click on it 🔍.
    - Click "Enable" 👍.

### 🔑 Create a Service Account

1.  **Navigate to Service Accounts:**
    - In the Cloud Console, navigate to "APIs & Services" > "Credentials" 🔐.
    - Click "Create Credentials" and select "Service account" 👤.
2.  **Service Account Details:**
    - Enter a service account name 📝.
    - Click "Create and Continue" 👉.
    - (Optional) Assign roles. For basic calendar access, you can use "Project" > "Viewer" or any more specific calendar role 🛡️.
    - Click "Continue" and then "Done" 🎉.
3.  **Create a JSON Key:**
    - Click on the newly created service account 🖱️.
    - Go to the "Keys" tab 🔑.
    - Click "Add Key" and select "Create new key" ➕.
    - Choose "JSON" as the key type and click "Create" 💾.
    - A JSON file will be downloaded. **Store this file securely.** Rename it to `credentials.json` and place it in the same directory as your Python scripts 📂.

### 📦 Setup Python Virtual Environment and Install Dependencies

1.  **Create a Virtual Environment:**
    - Open your terminal or command prompt 💻.
    - Navigate to the directory containing your scripts 🧭.
    - Run the following command to create a virtual environment:
      - On Windows: `python -m venv venv`
      - On macOS/Linux: `python3 -m venv venv`
2.  **Activate the Virtual Environment:**

    - On Windows: `venv\Scripts\activate`
    - On macOS/Linux: `source venv/bin/activate`

3.  **Install Dependencies:**
    - Run the following command to install the required Python libraries: `pip install -r requirements.txt`

### 🚀 Using the Scripts

#### `showCalendar.py` 🔍

This script finds or creates a calendar called "school" and outputs its URL.

1.  **Place the Script:**
    - Save `showCalendar.py` and `credentials.json` in the same directory 📂.
2.  **Run the Script:**
    - Open your terminal or command prompt 💻.
    - Ensure your virtual environment is activated.
    - Navigate to the directory containing the script 🧭.
    - Run the script: `python showCalendar.py` ▶️.
3.  **Output:**
    - The script will output the calendar's ID and URL, indicating whether it was found or created 📋.

#### `shareCalendar.py` 🤝

This script shares a specific calendar with a user-provided email address. It also generates a json file with the calendar ID.

1.  **Place the Script:**
    - Save `shareCalendar.py` and `credentials.json` in the same directory 📂.
2.  **Run the Script:**
    - Open your terminal or command prompt 💻.
    - Ensure your virtual environment is activated.
    - Navigate to the directory containing the script 🧭.
    - Run the script: `python shareCalendar.py` ▶️.
3.  **Interactive Input:**
    - The script will prompt you to enter the email address to share the calendar with 📧.
    - The script will prompt you to enter the calendar ID 🆔.
4.  **Output:**
    - The script will output a confirmation message indicating that the calendar has been shared ✅.
    - A `environment.json` file will be generated in the same directory, containing the calendar ID 📄.

### 🔒 Security Notes

- **Protect your `credentials.json` file:** This file contains sensitive information. Do not share it or commit it to version control systems 🛡️.
- **Restrict service account permissions:** Grant only the necessary permissions to the service account 🔑.
- **Regularly review and rotate service account keys:** This helps minimize the impact of compromised keys 🔄.
