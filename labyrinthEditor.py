#!/usr/bin/python3

import curses
from sys import argv, stderr
from os.path import exists
from math import floor
from time import sleep
from labyrinthLibrary import *

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
	
	labyrinthLoadedFlag = False
	# Doing argument processing here, because if I have to actually use one of the arguments passing it to the function would be annoying
	if len(argv) == 1 :
		#return("noParameters")
		# eh, that was kinda dickish
		
		warnString0 = "Warning : no arguments were given."
		warnString1 = "Execute \""+argv[0]+" help\" for more info."
		warnString2 = "Press any key to close this window."
		
		lengthOfLongestString = max(len(warnString0),len(warnString1),len(warnString2))
		warnWindow = standardScreen.subwin(5, lengthOfLongestString+2,floor(screenMaxY/2), floor(screenMaxX/2-(lengthOfLongestString/2)))
		warnWindow.border()
		warnWindow.addstr(1,1,warnString0.center(lengthOfLongestString))
		warnWindow.addstr(2,1,warnString1.center(lengthOfLongestString))
		warnWindow.addstr(3,1,warnString2.center(lengthOfLongestString))

		warnWindow.refresh()
		sleep(0.5)
		standardScreen.getch()
		warnWindow.clear()
		warnWindow.redrawwin()
		warnWindow.refresh()
		standardScreen.refresh()
		labyrinthLoadedFlag = False

	if len(argv) == 2 :
		# if we're using -f, there will be three or more. So if there are exactly two it's either "help" or a filename
		if argv.count("help") > 0 :
			return("getHelp")	
		else : #prob a fileName
			fileName = argv[1]
			if exists(fileName) : # else well we'll just save to that

				myLabyrinth = Labyrinth(fileName)
				labyrinthLoadedFlag = True		
			else :
				labyrinthLoadedFlag = False	

	if argv.count("-f") > 0 :
		fileName = argv[argv.index("-f")+1]
		if exists(fileName) :
			myLabyrinth = Labyrinth(fileName)
			labyrinthLoadedFlag = True
		else :
			labyrinthLoadedFlag = False
				
	if labyrinthLoadedFlag == False :
		myLabyrinth = Labyrinth()
		myLabyrinth.highscores = []
		myLabyrinth.name = "Edited labyrinth"
		myLabyrinth.author = "Labyrinth editor"
		
		
		if argv.count("-h") > 0 :
			myLabyrinth.levelSizeY = int(argv[argv.index("-h")+1])
		else :
			myLabyrinth.levelSizeY = 20
		if argv.count("-w") > 0 :
			myLabyrinth.levelSizeX = int(argv[argv.index("-w")+1])
		else :
			myLabyrinth.levelSizeX = 20	
		
		if argv.count("-b") > 0 :
			typeOfBlockToFillWith = int(argv[argv.index("-b")+1])
		else :
			typeOfBlockToFillWith = 0
		
		myLabyrinth.levelMap = []

		for y in range(myLabyrinth.levelSizeY) :
			newLabyLine = []
			for x in range(myLabyrinth.levelSizeX) :
				newLabyLine.append(typeOfBlockToFillWith)
			myLabyrinth.levelMap.append(newLabyLine)

		try :
			fileName
		except NameError :
			fileName = "a.laby" # name for what we'll save in case nothing got opened



	
	# alright so now we've got our labyrinth parsed/generated..

	#window with instructions : "you are.. to .. press .."
	titleWin = standardScreen.subwin(4, screenMaxX, screenMaxY-4,0)
	titleWin.border()
	if labyrinthLoadedFlag == True :
		titleWin.addstr(1,1, "Editing "+fileName)
	else :
		titleWin.addstr(1,1, "Editing new labyrinth")	
	titleWin.addstr(2,1,"Press H for help")	
	

	# drawing the labyrinth
	
	myPad = curses.newpad(myLabyrinth.levelSizeY+100, myLabyrinth.levelSizeX+100)
	standardScreen.border()

	startCoordSetFlag = False #for the starting position (marked 3 on the level layout)
		
	for y in range(0, myLabyrinth.levelSizeY) :
		for x in range(0, myLabyrinth.levelSizeX) :
			if myLabyrinth.levelMap[y][x] == 1 :
				myPad.addstr(y,x, " ", curses.color_pair(1))
			elif myLabyrinth.levelMap[y][x] == 0 : 
				myPad.addstr(y,x, " ")
			elif myLabyrinth.levelMap[y][x] == 2 :
				myPad.addstr(y,x, " ", curses.color_pair(2))
			elif myLabyrinth.levelMap[y][x] == 3 :
				myPad.addstr(y,x, " ", curses.color_pair(3))
	

	# placing the cursor
	yCoord = 0
	xCoord = 0

	
	myPad.addstr(yCoord,xCoord, "x", curses.color_pair(int("1"+str(myLabyrinth.levelMap[yCoord][xCoord])))) #yeah.. not super pretty.. but I didn't feel like doing all the ifs	
	standardScreen.refresh()
	myPad.refresh(int(yCoord-((screenMaxY-5)/2)), int(xCoord-((screenMaxX-3)/2)), 1, 1, screenMaxY-5, screenMaxX-2)	

	while True :	
		userInput = standardScreen.getch()

		# erasing the previous position
		if yCoord>=myLabyrinth.levelSizeY or xCoord>=myLabyrinth.levelSizeX :
			myPad.addstr(yCoord, xCoord, " ")
		elif myLabyrinth.levelMap[yCoord][xCoord] == 0 :
			myPad.addstr(yCoord, xCoord, " ")
		else :
			myPad.addstr(yCoord, xCoord, " ", curses.color_pair(myLabyrinth.levelMap[yCoord][xCoord])) # so yeah, in case you hadn't gotten it, it works because there's a correspondance between the color pairs and terrain codes ; both were set by the same person, you see.
	
		# obviously we don't give a damn about walls, we're in a level editor
		if userInput == curses.KEY_LEFT and xCoord > 0 :
			xCoord = xCoord -1
		if userInput == curses.KEY_RIGHT and xCoord < myLabyrinth.levelSizeX+99: # +99 because when creating the pad its dimension are those of the level +100
			xCoord = xCoord +1
		if userInput == curses.KEY_UP and yCoord > 0 :
			yCoord = yCoord -1
		if userInput == curses.KEY_DOWN and yCoord < myLabyrinth.levelSizeY+99 :
			yCoord = yCoord +1	

		if userInput == ord(' ') : #spacebar is "switch" key : path to wall and wall to path
			if yCoord<myLabyrinth.levelSizeY and xCoord<myLabyrinth.levelSizeX :
				if myLabyrinth.levelMap[yCoord][xCoord] == 0 :
					myLabyrinth.levelMap[yCoord][xCoord] = 1
					titleWin.addstr(2,1,("Switched square (y="+str(yCoord)+";x="+str(xCoord)+")").ljust(screenMaxX-2))
				elif myLabyrinth.levelMap[yCoord][xCoord] == 1 :
					myLabyrinth.levelMap[yCoord][xCoord] = 0
					titleWin.addstr(2,1,("Switched square (y="+str(yCoord)+";x="+str(xCoord)+")").ljust(screenMaxX-2))
				titleWin.refresh()
		
		if userInput == ord('r') or userInput == ord('R') : # allows to select any block
			if yCoord<myLabyrinth.levelSizeY and xCoord<myLabyrinth.levelSizeX :
				titleWin.addstr(2,1, ("(y="+str(yCoord)+";x="+str(xCoord)+") Press S for spawn, O for objective, W for wall, P for path.").ljust(screenMaxX-2))
				titleWin.refresh()
				secondInput = standardScreen.getch()
				if secondInput == ord('s') or secondInput == ord('S') :
					myLabyrinth.levelMap[yCoord][xCoord] = 3
					titleWin.addstr(2,1,("Changed square (y="+str(yCoord)+";x="+str(xCoord)+") to spawn point.").ljust(screenMaxX-2))
				elif secondInput == ord('o') or secondInput == ord('O') :
					myLabyrinth.levelMap[yCoord][xCoord] = 2
					titleWin.addstr(2,1,("Changed square (y="+str(yCoord)+";x="+str(xCoord)+") to objective.").ljust(screenMaxX-2))
				elif secondInput == ord('w') or secondInput == ord('W') :
					myLabyrinth.levelMap[yCoord][xCoord] = 1
					titleWin.addstr(2,1,("Changed square (y="+str(yCoord)+";x="+str(xCoord)+") to wall.").ljust(screenMaxX-2))
				elif secondInput == ord('p') or secondInput == ord('P') :
					myLabyrinth.levelMap[yCoord][xCoord] = 0
					titleWin.addstr(2,1,("Changed square (y="+str(yCoord)+";x="+str(xCoord)+") to pathway.").ljust(screenMaxX-2))
				else :
					titleWin.addstr(2,1,"No changes made.".ljust(screenMaxX-2))
				titleWin.refresh()			
	
		if userInput == ord('b') or userInput == ord('B') :
		# this is the brush tool. This simply means that everywhere you get on while it is active will be changed to the selected brush's
		# TODO brush sizes

			titleWin.addstr(2,1,"Entering brush mode. P for path brush, W walls, O objs, S spawns.".ljust(screenMaxX-2))
			titleWin.refresh()

			secondInput = standardScreen.getch()
			
			if secondInput == ord('p') or secondInput == ord('P') :
				terrainToFillWith = 0
				titleWin.addstr(2,1,"Brush mode active, painting paths.".ljust(screenMaxX-2))
			elif secondInput == ord('w') or secondInput == ord('W') :
				terrainToFillWith = 1
				titleWin.addstr(2,1,"Brush mode active, painting walls.".ljust(screenMaxX-2))
			elif secondInput == ord('o') or secondInput == ord('O') :
				terrainToFillWith = 2
				titleWin.addstr(2,1,"Brush mode active, painting objectives.".ljust(screenMaxX-2))
			elif secondInput == ord('s') or secondInput == ord('S') :
				terrainToFillWith = 3
				titleWin.addstr(2,1,"Brush mode active, painting spawns.".ljust(screenMaxX-2))
			else :
				terrainToFillWith = "exit"
				titleWin.addstr(2,1,"Exiting brush mode.".ljust(screenMaxX-2))
				
			titleWin.refresh()
			# alright so now I just GOT to complain about Python
			# "I have "+3+" oranges" crashes your program because oh god silent conversion this is awful !!!1!!
			# but 0 == False ? No problem at all ! Who cares about that ?
			# so yeah, I used False for exiting brush mode and paths (0) got taken as exits
			if terrainToFillWith != "exit" : 
				nbOfSquaresPainted = 0
				terrainWasPaintedLastTurn = False
				while True :
					#erasing last position
					if terrainWasPaintedLastTurn :
						if terrainToFillWith == 0 :
							myPad.addstr(yCoord,xCoord, " ")
						else :
							myPad.addstr(yCoord,xCoord, " ", curses.color_pair(terrainToFillWith))
					else :
						myPad.addstr(yCoord,xCoord, " ")

					terrainWasPaintedLastTurn = False
					secondInput = standardScreen.getch()
					if secondInput == curses.KEY_LEFT :
						xCoord = xCoord -1
					elif secondInput == curses.KEY_RIGHT :
						xCoord = xCoord +1
					elif secondInput == curses.KEY_UP :
						yCoord = yCoord -1
					elif secondInput == curses.KEY_DOWN :
						yCoord = yCoord +1	
					else :
						titleWin.addstr(2,1,("Exiting brush mode after painting "+str(nbOfSquaresPainted)+" squares.").ljust(screenMaxX-2))
						titleWin.refresh()
						break


					if xCoord>0 and yCoord>0 and xCoord< myLabyrinth.levelSizeX and yCoord < myLabyrinth.levelSizeY :
						myLabyrinth.levelMap[yCoord][xCoord] = terrainToFillWith
						#myPad.addstr(yCoord,xCoord, "x", curses.color_pair(int("1"+str(myLabyrinth.levelMap[yCoord][xCoord]))))
						terrainWasPaintedLastTurn = True
						nbOfSquaresPainted = nbOfSquaresPainted + 1
						myPad.addstr(yCoord,xCoord, "b", curses.color_pair(int("1"+str(terrainToFillWith))))

						titleWin.addstr(2,1,("Brush mode active, painted square (y="+str(yCoord)+";x="+str(xCoord)+")").ljust(screenMaxX-2))
						titleWin.refresh()
					else :
						myPad.addstr(yCoord,xCoord, "b", curses.color_pair(4))
						titleWin.addstr(2,1,"Out of bounds, brush not painting".ljust(screenMaxX-2))
						titleWin.refresh()

					myPad.refresh(int(yCoord-((screenMaxY-5)/2)), int(xCoord-((screenMaxX-3)/2)), 1, 1, screenMaxY-5, screenMaxX-2)

		if userInput == ord('t') or userInput == ord('T') :
		# this is the selection rectangle tool. 
		# press T, move the cursor to draw a rectangle, press a key to apply a command to all selected squares
			if yCoord > myLabyrinth.levelSizeY-1 or xCoord > myLabyrinth.levelSizeX-1 :
				titleWin.addstr(2,1,"Out of bounds, won't enter selection mode.".ljust(screenMaxX-2))
				titleWin.refresh()
			else :
				titleWin.addstr(2,1,"Entered selection mode, T to confirm selection".ljust(screenMaxX-2))
				titleWin.refresh()
				
				originCoordY = yCoord
				originCoordX = xCoord

				# now we're in a sub-loop where the user moves the cursor to draw a rectangle
				while True :
					userInput = standardScreen.getch()
					
					
					# here we redraw over the selection rectangle drawn earlier. I'm sure there's a more efficient way.

					if originCoordY > yCoord :
						for workingY in range(yCoord, originCoordY+1) :
							if originCoordX > xCoord :
								for workingX in range (xCoord, originCoordX+1) :
									if myLabyrinth.levelMap[workingY][workingX] == 0 :
										myPad.addstr(workingY, workingX, " ")
									else :
										myPad.addstr(workingY,workingX, " ", curses.color_pair(myLabyrinth.levelMap[workingY][workingX]))
							else :
								for workingX in range(originCoordX, xCoord+1) :
									if myLabyrinth.levelMap[workingY][workingX] == 0 :
										myPad.addstr(workingY, workingX, " ")
									else :
										myPad.addstr(workingY,workingX, " ", curses.color_pair(myLabyrinth.levelMap[workingY][workingX]))
					else :
						for workingY in range(originCoordY, yCoord+1) :			
							if originCoordX > xCoord :
								for workingX in range (xCoord, originCoordX+1) :
									if myLabyrinth.levelMap[workingY][workingX] == 0 :
										myPad.addstr(workingY, workingX, " ")
									else :
										myPad.addstr(workingY,workingX, " ", curses.color_pair(myLabyrinth.levelMap[workingY][workingX]))
							else :
								for workingX in range(originCoordX, xCoord+1) :
									if myLabyrinth.levelMap[workingY][workingX] == 0 :
										myPad.addstr(workingY, workingX, " ")
									else :
										myPad.addstr(workingY,workingX, " ", curses.color_pair(myLabyrinth.levelMap[workingY][workingX]))


					
					if userInput == curses.KEY_LEFT and xCoord > 0 :
						xCoord = xCoord -1
					if userInput == curses.KEY_RIGHT and xCoord < myLabyrinth.levelSizeX-1 :
						xCoord = xCoord +1
					if userInput == curses.KEY_UP and yCoord > 0 :
						yCoord = yCoord -1
					if userInput == curses.KEY_DOWN and yCoord < myLabyrinth.levelSizeY-1 :
						yCoord = yCoord +1	

					
					if userInput == ord('t') or userInput == ord('T') :
					# we end the selection and ask the user what they wanna do with it
						titleWin.addstr(2,1,"P to fill w/ paths, W walls, O targets, S spawns, R reverse, other to cancel".ljust(screenMaxX-2))
						titleWin.refresh()
						secondInput = standardScreen.getch()
						if secondInput == ord('p') or secondInput == ord('P') :
							terrainToFillWith = 0
						elif secondInput == ord('w') or secondInput == ord('W') :
							terrainToFillWith = 1
						elif secondInput == ord('o') or secondInput == ord('O') :
							terrainToFillWith = 2
						elif secondInput == ord('s') or secondInput == ord('S') :
							terrainToFillWith = 3
						elif secondInput == ord('r') or secondInput == ord('R') :
							terrainToFillWith = -1 # reverse
						else :
							terrainToFillWith = "exit"
							titleString = "Selection cancelled, no changes made."
						#stderr.write(str(originCoordX)+" "+str(originCoordY)+" "+str(xCoord)+" "+str(yCoord))

						if terrainToFillWith != "exit" :
							
							if originCoordY > yCoord :
								for workingY in range(yCoord, originCoordY+1) :
									if originCoordX > xCoord :
										for workingX in range (xCoord, originCoordX+1) :
											if terrainToFillWith == -1 :
												if  myLabyrinth.levelMap[workingY][workingX] == 0 :
													myLabyrinth.levelMap[workingY][workingX] = 1
												elif myLabyrinth.levelMap[workingY][workingX] == 1 :
													myLabyrinth.levelMap[workingY][workingX] = 0
											else :
												myLabyrinth.levelMap[workingY][workingX] = terrainToFillWith
											if myLabyrinth.levelMap[workingY][workingX] == 0 :
												myPad.addstr(workingY,workingX, " ")
											else :
												myPad.addstr(workingY,workingX, " ", curses.color_pair(myLabyrinth.levelMap[workingY][workingX]))
									else :
										for workingX in range(originCoordX, xCoord+1) :
											if terrainToFillWith == -1 :
												if  myLabyrinth.levelMap[workingY][workingX] == 0 :
													myLabyrinth.levelMap[workingY][workingX] = 1
												elif myLabyrinth.levelMap[workingY][workingX] == 1 :
													myLabyrinth.levelMap[workingY][workingX] = 0
											else :
												myLabyrinth.levelMap[workingY][workingX] = terrainToFillWith
											if myLabyrinth.levelMap[workingY][workingX] == 0 :
												myPad.addstr(workingY,workingX, " ")
											else :
												myPad.addstr(workingY,workingX, " ", curses.color_pair(myLabyrinth.levelMap[workingY][workingX]))
							else :
								for workingY in range(originCoordY, yCoord+1) :			
									if originCoordX > xCoord :
										for workingX in range (xCoord, originCoordX+1) :
											if terrainToFillWith == -1 :
												if  myLabyrinth.levelMap[workingY][workingX] == 0 :
													myLabyrinth.levelMap[workingY][workingX] = 1
												elif myLabyrinth.levelMap[workingY][workingX] == 1 :
													myLabyrinth.levelMap[workingY][workingX] = 0
											else :
												myLabyrinth.levelMap[workingY][workingX] = terrainToFillWith
											if myLabyrinth.levelMap[workingY][workingX] == 0 :
												myPad.addstr(workingY,workingX, " ")
											else :
												myPad.addstr(workingY,workingX, " ", curses.color_pair(myLabyrinth.levelMap[workingY][workingX]))
									else :
										for workingX in range(originCoordX, xCoord+1) :
											if terrainToFillWith == -1 :
												if  myLabyrinth.levelMap[workingY][workingX] == 0 :
													myLabyrinth.levelMap[workingY][workingX] = 1
												elif myLabyrinth.levelMap[workingY][workingX] == 1 :
													myLabyrinth.levelMap[workingY][workingX] = 0
											else :
												myLabyrinth.levelMap[workingY][workingX] = terrainToFillWith
											if myLabyrinth.levelMap[workingY][workingX] == 0 :
												myPad.addstr(workingY,workingX, " ")
											else :
												myPad.addstr(workingY,workingX, " ", curses.color_pair(myLabyrinth.levelMap[workingY][workingX]))
							titleString = "Changes applied."

						titleWin.addstr(2,1,titleString.ljust(screenMaxX-2))
						titleWin.refresh()
	
						myPad.refresh(int(yCoord-((screenMaxY-5)/2)), int(xCoord-((screenMaxX-3)/2)), 1, 1, screenMaxY-5, screenMaxX-2)	
						break
						
					
					
					myPad.addstr(originCoordY, originCoordX, "o")
					myPad.addstr(yCoord, xCoord, "x")

					# drawing the selection rectangle

					if originCoordY > yCoord :
						for workingY in range(yCoord, originCoordY+1) :
							if originCoordX > xCoord :
								for workingX in range (xCoord, originCoordX+1) :
									myPad.addstr(workingY,workingX,"#",curses.color_pair(int("1"+str(myLabyrinth.levelMap[workingY][workingX]))))
							else :
								for workingX in range(originCoordX, xCoord+1) :
									myPad.addstr(workingY,workingX,"#",curses.color_pair(int("1"+str(myLabyrinth.levelMap[workingY][workingX]))))
					else :
						for workingY in range(originCoordY, yCoord+1) :			
							if originCoordX > xCoord :
								for workingX in range (xCoord, originCoordX+1) :
									myPad.addstr(workingY,workingX,"#",curses.color_pair(int("1"+str(myLabyrinth.levelMap[workingY][workingX]))))
							else :
								for workingX in range(originCoordX, xCoord+1) :
									myPad.addstr(workingY,workingX,"#",curses.color_pair(int("1"+str(myLabyrinth.levelMap[workingY][workingX]))))

					myPad.addstr(originCoordY, originCoordX, "o", curses.color_pair(int("1"+str(myLabyrinth.levelMap[originCoordY][originCoordX]))))
					myPad.addstr(yCoord, xCoord, "x", curses.color_pair(int("1"+str(myLabyrinth.levelMap[yCoord][xCoord]))))

					myPad.refresh(int(yCoord-((screenMaxY-5)/2)), int(xCoord-((screenMaxX-3)/2)), 1, 1, screenMaxY-5, screenMaxX-2)	
				

	

		if userInput == ord('h') or userInput == ord('H') : # help window
			helpString0 = "HELP :"
			helpString1 = "Spacebar : switch wall/path"
			helpString2 = "R : replace block"
			helpString3 = "B : brush tool"
			helpString4 = "T : selection tool"
			helpString5 = "D : edit metadata"
			helpString6 = "S : save to file"
			helpString7 = "Q : quit"
			helpString8 = "H : this help"
			helpString9 = "Press any key to close this window."

			lengthOfLongestString=max(len(helpString0),len(helpString1),len(helpString2),len(helpString3),len(helpString4),len(helpString5),len(helpString6), len(helpString7), len(helpString8),len(helpString9))
			helpWindow = standardScreen.subwin(12, lengthOfLongestString+2, floor(screenMaxY/2-6), floor(screenMaxX/2-(lengthOfLongestString/2)))
			helpWindow.border()
			helpWindow.addstr(1,1,helpString0.center(lengthOfLongestString))
			helpWindow.addstr(2,1,helpString1.ljust(lengthOfLongestString))
			helpWindow.addstr(3,1,helpString2.ljust(lengthOfLongestString))
			helpWindow.addstr(4,1,helpString3.ljust(lengthOfLongestString))
			helpWindow.addstr(5,1,helpString4.ljust(lengthOfLongestString))
			helpWindow.addstr(6,1,helpString5.ljust(lengthOfLongestString))
			helpWindow.addstr(7,1,helpString6.ljust(lengthOfLongestString))
			helpWindow.addstr(8,1,helpString7.ljust(lengthOfLongestString))			
			helpWindow.addstr(9,1,helpString8.ljust(lengthOfLongestString))
			helpWindow.addstr(10,1,helpString9.center(lengthOfLongestString))

			helpWindow.refresh()
			sleep(0.5)
			standardScreen.getch()
			
			helpWindow.clear()
			helpWindow.redrawwin()
			helpWindow.refresh()
			titleWin.border()
			titleWin.refresh()
			standardScreen.refresh()

		if userInput == ord('d') or userInput == ord('D') :
			# this "metadata" window presents and offer to edit level name, author name and level to follow
			
			dataString0 = "METADATA :"

			dataString1 = "Level name (L to edit) :"
			try :
				dataString2 = myLabyrinth.name
			except AttributeError :
				dataString2 = "(None set)"
			dataString3 = "Author name (A to edit) :"
			try :
				dataString4 = myLabyrinth.author
			except AttributeError :
				dataString4 = "(None set)"
			dataString5 = "Level to follow (N to edit) :"
			try :
				dataString6 = myLabyrinth.nextLevel
			except AttributeError :
				dataString6 = "(None set)"
			dataString7 = "File name : (F to edit) :"
			dataString8 = fileName

			dataString9 = "Press any other key to close this window."
			
			lengthOfLongestString=max(len(dataString0),len(dataString1),len(dataString2),len(dataString3),len(dataString4),len(dataString5), len(dataString6), len(dataString7), len(dataString8), len(dataString9))
			if lengthOfLongestString<30 :
				lengthOfLongestString = 30

			dataWindow = standardScreen.subwin(12, lengthOfLongestString+2, floor(screenMaxY/2-6), floor(screenMaxX/2-(lengthOfLongestString/2)))
			dataWindow.border()
			dataWindow.addstr(1,1,dataString0.center(lengthOfLongestString))
			dataWindow.addstr(2,1,dataString1.ljust(lengthOfLongestString))
			dataWindow.addstr(3,1,("  "+dataString2).ljust(lengthOfLongestString))
			dataWindow.addstr(4,1,dataString3.ljust(lengthOfLongestString))
			dataWindow.addstr(5,1,("  "+dataString4).ljust(lengthOfLongestString))
			dataWindow.addstr(6,1,dataString5.ljust(lengthOfLongestString))
			dataWindow.addstr(7,1,("  "+dataString6).ljust(lengthOfLongestString))
			dataWindow.addstr(8,1,dataString7.ljust(lengthOfLongestString))
			dataWindow.addstr(9,1,("  "+dataString8).ljust(lengthOfLongestString))
			dataWindow.addstr(10,1,dataString9.center(lengthOfLongestString))

			dataWindow.refresh()
			# I'm reluctant to use curses.textpad.TextPad, because Ctrl+G to accept is not intuitive nor coherent with the rest of the program.
			secondInput = standardScreen.getch()

			if secondInput == (ord('l') or ord('L')) :
				levelNameString0 = "Level name : "+dataString2
				levelNameString1 = "Enter the new name :"
				levelNameString2 = "(press Enter to confirm)"
				lengthOfLongestString = max(len(levelNameString0),len(levelNameString1),len(levelNameString2))

				levelNameWindow = standardScreen.subwin(6,lengthOfLongestString+2, floor(screenMaxY/2-3), floor(screenMaxX/2-(lengthOfLongestString/2)))
				levelNameWindow.border()

				levelNameWindow.addstr(1,1,levelNameString0.center(lengthOfLongestString))
				levelNameWindow.addstr(2,1,levelNameString1.center(lengthOfLongestString))
				levelNameWindow.addstr(3,1,"".center(lengthOfLongestString)) 
				levelNameWindow.addstr(4,1,levelNameString2.center(lengthOfLongestString))
				
				#newLevelName = levelNameWindow.getstr(3,1,lengthOfLongestString)
				# getstr() doesn't provide instant feedback.. REAL men develop their own text inputs.
				kursorX = 1
				levelNameWindow.move(3,kursorX)
				newLevelName = ""
				levelNameWindow.refresh()	
				curses.curs_set(True)
				secondInput = standardScreen.getch()
				while secondInput !=ord("\n") :
					if secondInput == curses.KEY_BACKSPACE : #doc says it's unreliable
						if kursorX>1 :
							levelNameWindow.addstr(3, kursorX-1," ") # mask the deleted character
							kursorX = kursorX -1
							levelNameWindow.move(3,kursorX)
							newLevelName = newLevelName[0:len(newLevelName)-1]

					elif len(newLevelName) < lengthOfLongestString :
						newLevelName = newLevelName+chr(secondInput)
						kursorX = kursorX + 1
						levelNameWindow.move(3,kursorX)
						levelNameWindow.addstr(3, kursorX-1,chr(secondInput))
					levelNameWindow.refresh()
					secondInput = standardScreen.getch()
						
				if newLevelName != "" :
					myLabyrinth.name = str(newLevelName)
					titleWin.addstr(2,1,("Name changed to "+str(myLabyrinth.name)).ljust(screenMaxX-2))
				else :
					titleWin.addstr(2,1,"Rejected empty name".ljust(screenMaxX-2))
				curses.curs_set(False)
				levelNameWindow.clear()
				levelNameWindow.redrawwin()
				levelNameWindow.refresh()

			elif secondInput == (ord('a') or ord('A')) :
				levelAuthorString0 = "Author name : "+dataString4
				levelAuthorString1 = "Enter the new name :"
				levelAuthorString2 = "(press Enter to confirm)"
				lengthOfLongestString = max(len(levelAuthorString0),len(levelAuthorString1),len(levelAuthorString2))

				levelAuthorWindow = standardScreen.subwin(6,lengthOfLongestString+2, floor(screenMaxY/2-3), floor(screenMaxX/2-(lengthOfLongestString/2)))
				levelAuthorWindow.border()

				levelAuthorWindow.addstr(1,1,levelAuthorString0.center(lengthOfLongestString))
				levelAuthorWindow.addstr(2,1,levelAuthorString1.center(lengthOfLongestString))
				levelAuthorWindow.addstr(3,1,"".center(lengthOfLongestString)) 
				levelAuthorWindow.addstr(4,1,levelAuthorString2.center(lengthOfLongestString))
				
				kursorX = 1
				levelAuthorWindow.move(3,kursorX)
				newAuthorName = ""
				levelAuthorWindow.refresh()	
				curses.curs_set(True)
				secondInput = standardScreen.getch()
				while secondInput !=ord("\n") :
					if secondInput == curses.KEY_BACKSPACE : #doc says it's unreliable
						if kursorX>1 :
							levelAuthorWindow.addstr(3, kursorX-1," ") # mask the deleted character
							kursorX = kursorX -1
							levelAuthorWindow.move(3,kursorX)
							newAuthorName = newAuthorName[0:len(newAuthorName)-1]

					elif len(newAuthorName) < lengthOfLongestString :
						newAuthorName = newAuthorName+chr(secondInput)
						kursorX = kursorX + 1
						levelAuthorWindow.move(3,kursorX)
						levelAuthorWindow.addstr(3, kursorX-1,chr(secondInput))
					levelAuthorWindow.refresh()
					secondInput = standardScreen.getch()
						
				if newAuthorName != "" :
					myLabyrinth.author = str(newAuthorName)
					titleWin.addstr(2,1,("Author changed to "+str(myLabyrinth.author)).ljust(screenMaxX-2))
				else :
					titleWin.addstr(2,1,"Rejected empty name".ljust(screenMaxX-2))
				curses.curs_set(False)
				levelAuthorWindow.clear()
				levelAuthorWindow.redrawwin()
				levelAuthorWindow.refresh()

			elif secondInput == (ord('n') or ord('N')) :
				levelFollowerString0 = "Level to follow : "+dataString6
				levelFollowerString1 = "Enter the new filename :"
				levelFollowerString2 = "(press Enter to confirm)"
				lengthOfLongestString = max(len(levelFollowerString0),len(levelFollowerString1),len(levelFollowerString2))

				levelFollowerWindow = standardScreen.subwin(6,lengthOfLongestString+2, floor(screenMaxY/2-3), floor(screenMaxX/2-(lengthOfLongestString/2)))
				levelFollowerWindow.border()

				levelFollowerWindow.addstr(1,1,levelFollowerString0.center(lengthOfLongestString))
				levelFollowerWindow.addstr(2,1,levelFollowerString1.center(lengthOfLongestString))
				levelFollowerWindow.addstr(3,1,"".center(lengthOfLongestString)) 
				levelFollowerWindow.addstr(4,1,levelFollowerString2.center(lengthOfLongestString))
				
				kursorX = 1
				levelFollowerWindow.move(3,kursorX)
				newFollowerName = ""
				levelFollowerWindow.refresh()	
				curses.curs_set(True)
				secondInput = standardScreen.getch()
				while secondInput !=ord("\n") :
					if secondInput == curses.KEY_BACKSPACE : #doc says it's unreliable
						if kursorX>1 :
							levelFollowerWindow.addstr(3, kursorX-1," ") # mask the deleted character
							kursorX = kursorX -1
							levelFollowerWindow.move(3,kursorX)
							newFollowerName = newFollowerName[0:len(newFollowerName)-1]

					elif len(newFollowerName) < lengthOfLongestString :
						newFollowerName = newFollowerName+chr(secondInput)
						kursorX = kursorX + 1
						levelFollowerWindow.move(3,kursorX)
						levelFollowerWindow.addstr(3, kursorX-1,chr(secondInput))
					levelFollowerWindow.refresh()
					secondInput = standardScreen.getch()
						
				if newFollowerName != "" :
					myLabyrinth.nextLevel = str(newFollowerName)
					titleWin.addstr(2,1,("Following level changed to "+str(myLabyrinth.nextLevel)).ljust(screenMaxX-2))
				else :
					titleWin.addstr(2,1,"Rejected empty name".ljust(screenMaxX-2))
				curses.curs_set(False)
				levelFollowerWindow.clear()
				levelFollowerWindow.redrawwin()
				levelFollowerWindow.refresh()
			
			elif secondInput == (ord('f') or ord('F')) :
				fileNameString0 = "Filename to save to : "+dataString8
				fileNameString1 = "Enter the new filename :"
				fileNameString2 = "(press Enter to confirm)"
				lengthOfLongestString = max(len(fileNameString0),len(fileNameString1),len(fileNameString2))

				fileNameWindow = standardScreen.subwin(6,lengthOfLongestString+2, floor(screenMaxY/2-3), floor(screenMaxX/2-(lengthOfLongestString/2)))
				fileNameWindow.border()

				fileNameWindow.addstr(1,1,fileNameString0.center(lengthOfLongestString))
				fileNameWindow.addstr(2,1,fileNameString1.center(lengthOfLongestString))
				fileNameWindow.addstr(3,1,"".center(lengthOfLongestString)) 
				fileNameWindow.addstr(4,1,fileNameString2.center(lengthOfLongestString))
				
				kursorX = 1
				fileNameWindow.move(3,kursorX)
				newFileName = ""
				fileNameWindow.refresh()	
				curses.curs_set(True)
				secondInput = standardScreen.getch()
				while secondInput !=ord("\n") :
					if secondInput == curses.KEY_BACKSPACE : #doc says it's unreliable
						if kursorX>1 :
							fileNameWindow.addstr(3, kursorX-1," ") # mask the deleted character
							kursorX = kursorX -1
							fileNameWindow.move(3,kursorX)
							newFileName = newFileName[0:len(newFileName)-1]

					elif len(newFileName) < lengthOfLongestString :
						newFileName = newFileName+chr(secondInput)
						kursorX = kursorX + 1
						fileNameWindow.move(3,kursorX)
						fileNameWindow.addstr(3, kursorX-1,chr(secondInput))
					fileNameWindow.refresh()
					secondInput = standardScreen.getch()
						
				if newFileName != "" :
					fileName = newFileName
					titleWin.addstr(2,1,("Following level changed to "+fileName).ljust(screenMaxX-2))
				else :
					titleWin.addstr(2,1,"Rejected empty name".ljust(screenMaxX-2))
				curses.curs_set(False)
				fileNameWindow.clear()
				fileNameWindow.redrawwin()
				fileNameWindow.refresh()
	 

			else :
				titleWin.addstr(2,1, "No changes to metadata.".ljust(screenMaxX-2))
			
			dataWindow.clear()
			dataWindow.redrawwin()
			dataWindow.refresh()
			titleWin.refresh()
			standardScreen.refresh()

	
			




		if userInput == ord('s') or userInput == ord('S') : # save function !
			saveString0 = "The saved file name will be :"
			saveString1 = "Are you sure you want to save ?"
			saveString2 = "Press Y to confirm, or any other key to cancel."
			
			lengthOfLongestString = max(len(saveString0), len(saveString1), len(saveString2))
			saveWindow = standardScreen.subwin(6, lengthOfLongestString+2 ,floor(screenMaxY/2), floor(screenMaxX/2-(lengthOfLongestString/2)))
			# good thing I had already done that once
			saveWindow.border()
			saveWindow.addstr(1,1,saveString0.center(lengthOfLongestString))
			saveWindow.addstr(2,1,fileName.center(lengthOfLongestString))
			saveWindow.addstr(3,1,saveString1.center(lengthOfLongestString))
			saveWindow.addstr(4,1,saveString2.center(lengthOfLongestString))

			saveWindow.refresh()
			sleep(0.5) # no seriously, it *is* a good idea !
			secondInput = standardScreen.getch()
			if secondInput == ord('y') or secondInput == ord('Y') :
				
				myLabyrinth.write(fileName)
				titleWin.addstr(2,1, ("File "+str(fileName)+" saved !").ljust(screenMaxX-2))
			else :
				titleWin.addstr(2,1, "Changes NOT saved to file".ljust(screenMaxX-2))
			
			saveWindow.clear()
			saveWindow.redrawwin()
			saveWindow.refresh()
			titleWin.refresh()
			standardScreen.refresh()

		if userInput == ord('q') or userInput == ord('Q') :
			quitString0 = "Are you sure you want to quit ?"
			quitString1 = "All work you have not saved will be lost !"
			quitString2 = "Press Y if you are, or any other key to cancel."
			
			lengthOfLongestString = max(len(quitString0), len(quitString1), len(quitString2))
			quitWindow = standardScreen.subwin(5, lengthOfLongestString+2, floor(screenMaxY/2), floor(screenMaxX/2-(lengthOfLongestString/2)))
			
			quitWindow.border()
			quitWindow.addstr(1,1,quitString0.center(lengthOfLongestString))
			quitWindow.addstr(2,1,quitString1.center(lengthOfLongestString))
			quitWindow.addstr(3,1,quitString2.center(lengthOfLongestString))
			
			quitWindow.refresh()
			sleep(0.5)
			secondInput = standardScreen.getch()
			if secondInput == ord('y') or secondInput == ord('Y') :
				exit()
			else :
				quitWindow.clear()
				quitWindow.redrawwin()
				quitWindow.refresh()
				standardScreen.refresh()
		#TODO : process curses.KEY_RESIZE
	

		# drawing the new cursor

		if yCoord<myLabyrinth.levelSizeY and xCoord<myLabyrinth.levelSizeX :
			myPad.addstr(yCoord, xCoord, "x", curses.color_pair(int("1"+str(myLabyrinth.levelMap[yCoord][xCoord]))))
		else : # out of level bounds
			myPad.addstr(yCoord, xCoord, "x", curses.color_pair(4))

		standardScreen.refresh()
		myPad.refresh(int(yCoord-((screenMaxY-5)/2)), int(xCoord-((screenMaxX-3)/2)), 1, 1, screenMaxY-5, screenMaxX-2)	




# same idea as in the main labyrinth game.. curses blocks output elseway, and I like my errors

errorType = curses.wrapper(main)

if errorType == "noParameters" :
	stderr.write("No parameters were given. Please, use \""+argv[0]+" help\" to get precisions.\n")
	exit(1)

if errorType == "getHelp" :
	print("This program is a level editor for the labyrinth game I made.")
	print("Options :")
	print("-f (followed by a string) : name of file to open and/or save to (overwrites other options)")
	print("You can also pass a filename directly if it's the only argument")
	print("-h (followed by a number) : height of a new (blank) level to edit (defaults to 20)")
	print("-w (followed by a number) : width of a new (blank) level to edit (defaults to 20)")
	print("-b (followed by a number) : if you are opening a new level, what type of block to fill it with (0 -> pathways, 1 -> walls, defaults to pathways)")
	print("\nCheck out the readme/manual for more help !")
	exit()

if errorType == "readError" :
	stderr.write("Error when reading the arguments.\n\nReminder : you should specify no argument (to edit a blank level) or only one (an existing, valid level file). Maybe did you misspell the name of the file ? You can also call this program with the help argument, or read the readme file.\n\nThis error does not cover an error when parsing the file, only when opening it.\n")
	exit(2)

else :
	print(errorType)

