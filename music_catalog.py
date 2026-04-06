"""
Catálogo central do sistema MusicDB.

O MusicCatalog é o coração da aplicação: ele armazena todas as entidades
(artistas, álbuns, músicas) e expõe os dados de formas estruturadas para
que algoritmos de busca possam ser aplicados de maneira direta.

Estruturas disponíveis para algoritmos de busca
------------------------------------------------
  - artists_by_name     : lista de artistas ordenada pelo nome
  - songs_by_title      : lista de músicas ordenada pelo título
  - songs_by_plays      : lista de músicas ordenada pelo nº de reproduções (desc)
  - songs_by_year       : lista de músicas ordenada pelo ano de lançamento
  - albums_by_title     : lista de álbuns ordenada pelo título
  - albums_by_rating    : lista de álbuns ordenada pela nota (desc)
"""

from __future__ import annotations

from typing import Optional

from models.artist import Artist
from models.song import Song
from models.album import Album


class MusicCatalog:
    """
    Repositório central de dados musicais.

    Internamente mantém dicionários (hash maps) para O(1) no lookup por ID
    e listas ordenadas para uso direto nos algoritmos de busca.
    """

    # ------------------------------------------------------------------
    # Construção
    # ------------------------------------------------------------------

    def __init__(self) -> None:
        # ---- armazenamento primário (id → objeto) --------------------
        self._artists: dict[int, Artist] = {}
        self._songs: dict[int, Song] = {}
        self._albums: dict[int, Album] = {}

        # ---- listas pré-ordenadas (atualizadas ao adicionar/remover) --
        self.artists_by_name: list[Artist] = []
        self.songs_by_title: list[Song] = []
        self.songs_by_plays: list[Song] = []   # decrescente
        self.songs_by_year: list[Song] = []
        self.albums_by_title: list[Album] = []
        self.albums_by_rating: list[Album] = []  # decrescente

    # ------------------------------------------------------------------
    # Inserção
    # ------------------------------------------------------------------

    def add_artist(self, artist: Artist) -> None:
        """Adiciona um artista e recalcula as listas ordenadas."""
        if artist.artist_id in self._artists:
            raise ValueError(f"Artista com id={artist.artist_id} já existe.")
        self._artists[artist.artist_id] = artist
        self._rebuild_artist_lists()

    def add_song(self, song: Song) -> None:
        """Adiciona uma música e recalcula as listas ordenadas."""
        if song.song_id in self._songs:
            raise ValueError(f"Música com id={song.song_id} já existe.")
        self._songs[song.song_id] = song
        self._rebuild_song_lists()

    def add_album(self, album: Album) -> None:
        """Adiciona um álbum e recalcula as listas ordenadas."""
        if album.album_id in self._albums:
            raise ValueError(f"Álbum com id={album.album_id} já existe.")
        self._albums[album.album_id] = album
        self._rebuild_album_lists()

    def get_artist(self, artist_id: int) -> Optional[Artist]:
        return self._artists.get(artist_id)

    def get_song(self, song_id: int) -> Optional[Song]:
        return self._songs.get(song_id)

    def get_album(self, album_id: int) -> Optional[Album]:
        return self._albums.get(album_id)

    # ------------------------------------------------------------------
    # Consultas auxiliares
    # ------------------------------------------------------------------

    def songs_by_artist(self, artist_id: int) -> list[Song]:
        """Retorna todas as músicas de um artista (incluindo feats)."""
        return [
            s for s in self._songs.values()
            if s.artist_id == artist_id or artist_id in s.feat_ids
        ]

    def albums_by_artist(self, artist_id: int) -> list[Album]:
        """Retorna todos os álbuns de um artista."""
        return [a for a in self._albums.values() if a.artist_id == artist_id]

    def songs_in_album(self, album_id: int) -> list[Song]:
        """Retorna as músicas de um álbum na ordem das faixas."""
        album = self.get_album(album_id)
        if album is None:
            return []
        return [self._songs[sid] for sid in album.song_ids if sid in self._songs]

    def feat_partners(self, artist_id: int) -> list[Artist]:
        """Retorna todos os artistas com quem um dado artista fez feat."""
        partner_ids: set[int] = set()
        for song in self._songs.values():
            if song.artist_id == artist_id:
                partner_ids.update(song.feat_ids)
            elif artist_id in song.feat_ids:
                partner_ids.add(song.artist_id)
                partner_ids.update(song.feat_ids - {artist_id})
        return [self._artists[aid] for aid in partner_ids if aid in self._artists]

    # ------------------------------------------------------------------
    # Estatísticas simples
    # ------------------------------------------------------------------

    def stats(self) -> dict:
        return {
            "total_artists": len(self._artists),
            "total_albums": len(self._albums),
            "total_songs": len(self._songs),
            "total_plays": sum(s.plays for s in self._songs.values()),
            "genres": list({s.genre for s in self._songs.values()}),
        }

    # ------------------------------------------------------------------
    # Carga em lote  (muito mais rápido que N chamadas add_*)
    # ------------------------------------------------------------------

    def bulk_load(
        self,
        artists: list = (),
        albums: list = (),
        songs: list = (),
    ) -> None:
        """
        Insere múltiplos objetos de uma vez e reconstrói as listas
        ordenadas apenas UMA vez ao final — ideal para catálogos grandes.

        Parâmetros
        ----------
        artists : sequência de Artist
        albums  : sequência de Album
        songs   : sequência de Song
        """
        for artist in artists:
            self._artists[artist.artist_id] = artist
        for album in albums:
            self._albums[album.album_id] = album
        for song in songs:
            self._songs[song.song_id] = song

        self._rebuild_artist_lists()
        self._rebuild_album_lists()
        self._rebuild_song_lists()

    # ------------------------------------------------------------------
    # Reconstrução das listas ordenadas (chamada internamente)
    # ------------------------------------------------------------------

    def _rebuild_artist_lists(self) -> None:
        artists = list(self._artists.values())
        self.artists_by_name = sorted(artists, key=lambda a: a.name.lower())

    def _rebuild_song_lists(self) -> None:
        songs = list(self._songs.values())
        self.songs_by_title = sorted(songs, key=lambda s: s.title.lower())
        self.songs_by_plays = sorted(songs, key=lambda s: s.plays, reverse=True)
        self.songs_by_year = sorted(songs, key=lambda s: s.release_year)

    def _rebuild_album_lists(self) -> None:
        albums = list(self._albums.values())
        self.albums_by_title = sorted(albums, key=lambda a: a.title.lower())
        self.albums_by_rating = sorted(albums, key=lambda a: a.rating, reverse=True)

    # ------------------------------------------------------------------
    # Representação
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        s = self.stats()
        return (
            f"MusicCatalog("
            f"artists={s['total_artists']}, "
            f"albums={s['total_albums']}, "
            f"songs={s['total_songs']}, "
            f"plays={s['total_plays']})"
        )