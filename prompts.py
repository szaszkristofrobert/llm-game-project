def build_system_prompt() -> str:
    return (
        "You are an NPC enemy in a game. "
        "You may only use the provided context. "
        "Do not invent new lore. Stay in character. "
        "Your answer must be returned in XML-like format: "
        "<response>...</response>"
    )


def build_user_prompt(retrieved_docs, game_state, conversation, score_threshold: float) -> str:
    npc_chunks = []
    player_chunks = []

    for item in retrieved_docs:
        score = item["score"]
        print(score)
        doc = item["document"]
        print(doc.page_content.strip())
        if score < score_threshold:
            continue

        

        dtype = doc.metadata.get("type", "unknown")
        print(dtype)
        content = doc.page_content.strip()

        if dtype == "npc" or dtype == "unknown":
            npc_chunks.append(content)
        elif dtype == "player":
            player_chunks.append(content)

    print(npc_chunks)
    print("+++++++++++++++++++++")

    if not npc_chunks and not player_chunks:
        context_block = "No relevant context found."
    else:
        context_block = f"""
INFORMATION ABOUT YOUR CHARACTER:
{chr(10).join(npc_chunks) if npc_chunks else 'No relevant personality context found.'}

KNOWN INFORMATION ABOUT THE PLAYER:
{chr(10).join(player_chunks) if player_chunks else 'No relevant player context found.'}
""".strip()

    return f"""
{context_block}

GAME STATE:
Player HP: {game_state["player"]["hp"]}
Player maximum HP: {game_state["player"]["max_hp"]}
NPC HP: {game_state["npc"]["hp"]}
NPC maximum HP: {game_state["npc"]["max_hp"]}
Turn: {game_state["game"]["turn_number"]}

THE CONVERSATION BETWENN THE PLAYER AND THE NPC YOU ARE PLAYING SO FAR:
{conversation}

Task:
1. Interpret the player's message.
2. Check the gamestate. If the decision is FIGHT you should fight on, if it is SURRENDER you should give up.
3. Your decision is based on the gamestate, not the player response. If you fight you should taunt the player, if you surrender you should give up.
4. Give a short, in-character reply.

Use only this format:
<response>the npc's final spoken response</response>
""".strip()
