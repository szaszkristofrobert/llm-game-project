extends TextEdit

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func _on_text_changed():
	if self.get_text().length() > 30:
		self.editable = false

func _input(_event):
	if Input.is_action_just_pressed('ui_text_backspace'):
		self.editable = true
