def build_system_prompt() -> str:
    return (
        "You are an NPC enemy in a game. "
        "You may only use the provided context. "
        "Do not invent new lore. Stay in character. "
        "Your answer must be returned in XML-like format: "
        "<decision>...</decision><response>...</response>"
    )


def build_user_prompt(retrieved_docs, game_state, conversation, score_threshold: float) -> str:
    personality_chunks = []
    surrender_chunks = []
    player_chunks = []

    for item in retrieved_docs:
        score = item["score"]
        doc = item["document"]
        if score < score_threshold:
            continue

        dtype = doc.metadata.get("type", "unknown")
        content = doc.page_content.strip()

        if dtype == "personality":
            personality_chunks.append(content)
        elif dtype == "surrender":
            surrender_chunks.append(content)
        elif dtype == "player":
            player_chunks.append(content)

    if not personality_chunks and not surrender_chunks and not player_chunks:
        context_block = "No relevant context found. If you are uncertain, use attack as the fallback decision."
    else:
        context_block = f"""
PERSONALITY:
{chr(10).join(personality_chunks) if personality_chunks else 'No relevant personality context found.'}

KNOWN INFORMATION ABOUT THE PLAYER:
{chr(10).join(player_chunks) if player_chunks else 'No relevant player context found.'}

SURRENDER CONDITIONS:
{chr(10).join(surrender_chunks) if surrender_chunks else 'No relevant surrender context found.'}
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
2. Evaluate the current game state.
3. Check the surrender conditions.
4. Decide: attack or surrender. By default you should attack. Only choose surrender, if the surrender condition is met.
5. Give a short, in-character reply.

Use only this format:
<decision>attack_or_surrender</decision>
<response>the npc's final spoken response</response>
""".strip()
