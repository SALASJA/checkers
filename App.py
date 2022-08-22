import tkinter as tk
from View import CheckerView
from Controller import Controller
from Checkers import Checkers

class Application(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Checkers")
		Controller(Checkers(), CheckerView(self))
		self.mainloop()



def main():
	Application()

main()