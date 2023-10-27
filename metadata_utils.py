import os
import time
from typing import TYPE_CHECKING

import requests
from mutagen.flac import FLAC
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from rich import print

if TYPE_CHECKING:
    from models import SongMetadata


def safe_get(dictionary, key):
    # return the string representation, because sometimes the value is an object, rather than the required
    # string
    if key in dictionary:
        val = dictionary[key]
        return str(val) if not isinstance(val, list) else val
    else:
        return ''


def format_duration(track_length):
    duration_format = "%M:%S" if track_length < 3600 else "%H:%M:%S"
    return time.strftime(duration_format, time.gmtime(track_length))


def squeeze(list_or_str):
    if isinstance(list_or_str, list):
        return ", ".join(str(x) for x in list_or_str)
    elif isinstance(list_or_str, str):
        return list_or_str
    else:
        return ''


mb_url = 'https://musicbrainz.org/release/{0}'
cover_url = "https://coverartarchive.org/release/{0}"


class MetadataUtils:
    def __init__(self, song: "SongMetadata"):
        self.song = song

        file_extension = os.path.splitext(self.song.filepath)[-1]

        if not os.path.exists(self.song.filepath) or file_extension not in ['.mp3', '.flac', '.ogg']:
            return
        elif file_extension == '.mp3':
            self._parse_mp3()
        elif file_extension in ['.flac', '.ogg']:
            self._parse_vorbis()
        else:
            assert False

    def _parse_mp3(self):
        id3_metadata = ID3(self.song.filepath)
        print(id3_metadata)

        self.song.album = safe_get(id3_metadata, 'TALB')
        self.song.title = safe_get(id3_metadata, 'TIT2')
        self.song.duration = format_duration(MP3(self.song.filepath).info.length)
        self.song.artist = safe_get(id3_metadata, 'TPE1')
        self.song.genre = safe_get(id3_metadata, 'TCON')
        self.song.release_date = safe_get(id3_metadata, 'TDOR')
        self.song.mbid = safe_get(id3_metadata, 'TXXX:MusicBrainz Album Id')
        self.song.metadata_url = mb_url.format(self.song.mbid)
        self.song.image_url = self._get_image_url()

    def _parse_vorbis(self):
        file_extension = os.path.splitext(self.song.filepath)[-1]
        vorbis_metadata = FLAC(self.song.filepath) if file_extension == '.flac' else OggVorbis(self.song.filepath)
        self.song.album = squeeze(safe_get(vorbis_metadata, 'album'))
        self.song.title = squeeze(safe_get(vorbis_metadata, 'title'))
        self.song.duration = format_duration(vorbis_metadata.info.length)
        self.song.artist = squeeze(safe_get(vorbis_metadata, 'artist'))
        self.song.genre = squeeze(safe_get(vorbis_metadata, 'genre'))
        self.song.release_date = squeeze(safe_get(vorbis_metadata, 'date'))
        self.song.mbid = squeeze(safe_get(vorbis_metadata, 'musicbrainz_albumid'))
        self.song.metadata_url = mb_url.format(self.song.mbid)
        self.song.image_url = self._get_image_url()

    def _get_image_url(self):
        response = requests.get(cover_url.format(self.song.mbid))
        if response.status_code == 200:
            try:
                return response.json()['images'][0]['thumbnails']['large']
            except KeyError | IndexError:
                pass
            try:
                return response.json()['images'][0]['thumbnails']['small']
            except KeyError | IndexError:
                pass
            try:
                return response.json()['images'][0]['image']
            except KeyError | IndexError:
                pass
        return None
