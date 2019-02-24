from tkinter import *
from tkinter import font as tkfont

class GameButton(Button):
	def __init__(self, text, command, font=None, borderwidth=None, bg=None, fg=None):
		Button.__init__(self)
		self.text = text
		self.command = command
		self.font = tkfont.Font(family='fixedsys', size=16, weight="bold")
		self.borderwidth = 3
		self.bg = 'black'
		self.fg = '#ffff00'




