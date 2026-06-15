extends Node2D

var turn_number: int

# Called when the node enters the scene tree for the first time.
func _ready():
	self.turn_number = 0

func _on_pass_button_button_down():
	self.turn_number += 1
	var message = $TextEdit.get_text()
	var file = FileAccess.open("res://runtime/player_message.txt", FileAccess.WRITE)
	file.store_line(message)
	file.close()
	await rag()

	file = FileAccess.open("res://response.txt", FileAccess.READ)
	var response = file.get_as_text()
	file.close()

	$Enemy_Bubble.text = response

func _on_attack_button_button_down():
	var gamestate_file = FileAccess.open("res://runtime/game_state.json", FileAccess.READ)
	var gamestate_json = JSON.new()
	gamestate_json.parse(gamestate_file.get_as_text())
	gamestate_file.close()

	print('piss')

	var gamestate = gamestate_json.data
	self.turn_number += 1
	gamestate["game"]["turn_number"] = self.turn_number
	gamestate["npc"]["hp"] = gamestate["npc"]["hp"] - 29
	var npc_hp = gamestate["npc"]["hp"]
	var decision = self.decide(npc_hp)
	if decision == "fight":
		gamestate["player"]["hp"] = gamestate["player"]["hp"] - 20
	gamestate["npc"]["decision"] = decision

	print("poo")

	var gamestate_file = FileAccess.open("res://runtime/game_state.json", FileAccess.WRITE)
	file.store_line(gamestate_json.stringify())
	
	var message = $TextEdit.get_text()
	var file = FileAccess.open("res://runtime/player_message.txt", FileAccess.WRITE)
	file.store_line(message)
	file.close()
	await rag()


	file = FileAccess.open("res://response.txt", FileAccess.READ)
	var response = file.get_as_text()
	file.close()

	$Enemy_Bubble.text = response

func decide(npc_hp):
	if npc_hp < 40:
		return "surrender"
	else:
		return "fight"

func rag():
	var output = []
	print(OS.execute("python", ["run.py"], output))
	return
