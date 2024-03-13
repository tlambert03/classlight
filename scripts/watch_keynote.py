from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from contextlib import suppress
from datetime import datetime
from typing import TYPE_CHECKING
from urllib.request import Request, urlopen

if TYPE_CHECKING:
    from typing import TypedDict, Unpack

    class Row(TypedDict, total=False):
        slide_num: int | str
        timestamp: str | None
        program: str | None
        presentation: str | None


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
    "connection": "keep-alive",
    "user-agent": "python-httpx/0.25.2",
}
REQ = Request(REST_URL, headers=HEADERS, method="POST")


def log_slide_number(**body: Unpack[Row]) -> None:
    """Save the slide number and timestamp to the database."""
    try:
        with urlopen(REQ, json.dumps(body).encode("utf-8")) as response:
            if response.status == 201:
                print(f"Logged slide number: {body.get('slide_num')}")
    except Exception as e:
        print(f"Error logging slide number: {e}")


def watch_keynote(name: str | None = None) -> None:
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
            for line in proc.stdout or []:
                with suppress(Exception):
                    data = json.loads(line)
                    if match := SLIDE_RE.search(data.get("eventMessage", "")):
                        log_slide_number(
                            slide_num=match.group(1),
                            timestamp=data["timestamp"],
                            presentation=name,
                            program="Keynote",
                        )
        except KeyboardInterrupt:
            return


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Watch Keynote and log slide number to Supabase"
    )
    parser.add_argument(
        "name", nargs="?", help="Name of the presentation.", default=None
    )
    parser.add_argument("--test", action="store_true", help="Send single test log")
    args = parser.parse_args()

    if args.test:
        stamp = datetime.now().isoformat()
        log_slide_number(
            slide_num=9999, timestamp=stamp, program="__test__", presentation=args.name
        )
        sys.exit(0)

    watch_keynote(args.name)
