from __future__ import annotations

from typing import Union

from pydantic import BaseModel, Field
from rich import print

from metadata_utils import MetadataUtils


class SongMetadata(BaseModel):
    artist: Union[str, None] = Field(..., alias='Artist')
    album: Union[str, None] = Field(..., alias='Album')
    title: Union[str, None] = Field(..., alias='Title')
    filepath: Union[str, None] = Field(..., alias='Path')
    duration: Union[str, None] = Field(..., alias='Duration')
    zone: Union[str, None] = Field(..., alias='Zone')
    genre: Union[str, None] = None
    release_date: Union[str, None] = None
    mbid: Union[str, None] = None
    metadata_url: Union[str, None] = None
    image_url: Union[str, None] = None

    def model_post_init(self, __context) -> None:
        MetadataUtils(self)

    class Config:
        collection = 'now_playing'


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
