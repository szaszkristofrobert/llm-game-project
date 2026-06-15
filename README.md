# NPC RAG project scaffold

This project was prepared based on your system design: static `.txt` lore files, dynamic `game_state.json` and `player_message.txt`, `all-MiniLM-L6-v2` embeddings, FAISS retrieval, and a local Llama 3.1 call that returns an XML-like decision and response.

## Installation

```bash
pip install -r requirements.txt
```

## Files

- `config.py` – central settings and paths
- `build_index.py` – loads `.txt` files, chunks them, and builds the FAISS index
- `vector_store.py` – embeddings, search, save, and load
- `prompts.py` – system and user prompt generation
- `llm_client.py` – local Llama 3.1 call through Ollama
- `parser_utils.py` – parses `<response>`
- `rag_pipeline.py` – full NPC turn execution and `npc_output.json` output
- `example_run.py` – simple test runner

## First run

1. Start Ollama and make sure the `llama3.1:8b` model is available.
2. Build the index:

```bash
python build_index.py
```

3. Run one NPC turn:

```bash
python rag_pipeline.py
```

4. The result will be saved here:

```text
data/godot/runtime/npc_output.json
```

## Godot integration idea

According to the system design, Godot should write `game_state.json` and `player_message.txt` at the end of the player's turn, then call the Python pipeline, and finally read back `npc_output.json`. This matches the file-based bridge described in the architecture section of the plan.

## Note

The original design also mentioned a `<thinking>` block, but this scaffold intentionally keeps only the stable fields that are easy to parse:

```xml
<response>Enough. I will not continue this fight.</response>
```
