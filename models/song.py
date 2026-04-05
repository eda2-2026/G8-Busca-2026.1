"""
Modelo de Música para o sistema MusicDB.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Song:
    """
    Representa uma música no sistema.

    Attributes:
        song_id       : Identificador único da música.
        title         : Título da música.
        artist_id     : ID do artista/banda principal.
        album_id      : ID do álbum ao qual pertence (pode ser None).
        duration_sec  : Duração em segundos.
        release_year  : Ano de lançamento.
        genre         : Gênero musical.
        plays         : Número de reproduções.
        feat_ids      : Lista de IDs dos artistas participantes (feats).
    """

    song_id: int
    title: str
    artist_id: int
    album_id: Optional[int]
    duration_sec: int
    release_year: int
    genre: str
    plays: int = 0
    feat_ids: list[int] = field(default_factory=list)

    @property
    def duration_fmt(self) -> str:
        """Retorna duração no formato mm:ss."""
        minutes, seconds = divmod(self.duration_sec, 60)
        return f"{minutes}:{seconds:02d}"

    def has_feat(self) -> bool:
        """Retorna True se a música possui artistas participantes."""
        return len(self.feat_ids) > 0

    def __repr__(self) -> str:
        feat_info = f", feats={self.feat_ids}" if self.has_feat() else ""
        return (
            f"Song(id={self.song_id}, title='{self.title}', "
            f"artist_id={self.artist_id}, year={self.release_year}, "
            f"plays={self.plays}{feat_info})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Song):
            return NotImplemented
        return self.song_id == other.song_id

    def __lt__(self, other: "Song") -> bool:
        """Permite comparação e ordenação pelo título."""
        return self.title.lower() < other.title.lower()

    def to_dict(self) -> dict:
        return {
            "song_id": self.song_id,
            "title": self.title,
            "artist_id": self.artist_id,
            "album_id": self.album_id,
            "duration_sec": self.duration_sec,
            "release_year": self.release_year,
            "genre": self.genre,
            "plays": self.plays,
            "feat_ids": self.feat_ids,
        }
