from tkinter import *
from tkinter import font as tkfont

class MyButton(Button):
	def __init__(self, parent, *args, **kwargs):
		Button.__init__(self, parent, *args, **kwargs)
		self['font'] = tkfont.Font(family='fixedsys', size=16, weight="bold")
		self['borderwidth'] = 3
		self['bg'] = '#2c3738'
		self['fg'] = '#ffff00'


class MyLabel(Label):
	def __init__(self, parent, *args, **kwargs):
		Label.__init__(self,parent, *args, **kwargs)
		self['font'] = tkfont.Font(family='fixedsys', size=5, weight="bold")
		self['bg'] = 'black'
		self['fg'] = '#ffff00'

