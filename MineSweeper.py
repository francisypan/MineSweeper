# ////////////////////////////////////////////////////////////////
# /////////////////////////////////////////// IMPORT STATEMENTS //
# ////////////////////////////////////////////////////////////////

from kivy.app import App
from kivy.uix import togglebutton
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import *
from kivy.uix.behaviors import ButtonBehavior

import random
# ////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////// GLOBALS //
# ////////////////////////////////////////////////////////////////

gameSize = 10
numBombs = 10
numFlagged = 0
numCorrect = 0
gameWon = False
# ////////////////////////////////////////////////////////////////
# //////////////////////////////////// DECLARE APP, MAINSCREEN, //
# ///////////////////// ACTOR CLASSES/METHODS AND SCREENMANAGER //
# ////////////////////////////////////////////////////////////////

sm = ScreenManager()

class MinesweeperApp(App):
	def build(self):
		return sm

Window.clearcolor = (0.8, 0.8, 0.8, 1)
Window.system_size = (10 + gameSize * 25, 55 + gameSize * 25)
Window.set_icon ('mine.jpg')
Builder.load_file('MineSweeper.kv')

class GameScene(Screen):
	def buttonDown(self):
		self.ids.resetButton.source = '-1.jpg'

	def resetGame(self):
		resetBoard()

	def buttonUp(self):
		global gameWon
		if (gameWon == False):
			self.ids.resetButton.source = 'reset.jpg'

		else:
			self.ids.resetButton.source = 'flagged.jpg'

# ////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////// METHODS //
# ////////////////////////////////////////////////////////////////

# /////////////////////// ADDS DESIRED NUMBER OF BOMBS TO BOARD //
def addBombs():
	global numBombs
	global tileStates
	bombsLeft = numBombs
	while bombsLeft > 0:
		addBomb()
		bombsLeft -= 1
# ///////////////// RANDOMLY ADDS A BOMB TO AN UNOCCCUPIED TILE //
def addBomb():
	global tileStates
	global gameBoard
	randX = random.randint(-1, gameSize - 1)
	randY = random.randint(-1, gameSize - 1)
	if (tileStates[randX][randY] == 0):
		tileStates[randX][randY] = -1
		gameBoard[randX][randY].tileStatus = -1
	else:
		addBomb()
# /////////////////////////// FILLS BOARD WITH REQUIRED NUMBERS //
def fillBoard():
	global tileStates
	for x in range(gameSize):
		for y in range(gameSize):
			if (tileStates[x][y] == -1):
				trySetTile(x - 1, y - 1)
				trySetTile(x - 1, y)
				trySetTile(x - 1, y + 1)
				trySetTile(x, y - 1)
				trySetTile(x, y + 1)
				trySetTile(x + 1, y - 1)
				trySetTile(x + 1, y)
				trySetTile(x + 1, y + 1)
# ///////////////////////////// UPDATES THE STATUS OF ONE TILE //
def trySetTile(x, y):
	global tileStates
	global gameBoard
	if (x > gameSize - 1 or x < 0 or y > gameSize - 1 or y < 0 or tileStates[x][y] == -1):
		return # // Takes care of index out of bounds or if the tile is a mine
	else:
		tileStates[x][y] += 1
		gameBoard[x][y].tileStatus = tileStates[x][y]

def checkNeighbors(pos):
	x, y = pos
	tileCheck(x - 1, y - 1)
	tileCheck(x - 1, y)
	tileCheck(x - 1, y + 1)
	tileCheck(x, y - 1)
	tileCheck(x, y + 1)
	tileCheck(x + 1, y - 1)
	tileCheck(x + 1, y)
	tileCheck(x + 1, y + 1)

def tileCheck(x, y):
	global gameBoard
	global tileStates
	if (x > gameSize - 1 or x < 0 or y > gameSize - 1 or y < 0 or tileStates[x][y] == -1 or gameBoard[x][y].revealed == True):
		return
	elif (tileStates[x][y] == 0):
		gameBoard[x][y].source = str(tileStates[x][y]) + '.jpg'
		gameBoard[x][y].revealed = True
		pos = x, y
		checkNeighbors(pos)
	else:
		gameBoard[x][y].source = str(tileStates[x][y]) + '.jpg'
		gameBoard[x][y].revealed = True

def loseGame():
	revealAllMines()

def checkWin():
	global gameBoard
	global numBombs
	global numCorrect
	for x in range (gameSize):
	    for y in range (gameSize):
			if (gameBoard[x][y].flagged == True and gameBoard[x][y].tileStatus == -1):
				numCorrect += 1
	if (numCorrect == numBombs):
		win()
	else:
		numCorrect = 0

def revealAllMines():
	global gameBoard
	global tileStates
	for x in range(gameSize):
		for y in range(gameSize):
			if (gameBoard[x][y].flagged == True and gameBoard[x][y].tileStatus != -1):
				gameBoard[x][y].source = 'wrongFlag.jpg'
			elif (gameBoard[x][y].revealed == False and gameBoard[x][y].tileStatus == -1 and gameBoard[x][y].flagged == False):
				gameBoard[x][y].source = '-1.jpg'
			gameBoard[x][y].revealed = True

def resetBoard():
	global gameBoard
	global tileStates
	global numFlagged
	global numCorrect
	global gameWon
	numFlagged = 0
	numCorrect = 0
	gameWon = False
	for x in range (gameSize):
	    for y in range (gameSize):
			gameBoard[x][y].source = 'default.jpg'
			gameBoard[x][y].revealed = False
			gameBoard[x][y].flagged = False
			gameBoard[x][y].tileStatus = 0
			tileStates[x][y] = 0
	createBoard()

def createBoard():
	addBombs()
	fillBoard()

def win():
	global gameWon
	gameWon = True
	sm.current_screen.ids.resetButton.source = 'flagged.jpg'

#////////////////////////////////////////////// GAME TILE CLASS //
class GameTile(ButtonBehavior, Image):
	def __init__(self, **kwargs):
		super(GameTile, self).__init__(**kwargs)
		self.revealed = False
		self.flagged = False
		self.tileStatus = 0
		self.tilePos = 0, 0
		self.allow_stretch = True
		self.background_color = 0, 0, 0, 0
		self.background_normal = ''
		self.source = 'default.jpg'

	def on_touch_down(self, touch):
		global numFlagged
		if self.collide_point(touch.x, touch.y):
			if (touch.button == 'right' and self.flagged == False and self.revealed == False):
				self.source = 'flagged.jpg'
				self.flagged = True
				numFlagged += 1
				if (numFlagged == numBombs):
					checkWin()
			elif (touch.button == 'right' and self.flagged == True and self.revealed == False):
				self.source = 'default.jpg'
				self.flagged = False
				numFlagged -=1
			elif (touch.button == 'left' and self.flagged == False and self.revealed == False):
				self.reveal(self.tileStatus)

	def reveal(self, tileStatus):
		self.source = str(tileStatus) + '.jpg'
		self.revealed = True
		if (tileStatus == -1):
			self.source = 'whoops.jpg'
			loseGame()
		if (tileStatus == 0):
			checkNeighbors(self.tilePos)

#////////////////////////////////////// INITIALLIZES MINE FIELD //

gameBoard = [[GameTile() for y in range(gameSize)] for x in range(gameSize)]
tileStates = [[0 for y in range(gameSize)] for x in range(gameSize)]
createBoard()

# ////////////////////////////////////////////////////////////////
# ////////////////////////////////////// CREATE GRID AND ACTORS //
# ////////////////////////////////////////////////////////////////

grid = GridLayout(
    id = 'grid',
    cols = gameSize,
    rows = gameSize,
    padding = [5, 50, 5, 5],
    spacing = 0,
    col_default_width = 25,
    col_force_default = True,
    row_default_height = 25,
    row_force_default = True)

for x in range (gameSize):
    for y in range (gameSize):
		global gameBoard
		gameBoard[x][y].tilePos = x, y
		grid.add_widget(gameBoard[x][y])

game = GameScene(name = 'game')
game.add_widget(grid)
sm.add_widget(game)

# ////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////// RUN APP //
# ////////////////////////////////////////////////////////////////

MinesweeperApp().run()
