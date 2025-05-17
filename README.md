# Untis to Google Calendar Transfer Tool

This tool transfers your Untis timetable to a Google Calendar and can **notify you of important changes via Telegram**.

---

## 🚀 Features

- 🪞 **Live Schedule Sync:** Mirrors your Untis schedule in Google Calendar.
- ➕ **Additive Updates:** Previous calendar entries are preserved; nothing is deleted.
- 🖋️ **Configurable Entries:** Customize what info gets added to the calendar.
- 🔔 **Telegram Notifications:** Get real-time alerts for schedule changes, cancellations, and exams.
- 👥 **Calendar Sharing:** Share your school calendar with others via email.
- 🧹 **Flush Calendar:** Delete all events from your school calendar with a single command.

---

## ⚙️ Configuration

Edit your configuration in [`config.json`](config.json):

```json
{
  "classID": "3306",
  "color-scheme": {
    "primary": "1",
    "cancelled": "11",
    "changed": "5",
    "exam": "10"
  },
  "weeksAhead": 5
}
```

- `classID`: String ID from the Untis API (e.g., `"3306"`)
- `color-scheme`: Google Calendar color codes for different event types
- `weeksAhead`: Number of weeks to look ahead (integer)

**Note:** The `group` parameter is no longer required.

### 🖍️ Color Codes

| colorID | Name      | hexCode   | Example                |
| ------- | --------- | --------- | ---------------------- |
| 1       | Lavender  | #A4BDFC   | ![#A4BDFC](https://via.placeholder.com/20/A4BDFC/000000?text=+) |
| 2       | Sage      | #7AE7BF   | ![#7AE7BF](https://via.placeholder.com/20/7AE7BF/000000?text=+) |
| 3       | Grape     | #DBADFF   | ![#DBADFF](https://via.placeholder.com/20/DBADFF/000000?text=+) |
| 4       | Flamingo  | #FF887C   | ![#FF887C](https://via.placeholder.com/20/FF887C/000000?text=+) |
| 5       | Banana    | #FBD75B   | ![#FBD75B](https://via.placeholder.com/20/FBD75B/000000?text=+) |
| 6       | Tangerine | #FFB878   | ![#FFB878](https://via.placeholder.com/20/FFB878/000000?text=+) |
| 7       | Peacock   | #46D6DB   | ![#46D6DB](https://via.placeholder.com/20/46D6DB/000000?text=+) |
| 8       | Graphite  | #E1E1E1   | ![#E1E1E1](https://via.placeholder.com/20/E1E1E1/000000?text=+) |
| 9       | Blueberry | #5484ED   | ![#5484ED](https://via.placeholder.com/20/5484ED/000000?text=+) |
| 10      | Basil     | #51B749   | ![#51B749](https://via.placeholder.com/20/51B749/000000?text=+) |
| 11      | Tomato    | #DC2127   | ![#DC2127](https://via.placeholder.com/20/DC2127/000000?text=+) |

---

## 📢 Telegram Notification Feature

**Stay up to date with instant Telegram alerts for schedule changes, cancellations, and exams.**

### How It Works

- The Telegram bot sends formatted notifications about changes, cancellations, or exams to your chosen Telegram chat/channel.
- Notifications are triggered automatically when relevant changes are detected during sync.

### Setup

1. **Create a bot** via [BotFather](https://t.me/botfather) and get your token.
2. **Add the bot** to your group/channel and allow it to post.
3. **Find your chat/channel ID** (e.g., use [userinfobot](https://t.me/userinfobot)).
4. **Edit your `env.py`** (not versioned, see `.gitignore`):

    ```python
    telegramToken = "YOUR_BOT_TOKEN"
    telegramChat = "YOUR_CHAT_ID"
    ```

5. **Run the main script** (`runner.py`)—notifications are sent whenever there are relevant changes.

#### Example Notification

```
<b>Mathematik (CHANGED)</b>
<b>Raum:</b> 101
<b>Stunde</b>: 17.05.2025 08:00-09:00
<b>Beschreibung:</b> Vertretung: Herr Müller
```

---

## 🧩 Modules

- [`google_cal_connector.py`](google_cal_connector.py): Google Calendar API interface, event creation, and Telegram notification integration.
- [`untis_connector.py`](untis_connector.py): Fetches data from Untis.
- [`configReader.py`](configReader.py): Validates and reads configuration.
- [`runner.py`](runner.py): Runs the main sync script.
- [`telegramBot.py`](telegramBot.py): Sends Telegram messages.
- [`telegramBotInteractions.py`](telegramBotInteractions.py): Starts Telegram bot interactions.
- [`shareCalendar.py`](shareCalendar.py): Shares Google Calendar access interactively.
- [`shareCalendarBot.py`](shareCalendarBot.py): Shares Google Calendar access (programmatic).
- [`flush_calendar.py`](flush_calendar.py): Deletes all events from the school calendar.
- [`showCalandars.py`](showCalandars.py): Finds or creates the "school" calendar and outputs its URL.

---

## 🔌 API Endpoints Used

- `https://erato.webuntis.com/WebUntis/api/rest/view/v1/timetable/entries`
- `https://www.googleapis.com/auth/calendar`

---

## 🛠️ Setup

### 📅 Google Calendar Automation

1. **Create a Google Cloud Project:**
    - Go to [Google Cloud Console](https://console.cloud.google.com/).
    - Create a new project.
2. **Enable the Google Calendar API:**
    - In the Cloud Console, navigate to "APIs & Services" > "Dashboard".
    - Click "Enable APIs and Services" and search for "Google Calendar API".
    - Click "Enable".
3. **Create a Service Account and Credentials:**
    - In "APIs & Services" > "Credentials", click "Create Credentials" > "Service account".
    - Follow the prompts and download the JSON key file (`credentials.json`). Place it in your project directory.
4. **Set up Python Environment and install dependencies:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
5. **Configure your project** as described above.

---

## 🚀 Usage

### Show or Create a Calendar

```sh
python showCalandars.py
```
Finds or creates a calendar called "school" and outputs its URL.

### Share a Calendar

```sh
python shareCalendar.py
```
Shares the specified calendar with an email and generates `environment.json`.

### Flush (Delete All Events) from Calendar

```sh
python flush_calendar.py
```
Deletes all events from the configured calendar.

### Run the Main Sync

```sh
python runner.py
```
Syncs your Untis timetable to Google Calendar and sends Telegram notifications for changes.

---

## 🔒 Security Notes

- **Protect `credentials.json`:** Never share or commit this file.
- **Restrict Service Account Permissions:** Only grant what’s necessary.
- **Rotate Keys Regularly:** Reduce risk if credentials are ever leaked.

---

## 📄 License

MIT or your preferred license here.
