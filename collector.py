from __future__ import annotations

import traceback
from time import sleep

import requests

from backend import Backend
from models import SongMetadata

while True:
    try:
        response = requests.get('http://localhost:9670')
        if response.status_code == 200:
            data = response.json()
            if "current_song" in data:
                current_song = data["current_song"]
                backend = Backend()
                backend.push( SongMetadata(**current_song))
                sleep_for = current_song["Duration"] - current_song["Elapsed"] + 1
                sleep(sleep_for)
            else:
                sleep(5)
    except Exception as e:
        traceback.print_exc()
        sleep(5)
