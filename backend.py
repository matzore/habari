import os

from DirectusPyWrapper import Directus
from dotenv import load_dotenv

from models import SongMetadata

load_dotenv()
url = os.getenv('DIRECTUS_URL')
token = os.getenv('DIRECTUS_TOKEN')


class Backend:
    def __init__(self):
        self.directus = Directus(url=url, token=token)

    def push(self, song_metadata: SongMetadata):
        self.directus.collection(SongMetadata).update_one(None, song_metadata.model_dump())


if __name__ == '__main__':
    current = {
        "Artist": "Dave Matthews Band",
        "Album": "Before These Crowded Streets",
        "Title": "Crush",
        "Path": "08 Crush.mp3",
        "Duration": "489",
        "Elapsed": "167",
        "Zone": "Alternative"
    }
    song = SongMetadata(**current)
    print(song.model_dump())
    backend = Backend()
    backend.push(song)
