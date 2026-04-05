"""
Dados de exemplo para popular o MusicCatalog.

Execute este módulo diretamente para verificar a integridade dos dados:
    python data/seed.py
"""

from models.artist import Artist
from models.song import Song
from models.album import Album
from music_catalog import MusicCatalog


# =============================================================================
# ARTISTAS
# =============================================================================
ARTISTS: list[Artist] = [
    # ── Internacionais ────────────────────────────────────────────────────────
    Artist(1,  "The Beatles",        "Rock",          "Reino Unido",  1960, is_band=True,
           members=["John Lennon", "Paul McCartney", "George Harrison", "Ringo Starr"]),
    Artist(2,  "Michael Jackson",    "Pop",           "Estados Unidos", 1964),
    Artist(3,  "Queen",              "Rock",          "Reino Unido",  1970, is_band=True,
           members=["Freddie Mercury", "Brian May", "Roger Taylor", "John Deacon"]),
    Artist(4,  "Beyoncé",            "Pop/R&B",       "Estados Unidos", 1997),
    Artist(5,  "Kendrick Lamar",     "Hip-Hop",       "Estados Unidos", 2003),
    Artist(6,  "Taylor Swift",       "Pop/Country",   "Estados Unidos", 2004),
    Artist(7,  "Daft Punk",          "Electronic",    "França",       1993, is_band=True,
           members=["Thomas Bangalter", "Guy-Manuel de Homem-Christo"]),
    Artist(8,  "Radiohead",          "Alternative",   "Reino Unido",  1985, is_band=True,
           members=["Thom Yorke", "Jonny Greenwood", "Ed O'Brien", "Colin Greenwood", "Philip Selway"]),
    Artist(9,  "Jay-Z",              "Hip-Hop",       "Estados Unidos", 1986),
    Artist(10, "Pharrell Williams",  "Pop/R&B",       "Estados Unidos", 1992),

    # ── Nacionais (Brasil) ────────────────────────────────────────────────────
    Artist(11, "Caetano Veloso",     "MPB",           "Brasil",       1965),
    Artist(12, "Djavan",             "MPB/Jazz",      "Brasil",       1972),
    Artist(13, "Gilberto Gil",       "MPB/Reggae",    "Brasil",       1962),
    Artist(14, "Emicida",            "Hip-Hop",       "Brasil",       2003),
    Artist(15, "Anitta",             "Pop/Funk",      "Brasil",       2010),
    Artist(16, "Criolo",             "Hip-Hop/MPB",   "Brasil",       2006),
    Artist(17, "Ludmilla",           "Funk/Pop",      "Brasil",       2012),
    Artist(18, "Seu Jorge",          "Samba/MPB",     "Brasil",       1998),
    Artist(19, "Projota",            "Hip-Hop",       "Brasil",       2006),
    Artist(20, "Liniker",            "Soul/MPB",      "Brasil",       2015),
]

# =============================================================================
# ÁLBUNS
# =============================================================================
ALBUMS: list[Album] = [
    Album(1,  "Abbey Road",                1,  1969, "Rock",        song_ids=[1,2,3],      rating=9.8),
    Album(2,  "Thriller",                  2,  1982, "Pop",         song_ids=[4,5,6],      rating=9.5),
    Album(3,  "A Night at the Opera",      3,  1975, "Rock",        song_ids=[7,8],        rating=9.4),
    Album(4,  "Lemonade",                  4,  2016, "Pop/R&B",     song_ids=[9,10],       rating=9.2),
    Album(5,  "To Pimp a Butterfly",       5,  2015, "Hip-Hop",     song_ids=[11,12,13],   rating=9.7),
    Album(6,  "1989",                      6,  2014, "Pop",         song_ids=[14,15],      rating=8.8),
    Album(7,  "Random Access Memories",    7,  2013, "Electronic",  song_ids=[16,17],      rating=9.1),
    Album(8,  "OK Computer",               8,  1997, "Alternative", song_ids=[18,19],      rating=9.6),
    Album(9,  "The Blueprint",             9,  2001, "Hip-Hop",     song_ids=[20,21],      rating=9.0),
    Album(10, "Transa",                    11, 1972, "MPB",         song_ids=[22,23],      rating=9.3),
    Album(11, "Luz",                       12, 1982, "MPB/Jazz",    song_ids=[24,25],      rating=9.1),
    Album(12, "Quanta",                    13, 1997, "MPB/Reggae",  song_ids=[26,27],      rating=8.9),
    Album(13, "Sobre Crianças, Quadris...",14, 2015, "Hip-Hop",     song_ids=[28,29,30],   rating=9.4),
    Album(14, "Versions of Me",            15, 2022, "Pop/Funk",    song_ids=[31,32],      rating=8.5),
    Album(15, "Nó na Orelha",              16, 2011, "Hip-Hop/MPB", song_ids=[33,34],      rating=9.6),
]

# =============================================================================
# MÚSICAS
# =============================================================================
SONGS: list[Song] = [
    # Abbey Road
    Song(1,  "Come Together",          1,  1, 259, 1969, "Rock",        plays=980_000_000),
    Song(2,  "Something",              1,  1, 182, 1969, "Rock",        plays=850_000_000),
    Song(3,  "Here Comes the Sun",     1,  1, 185, 1969, "Rock",        plays=1_100_000_000),

    # Thriller
    Song(4,  "Billie Jean",            2,  2, 294, 1982, "Pop",         plays=1_300_000_000),
    Song(5,  "Thriller",               2,  2, 358, 1982, "Pop",         plays=1_050_000_000),
    Song(6,  "Beat It",                2,  2, 258, 1982, "Pop",         plays=920_000_000),

    # A Night at the Opera
    Song(7,  "Bohemian Rhapsody",      3,  3, 354, 1975, "Rock",        plays=1_600_000_000),
    Song(8,  "Love of My Life",        3,  3, 211, 1975, "Rock",        plays=700_000_000),

    # Lemonade
    Song(9,  "Formation",              4,  4, 213, 2016, "Pop/R&B",     plays=430_000_000),
    Song(10, "Hold Up",                4,  4, 215, 2016, "Pop/R&B",     plays=380_000_000),

    # To Pimp a Butterfly
    Song(11, "Alright",                5,  5, 219, 2015, "Hip-Hop",     plays=360_000_000),
    Song(12, "King Kunta",             5,  5, 234, 2015, "Hip-Hop",     plays=290_000_000),
    Song(13, "These Walls",            5,  5, 290, 2015, "Hip-Hop",     plays=220_000_000,
         feat_ids=[10]),  # feat Pharrell

    # 1989
    Song(14, "Shake It Off",           6,  6, 219, 2014, "Pop",         plays=1_050_000_000),
    Song(15, "Blank Space",            6,  6, 231, 2014, "Pop",         plays=980_000_000),

    # Random Access Memories
    Song(16, "Get Lucky",              7,  7, 369, 2013, "Electronic",  plays=1_200_000_000,
         feat_ids=[10]),  # feat Pharrell
    Song(17, "Instant Crush",          7,  7, 337, 2013, "Electronic",  plays=450_000_000),

    # OK Computer
    Song(18, "Karma Police",           8,  8, 263, 1997, "Alternative", plays=560_000_000),
    Song(19, "Paranoid Android",       8,  8, 383, 1997, "Alternative", plays=480_000_000),

    # The Blueprint
    Song(20, "Izzo (H.O.V.A.)",        9,  9, 228, 2001, "Hip-Hop",     plays=310_000_000),
    Song(21, "Song Cry",               9,  9, 261, 2001, "Hip-Hop",     plays=200_000_000),

    # Transa
    Song(22, "Triste Bahia",           11, 10, 195, 1972, "MPB",        plays=45_000_000),
    Song(23, "Mora na Filosofia",       11, 10, 188, 1972, "MPB",        plays=38_000_000),

    # Luz
    Song(24, "Flor de Lis",            12, 11, 244, 1982, "MPB/Jazz",   plays=62_000_000),
    Song(25, "Oceano",                 12, 11, 258, 1982, "MPB/Jazz",   plays=88_000_000),

    # Quanta
    Song(26, "Drão",                   13, 12, 232, 1997, "MPB/Reggae", plays=40_000_000),
    Song(27, "Happiness",              13, 12, 210, 1997, "MPB/Reggae", plays=33_000_000),

    # Sobre Crianças, Quadris...
    Song(28, "AmarElo",                14, 13, 267, 2015, "Hip-Hop",    plays=55_000_000,
         feat_ids=[16]),  # feat Criolo
    Song(29, "Boa Esperança",          14, 13, 244, 2015, "Hip-Hop",    plays=48_000_000),
    Song(30, "Mandume",                14, 13, 231, 2015, "Hip-Hop",    plays=38_000_000,
         feat_ids=[16, 19]),  # feat Criolo + Projota

    # Versions of Me
    Song(31, "Envolver",               15, 14, 193, 2022, "Pop/Funk",   plays=320_000_000),
    Song(32, "Gata",                   15, 14, 185, 2022, "Pop/Funk",   plays=180_000_000,
         feat_ids=[17]),  # feat Ludmilla

    # Nó na Orelha
    Song(33, "Subirusdoistiozinhos",   16, 15, 209, 2011, "Hip-Hop/MPB", plays=72_000_000),
    Song(34, "Ainda Há Tempo",         16, 15, 255, 2011, "Hip-Hop/MPB", plays=59_000_000,
         feat_ids=[20]),  # feat Liniker

    # Singles / sem álbum
    Song(35, "Umbrella",               4,  None, 275, 2007, "Pop",       plays=870_000_000),
    Song(36, "HUMBLE.",                5,  None, 177, 2017, "Hip-Hop",   plays=820_000_000),
    Song(37, "Crazy in Love",          4,  None, 236, 2003, "Pop/R&B",   plays=750_000_000,
         feat_ids=[9]),  # feat Jay-Z
    Song(38, "Empire State of Mind",   9,  None, 274, 2009, "Hip-Hop",   plays=540_000_000,
         feat_ids=[4]),  # feat Alicia Keys — usando Beyoncé como proxy
    Song(39, "Baile de Favela",        14, None, 215, 2016, "Hip-Hop",   plays=210_000_000,
         feat_ids=[15]),  # Emicida feat Anitta
    Song(40, "Dona",                   18, None, 198, 2004, "Samba/MPB", plays=30_000_000,
         feat_ids=[11]),  # Seu Jorge feat Caetano
]


# =============================================================================
# Função de montagem
# =============================================================================

def build_catalog() -> MusicCatalog:
    """Instancia e popula o MusicCatalog com todos os dados de exemplo."""
    catalog = MusicCatalog()
    for artist in ARTISTS:
        catalog.add_artist(artist)
    for album in ALBUMS:
        catalog.add_album(album)
    for song in SONGS:
        catalog.add_song(song)
    return catalog


# =============================================================================
# Verificação rápida
# =============================================================================

if __name__ == "__main__":
    catalog = build_catalog()
    print(catalog)
    print("\n=== Estatísticas ===")
    for k, v in catalog.stats().items():
        print(f"  {k}: {v}")

    print("\n=== Top 5 músicas mais tocadas ===")
    for song in catalog.songs_by_plays[:5]:
        artist = catalog.get_artist(song.artist_id)
        print(f"  {song.title} — {artist.name}  ({song.plays:,} plays)")
