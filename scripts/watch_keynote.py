from contextlib import suppress
import os
import subprocess
import sys
import supabase
import json
import re

ANON = os.getenv("VITE_SUPABASE_ANON_KEY", "") or os.getenv("SUPABASE_ANON_KEY", "")
if not ANON:
    raise ValueError("SUPABASE_ANON_KEY environment variable not set")

SB_URL = "https://zxfscexnhikqhyqtiifw.supabase.co"
SLIDE_RE = re.compile(r"\(slide:\s(\d+),")

try:
    db = supabase.create_client(SB_URL, ANON)
except Exception as e:
    print(f"Error connecting to Supabase: {e}")
    sys.exit(1)


def log_slide_number(slide_num: str, timestamp: str):
    """Save the slide number and timestamp to the database."""
    data = {"slide_num": slide_num, "timestamp": timestamp}
    db.table("keynote").insert(data).execute()


def watch_keynote():
    """Stream the logs from Keynote and log the slide number and timestamp."""
    if not sys.platform == "darwin":
        raise ValueError("This script is only for macOS")

    cmd = [
        "log",
        "stream",
        "--process",
        "Keynote",
        "--style",
        "ndjson",
        "--predicate",
        'composedMessage CONTAINS[cd] "KNPlaybackController p_presentPlaybackEvent" '
        'AND composedMessage CONTAINS[cd] "shouldAnimate: 0"',
    ]
    # run the command in a subprocess and call a function
    # whenever a new line is printed to the console
    print("Watching Keynote... Press Ctrl+C to stop.")
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True) as proc:
        try:
            for line in proc.stdout:
                with suppress(Exception):
                    data = json.loads(line)
                    if match := SLIDE_RE.search(data.get("eventMessage", "")):
                        slide_num = match.group(1)
                        log_slide_number(slide_num, data["timestamp"])
        except KeyboardInterrupt:
            return


if __name__ == "__main__":
    watch_keynote()
