"""
Gerador de dados sintéticos para benchmark — MusicDB
=====================================================

Gera um MusicCatalog com n músicas, artistas e álbuns de forma
totalmente aleatória, mantendo a mesma estrutura do catálogo real.

Uso básico
----------
    from data.generator import generate_catalog
    catalog = generate_catalog(n_songs=10_000)

Uso no benchmark
----------------
    from data.generator import generate_catalog
    from search_algorithms import benchmark
    benchmark(generate_catalog(n_songs=10_000))
"""

import random
import string

from models.artist import Artist
from models.song import Song
from models.album import Album
from music_catalog import MusicCatalog


# =============================================================================
# Vocabulário para geração de nomes aleatórios
# =============================================================================

_WORD_PARTS = [
    "dark", "light", "fire", "storm", "echo", "night", "solar", "lunar",
    "iron", "crystal", "silver", "golden", "broken", "frozen", "silent",
    "royal", "electric", "hollow", "wild", "neon", "ancient", "rising",
    "lost", "burning", "velvet", "black", "white", "blue", "red", "deep",
    "stone", "wave", "ocean", "cloud", "thunder", "shadow", "ghost",
    "ember", "fever", "dream", "acid", "steel", "violet", "bitter", "sweet",
]

_NOUNS = [
    "road", "sky", "heart", "mind", "soul", "star", "rain", "king", "queen",
    "blade", "river", "mountain", "desert", "city", "ocean", "mirror",
    "flame", "wolf", "lion", "raven", "phoenix", "angel", "demon", "ghost",
    "clock", "garden", "bridge", "tower", "door", "window", "night", "day",
    "world", "earth", "sun", "moon", "wind", "tide", "blood", "bone",
]

_GENRES = [
    "Rock", "Pop", "Hip-Hop", "MPB", "Jazz", "Electronic", "R&B",
    "Metal", "Indie", "Alternative", "Funk", "Soul", "Reggae", "Blues",
    "Country", "Classical", "Samba", "Forró", "Trap", "Lo-fi",
]

_COUNTRIES = [
    "Brasil", "Estados Unidos", "Reino Unido", "França", "Japão",
    "Alemanha", "Canadá", "Austrália", "Argentina", "México",
    "Colômbia", "Itália", "Espanha", "Portugal", "Coreia do Sul",
]


# =============================================================================
# Funções auxiliares de geração de nomes
# =============================================================================

def _random_title() -> str:
    """Gera um título de 2 a 4 palavras."""
    length = random.randint(2, 4)
    pool = _WORD_PARTS + _NOUNS
    words = random.sample(pool, length)
    return " ".join(w.capitalize() for w in words)


def _random_artist_name() -> str:
    """Gera um nome de artista ou banda."""
    patterns = [
        # "The + Noun"
        lambda: f"The {random.choice(_NOUNS).capitalize()}s",
        # "Adj + Noun"
        lambda: f"{random.choice(_WORD_PARTS).capitalize()} {random.choice(_NOUNS).capitalize()}",
        # nome simples
        lambda: random.choice(_WORD_PARTS).capitalize(),
        # duas palavras maiúsculas
        lambda: f"{random.choice(_WORD_PARTS).upper()} {random.choice(_NOUNS).upper()}",
    ]
    return random.choice(patterns)()


def _random_album_title() -> str:
    return _random_title()


# =============================================================================
# Gerador principal
# =============================================================================

def generate_catalog(
    n_songs: int = 1_000,
    n_artists: int | None = None,
    n_albums: int | None = None,
    seed: int | None = None,
) -> MusicCatalog:
    """
    Gera um MusicCatalog sintético com tamanho configurável.

    Parâmetros
    ----------
    n_songs   : número de músicas a gerar (padrão: 1.000)
    n_artists : número de artistas; se None, usa n_songs // 20
    n_albums  : número de álbuns;   se None, usa n_songs // 8
    seed      : semente para reprodutibilidade (None = aleatório)

    Retorno
    -------
    MusicCatalog populado e com todas as listas ordenadas prontas.

    Exemplos de escala
    ------------------
    Pequeno  :   1.000 músicas  →  generate_catalog(1_000)
    Médio    :  10.000 músicas  →  generate_catalog(10_000)
    Grande   : 100.000 músicas  →  generate_catalog(100_000)
    """
    if seed is not None:
        random.seed(seed)

    # Proporções automáticas
    if n_artists is None:
        n_artists = max(10, n_songs // 20)
    if n_albums is None:
        n_albums = max(5, n_songs // 8)

    # ------------------------------------------------------------------
    # 1. Artistas
    # ------------------------------------------------------------------
    artists: list[Artist] = []
    used_names: set[str] = set()
    for i in range(1, n_artists + 1):
        name = _random_artist_name()
        while name in used_names:
            name = _random_artist_name()
        used_names.add(name)

        is_band = random.random() < 0.4
        members = [_random_artist_name() for _ in range(random.randint(2, 5))] if is_band else []

        artists.append(Artist(
            artist_id=i,
            name=name,
            genre=random.choice(_GENRES),
            country=random.choice(_COUNTRIES),
            formed_year=random.randint(1960, 2023),
            is_band=is_band,
            members=members,
        ))

    artist_ids = list(range(1, n_artists + 1))

    # ------------------------------------------------------------------
    # 2. Álbuns
    # ------------------------------------------------------------------
    albums: list[Album] = []
    for j in range(1, n_albums + 1):
        albums.append(Album(
            album_id=j,
            title=_random_album_title(),
            artist_id=random.choice(artist_ids),
            release_year=random.randint(1960, 2024),
            genre=random.choice(_GENRES),
            song_ids=[],
            rating=round(random.uniform(4.0, 10.0), 1),
        ))

    album_ids = list(range(1, n_albums + 1))
    album_map = {a.album_id: a for a in albums}

    # ------------------------------------------------------------------
    # 3. Músicas
    # ------------------------------------------------------------------
    songs: list[Song] = []
    for k in range(1, n_songs + 1):
        artist_id = random.choice(artist_ids)

        feat_ids: list[int] = []
        if random.random() < 0.2:
            possible = [a for a in artist_ids if a != artist_id]
            feat_ids = random.sample(possible, k=min(random.randint(1, 2), len(possible)))

        album_id = random.choice(album_ids) if random.random() < 0.85 else None
        if album_id is not None:
            album_map[album_id].song_ids.append(k)

        songs.append(Song(
            song_id=k,
            title=_random_title(),
            artist_id=artist_id,
            album_id=album_id,
            duration_sec=random.randint(120, 420),
            release_year=random.randint(1960, 2024),
            genre=random.choice(_GENRES),
            plays=random.randint(1_000, 2_000_000_000),
            feat_ids=feat_ids,
        ))

    # ------------------------------------------------------------------
    # 4. Carga em lote — ordena tudo de uma vez só
    # ------------------------------------------------------------------
    catalog = MusicCatalog()
    catalog.bulk_load(artists=artists, albums=albums, songs=songs)
    return catalog


# =============================================================================
# Verificação rápida
# =============================================================================

if __name__ == "__main__":
    for size in [1_000, 10_000, 100_000]:
        cat = generate_catalog(n_songs=size, seed=42)
        print(f"n={size:>7,}  →  {cat}")
