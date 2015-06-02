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

	standardScreen.addstr(1,1,".:: Labyrinthos 3000 ::.".center(screenMaxX-1))
	standardScreen.addstr(2,1,"Frégate Productions".center(screenMaxX-1))
	
	if labyrinthLoadedFlag == True :
		standardScreen.addstr(4,1, "A labyrinth has been loaded :".center(screenMaxX-1))	
		standardScreen.addstr(5,1, fileName.center(screenMaxX-1))
	else :
		standardScreen.addstr(4,1, "Using the default labyrinth.".center(screenMaxX-1))	

	standardScreen.addstr(7,1, "Your target is the red square !".center(screenMaxX-1))
	standardScreen.addstr(8,1, "You can't pass the white walls.".center(screenMaxX-1))
	
	standardScreen.addstr(10,1, "Press any key to start. Once".center(screenMaxX-1))
	standardScreen.addstr(11,1, "in game, use the arrow keys to".center(screenMaxX-1))
	standardScreen.addstr(12,1, "move, and Q (or ^C) to quit.".center(screenMaxX-1))
	

	#TODO : all this really should be in a pad so we don't worry about size problems	

	startGameInput = standardScreen.getch()
	standardScreen.clear()	
	
	#title bar : level name, number of moves

	titleWin = standardScreen.subwin(3, screenMaxX, 0,0)
	titleWin.border()
	if labyrinthLoadedFlag == True :
		titleWin.addstr(1,1, fileName)
	else :
		titleWin.addstr(1,1, "No labyrinth loaded")	
	titleWin.addstr(1, screenMaxX-5, "0")	

	# drawing the labyrinth
	
	#myPad = standardScreen.subpad((screenMaxY-2), (screenMaxX-2), 1, 1)
	#myPad = standardScreen.subpad(levelSizeY+2, levelSizeX+2, 1, 1)
	myPad = standardScreen.subpad(3,1)
	standardScreen.border()

	startCoordSetFlag = False #for the starting position (marked 3 on the level layout)
		
	for y in range(0, levelSizeY) :
		for x in range(0, levelSizeX) :
			if myLabyrinth[y][x] == 1 :
				myPad.addstr(y,x, " ", curses.color_pair(1))
			elif myLabyrinth[y][x] == 0 : 
				myPad.addstr(y,x, " ")
				if startCoordSetFlag == False :
					stardCoordY = y
					startCoordX = x
					# this means that if there isn't a starting position defined, we'll at least be starting somewhere without walls
			elif myLabyrinth[y][x] == 2 :
				myPad.addstr(y,x, " ", curses.color_pair(2))
			elif myLabyrinth[y][x] == 3 :
				myPad.addstr(y,x, " ", curses.color_pair(3))
				startCoordY = y
				startCoordX = x
				startCoordSetFlag = True
	
	# adding boundaries, in case the labyrinth is smaller than the drawing surface
	for y in range(0, (levelSizeY+1)) :
		myPad.addstr(y,levelSizeX, "+", curses.color_pair(4))
	for x in range(0, levelSizeX) :
		myPad.addstr(levelSizeY, x, "+", curses.color_pair(4))	

	#myPad.addstr(1,1,"y")
	#myPad.refresh(0,0,5,5,10,10)
	
	haveWeWonYetFlag = False # because we haven't won yet
	nbMoves=0
	
	xCoord = startCoordX
	yCoord = startCoordY
	
	myPad.addstr(yCoord, xCoord, "x", curses.color_pair(3))

	while True :
		#standardScreen.refresh()

		userInput = standardScreen.getch()

		# erasing the previous position
		if myLabyrinth[yCoord][xCoord] == 0 : 
			myPad.addstr(yCoord, xCoord, " ") 
		elif myLabyrinth[yCoord][xCoord] == 2 :
			myPad.addstr(yCoord, xCoord, " ", curses.color_pair(2))
		elif myLabyrinth[yCoord][xCoord] == 3 :
			myPad.addstr(yCoord, xCoord, " ", curses.color_pair(3))
		
		# going forward
		if userInput == curses.KEY_LEFT and xCoord > 0 :
			if myLabyrinth[yCoord][xCoord-1] != 1 :
				xCoord = xCoord - 1
				if nbMoves < 10000 : #fuck the guy who'll try to crash through excessive movement
					nbMoves = nbMoves+1
		elif userInput == curses.KEY_RIGHT and xCoord < (levelSizeX-1) :
			if myLabyrinth[yCoord][xCoord+1] != 1 : 
				xCoord = xCoord + 1
				if nbMoves < 10000 :
					nbMoves = nbMoves+1
		elif userInput == curses.KEY_DOWN and yCoord < (levelSizeY-1) :
			if myLabyrinth[yCoord+1][xCoord] != 1 : 
				yCoord = yCoord + 1
				if nbMoves < 10000 :
					nbMoves = nbMoves+1
		elif userInput == curses.KEY_UP and yCoord > 0 :
			if myLabyrinth[yCoord-1][xCoord] != 1 : 
				yCoord = yCoord - 1
				if nbMoves < 10000 :
					nbMoves = nbMoves+1
	
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
		


		if myLabyrinth[yCoord][xCoord] == 2 : #yay !
			myPad.addstr(yCoord, xCoord, "x", curses.color_pair(2))			
			myPad.refresh()	
			titleWin.addstr(1, screenMaxX-5, str(nbMoves))
			titleWin.refresh()	
			if haveWeWonYetFlag == False :
				haveWeWonYetFlag = True
				winString0 = "You Won ! Congratulations !"
				winString1 = "You did it in "+str(nbMoves)+" moves !"
				winString2 = "Press Q to quit."
				lengthOfLongestString = max(len(winString0), len(winString1), len(winString2))
				
				youWonWindow = standardScreen.subwin(5, lengthOfLongestString+2 ,floor(screenMaxY/2), floor(screenMaxX/2-(lengthOfLongestString/2)))
				# all that for centering

				 
				youWonWindow.border()
				youWonWindow.addstr(1,1,winString0.center(lengthOfLongestString))
				youWonWindow.addstr(2,1,winString1.center(lengthOfLongestString))
				youWonWindow.addstr(3,1,winString2.center(lengthOfLongestString))
				youWonWindow.refresh()
				if standardScreen.getch() == ord('q') :
					exit()
				youWonWindow.clear()
				youWonWindow.redrawwin()
				youWonWindow.refresh()
				standardScreen.refresh()
		elif myLabyrinth[yCoord][xCoord] == 3 : #that's the spawn point, how ambitious
			myPad.addstr(yCoord, xCoord, "x", curses.color_pair(3))	
		else :
			myPad.addstr(yCoord, xCoord, "x")
		
			
		titleWin.addstr(1, screenMaxX-5, str(nbMoves))
		titleWin.refresh()	
		myPad.refresh()
curses.wrapper(main)
