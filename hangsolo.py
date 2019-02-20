

from tkinter import *
from tkinter import font as tkfont 
import random
import ascii_art as a #separate file that holds the ascii art images
import words as w #separate file which has the word dictionaries and hints


class BaseApp(Tk):

	def __init__(self):
		Tk.__init__(self)
		self.title('HANG SOLO')

		#styling of widgets which will be used throughout
		self.app_font = tkfont.Font(family='fixedsys', size=16, weight="bold")
		self.bg_color = 'black'
		self.fg_color = '#ffff00'

		container = Frame(self, background='#2c3738')
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		container.config(borderwidth=20, relief=GROOVE)

		self.words = w.all_words
		self.good_phrases = w.good_phrases
		self.bad_phrases = w.bad_phrases

		self.frames = {}
		for F in (WelcomePage, PlayPage, WinPage, LostPage):
			
			page_name = F.__name__
			frame = F(parent=container, controller=self)
			self.frames[page_name] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame('WelcomePage')

	def show_frame(self, page_name):
		frame = self.frames[page_name]
		frame.tkraise()



class WelcomePage(Frame):

	'''The start page introducing the game'''

	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller
		self.config(bg=controller.bg_color)

		header = Label(self, text='W E L C O M E\n Guess a planet or a creature from the Star Wars universe', 
			font=controller.app_font, fg=controller.fg_color, bg=controller.bg_color)
		header.pack()

		#ascii art image imported from the separate file
		tie_fighter_image = Label(self, text=a.tie_figther, font=('fixedsys', 9), fg=controller.fg_color, bg=controller.bg_color) 
		tie_fighter_image.pack()

		play_button = Button(self, text='P L A Y', font=controller.app_font, borderwidth=3, fg=controller.fg_color, 
			bg='#2c3738', command=lambda: controller.show_frame('PlayPage'))
		play_button.pack()




class PlayPage(Frame):

	''' The main game page '''

	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller
		self.config(bg=controller.bg_color)

		#the text in this label will change depending on the progress of the game
		self.label = Label(self, text="GUESS A LETTER:", font=controller.app_font, fg=controller.fg_color, bg=controller.bg_color) 
		self.label.pack(side="top", fill="x", pady=10)

		#adding some empty space to separate the widgets
		filler1 = Label(self, text='', bg=controller.bg_color)
		filler1.pack()

		self.random_word = random.choice(controller.words)
		
		# #each user guess will be stored here until the whole word is guessed
		self.user_word = [] 
		self.wrong_guesses = 0
		self.hidden_word = ['_' for i in self.random_word]
		

		#this label shows the word progress and it updates every time the user makes a correct guess
		self.word_display = Label(self, text=self.hidden_word, font=controller.app_font, fg=controller.fg_color, bg=controller.bg_color)
		self.word_display.pack()

		filler2 = Label(self, text='', bg=controller.bg_color)
		filler2.pack()

		#a widget for the user to enter their guess, it then gets stored to be checked
		self.entry_box = Entry(self)
		self.entry_box.pack(pady=10)
		self.user_guess = ''

		filler3 = Label(self, text='', bg=controller.bg_color)
		filler3.pack()

		submit_button = Button(self, text='C H E C K', font=controller.app_font, fg=controller.fg_color, 
			bg='#2c3738', command=lambda: self.check_user_guess(self.user_guess))
		submit_button.pack(pady=10)
        
        #gets the value from the hints dictionary imported through the words module
		self.hint_text = Label(self, text=w.hints.get(self.random_word), font=('fixedsys', 9), fg='black', bg=controller.bg_color) 
		self.hint_text.pack(pady=10)

		hint_button = Button(self, text='H I N T', font=controller.app_font, fg=controller.fg_color, 
			bg='#2c3738', command=lambda:self.display_hint())
		hint_button.pack(side=BOTTOM, pady=10)


	def display_hint(self):
		'''making the hint text appear by changing its font color
		'''
		self.hint_text['fg'] = self.controller.fg_color



	def check_user_guess(self, user_guess): 
		'''Checking each letter entered by the user. Once the full word has been guessed, the WinPage() 
		   is displayed. Or if the player has made too many wrong guesses, the LostPage() is displayed
		'''
		self.user_guess = self.entry_box.get()

		if self.user_guess.title() in self.random_word:
			self.user_word.append(self.user_guess.title())
			self.label['text'] = random.choice(self.controller.good_phrases)
			self.word_progress = [i if i in self.user_word else '_' for i in self.random_word]
			self.word_display['text'] = self.word_progress
		else:
			self.label['text'] = random.choice(self.controller.bad_phrases)
			self.wrong_guesses += 1
		self.entry_box.delete(0, END)

		#checking if the full word has been guessed correctly and the game was won
		if len(self.user_word) == len(set(self.random_word)):
			self.new_game()
			self.controller.show_frame('WinPage')
		
		#checking if too many wrong guesses and the game was lost
		elif self.wrong_guesses > 3:
			self.new_game()
			self.controller.show_frame('LostPage')



	def new_game(self):
		''' This function is called to invoke a new game and clear
		    the data saved from the previous game.This is only after the previous word
		    has been guessed or the game was lost'''

		self.random_word = random.choice(self.controller.words)
		self.user_word = []
		self.wrong_guesses = 0
		self.hidden_word = ['_' for i in self.random_word]
		self.word_display['text'] = self.hidden_word
		self.label['text'] = 'GUESS A LETTER:'
	


class WinPage(Frame):

	def __init__(self,parent,controller):
		Frame.__init__(self,parent)
		self.controller = controller
		self.config(bg='black')

		self.winner = Label(self, text=' WELL DONE PADAWAN!\n YOU HAVE SAVED HAN SOLO!', font=controller.app_font, 
			fg=controller.fg_color, bg=controller.bg_color)
		self.winner.pack()

		self.falcon = Label(self, text=a.falcon, font=('consolas', 10), fg=controller.fg_color, bg=controller.bg_color)
		self.falcon.pack()

		self.menu = Button(self, text='PLAY AGAIN', font=controller.app_font, fg=controller.fg_color, 
			bg='#2c3738', command=lambda: controller.show_frame('WelcomePage'))
		self.menu.pack()



class LostPage(Frame):

	def __init__(self,parent,controller):
		Frame.__init__(self,parent)
		self.controller = controller
		self.config(bg='black')

		self.loser = Label(self, text=' YOU HAVE LOST!\n SOLO WAS HUNG AND HE IS NOT HAPPY!', font=controller.app_font, fg=controller.fg_color, bg=controller.bg_color)
		self.loser.pack()

		# self.hangman = Label(self, text=a.hangman, font=('consolas', 15), fg=controller.fg_color, bg=controller.bg_color)
		# self.hangman.pack()

		self.menu1 = Button(self, text='PLAY AGAIN', font=controller.app_font, borderwidth=3, fg=controller.fg_color, 
			bg='#2c3738', command=lambda: controller.show_frame('WelcomePage'))
		self.menu1.pack()



if __name__ == '__main__':
	app = BaseApp()
	app.geometry('700x500')
	app.mainloop()

