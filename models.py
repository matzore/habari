from __future__ import annotations

from pydantic import BaseModel, Field
from rich import print

from metadata_utils import MetadataUtils


class SongMetadata(BaseModel):
    artist: str | None = Field(..., alias='Artist')
    album: str | None = Field(..., alias='Album')
    title: str | None = Field(..., alias='Title')
    filepath: str | None = Field(..., alias='Path')
    duration: str | None = Field(..., alias='Duration')
    zone: str | None = Field(..., alias='Zone')
    genre: str | None = None
    release_date: str | None = None
    mbid: str | None = None
    metadata_url: str | None = None
    image_url: str | None = None

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
