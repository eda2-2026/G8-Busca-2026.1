"""
Módulo de Algoritmos de Busca — MusicDB
========================================

Este módulo é o CORAÇÃO do trabalho de Estrutura de Dados 2.
Cada função abaixo representa um algoritmo a ser implementado pelo estudante.

As funções recebem uma lista JÁ ORDENADA (fornecida pelo MusicCatalog) e
uma chave de busca, retornando o índice do elemento encontrado ou -1.

Convenções
----------
  - Todas as buscas em strings são CASE-INSENSITIVE.
  - Retorno  >= 0  → índice do elemento encontrado na lista.
  - Retorno  == -1 → elemento não encontrado.
  - Os parâmetros `comparisons` são contadores opcionais para análise de
    desempenho — use-os para registrar quantas comparações cada algoritmo faz.

Algoritmos contemplados
-----------------------
  1. Busca Linear indexada
  2. Busca Binária         
  3. Busca por Interpolação
  4. Hash
"""

from __future__ import annotations
import math
from typing import Any

from models.artist import Artist
from models.song import Song
from models.album import Album


# =============================================================================
# 1. BUSCA LINEAR INDEXADA
# =============================================================================

def linear_search_song_by_title(songs: list[Song], title: str) -> int:
    """
    Percorre a lista sequencialmente até encontrar a música pelo título.

    Parâmetros
    ----------
    songs : lista de Song (qualquer ordem)
    title : título a buscar (case-insensitive)

    Retorno
    -------
    Índice do elemento encontrado, ou -1.

    Complexidade: O(n)
    """
    # TODO: implemente a busca linear aqui
    raise NotImplementedError("Implemente linear_search_song_by_title()")


def linear_search_artist_by_name(artists: list[Artist], name: str) -> int:
    """
    Busca linear de artista pelo nome.

    Complexidade: O(n)
    """
    # TODO: implemente a busca linear aqui
    raise NotImplementedError("Implemente linear_search_artist_by_name()")


# =============================================================================
# 2. BUSCA BINÁRIA
# =============================================================================

def binary_search_song_by_title(songs: list[Song], title: str) -> int:
    """
    Busca binária em lista de músicas ordenada ALFABETICAMENTE pelo título.
    Pré-condição: `songs` deve estar ordenada por título (a–z).
    Complexidade: O(log n)
    """
    low = 0
    high = len(songs) - 1
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
    Busca binária em lista de artistas ordenada ALFABETICAMENTE pelo nome.
    Pré-condição: `artists` deve estar ordenada por nome (a–z).
    Complexidade: O(log n)
    """
    low = 0
    high = len(artists) - 1
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
    Busca binária em lista de álbuns ordenada ALFABETICAMENTE pelo título.
    Pré-condição: `albums` deve estar ordenada por título (a–z).
    Complexidade: O(log n)
    """
    low = 0
    high = len(albums) - 1
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
# 3. BUSCA POR INTERPOLAÇÃO
# =============================================================================

def interpolation_search_song_by_plays(songs: list[Song], plays: int) -> int:
    """
    Busca por interpolação em lista de músicas ordenada CRESCENTEMENTE por plays.
    Mais eficiente que a binária quando os dados são uniformemente distribuídos.
    Pré-condição: `songs` deve estar ordenada por plays de forma CRESCENTE.
    Complexidade: O(log log n) esperado; O(n) no pior caso.
    """
    low = 0
    high = len(songs) - 1

    # condição do loop garante que o alvo esteja dentro dos limites atuais
    while low <= high and plays >= songs[low].plays and plays <= songs[high].plays:
        
        # vai evitar divisão por zero caso todos os elementos restantes sejam iguais
        if low == high or songs[high].plays == songs[low].plays:
            if songs[low].plays == plays:
                return low
            return -1

        # fórmula da posição da interpolação
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
# 4. BUSCA POR HASHING
# =============================================================================

def hashing_search_song_by_plays(songs: list[Song], plays: int) -> int:
    """
    """
    # TODO: implemente a busca por hashing aqui
    raise NotImplementedError("Implemente hashing_search_song_by_plays()")



# =============================================================================
# UTILITÁRIO — comparação de desempenho
# =============================================================================

def benchmark(catalog=None, n_songs: int = 10_000, runs: int = 10) -> None:
    """
    Executa todos os algoritmos implementados e exibe tempo médio de execução.

    Por padrão gera um catálogo sintético com `n_songs` músicas para que as
    diferenças de complexidade fiquem visíveis. Você também pode passar um
    catálogo real (ex: o do seed.py), mas os tempos serão muito parecidos
    devido ao tamanho pequeno dos dados.

    Parâmetros
    ----------
    catalog : MusicCatalog já populado, ou None para gerar um sintético
    n_songs : tamanho do catálogo sintético (usado só se catalog=None)
    runs    : número de execuções para calcular a média

    Exemplos de uso
    ---------------
    # Catálogo sintético (recomendado para benchmark real):
    from search_algorithms import benchmark
    benchmark()                        # padrão: 10.000 músicas
    benchmark(n_songs=1_000)
    benchmark(n_songs=50_000)

    # Catálogo real (dados do seed):
    from data.seed import build_catalog
    benchmark(catalog=build_catalog())
    """
    import time
    from data.generator import generate_catalog

    if catalog is None:
        print(f"  Gerando catálogo sintético com {n_songs:,} músicas...", end=" ", flush=True)
        catalog = generate_catalog(n_songs=n_songs, seed=0)
        print("pronto.\n")

    n = len(catalog.songs_by_title)
    a = len(catalog.artists_by_name)

    # Escolhe alvos que estão garantidamente nas listas
    # (último elemento → pior caso para Linear)
    target_song_title  = catalog.songs_by_title[-1].title
    target_artist_name = catalog.artists_by_name[-1].name
    target_plays       = list(reversed(catalog.songs_by_plays))[n // 2].plays
    target_year        = catalog.songs_by_year[n // 2].release_year

    print("=" * 65)
    print(f"  BENCHMARK — {n:,} músicas / {a:,} artistas  ({runs} execuções)")
    print("=" * 65)
    print(f"  {'Algoritmo':<38} {'idx':>5}  {'avg (µs)':>10}")
    print(f"  {'-'*38}  {'-'*5}  {'-'*10}")

    # ------------------------------------------------------------------
    # Adicione aqui cada algoritmo à medida que for implementando.
    # Formato: "Rótulo": (função, lista, chave)
    # ------------------------------------------------------------------
    algorithms = {
        "Busca Linear       (título)":    (linear_search_song_by_title,           catalog.songs_by_title,                        target_song_title),
        "Busca Binária      (título)":    (binary_search_song_by_title,            catalog.songs_by_title,                        target_song_title),
        "Busca Binária      (artista)":   (binary_search_artist_by_name,           catalog.artists_by_name,                       target_artist_name),
        "Busca Linear       (artista)":   (linear_search_artist_by_name,           catalog.artists_by_name,                       target_artist_name),
        "Busca Interpolação (plays)":     (interpolation_search_song_by_plays,     list(reversed(catalog.songs_by_plays)),        target_plays),
        "Busca Binária      (álbum)":     (binary_search_album_by_title,           catalog.albums_by_title,                       catalog.albums_by_title[len(catalog.albums_by_title)//2].title),
        "Busca Hashing      (plays)":      (hashing_search_song_by_plays,     list(reversed(catalog.songs_by_plays)),        target_plays),
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