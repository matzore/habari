from __future__ import annotations

import sys
import traceback
from time import sleep
from rich import print
import requests

from backend import Backend
from models import SongMetadata

print("Starting collector")
while True:
    try:
        response = requests.get('http://localhost:9670')
        if response.status_code == 200:
            data = response.json()
            if "current_song" in data:
                current_song = data["current_song"]
                backend = Backend()
                song_metadata = SongMetadata(**current_song)
                backend.push(song_metadata)
                print("Pushed song to backend")
                print(song_metadata)

                sleep_for = int(current_song["Duration"]) - int(current_song["Elapsed"]) + 1
                sleep(sleep_for)
            else:
                sleep(5)
    except Exception as e:
        traceback.print_exc()

        sleep(5)
