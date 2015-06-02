# using python 3
# more ncurses
# I'm trying to do a labyrinth game here

import curses
from math import floor
from sys import argv

def main(standardScreen) :
	curses.curs_set(False)
	curses.use_default_colors()

	screenMaxY, screenMaxX = standardScreen.getmaxyx()

	curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE) # walls
	curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED) # objective
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE) # spawn point
	curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK) # boundaries
	


	#TODO : function to read levels and such from a file !
	# files will contain size & schematics for level
	# labyrinths (2D grids) are to be represented as 2D tables
	# 0 is a path, 1 is a wall, 2 is the objective, 3 is the spawn point
	if len(argv) == 1 :
		labyrinthLoadedFlag = False
		myLabyrinth = [
			[0,1,3,1,0,0,0,0,1,0],
			[0,1,0,1,0,0,0,1,1,0],
			[0,1,0,0,0,1,0,0,0,0],
			[0,1,1,1,1,1,0,1,1,1],
			[0,0,0,0,0,0,0,0,0,0],
			[0,1,0,1,1,1,1,0,0,0],
			[1,1,0,1,0,0,1,0,0,0],
			[0,0,0,1,0,1,1,0,1,0],
			[0,1,0,0,0,1,0,0,1,0],
			[0,1,0,1,0,2,0,1,1,0],
			]

		levelSizeY = 10
		levelSizeX = 10	
	
	else :
		# that's where the fun begins
		# we'll only be reading the first argument
		labyrinthLoadedFlag = True
		fileName = argv[1]
		fileStream = open(fileName)
		workingLine="--"
		myLabyrinth = []
		levelSizeY = 0
		levelSizeX = 0
		while workingLine != "" :
			workingLine = fileStream.readline().strip()
			if workingLine == "" :
				break # no seriously, else there's a last line with only a \n
			newLabyLine = []
			for i in range(len(workingLine)) :
				newLabyLine.append(int(workingLine[i]))
				if len(newLabyLine) > levelSizeX :
					levelSizeX = len(newLabyLine)
			myLabyrinth.append(newLabyLine)
			levelSizeY = levelSizeY + 1 
		fileStream.close()
		

	# greetings

	standardScreen.addstr(1,1,".:: Labyrinthos 3000 ::.".center(30))
	standardScreen.addstr(2,1,"Frégate Productions".center(30))
	
	if labyrinthLoadedFlag == True :
		standardScreen.addstr(4,1, "A labyrinth has been loaded !".center(30))	
		standardScreen.addstr(5,1, fileName.center(30))
	else :
		standardScreen.addstr(4,1, "Using default labyrinth.".center(30))	

	standardScreen.addstr(7,1, "Your target is the red square !".center(30))
	standardScreen.addstr(8,1, "You can't pass the white walls.".center(30))
	
	standardScreen.addstr(10,1, "Press any key to start. Once".center(30))
	standardScreen.addstr(11,1, "in game, use the arrow keys to".center(30))
	standardScreen.addstr(12,1, "move, and Q (or ^C) to quit.".center(30))
	

	#TODO : all this really should be in a pad so we don't worry about size problems	

	startGameInput = standardScreen.getch()
	standardScreen.clear()	
	# drawing the labyrinth
	
	#myPad = standardScreen.subpad((screenMaxY-2), (screenMaxX-2), 1, 1)
	myPad = standardScreen.subpad(levelSizeY+2, levelSizeX+2, 1, 1)
	standardScreen.border()

	startCoordSetFlag = False #for the starting position (marked 3)
		
	for y in range(0, levelSizeY) :
		for x in range(0, levelSizeX) :
			if myLabyrinth[y][x] == 1 :
				myPad.addstr(y,x, " ", curses.color_pair(1))
			elif myLabyrinth[y][x] == 0 : 
				myPad.addstr(y,x, " ")
				if startCoordSetFlag == False :
					stardCoordY = y+1
					startCoordX = x+1
					# this means that if there isn't a starting position defined, we'll at least be starting somewhere without walls
			elif myLabyrinth[y][x] == 2 :
				myPad.addstr(y,x, " ", curses.color_pair(2))
			elif myLabyrinth[y][x] == 3 :
				myPad.addstr(y,x, " ", curses.color_pair(3))
				startCoordY = y+1
				startCoordX = x+1
				startCoordSetFlag = True
	
	# adding boundaries, in case the labyrinth is smaller than the drawing surface
	for y in range(0, (levelSizeY+1)) :
		myPad.addstr(y,levelSizeX, "+", curses.color_pair(4))
	for x in range(0, levelSizeX) :
		myPad.addstr(levelSizeY, x, "+", curses.color_pair(4))	

	#myPad.addstr(1,1,"y")
	#myPad.refresh(0,0,5,5,10,10)
	
	xCoord = startCoordX
	yCoord = startCoordY
	
	standardScreen.addstr(yCoord, xCoord, "x", curses.color_pair(3))

	while True :
		standardScreen.refresh()

		userInput = standardScreen.getch()

		# erasing the previous position
		if myLabyrinth[yCoord-1][xCoord-1] == 0 : 
			standardScreen.addstr(yCoord, xCoord, " ") 
		elif myLabyrinth[yCoord-1][xCoord-1] == 2 :
			standardScreen.addstr(yCoord, xCoord, " ", curses.color_pair(2))
		elif myLabyrinth[yCoord-1][xCoord-1] == 3 :
			standardScreen.addstr(yCoord, xCoord, " ", curses.color_pair(3))

		# "-1"s everywhere because curses thinks we are at (1;1) but the table is indexed from 0 
		if userInput == curses.KEY_LEFT and xCoord > 1 :
			if myLabyrinth[yCoord-1][xCoord-1-1] != 1 :
				xCoord = xCoord - 1
		elif userInput == curses.KEY_RIGHT and xCoord < (screenMaxX - 2) and xCoord < levelSizeX :
			if myLabyrinth[yCoord-1][xCoord-1+1] != 1 : 
				xCoord = xCoord + 1
		elif userInput == curses.KEY_DOWN and yCoord < (screenMaxY - 2) and yCoord < levelSizeY :
			if myLabyrinth[yCoord-1+1][xCoord-1] != 1 : 
				yCoord = yCoord + 1
		elif userInput == curses.KEY_UP and yCoord > 1 :
			if myLabyrinth[yCoord-1-1][xCoord-1] != 1 : 
				yCoord = yCoord - 1
	
		elif userInput == curses.KEY_RESIZE :
			screenMaxY, screenMaxX = standardScreen.getmaxyx()
			standardScreen.clear()
			#myPad = standardScreen.subpad((screenMaxY-2), (screenMaxX-2), 1, 1)
			#myPad = standardScreen.subpad(levelSizeY+2, levelSizeX+2, 1, 1)
			#myPad.refresh(1,1,1,1, screenMaxY-1, screenMaxX-1)
			myPad.refresh()
			standardScreen.border()
			for y in range(0, (levelSizeY)) :
				for x in range(0, (levelSizeX)) :
					if myLabyrinth[y][x] == 1 :
						myPad.addstr(y,x, " ", curses.color_pair(1))
					elif myLabyrinth[y][x] == 0 : 
						myPad.addstr(y,x, " ")
					elif myLabyrinth[y][x] == 2 :
						myPad.addstr(y,x, " ", curses.color_pair(2))
					elif myLabyrinth[y][x] == 3 :
						myPad.addstr(y,x, " ", curses.color_pair(3))
				
			for y in range(0, (levelSizeY+1)) :
				myPad.addstr(y,levelSizeX, "+", curses.color_pair(4))
			for x in range(0, levelSizeX) :
				myPad.addstr(levelSizeY, x, "+", curses.color_pair(4))	

			if xCoord > (screenMaxX - 2) or yCoord > (screenMaxY - 2) :
				xCoord = startCoordX 
				yCoord = startCoordY # back to the start case
				#TODO : a pad can have more than it can display at once.. work on this so that the labyrinths can have sizes superior to the window size					

		elif userInput == ord("q") : # we totally can quit this
			break

		else :
			pass
		


		if myLabyrinth[yCoord-1][xCoord-1] == 2 : #yay !
			winString = "You Won ! Congratulations !"
			youWonWindow = standardScreen.subwin(3, len(winString)+2 ,floor(screenMaxY/2), floor(screenMaxX/2-(len(winString)/2))) 
			youWonWindow.border()
			youWonWindow.addstr(1,1,winString)
			youWonWindow.refresh()
			standardScreen.addstr(yCoord, xCoord, "x", curses.color_pair(2))			
		elif myLabyrinth[yCoord-1][xCoord-1] == 3 : #that's the spawn point, how ambitious
			standardScreen.addstr(yCoord, xCoord, "x", curses.color_pair(3))	
		else :
			standardScreen.addstr(yCoord, xCoord, "x")
		
curses.wrapper(main)
