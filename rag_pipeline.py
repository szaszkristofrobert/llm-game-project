import json

from config import (
    DOCSTORE_PATH,
    EMBED_MODEL_NAME,
    INDEX_PATH,
    RUNTIME_DIR,
    SCORE_THRESHOLD,
    TOP_K,
)
from llm_client import call_llm
from parser_utils import parse_response
from prompts import build_system_prompt, build_user_prompt
from vector_store import LocalVectorStore


class NPCPipeline:
    def __init__(self):
        self.store = LocalVectorStore(EMBED_MODEL_NAME)
        self.store.load(INDEX_PATH, DOCSTORE_PATH)

    def load_runtime_state(self):
        with open(RUNTIME_DIR / "jatekallas.json", "r", encoding="utf-8") as f:
            game_state = json.load(f)

        with open(RUNTIME_DIR / "jatekos_valasz.txt", "r", encoding="utf-8") as f:
            player_message = f.read().strip()

        return game_state, player_message

    def npc_kor(self) -> dict:
        game_state, player_message = self.load_runtime_state()

        query = f"""
Játékos üzenete: {player_message}
Játékos HP: {game_state.get('jatekos_hp')}
Ellenfél HP: {game_state.get('ellenfel_hp')}
Kör: {game_state.get('korszam')}
""".strip()

        retrieved = self.store.search(query, k=TOP_K)
        system_prompt = build_system_prompt()
        user_prompt = build_user_prompt(retrieved, game_state, player_message, SCORE_THRESHOLD)

        raw_output = call_llm(system_prompt, user_prompt)
        decision, response = parse_response(raw_output)

        result = {
            "decision": decision,
            "response": response,
            "raw_output": raw_output,
            "retrieved": [
                {
                    "score": round(x["score"], 4),
                    "type": x["document"].metadata.get("type"),
                    "source": x["document"].metadata.get("source"),
                }
                for x in retrieved
            ],
        }
        return result


if __name__ == "__main__":
    pipeline = NPCPipeline()
    result = pipeline.npc_kor()

    output_path = RUNTIME_DIR / "npc_output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"NPC output mentve: {output_path}")
