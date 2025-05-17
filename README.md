Untis to Google Calendar Transfer Tool

This tool transfers your Untis timetable to a Google Calendar and can notify you of important changes via Telegram.
🚀 Features

    🪞 Live Schedule Sync: Mirrors your Untis schedule in Google Calendar.
    ➕ Additive Updates: Previous calendar entries are preserved; nothing is deleted.
    🖋️ Configurable Entries: Customize what info gets added to the calendar.
    🔔 Telegram Notifications: Get real-time alerts for schedule changes, cancellations, and exams.

⚙️ Configuration

Edit your configuration in the appropriate file(s):

    group: "A" or "B"
    classID: String ID from the Untis API
    color-scheme:
        primary: Google Calendar color code (string)
        cancelled: Google Calendar color code (string)
        changed: Google Calendar color code (string)
        exams: Google Calendar color code (string)
    weeksAhead: Number of weeks to look ahead (integer)

Example:
JSON

{
  "group": "B",
  "classID": "3306",
  "color-scheme": {
    "primary": "1",
    "cancelled": "11",
    "changed": "5",
    "exams": "10"
  },
  "weeksAhead": 1
}

🖍️ Color Codes
colorID	Name	hexCode
1	Lavender	#A4BDFC
2	Sage	#7AE7BF
3	Grape	#DBADFF
4	Flamingo	#FF887C
5	Banana	#FBD75B
6	Tangerine	#FFB878
7	Peacock	#46D6DB
8	Graphite	#E1E1E1
9	Blueberry	#5484ED
10	Basil	#51B749
11	Tomato	#DC2127
None	Calendar's color	
📢 Telegram Notification Feature

Stay up to date with instant Telegram alerts for schedule changes.
How It Works

    The Telegram bot sends formatted notifications about changes, cancellations, or exams to your chosen Telegram chat/channel.

Setup

    Create a bot via BotFather and get your token.
    Add the bot to your group/channel and allow it to post.
    Find your chat/channel ID (for example, use userinfobot).
    Edit the env file:
    Python

    telegramToken = "YOUR_BOT_TOKEN"
    telegramChat = "YOUR_CHAT_ID"

    Run the script—notifications are sent whenever there are relevant changes.

Example Notification:
Code

<b>Mathematik (CHANGED)</b>
<b>Raum:</b> 101
<b>Stunde</b>: 17.05.2025 08:00-09:00
<b>Beschreibung:</b> Vertretung: Herr Müller

🧩 Modules

    google_cal_connector.py – Google Calendar API interface
    untis_connector.py – Fetches data from Untis
    configReader.py – Validates and reads configuration
    runner.py – Runs the main script
    telegramBot.py – Sends Telegram messages
    telegramBotInteractions.py – Starts Telegram bot interactions
    shareCalendarBot.py – Shares Google Calendar access

🔌 API Endpoints Used

    https://erato.webuntis.com/WebUntis/api/public/timetable/weekly/data
    https://www.googleapis.com/auth/calendar

🛠️ Setup
📅 Google Calendar Automation

    Create a Google Cloud Project:
        Go to Google Cloud Console.
        Create a new project.
    Enable the Google Calendar API:
        In the Cloud Console, navigate to "APIs & Services" > "Dashboard".
        Click "Enable APIs and Services" and search for "Google Calendar API".
        Click "Enable".
    Create a Service Account and Credentials:
        In "APIs & Services" > "Credentials", click "Create Credentials" > "Service account".
        Follow the prompts and download the JSON key file (credentials.json). Place it in your project directory.
    Set up Python Environment and install dependencies:
    sh

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    Configure your project as described above.

🚀 Usage
Show or Create a Calendar
sh

python showCalendar.py

Finds or creates a calendar called "school" and outputs its URL.
Share a Calendar
sh

python shareCalendar.py

Shares the specified calendar with an email and generates environment.json.
🔒 Security Notes

    Protect credentials.json: Never share or commit this file.
    Restrict Service Account Permissions: Only grant what’s necessary.
    Rotate Keys Regularly: Reduce risk if credentials are ever leaked.

📄 License

MIT or your preferred license here.
