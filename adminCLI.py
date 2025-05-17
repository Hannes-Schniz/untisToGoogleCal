import subprocess
import sys
import termios
import tty
import os

def get_key():
    """
    Reads a single keypress from stdin and returns it.
    Supports arrow keys and single characters.
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch1 = sys.stdin.read(1)
        if ch1 == '\x1b':  # Arrow keys start with ESC
            ch2 = sys.stdin.read(1)
            if ch2 == '[':
                ch3 = sys.stdin.read(1)
                return ch1 + ch2 + ch3
        return ch1
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# Define all option metadata in a single structure for easy editing
OPTIONS_META = [
    {
        "name": "simulate",
        "label": "Simulation mode",
        "type": "bool",
        "key": "s",
        "legend": "Toggle simulation mode",
        "default": False,
        "supported_scripts": ["flush_calendar.py", "runner.py"]
    },
    {
        "name": "verbose",
        "label": "Verbose mode",
        "type": "bool",
        "key": "v",
        "legend": "Toggle verbose mode",
        "default": False,
        "supported_scripts": None  # Supported by all
    },
    {
        "name": "output_file",
        "label": "Output file",
        "type": "str",
        "key": "o",
        "legend": "Set output file for script output",
        "default": None,
        "supported_scripts": None
    }
]

def print_legend():
    print("Legend:")
    print("  ↑/↓ : Navigate scripts")
    print("  Enter : Run selected script with chosen options")
    print("  h : Show help for selected script")
    for opt in OPTIONS_META:
        print(f"  {opt['key']} : {opt['legend']}")
    print("  p : Change/remove options")
    print("  q : Quit\n")

def options_menu(options_state):
    """
    Allows the user to change/remove options before running the script.
    Navigation: ↑/↓ to select, c to change/toggle, d to delete (for output file), q to quit options menu.
    """
    selected = 0
    while True:
        clear_screen()
        print("Options Menu (↑/↓: navigate, c: change/toggle, d: delete, q: back):\n")
        for idx, opt in enumerate(OPTIONS_META):
            prefix = "👉 " if idx == selected else "   "
            val = options_state[opt['name']]
            if opt["type"] == "bool":
                val_str = "ON" if val else "OFF"
            else:
                val_str = val if val else "None"
            print(f"{prefix}{opt['label']}: {val_str}")
        key = get_key()
        if key == '\x1b[A':  # Up arrow
            selected = (selected - 1) % len(OPTIONS_META)
        elif key == '\x1b[B':  # Down arrow
            selected = (selected + 1) % len(OPTIONS_META)
        elif key.lower() == 'q':
            break
        elif key.lower() == 'c':
            opt = OPTIONS_META[selected]
            if opt["type"] == "bool":
                options_state[opt["name"]] = not options_state[opt["name"]]
            else:
                val = input(f"Enter value for {opt['label']} (leave empty to disable): ").strip()
                options_state[opt["name"]] = val if val else None
        elif key.lower() == 'd':
            opt = OPTIONS_META[selected]
            if opt["type"] == "str":
                options_state[opt["name"]] = None
        # Ignore other keys
    return options_state

def main():
    scripts = [
        {
            "name": "Share Google Calendar",
            "file": "shareCalendar.py",
            "description": "Share your Google Calendar with an email and update environment.json."
        },
        {
            "name": "Show or Create School Calendar",
            "file": "showCalandars.py",
            "description": "Find or create the 'school' calendar and output its URL."
        },
        {
            "name": "Flush Calendar",
            "file": "flush_calendar.py",
            "description": "Delete all events from the configured calendar. Supports simulation mode (--simulate)."
        },
        {
            "name": "Run Main Sync",
            "file": "runner.py",
            "description": "Sync Untis timetable to Google Calendar and send Telegram notifications. Supports simulation mode (--simulate)"
        }
    ]

    # Initialize options state from meta
    options_state = {opt['name']: opt['default'] for opt in OPTIONS_META}

    selected = 0

    while True:
        clear_screen()
        print("Use ↑/↓ to navigate, Enter to run, h for help, p to change/remove options, q to quit.\n")
        print_legend()
        for idx, script in enumerate(scripts):
            prefix = "👉 " if idx == selected else "   "
            print(f"{prefix}{script['name']}\n      {script['description']}\n")
        # Show chosen options at the bottom
        chosen_opts = []
        for opt in OPTIONS_META:
            val = options_state[opt['name']]
            if opt['type'] == 'bool' and val:
                chosen_opts.append(f"--{opt['name']}")
            elif opt['type'] == 'str' and val:
                chosen_opts.append(f"{opt['label']}: {val}")
        print("\nChosen options: " + (" ".join(chosen_opts) if chosen_opts else "None"))
        key = get_key()
        if key == '\x1b[A':  # Up arrow
            selected = (selected - 1) % len(scripts)
        elif key == '\x1b[B':  # Down arrow
            selected = (selected + 1) % len(scripts)
        elif key.lower() == 'q':
            print("Exiting.")
            break
        elif key.lower() == 'h':
            clear_screen()
            script_file = scripts[selected]["file"]
            print(f"Help for {scripts[selected]['name']} (from `{script_file} -h`):\n")
            try:
                result = subprocess.run(
                    ["python3", script_file, "-h"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    timeout=10
                )
                print(result.stdout)
            except Exception as e:
                print(f"Could not get help output: {e}")
            input("\nPress Enter to return to menu...")
        elif key.lower() == 'p':
            options_state = options_menu(options_state)
        else:
            # Handle option keys
            for opt in OPTIONS_META:
                if key.lower() == opt['key']:
                    # Only toggle if supported for this script
                    
                    if opt['type'] == 'bool':
                        options_state[opt['name']] = not options_state[opt['name']]
                    elif opt['type'] == 'str':
                        val = input(f"Enter value for {opt['label']} (leave empty to disable): ").strip()
                        options_state[opt['name']] = val if val else None
                    
        if key == '\r' or key == '\n':  # Enter
            # Check if any selected options are not supported by the script
            script_file = scripts[selected]["file"]
            unsupported = [
                opt for opt in OPTIONS_META
                if (
                    opt['type'] == 'bool' and options_state[opt['name']] and
                    opt['supported_scripts'] is not None and script_file not in opt['supported_scripts']
                )
            ]
            if unsupported:
                clear_screen()
                print("The following options are not supported for this script:")
                for opt in unsupported:
                    print(f"  --{opt['name']}")
                input("\nPress Enter to return to menu...")
                continue

            clear_screen()
            cmd = ["python3", script_file]
            # Add options as CLI args
            for opt in OPTIONS_META:
                val = options_state[opt['name']]
                if opt['type'] == 'bool' and val:
                    cmd.append(f"--{opt['name']}")
                elif opt['type'] == 'str' and val:
                    # Output file is handled separately
                    pass
            print(f"Running {script_file} with options: {' '.join(cmd[2:])}\n")
            output_file = options_state.get("output_file")
            if output_file:
                with open(output_file, "w") as f:
                    process = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT)
                    process.communicate()
                print(f"\nOutput written to {output_file}")
            else:
                subprocess.run(cmd)
            input("\nPress Enter to return to menu...")

if __name__ == "__main__":
    main()