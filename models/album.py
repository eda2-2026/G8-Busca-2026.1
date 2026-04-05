"""
Modelo de Álbum para o sistema MusicDB.
"""

from dataclasses import dataclass, field


@dataclass
class Album:
    """
    Representa um álbum no sistema.

    Attributes:
        album_id     : Identificador único do álbum.
        title        : Título do álbum.
        artist_id    : ID do artista/banda responsável.
        release_year : Ano de lançamento.
        genre        : Gênero musical principal.
        song_ids     : Lista ordenada de IDs das músicas do álbum.
        rating       : Nota média do álbum (0.0 a 10.0).
    """

    album_id: int
    title: str
    artist_id: int
    release_year: int
    genre: str
    song_ids: list[int] = field(default_factory=list)
    rating: float = 0.0

    def num_tracks(self) -> int:
        """Retorna a quantidade de faixas do álbum."""
        return len(self.song_ids)

    def __repr__(self) -> str:
        return (
            f"Album(id={self.album_id}, title='{self.title}', "
            f"artist_id={self.artist_id}, year={self.release_year}, "
            f"tracks={self.num_tracks()}, rating={self.rating})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Album):
            return NotImplemented
        return self.album_id == other.album_id

    def __lt__(self, other: "Album") -> bool:
        """Permite comparação e ordenação pelo título."""
        return self.title.lower() < other.title.lower()

    def to_dict(self) -> dict:
        return {
            "album_id": self.album_id,
            "title": self.title,
            "artist_id": self.artist_id,
            "release_year": self.release_year,
            "genre": self.genre,
            "song_ids": self.song_ids,
            "rating": self.rating,
        }
