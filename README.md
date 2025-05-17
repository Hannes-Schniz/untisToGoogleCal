# ClassCompass

![2025-05-17_19-54](https://github.com/user-attachments/assets/e3673d16-a7b0-4993-bd64-000b31d6c1d6)


This tool transfers your Untis timetable to a Google Calendar and can **notify you of important changes via Telegram**.

---

## 🚀 Features

- 🪞 **Live Schedule Sync:** Mirrors your Untis schedule in Google Calendar.
- ➕ **Additive Updates:** Previous calendar entries are preserved; nothing is deleted.
- 🖋️ **Configurable Entries:** Customize what info gets added to the calendar.
- 🔔 **Telegram Notifications:** Get real-time alerts for schedule changes, cancellations, and exams.
- 👥 **Calendar Sharing:** Share your school calendar with others via email.
- 🧹 **Flush Calendar:** Delete all events from your school calendar with a single command.
- 🛠️ **Admin CLI:** Interactive menu to run and configure all scripts with simulation and verbose modes.

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

| colorID | Name      | hexCode |
| ------- | --------- | ------- |
| 1       | Lavender  | #A4BDFC |
| 2       | Sage      | #7AE7BF |
| 3       | Grape     | #DBADFF |
| 4       | Flamingo  | #FF887C |
| 5       | Banana    | #FBD75B |
| 6       | Tangerine | #FFB878 |
| 7       | Peacock   | #46D6DB |
| 8       | Graphite  | #E1E1E1 |
| 9       | Blueberry | #5484ED |
| 10      | Basil     | #51B749 |
| 11      | Tomato    | #DC2127 |

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
4. **Edit your `environment.json`** (not versioned, see `.gitignore`):

   ```json
   {
     "calendarID": "YOUR_CALENDAR_ID",
     "cookie": "YOUR_SESSION_COOKIE",
     "anonymous-school": "YOUR_SCHOOL_ID",
     "telegramToken": "YOUR_BOT_TOKEN",
     "telegramChat": "YOUR_CHAT_ID"
   }
   ```

   - `calendarID`: Your Google Calendar ID (created or found by `showCalandars.py`)
   - `cookie`: Session cookie for Untis API access
   - `anonymous-school`: Your Untis school identifier
   - `telegramToken`: Telegram bot token
   - `telegramChat`: Telegram chat or channel ID

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

- [`adminCLI.py`](adminCLI.py): **Interactive Admin CLI** to run and configure all scripts with options.
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

## 🖥️ **Admin CLI (Recommended)**

The **Admin CLI** (`adminCLI.py`) is the recommended way to use and manage this project.  
It provides an interactive menu to:

- Select and run any script in the project.
- Toggle simulation and verbose modes.
- Set output files for script results.
- Change/remove options before running scripts.
- See which options are supported for each script.
- View help for each script.

### Start the Admin CLI

```sh
python adminCLI.py
```

**Navigation:**

- `↑/↓` : Navigate scripts or options
- `Enter` : Run selected script with chosen options
- `h` : Show help for selected script
- `p` : Change/remove options (simulation, verbose, output file, etc.)
- Option keys (e.g. `s`, `v`, `o`) : Toggle options directly
- `q` : Quit

**Example:**

- Toggle simulation mode (`s`) and verbose mode (`v`), then run the main sync script.
- Set an output file to save results.
- Only supported options for each script are enabled.

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
5. **Edit your `environment.json`** as described above.

---

## 🚀 Usage

### **Recommended: Use the Admin CLI**

```sh
python adminCLI.py
```

- Interactive menu for all scripts and options.
- See above for navigation and features.

---

### Individual Scripts

#### Show or Create a Calendar

```sh
python showCalandars.py
```

Finds or creates a calendar called "school" and outputs its URL.

#### Share a Calendar

```sh
python shareCalendar.py
```

Shares the specified calendar with an email and generates/updates `environment.json`.

#### Flush (Delete All Events) from Calendar

```sh
python flush_calendar.py
```

Deletes all events from the configured calendar.

#### Run the Main Sync

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

[MIT License](https://opensource.org/licenses/MIT)
