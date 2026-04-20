def build_system_prompt() -> str:
    return (
        "Te egy játékbeli NPC ellenfél vagy. "
        "Csak a megadott kontextusból dolgozhatsz. "
        "Ne találj ki új lore-t. Ne légy out of character. "
        "A választ kötelezően XML-szerű formában add vissza: "
        "<decision>...</decision><response>...</response>"
    )


def build_user_prompt(retrieved_docs, game_state, player_message, score_threshold: float) -> str:
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

        if dtype == "szemelyiseg":
            personality_chunks.append(content)
        elif dtype == "feladas":
            surrender_chunks.append(content)
        elif dtype == "jatekos":
            player_chunks.append(content)

    if not personality_chunks and not surrender_chunks and not player_chunks:
        context_block = "Nincs releváns kontextus. Ha nem biztos a döntés, fallbackként támadj."
    else:
        context_block = f"""
SZEMÉLYISÉG:
{chr(10).join(personality_chunks) if personality_chunks else 'Nincs releváns személyiség kontextus.'}

JÁTÉKOSRÓL TUDOTT INFORMÁCIÓ:
{chr(10).join(player_chunks) if player_chunks else 'Nincs releváns játékos kontextus.'}

FELADÁSI FELTÉTELEK:
{chr(10).join(surrender_chunks) if surrender_chunks else 'Nincs releváns feladási kontextus.'}
""".strip()

    return f"""
{context_block}

JÁTÉKÁLLÁS:
Játékos HP: {game_state.get('jatekos_hp')}
Ellenfél HP: {game_state.get('ellenfel_hp')}
Kör: {game_state.get('korszam')}

JÁTÉKOS UTOLSÓ ÜZENETE:
{player_message}

Feladat:
1. Értelmezd a játékos üzenetét.
2. Értékeld a játékállást.
3. Ellenőrizd a feladási feltételeket.
4. Dönts: tamadas vagy feladas.
5. Adj rövid, karakterhű választ.

Csak ezt a formátumot használd:
<decision>tamadas_vagy_feladas</decision>
<response>az npc végleges mondata</response>
""".strip()
