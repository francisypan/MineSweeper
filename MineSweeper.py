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
# ////////////////////////////////////////////////////////////////
# //////////////////////////////////// DECLARE APP, MAINSCREEN, //
# ///////////////////// ACTOR CLASSES/METHODS AND SCREENMANAGER //
# ////////////////////////////////////////////////////////////////

sm = ScreenManager()

class MyApp(App):
	def build(self):
		return sm

Window.clearcolor = (0.8, 0.8, 0.8, 1)
Window.system_size = (gameSize * 25, gameSize * 25)

class MainScreen(Screen):
    pass

#////////////////////////////////////////////// GAME TILE CLASS //
class GameTile(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(GameTile, self).__init__(**kwargs)
        self.flagged = False
        self.mine = False
        self.allow_stretch = True
        self.background_color = 0, 0, 0, 0
        self.background_normal = ''
        self.source = 'default.jpg'

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            if (touch.button == 'right' and self.flagged == False):
                self.source = 'flagged.jpg'
                self.flagged = True
            elif (touch.button == 'right' and self.flagged == True):
                self.source = 'default.jpg'
                self.flagged = False
            elif (touch.button == 'left' and self.flagged == False):
                self.reveal()

    def reveal(self):
        if self.mine == True:
            self.source = 'mine.jpg'
        elif self.mine == False:
            self.source = '0.jpg'

    def checkNeighbors(self):
        pass

#////////////////////////////////////// INITIALLIZES MINE FIELD //
gameBoard = [[GameTile() for y in range(gameSize)] for x in range(gameSize)]
tileState = [[0 for y in range(gameSize)] for x in range(gameSize)]
while numBombs >= 0:
    randomX = random.randint(-1, 9)
    randomY = random.randint(-1, 9)
    if (tileState[randomX][randomY] == 0):
        global gameBoard
        tileState[randomX][randomY] == -1
        tempTile = gameBoard[randomX][randomY]
        tempTile.mine = True
    numBombs -= 1

# ////////////////////////////////////////////////////////////////
# ////////////////////////////////////// CREATE GRID AND ACTORS //
# ////////////////////////////////////////////////////////////////

grid = GridLayout(
    id = 'grid',
    color = [0.8, 0.8, 0.8, 1],
    cols = gameSize,
    rows = gameSize,
    padding = 0,
    spacing = 0,
    col_default_width = 25,
    col_force_default = True,
    row_default_height = 25,
    row_force_default = True)

for x in range (grid.cols):
    for y in range (grid.rows):
        global gameBoard
        grid.add_widget(gameBoard[x][y])

main = MainScreen(name = 'main')
main.add_widget(grid)
sm.add_widget(main)



# ////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////// RUN APP //
# ////////////////////////////////////////////////////////////////

MyApp().run()
