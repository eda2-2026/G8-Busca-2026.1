"""
MusicDB — Ponto de entrada da aplicação.

Execute:
    python main.py

Demonstra como o catálogo é construído, como as listas ordenadas
são acessadas e como o módulo de busca deve ser utilizado.
"""

from data.seed import build_catalog
from algoritimos_busca import benchmark


def section(title: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main() -> None:
    # ------------------------------------------------------------------
    # 1. Montar o catálogo
    # ------------------------------------------------------------------
    catalog = build_catalog()
    print(catalog)

    # ------------------------------------------------------------------
    # 2. Estatísticas gerais
    # ------------------------------------------------------------------
    section("Estatísticas do Catálogo")
    stats = catalog.stats()
    print(f"  Artistas   : {stats['total_artists']}")
    print(f"  Álbuns     : {stats['total_albums']}")
    print(f"  Músicas    : {stats['total_songs']}")
    print(f"  Reproduções: {stats['total_plays']:,}")
    print(f"  Gêneros    : {', '.join(sorted(stats['genres']))}")

    # ------------------------------------------------------------------
    # 3. Listas ordenadas disponíveis para os algoritmos de busca
    # ------------------------------------------------------------------
    section("Listas ordenadas disponíveis")
    print(f"  catalog.artists_by_name   — {len(catalog.artists_by_name)} artistas (ordem alfabética)")
    print(f"  catalog.songs_by_title    — {len(catalog.songs_by_title)} músicas (ordem alfabética)")
    print(f"  catalog.songs_by_plays    — {len(catalog.songs_by_plays)} músicas (mais tocadas primeiro)")
    print(f"  catalog.songs_by_year     — {len(catalog.songs_by_year)} músicas (mais antigas primeiro)")
    print(f"  catalog.albums_by_title   — {len(catalog.albums_by_title)} álbuns (ordem alfabética)")
    print(f"  catalog.albums_by_rating  — {len(catalog.albums_by_rating)} álbuns (melhor nota primeiro)")

    # ------------------------------------------------------------------
    # 4. Visualizar as listas que serão usadas nas buscas
    # ------------------------------------------------------------------
    section("Artistas em ordem alfabética (para Busca Binária)")
    for i, artist in enumerate(catalog.artists_by_name):
        print(f"  [{i:02d}] {artist.name}")

    section("Músicas em ordem alfabética (para Busca Binária)")
    for i, song in enumerate(catalog.songs_by_title):
        artist = catalog.get_artist(song.artist_id)
        feat = ""
        if song.feat_ids:
            nomes = [catalog.get_artist(fid).name for fid in song.feat_ids if catalog.get_artist(fid)]
            feat = f"  feat: {', '.join(nomes)}"
        print(f"  [{i:02d}] {song.title} — {artist.name}{feat}")

    section("Músicas ordenadas por reproduções (para Interpolação)")
    plays_asc = list(reversed(catalog.songs_by_plays))
    for i, song in enumerate(plays_asc):
        print(f"  [{i:02d}] plays={song.plays:>14,}  {song.title}")

    # ------------------------------------------------------------------
    # 5. Consultas auxiliares úteis para exploração
    # ------------------------------------------------------------------
    section("Feats do artista Emicida (id=14)")
    partners = catalog.feat_partners(14)
    for p in partners:
        print(f"  {p.name}")

    section("Músicas do álbum 'To Pimp a Butterfly'")
    for song in catalog.songs_in_album(5):
        feat = ""
        if song.feat_ids:
            nomes = [catalog.get_artist(fid).name for fid in song.feat_ids if catalog.get_artist(fid)]
            feat = f"  feat: {', '.join(nomes)}"
        print(f"  {song.title} ({song.duration_fmt}){feat}")

    # ------------------------------------------------------------------
    # 6. Benchmark dos algoritmos
    # ------------------------------------------------------------------
    section("Benchmark dos Algoritmos de Busca")
    benchmark(catalog)

    print("\n")


if __name__ == "__main__":
    main()
