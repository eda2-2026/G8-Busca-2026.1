# MusicDB — Plataforma de Dados Musicais

Projeto base para implementação de **Algoritmos de Busca** na disciplina de **Estrutura de Dados 2**.

---

## Objetivo do Projeto

O MusicDB é um sistema orientado a objetos que simula o catálogo interno de uma plataforma de streaming musical. Ele armazena informações sobre **artistas**, **bandas**, **álbuns** e **músicas** — incluindo colaborações (**feats**) — e serve como base real para você implementar e comparar diferentes algoritmos de busca estudados na disciplina.

A ideia é simples: ao invés de rodar algoritmos sobre arrays genéricos de inteiros, você vai buscá-los sobre **dados com significado real**, o que torna a análise de desempenho muito mais interessante.

---

## Estrutura de Arquivos

```
musicdb/
│
├── main.py                  
│
├── music_catalog.py         
│
├── search_algorithms.py     
│
├── models/
│   ├── artist.py            
│   ├── song.py              
│   └── album.py             
│
└── data/
    └── seed.py              
```

---

## Modelo de Dados

### `Artist`
Representa um artista solo ou banda.

| Campo         | Tipo        | Descrição                                  |
|---------------|-------------|--------------------------------------------|
| `artist_id`   | `int`       | Identificador único                        |
| `name`        | `str`       | Nome do artista ou banda                   |
| `genre`       | `str`       | Gênero musical principal                   |
| `country`     | `str`       | País de origem                             |
| `formed_year` | `int`       | Ano de formação / início de carreira       |
| `is_band`     | `bool`      | `True` se for banda                        |
| `members`     | `list[str]` | Integrantes (somente para bandas)          |

### `Song`
Representa uma música, podendo ter artistas participantes (feats).

| Campo          | Tipo        | Descrição                                  |
|----------------|-------------|--------------------------------------------|
| `song_id`      | `int`       | Identificador único                        |
| `title`        | `str`       | Título da música                           |
| `artist_id`    | `int`       | ID do artista/banda principal              |
| `album_id`     | `int?`      | ID do álbum (`None` para singles)          |
| `duration_sec` | `int`       | Duração em segundos                        |
| `release_year` | `int`       | Ano de lançamento                          |
| `genre`        | `str`       | Gênero musical                             |
| `plays`        | `int`       | Número de reproduções                      |
| `feat_ids`     | `list[int]` | IDs dos artistas participantes (feats)     |

### `Album`
Representa um álbum discográfico.

| Campo          | Tipo        | Descrição                                  |
|----------------|-------------|--------------------------------------------|
| `album_id`     | `int`       | Identificador único                        |
| `title`        | `str`       | Título do álbum                            |
| `artist_id`    | `int`       | ID do artista/banda                        |
| `release_year` | `int`       | Ano de lançamento                          |
| `genre`        | `str`       | Gênero musical principal                   |
| `song_ids`     | `list[int]` | IDs das faixas (na ordem do álbum)         |
| `rating`       | `float`     | Nota média (0.0 a 10.0)                    |

---

## Algoritmos de Busca a Implementar

Todos os algoritmos ficam no arquivo **`search_algorithms.py`**.
Cada função recebe uma **lista já ordenada** (fornecida pelo `MusicCatalog`) e uma chave de busca.

| # | Algoritmo               | Função(ões) alvo                                         | Complexidade         |
|---|-------------------------|----------------------------------------------------------|----------------------|
| 1 | **Busca Linear**        | `linear_search_song_by_title` <br> `linear_search_artist_by_name` | O(n)       |
| 2 | **Busca Binária**       | `binary_search_song_by_title` <br> `binary_search_artist_by_name` <br> `binary_search_album_by_title` | O(log n)  |
| 3 | **Busca por Salto**     | `jump_search_song_by_plays`                              | O(√n)                |
| 4 | **Busca por Interpolação** | `interpolation_search_song_by_plays`                  | O(log log n) esperado |
| 5 | **Busca Exponencial**   | `exponential_search_song_by_year`                        | O(log n)             |
| 6 | **Busca Fibonacci**     | `fibonacci_search_artist_by_name`                        | O(log n)             |

### Listas pré-ordenadas disponíveis no `MusicCatalog`

O `MusicCatalog` já entrega as listas prontas para cada tipo de busca:

```python
catalog.artists_by_name    # artistas em ordem alfabética (a→z)
catalog.songs_by_title     # músicas em ordem alfabética (a→z)
catalog.songs_by_plays     # músicas do mais tocado → menos tocado
catalog.songs_by_year      # músicas do mais antigo → mais recente
catalog.albums_by_title    # álbuns em ordem alfabética (a→z)
catalog.albums_by_rating   # álbuns da melhor nota → pior nota
```

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10 ou superior (usa `list[str]` como type hint nativo)
- Nenhuma dependência externa necessária

### Rodando o projeto

```bash
# A partir da pasta G8-BUSCA-2026.1/
PYTHONPATH=. python main.py
```

Você verá no terminal:
- Estatísticas gerais do catálogo
- Todas as listas ordenadas com índices visíveis
- Os feats de um artista de exemplo
- As faixas de um álbum
- O resultado do benchmark

### Validando os dados

```bash
PYTHONPATH=. python data/seed.py
```

---

## Análise de Desempenho (Benchmark)

Após implementar os algoritmos, chame `benchmark(catalog)` em `main.py` para comparar o tempo de execução médio de cada um:

```
============================================================
BENCHMARK DOS ALGORITMOS DE BUSCA — MusicDB
============================================================
  Busca Linear (título)              resultado= 8  avg=2.41 µs
  Busca Binária (título)             resultado= 8  avg=0.89 µs
  Busca Linear (artista)             resultado=15  avg=1.73 µs
  Busca Binária (artista)            resultado=15  avg=0.61 µs
============================================================
```
