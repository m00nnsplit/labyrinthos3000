#!/usr/bin/python3

import curses
from sys import argv, stderr
from math import floor
from time import sleep

def errorOutput() :
	# same idea as in the main labyrinth game.. curses blocks output elseway, and I like my errors

	errorType = curses.wrapper(main)
	
	if errorType == "noParameters" :
		stderr.write("No parameters were given. Please, use \""+argv[0]+" help\" to get precisions.\n")
		exit(1)

	if errorType == "getHelp" :
		print("This program is a level editor for the labyrinth game I made.")
		print("Options :")
		print("-f (followed by a string) : name of file to open (overwrites other options)")
		print("-h (followed by a number) : height of a new (blank) level to edit")
		print("-w (followed by a number) : width of a new (blank) level to edit")
		print("Specify both height and width if you wish to edit a blank level !")
		print("-b (followed by a number) : if you are opening a new level, what type of block to fill it with (0 -> pathways, 1 -> walls, defaults to pathways)")
		print("\n Check out the readme/manual for more help !")
		exit()

	if errorType == "readError" :
		stderr.write("Error when reading the arguments.\n\nReminder : you should specify no argument (to edit a blank level) or only one (an existing, valid level file). Maybe did you misspell the name of the file ? You can also call this program with the help argument, or read the readme file.\n\nThis error does not cover an error when parsing the file, only when opening it.\n")
		exit(2)

	else :
		print(errorType)

def main(standardScreen) :
	curses.curs_set(False)
	curses.use_default_colors()


	screenMaxY, screenMaxX = standardScreen.getmaxyx()

	curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE) # walls
	curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)   # objective
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)  # spawn point
	curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)  # boundaries

	curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_GREEN) # cursor for paths
	curses.init_pair(11, curses.COLOR_WHITE, curses.COLOR_GREEN) # cursor for walls
	curses.init_pair(12, curses.COLOR_RED, curses.COLOR_GREEN)   # cursor for objective
	curses.init_pair(13, curses.COLOR_BLUE, curses.COLOR_GREEN)  # cursor for spawn
	
	# Doing argument processing here, because if I have to actually use one of the arguments passing it to the function would be annoying
	if len(argv) == 1 :
		return("noParameters")
	if argv.count("help") > 0 :
		return("getHelp")	

	if argv.count("-f") > 0 :
		fileName = argv[argv.index("-f")+1]

		try :
			fileStream = open(fileName)
		except OSError as readError :
			return("readError")

		workingLine="--"
		myLabyrinth = []
		labyHeight = 0
		labyWidth = 0
		while workingLine != "" :
			workingLine = fileStream.readline().strip()
			if workingLine == "" :
				break # no seriously, else there's a last line with only a \n
			newLabyLine = []
			for i in range(len(workingLine)) :
				newLabyLine.append(int(workingLine[i]))
				if len(newLabyLine) > labyWidth :
					labyWidth = len(newLabyLine)
			myLabyrinth.append(newLabyLine)
			labyHeight = labyHeight + 1
		fileStream.close()
		labyrinthLoadedFlag = True
	else :
		fileName = "a.laby" # name for what we'll save in case nothing got opened

	if argv.count("-h") > 0 and argv.count("-w") > 0 :
		labyHeight = int(argv[argv.index("-h")+1])
		labyWidth = int(argv[argv.index("-w")+1])
		
		if argv.count("-b") > 0 :
			typeOfBlockToFillWith = int(argv[argv.index("-b")+1])
		else :
			typeOfBlockToFillWith = 0

		myLabyrinth = []

		for y in range(labyHeight) :
		        newLabyLine = []
		        for x in range(labyWidth) :
       		 	        newLabyLine.append(typeOfBlockToFillWith)
		        myLabyrinth.append(newLabyLine)

		labyrinthLoadedFlag = False


	# alright so now we've got our labyrinth parsed/generated..

	#window with instructions : "you are.. to .. press .."
	titleWin = standardScreen.subwin(4, screenMaxX, screenMaxY-4,0)
	titleWin.border()
	if labyrinthLoadedFlag == True :
		titleWin.addstr(1,1, "Editing "+fileName)
	else :
		titleWin.addstr(1,1, "Editing new labyrinth")	
	
	#TODO : add commands and all. Context-sensitive-help ?
	

	# drawing the labyrinth
	
	myPad = curses.newpad(labyHeight+100, labyWidth+100) #TODO : for now the cursor can get out of the pad and crash the program.. This should not be possible, add a check or boundaries or something 
	standardScreen.border()

	startCoordSetFlag = False #for the starting position (marked 3 on the level layout)
		
	for y in range(0, labyHeight) :
		for x in range(0, labyWidth) :
			if myLabyrinth[y][x] == 1 :
				myPad.addstr(y,x, " ", curses.color_pair(1))
			elif myLabyrinth[y][x] == 0 : 
				myPad.addstr(y,x, " ")
			elif myLabyrinth[y][x] == 2 :
				myPad.addstr(y,x, " ", curses.color_pair(2))
			elif myLabyrinth[y][x] == 3 :
				myPad.addstr(y,x, " ", curses.color_pair(3))
	

	# placing the cursor
	yCoord = 0
	xCoord = 0

	
	myPad.addstr(yCoord,xCoord, "x", curses.color_pair(int("1"+str(myLabyrinth[yCoord][xCoord])))) #yeah.. not super pretty.. but I didn't feel like doing all the ifs	
	standardScreen.refresh()
	myPad.refresh(int(yCoord-((screenMaxY-5)/2)), int(xCoord-((screenMaxX-3)/2)), 3, 1, screenMaxY-5, screenMaxX-2)	

	while True :	
		userInput = standardScreen.getch()

		# erasing the previous position
		if yCoord>=labyHeight or xCoord>=labyWidth :
			myPad.addstr(yCoord, xCoord, " ")
		elif myLabyrinth[yCoord][xCoord] == 0 :
			myPad.addstr(yCoord, xCoord, " ")
		else :
			myPad.addstr(yCoord, xCoord, " ", curses.color_pair(myLabyrinth[yCoord][xCoord])) # so yeah, in case you hadn't gotten it, it works because there's a correspondance between the color pairs and terrain codes ; both were set by the same person, you see.
	
		# obviously we don't give a damn about walls, we're in a level editor
		if userInput == curses.KEY_LEFT and xCoord > 0 :
			xCoord = xCoord -1
		if userInput == curses.KEY_RIGHT and xCoord < screenMaxX :
			xCoord = xCoord +1
		if userInput == curses.KEY_UP and yCoord > 0 :
			yCoord = yCoord -1
		if userInput == curses.KEY_DOWN and yCoord < screenMaxY :
			yCoord = yCoord +1	

		if userInput == ord(' ') : #spacebar is "switch" key : path to wall and wall to path
			if yCoord<labyHeight and xCoord<labyWidth :
				if myLabyrinth[yCoord][xCoord] == 0 :
					myLabyrinth[yCoord][xCoord] = 1
					titleWin.addstr(2,1,"Switched square (y="+str(yCoord)+";x="+str(xCoord)+")")
				elif myLabyrinth[yCoord][xCoord] == 1 :
					myLabyrinth[yCoord][xCoord] = 0
					titleWin.addstr(2,1,"Switched square (y="+str(yCoord)+";x="+str(xCoord)+")")
				titleWin.refresh()
		
		if userInput == ord('r') or userInput == ord('R') : # allows to select any block
			if yCoord<labyHeight and xCoord<labyWidth :
				titleWin.addstr(2,1, "(y="+str(yCoord)+";x="+str(xCoord)+") Press S for spawn, O for objective, W for wall, P for path.")
				titleWin.refresh()
				secondInput = standardScreen.getch()
				if secondInput == ord('s') or secondInput == ord('S') :
					myLabyrinth[yCoord][xCoord] = 3
					titleWin.addstr(2,1,"Changed square (y="+str(yCoord)+";x="+str(xCoord)+") to spawn point.")
				elif secondInput == ord('o') or secondInput == ord('O') :
					myLabyrinth[yCoord][xCoord] = 2
					titleWin.addstr(2,1,"Changed square (y="+str(yCoord)+";x="+str(xCoord)+") to objective.")
				elif secondInput == ord('w') or secondInput == ord('W') :
					myLabyrinth[yCoord][xCoord] = 1
					titleWin.addstr(2,1,"Changed square (y="+str(yCoord)+";x="+str(xCoord)+") to wall.")
				elif secondInput == ord('p') or secondInput == ord('P') :
					myLabyrinth[yCoord][xCoord] = 0
					titleWin.addstr(2,1,"Changed square (y="+str(yCoord)+";x="+str(xCoord)+") to pathway.")
				titleWin.refresh()			

		if userInput == ord('s') or userInput == ord('S') : # save function !
			saveString0 = "The saved file name will be :"
			saveString1 = "Are you sure you want to save ?"
			saveString2 = "Press Y to confirm, or N to cancel."
			
			lengthOfLongestString = max(len(winString0), len(winString1), len(winString2))
			saveWindow = standardScreen.subwin(6, lengthOfLongestString+2 ,floor(screenMaxY/2), floor(screenMaxX/2-(lengthOfLongestString/2)))
			# good thing I had already done that once
			saveWindow.border()
			saveWindow.addstr(1,1,saveString0.center(lengthOfLongestString))
			saveWindow.addstr(2,1,fileName.center(lengthOfLongestString))
			saveWindow.addstr(3,1,saveString1.center(lengthOfLongestString))
			saveWindow.addstr(4,1,saveString2.center(lengthOfLongestString))

			youWonWindow.refresh()
			sleep(0.5) # no seriously, it *is* a good idea !
			secondInput = standardScreen.getch()
			if secondInput == ord('y') or secondInput == ord('Y') :
				#TODO :save function	
			#elif secondInput == ord('n') or secondInput == ord('N') :
			

		if userInput == ord('q') or userInput == ord('Q') :
			exit()	
		#TODO : process curses.KEY_RESIZE
	

		# drawing the new cursor

		if yCoord<labyHeight and xCoord<labyWidth :
			myPad.addstr(yCoord, xCoord, "x", curses.color_pair(int("1"+str(myLabyrinth[yCoord][xCoord]))))
		else : # out of level bounds
			myPad.addstr(yCoord, xCoord, "x", curses.color_pair(4))

		standardScreen.refresh()
		myPad.refresh(int(yCoord-((screenMaxY-5)/2)), int(xCoord-((screenMaxX-3)/2)), 3, 1, screenMaxY-5, screenMaxX-2)	


errorOutput()	





