import json
import os
import re
import subprocess
import sys
from contextlib import suppress
from urllib.request import Request, urlopen

ANON = os.getenv("VITE_SUPABASE_ANON_KEY", "") or os.getenv("SUPABASE_ANON_KEY", "")
if not ANON:
    raise ValueError("SUPABASE_ANON_KEY environment variable not set")

SB_URL = "https://zxfscexnhikqhyqtiifw.supabase.co"
REST_URL = f"{SB_URL}/rest/v1/keynote"
SLIDE_RE = re.compile(r"\(slide:\s(\d+),")
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ANON}",
    "Apikey": ANON,
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "connection": "keep-alive",
    "user-agent": "python-httpx/0.25.2",
}


def log_slide_number(slide_num: str, timestamp: str):
    """Save the slide number and timestamp to the database."""
    body = {"slide_num": str(slide_num), "timestamp": str(timestamp)}
    data_bytes = json.dumps(body).encode("utf-8")
    req = Request(REST_URL, headers=HEADERS, method="POST")
    req.add_header("Content-Length", str(len(data_bytes)))
    try:
        with urlopen(req, data_bytes) as response:
            if response.status == 201:
                print(f"Logged slide number: {slide_num}")
    except Exception as e:
        print(f"Error logging slide number: {e}")


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
