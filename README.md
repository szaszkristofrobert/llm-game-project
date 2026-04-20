# NPC RAG projektváz

Ez a projekt a rendszerterved alapján készült: statikus `.txt` lore fájlok, dinamikus `jatekallas.json` és `jatekos_valasz.txt`, `all-MiniLM-L6-v2` embedding, FAISS retrieval, majd lokális Llama 3.1 meghívás XML-szerű döntéssel.

## Telepítés

```bash
pip install -r requirements.txt
```

## Fájlok

- `config.py` – központi beállítások
- `build_index.py` – `.txt` fájlok betöltése, chunkolás, FAISS index építés
- `vector_store.py` – embedding + keresés + mentés/betöltés
- `prompts.py` – system és user prompt generálás
- `llm_client.py` – lokális Llama 3.1 hívása Ollamán keresztül
- `parser_utils.py` – `<decision>` és `<response>` parse
- `rag_pipeline.py` – teljes körfuttatás, `npc_output.json` mentéssel
- `example_run.py` – egyszerű tesztindítás

## Első futtatás

1. Indítsd el az Ollamát úgy, hogy a `llama3.1` modell elérhető legyen.
2. Építs indexet:

```bash
python build_index.py
```

3. Futtasd az NPC kört:

```bash
python rag_pipeline.py
```

4. Az eredmény itt lesz:

```text
data/runtime/npc_output.json
```

## Godot integráció ötlet

A rendszerterv szerint a Godot kör végén kiírja a `jatekallas.json`-t és `jatekos_valasz.txt`-t, majd meghívja a Python pipeline-t, végül visszaolvassa a `npc_output.json`-t.

## Megjegyzés

A rendszertervben szereplő `<thinking>` blokk helyett itt direkt csak a stabilan parse-olható mezők maradtak:

```xml
<decision>feladas</decision>
<response>Elég... most nem folytatom tovább.</response>
```
