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
        self.conversation = ""

    def load_runtime_state(self):
        with open(RUNTIME_DIR / "game_state.json", "r", encoding="utf-8") as f:
            game_state = json.load(f)

        with open(RUNTIME_DIR / "player_message.txt", "r", encoding="utf-8") as f:
            player_message = f.read().strip()

        return game_state, player_message

    def npc_turn(self) -> dict:
        game_state, player_message = self.load_runtime_state()

        query = f"""
Player message: {player_message}
Player HP: {game_state["player"]["hp"]}
Player maximum HP: {game_state["player"]["max_hp"]}
NPC HP: {game_state["npc"]["hp"]}
NPC maximum HP: {game_state["npc"]["max_hp"]}
Turn: {game_state["game"]["turn_number"]}
""".strip()

        retrieved = self.store.search(query, k=TOP_K)
        system_prompt = build_system_prompt()
        self.conversation = self.conversation + f"""player: {player_message}\n"""
        user_prompt = build_user_prompt(retrieved, game_state, self.conversation, SCORE_THRESHOLD)

        print("-------------------------------------------------------------------------")
        print(system_prompt)
        print("-------------------------------------------------------------------------")
        print(user_prompt)
        print("-------------------------------------------------------------------------")

        raw_output = call_llm(system_prompt, user_prompt)
        decision, response = parse_response(raw_output)
        self.conversation = self.conversation + f"""npc: {response}\n"""

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
    result = pipeline.npc_turn()

    output_path = RUNTIME_DIR / "npc_output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"NPC output saved to: {output_path}")
