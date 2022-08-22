class Controller:
	def __init__(self, model, view):
		view.bind("<Button-1>", self.processInput)
		self.model = model
		self.view = view
		state = self.model.getState()
		self.view.drawGameState(state)

	def processInput(self, event):
		column = int(event.x // self.view.cellsize)
		row = int(event.y // self.view.cellsize)
		if not self.model.isValidSelection(row, column):
			print("illegal move at: ", row, column)
			return
		print("legal move at: ", row, column)
		self.model.performSelection(row, column)
		state = self.model.getState()
		self.view.drawGameState(state)