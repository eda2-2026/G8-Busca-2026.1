from __future__ import annotations
import math

from models.artist import Artist
from models.song import Song
from models.album import Album


# =============================================================================
# 1. BUSCA LINEAR COM SENTINELA
# =============================================================================

def linear_search_song_by_title(songs: list[Song], title: str) -> int:

    tamanho = len(songs)
    if tamanho == 0:
        return -1

    target = title.lower()

    # Salva o último elemento e coloca a sentinela no lugar
    ultimo_original = songs[-1]
    songs[-1] = Song(
        song_id=-1,
        title=title,          
        artist_id=-1,
        album_id=None,
        duration_sec=0,
        release_year=0,
        genre="",
    )

    i = 0
    while songs[i].title.lower() != target:
        i += 1

    # Restaura o elemento original antes de qualquer retorno
    songs[-1] = ultimo_original

    # Encontrou antes da sentinela → resultado real
    if i < tamanho - 1:
        return i

    # Parou na última posição — pode ser a sentinela ou o elemento real
    if ultimo_original.title.lower() == target:
        return tamanho - 1

    return -1


def linear_search_artist_by_name(artists: list[Artist], name: str) -> int:
    """
    Busca linear simples de artista pelo nome.

    Complexidade: O(n)
    """
    target = name.lower()
    for i, artist in enumerate(artists):
        if artist.name.lower() == target:
            return i
    return -1


# =============================================================================
# 2. BUSCA LINEAR INDEXADA
# =============================================================================

def _build_plays_index(songs: list[Song], block_size: int | None = None) -> list[tuple[int, int]]:
    """
    Constrói o índice para uma lista de músicas ordenada por plays (crescente).

    Retorna lista de tuplas (plays_do_início_do_bloco, posição_na_lista).
    """
    n = len(songs)
    if n == 0:
        return []
    if block_size is None:
        block_size = max(1, int(math.sqrt(n)))
    return [(songs[i].plays, i) for i in range(0, n, block_size)]


def indexed_linear_search_song_by_plays(
    songs: list[Song],
    plays: int,
    index: list[tuple[int, int]] | None = None,
    block_size: int | None = None,
) -> int:

    n = len(songs)
    if n == 0:
        return -1

    if block_size is None:
        block_size = max(1, int(math.sqrt(n)))
    if index is None:
        index = _build_plays_index(songs, block_size)

    # bloco
    block_start = 0
    for idx_plays, list_pos in index:
        if idx_plays > plays:
            break
        block_start = list_pos

    # busca linear dentro do bloco
    block_end = min(block_start + block_size, n)
    for i in range(block_start, block_end):
        if songs[i].plays == plays:
            return i
        if songs[i].plays > plays:
            return -1

    return -1


# =============================================================================
# 3. BUSCA BINÁRIA
# =============================================================================

def binary_search_song_by_title(songs: list[Song], title: str) -> int:
    """
    Busca binária em lista de músicas ordenada alfabeticamente pelo título.
    Complexidade: O(log n)
    """
    low, high = 0, len(songs) - 1
    target = title.lower()

    while low <= high:
        mid = (low + high) // 2
        mid_title = songs[mid].title.lower()
        if mid_title == target:
            return mid
        elif mid_title < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


def binary_search_artist_by_name(artists: list[Artist], name: str) -> int:
    """
    Busca binária em lista de artistas ordenada alfabeticamente pelo nome.
    Complexidade: O(log n)
    """
    low, high = 0, len(artists) - 1
    target = name.lower()

    while low <= high:
        mid = (low + high) // 2
        mid_name = artists[mid].name.lower()
        if mid_name == target:
            return mid
        elif mid_name < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


def binary_search_album_by_title(albums: list[Album], title: str) -> int:
    """
    Busca binária em lista de álbuns ordenada alfabeticamente pelo título.
    Complexidade: O(log n)
    """
    low, high = 0, len(albums) - 1
    target = title.lower()

    while low <= high:
        mid = (low + high) // 2
        mid_title = albums[mid].title.lower()
        if mid_title == target:
            return mid
        elif mid_title < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


# =============================================================================
# 4. BUSCA POR INTERPOLAÇÃO
# =============================================================================

def interpolation_search_song_by_plays(songs: list[Song], plays: int) -> int:
    """
    Busca por interpolação em lista de músicas ordenada por plays (crescente).

    Estima a posição do alvo proporcionalmente ao seu valor entre os extremos,
    em vez de sempre ir para o meio como a busca binária.

    Complexidade: O(log log n) esperado; O(n) no pior caso.
    """
    low, high = 0, len(songs) - 1

    while low <= high and plays >= songs[low].plays and plays <= songs[high].plays:

        # Evita divisão por zero quando todos os elementos restantes são iguais
        if low == high or songs[high].plays == songs[low].plays:
            return low if songs[low].plays == plays else -1

        # Fórmula da interpolação: estima onde o alvo deve estar
        pos_num = (plays - songs[low].plays) * (high - low)
        pos_den = (songs[high].plays - songs[low].plays)
        mid = low + (pos_num // pos_den)

        if songs[mid].plays == plays:
            return mid
        elif songs[mid].plays < plays:
            low = mid + 1
        else:
            high = mid - 1

    return -1


# =============================================================================
# 5. BUSCA POR HASHING
# =============================================================================

class HashTable:

    def __init__(self, size: int) -> None:
        self.size = size
        self.table: list[list[tuple[int, int]]] = [[] for _ in range(size)]

    def _hash(self, plays: int) -> int:

        return plays % self.size

    def insert(self, plays: int, index: int) -> None:

        balde = self._hash(plays)          
        self.table[balde].append((plays, index))

    def search(self, plays: int) -> int:

        balde = self._hash(plays)          
        for par_plays, par_index in self.table[balde]:
            if par_plays == plays:
                return par_index
        return -1


def _build_hash_table(songs: list[Song]) -> HashTable:

    def _proximo_primo(n: int) -> int:
        """Retorna o menor primo >= n."""
        def _eh_primo(x: int) -> bool:
            if x < 2:
                return False
            for d in range(2, int(math.sqrt(x)) + 1):
                if x % d == 0:
                    return False
            return True

        while not _eh_primo(n):
            n += 1
        return n

    size = _proximo_primo(len(songs))
    ht = HashTable(size)

    for i, song in enumerate(songs):
        ht.insert(song.plays, i)

    return ht


def hashing_search_song_by_plays(
    songs: list[Song],
    plays: int,
    hash_table: HashTable | None = None,
) -> int:

    if hash_table is None:
        hash_table = _build_hash_table(songs)

    return hash_table.search(plays)


# =============================================================================
# UTILITÁRIO — comparação de desempenho
# =============================================================================

def benchmark(catalog=None, n_songs: int = 10_000, runs: int = 10) -> None:
    """
    Executa todos os algoritmos implementados e exibe tempo médio de execução.

    Parâmetros
    ----------
    catalog : MusicCatalog já populado, ou None para gerar um sintético
    n_songs : tamanho do catálogo sintético (usado só se catalog=None)
    runs    : número de execuções para calcular a média

    Exemplos
    --------
    benchmark()                   # catálogo sintético com 10.000 músicas
    benchmark(n_songs=1_000)
    benchmark(catalog=build_catalog())   # catálogo real do seed
    """
    import time
    from data.generator import generate_catalog

    if catalog is None:
        print(f"  Gerando catálogo sintético com {n_songs:,} músicas...", end=" ", flush=True)
        catalog = generate_catalog(n_songs=n_songs, seed=0)
        print("pronto.\n")

    n = len(catalog.songs_by_title)
    a = len(catalog.artists_by_name)

    # Alvos garantidamente presentes (último elemento = pior caso para Linear)
    target_song_title  = catalog.songs_by_title[-1].title
    target_artist_name = catalog.artists_by_name[-1].name
    plays_asc          = list(reversed(catalog.songs_by_plays))
    target_plays       = plays_asc[n // 2].plays
    target_album_title = catalog.albums_by_title[len(catalog.albums_by_title) // 2].title

    # Estruturas auxiliares construídas UMA vez — o benchmark mede só a busca
    plays_index = _build_plays_index(plays_asc)
    try:
        hash_table = _build_hash_table(plays_asc)
    except NotImplementedError:
        hash_table = None

    print("=" * 65)
    print(f"  BENCHMARK — {n:,} músicas / {a:,} artistas  ({runs} execuções)")
    print("=" * 65)
    print(f"  {'Algoritmo':<38} {'idx':>5}  {'avg (µs)':>10}")
    print(f"  {'-'*38}  {'-'*5}  {'-'*10}")

    algorithms: dict = {
        "Busca Linear Sentinela     (título)": (
            linear_search_song_by_title,
            catalog.songs_by_title,
            target_song_title,
        ),
        "Busca Binária              (título)": (
            binary_search_song_by_title,
            catalog.songs_by_title,
            target_song_title,
        ),
        "Busca Linear               (artista)": (
            linear_search_artist_by_name,
            catalog.artists_by_name,
            target_artist_name,
        ),
        "Busca Binária              (artista)": (
            binary_search_artist_by_name,
            catalog.artists_by_name,
            target_artist_name,
        ),
        "Busca Interpolação         (plays)": (
            interpolation_search_song_by_plays,
            plays_asc,
            target_plays,
        ),
        # Lambda garante que o benchmark meça SÓ a busca, não a construção
        "Busca Linear Indexada      (plays)": (
            lambda l, k: indexed_linear_search_song_by_plays(l, k, index=plays_index),
            plays_asc,
            target_plays,
        ),
        "Busca Hashing              (plays)": (
            lambda l, k: hashing_search_song_by_plays(l, k, hash_table=hash_table),
            plays_asc,
            target_plays,
        ),
        "Busca Binária              (álbum)": (
            binary_search_album_by_title,
            catalog.albums_by_title,
            target_album_title,
        ),
    }

    for label, (fn, lst, key) in algorithms.items():
        try:
            times = []
            result = -2
            for _ in range(runs):
                start = time.perf_counter()
                result = fn(lst, key)
                elapsed = time.perf_counter() - start
                times.append(elapsed)
            avg_us = (sum(times) / runs) * 1_000_000
            found = "✓" if result >= 0 else "✗ NÃO ENCONTRADO"
            print(f"  {label:<38} {result:>5}  {avg_us:>10.2f}  {found}")
        except NotImplementedError:
            print(f"  {label:<38} {'---':>5}  {'---':>10}  *** NÃO IMPLEMENTADO ***")
        except Exception as e:
            print(f"  {label:<38} {'ERR':>5}  {'---':>10}  {e}")

    print("=" * 65)