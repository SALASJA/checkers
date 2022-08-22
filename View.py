import tkinter as tk
import turtle as t

class Grid(tk.Canvas):
	def __init__(self, parent, width=400, height=450):
		super().__init__(parent, width=width, height=height)
		self.gridwidth = width
		self.gridheight = height
		self.cellsize = width/8
		self.colorA = "#ffebcb" #sandy color
		self.colorB = "#006400" #dark green
		self.screen = t.TurtleScreen(self)
		self.screen.tracer(0,0)
		self.turt = t.RawTurtle(self.screen)
		self.turt.hideturtle()
		self.drawGrid()
		self.pack()
		
	def drawGrid(self, clear=True):
		if clear:
			self.turt.clear()
		starting_color_mode = True
		current_y = self.gridheight/2
		for i in range(8):
			current_x = -self.gridwidth/2
			is_sandy_color_mode = starting_color_mode
			for j in range(8):
				current_color = None
				
				if is_sandy_color_mode:
					current_color = self.colorA
				else:
					current_color = self.colorB
					
				self.filledSquare(current_color, self.cellsize, current_x, current_y)
				is_sandy_color_mode = not is_sandy_color_mode
				current_x += self.cellsize
			current_y -= self.cellsize
			starting_color_mode = not starting_color_mode
		self.screen.update()

	def filledSquare(self, color, size, x, y):
		self.turt.penup()
		self.turt.goto(x,y)
		self.turt.pendown()
		self.turt.color(color)
		self.turt.begin_fill()
		for i in range(4):
			self.turt.forward(size)
			self.turt.right(90)
		self.turt.end_fill()


#BDBDBD grey
#part of the game rules will be checkers
#part of the game in controller
		
#game rules should not be here
class CheckerView(Grid):
	def __init__(self,parent, width=400, height=450):
		super().__init__(parent, width, height)


	def drawGameState(self, state):
		#using the location information, draw the pieces 
		locations = state["locations"]
		self.drawGrid()
		for row in range(len(locations)):
			for column in range(len(locations[0])):
				self.drawCircle(row,column,locations[row][column])

		selected = state["selected"]
		if selected != None:
			self.drawSquareOutline(selected)
		turn = state["turn"] #false is red, true is white
		multijump = state["multijump"]
		self.drawTurn(turn, multijump)
		
		self.screen.update()

	def drawTurn(self, turn, multijump):
		square_x = lambda j: self.cellsize * j - self.gridwidth/2   #lambda x: 25 * x - 100
		square_y = lambda i: -self.cellsize * i + self.gridheight/2 
		square_x_position = square_x(2)
		square_y_position = square_y(8)
		self.filledSquare("#bdbdbd", self.cellsize, square_x_position, square_y_position)
		self.drawCircle(8,2, 1 if turn else 2)
		self.turt.penup()
		self.turt.goto(square_x_position - 20, square_y_position - 35)
		self.turt.pendown()
		self.turt.write("Turn:", move=False, align='center', font=('Arial', 12, 'normal'))
		self.turt.penup()
		self.turt.goto(square_x_position + 200, square_y_position - 35)
		self.turt.pendown()
		if multijump:
			self.turt.write("Must continue jump!", move=False, align='center', font=('Arial', 12, 'normal'))

		

	def drawSquareOutline(self, selected):
		calc_x = lambda j: self.cellsize * j - self.gridwidth/2   #lambda x: 25 * x - 100
		calc_y = lambda i: -self.cellsize * i + self.gridheight/2 
		current_x = calc_x(selected[1]) + 2
		current_y = calc_y(selected[0]) - 2
		self.turt.penup()
		self.turt.goto(current_x, current_y)
		self.turt.pendown()
		self.turt.color("black")
		self.turt.pensize(3)
		for i in range(4):
			self.turt.forward(self.cellsize * 0.9)
			self.turt.right(90)
		self.turt.pensize(1)
			
		


	def drawCircle(self, row, column, type):
		if type < 1 or 4 < type:
			return
		colors = ["white", "red","white", "red"]
		color_string = colors[type - 1]
		calc_x = lambda j: self.cellsize * (j + 0.5) - self.gridwidth/2   #lambda x: 25 * x - 100
		calc_y = lambda i: -self.cellsize * (i + 0.85) + self.gridheight/2   #lambda: x: -25 * x + 100
		self.turt.penup()
		current_x = calc_x(column)
		current_y = calc_y(row)
		self.turt.goto(current_x,current_y)
		self.turt.pendown()
		self.turt.color(color_string)
		self.turt.begin_fill()
		self.turt.circle((self.cellsize * 0.65) / 2)
		self.turt.end_fill()
		self.turt.color("black")
		self.turt.circle((self.cellsize * 0.65) / 2)
		if type == 3 or type == 4:
			self.turt.penup()
			self.turt.goto(current_x + 1, current_y - 15)
			self.turt.pendown()
			self.turt.write("*", move=False, align='center', font=('Arial', 30, 'normal'))
			
		
				



			

