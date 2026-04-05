"""
Modelo de Artista/Banda para o sistema MusicDB.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Artist:
    """
    Representa um artista ou banda no sistema.

    Attributes:
        artist_id   : Identificador único do artista.
        name        : Nome do artista ou banda.
        genre       : Gênero musical principal.
        country     : País de origem.
        formed_year : Ano de formação/início de carreira.
        is_band     : True se for banda; False se for artista solo.
        members     : Lista de nomes dos integrantes (apenas para bandas).
    """

    artist_id: int
    name: str
    genre: str
    country: str
    formed_year: int
    is_band: bool = False
    members: list[str] = field(default_factory=list)

    def __repr__(self) -> str:
        kind = "Banda" if self.is_band else "Artista"
        return (
            f"{kind}(id={self.artist_id}, name='{self.name}', "
            f"genre='{self.genre}', country='{self.country}', "
            f"formed={self.formed_year})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Artist):
            return NotImplemented
        return self.artist_id == other.artist_id

    def __lt__(self, other: "Artist") -> bool:
        """Permite comparação e ordenação pelo nome."""
        return self.name.lower() < other.name.lower()

    def to_dict(self) -> dict:
        return {
            "artist_id": self.artist_id,
            "name": self.name,
            "genre": self.genre,
            "country": self.country,
            "formed_year": self.formed_year,
            "is_band": self.is_band,
            "members": self.members,
        }
