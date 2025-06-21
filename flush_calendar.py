import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_cal_connector import googleCalCon
import sys

# Path to your credentials.json and environment.json files
SERVICE_ACCOUNT_FILE = 'credentials.json'
ENVIRONMENT_FILE = 'environment.json'

# Scopes (permissions) required for accessing the calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

HELP_TEXT = """
Deletes all events from the configured school calendar.

Usage:
  python flush_calendar.py [--simulate]

Options:
  -h, --help      Show this help message and exit
  --simulate      Show what would be deleted, but do not actually delete anything

This script will remove all events from the calendar specified in environment.json.
You will be prompted for confirmation before deletion.
"""

def delete_all_calendar_events(simulate=False, verbose=False):
    """Deletes all events from the specified calendar, or simulates deletion if simulate=True."""
    try:
        
        google = googleCalCon(weeks=-1, simulate=simulate, verbose=verbose)

        google.removeEvents()

    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(HELP_TEXT)
        sys.exit(0)

    simulate = "--simulate" in sys.argv
    
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    
    yes = "-y" in sys.argv

    try:
        with open(ENVIRONMENT_FILE, 'r') as f:
            env = json.load(f)
            calendar_id_to_clear = env['calendarID']

        if simulate:
            print("Simulation mode enabled. No events will be deleted.\n")
            delete_all_calendar_events(simulate=simulate, verbose=verbose)
        else:
            confirmation = True
            if not yes:
                confirmation = input(f"Are you sure you want to delete ALL events from calendar {calendar_id_to_clear}? (yes/no): ")
            if confirmation.lower() == 'yes':
                delete_all_calendar_events(verbose=verbose)
            else:
                print("Deletion cancelled.")

    except FileNotFoundError:
        print(f"Error: {ENVIRONMENT_FILE} not found.")
    except KeyError:
        print(f"Error: 'calendarID' not found in {ENVIRONMENT_FILE}.")
    except json.JSONDecodeError:
        print(f"Error: {ENVIRONMENT_FILE} is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")