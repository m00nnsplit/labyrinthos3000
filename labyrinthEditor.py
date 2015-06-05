#!/usr/bin/python3

import curses
from sys import argv, stderr
from os.path import exists
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
		#return("noParameters")
		# eh, that was kinda dickish
		labyrinthLoadedFlag = False
		
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
				labyrinthLoadedFlag = False	

	if argv.count("-f") > 0 :
		fileName = argv[argv.index("-f")+1]
		if exists(fileName) :
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
			labyrinthLoadedFlag = False
				
	if labyrinthLoadedFlag == False :
		if argv.count("-h") > 0 :
			labyHeight = int(argv[argv.index("-h")+1])
		else :
			labyHeight = 20
		if argv.count("-w") > 0 :
			labyWidth = int(argv[argv.index("-w")+1])
		else :
			labyWidth = 20	
		
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
	myPad.refresh(int(yCoord-((screenMaxY-5)/2)), int(xCoord-((screenMaxX-3)/2)), 1, 1, screenMaxY-5, screenMaxX-2)	

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
					titleWin.addstr(2,1,("Switched square (y="+str(yCoord)+";x="+str(xCoord)+")").ljust(screenMaxX-2))
				elif myLabyrinth[yCoord][xCoord] == 1 :
					myLabyrinth[yCoord][xCoord] = 0
					titleWin.addstr(2,1,("Switched square (y="+str(yCoord)+";x="+str(xCoord)+")").ljust(screenMaxX-2))
				titleWin.refresh()
		
		if userInput == ord('r') or userInput == ord('R') : # allows to select any block
			if yCoord<labyHeight and xCoord<labyWidth :
				titleWin.addstr(2,1, ("(y="+str(yCoord)+";x="+str(xCoord)+") Press S for spawn, O for objective, W for wall, P for path.").ljust(screenMaxX-2))
				titleWin.refresh()
				secondInput = standardScreen.getch()
				if secondInput == ord('s') or secondInput == ord('S') :
					myLabyrinth[yCoord][xCoord] = 3
					titleWin.addstr(2,1,("Changed square (y="+str(yCoord)+";x="+str(xCoord)+") to spawn point.").ljust(screenMaxX-2))
				elif secondInput == ord('o') or secondInput == ord('O') :
					myLabyrinth[yCoord][xCoord] = 2
					titleWin.addstr(2,1,("Changed square (y="+str(yCoord)+";x="+str(xCoord)+") to objective.").ljust(screenMaxX-2))
				elif secondInput == ord('w') or secondInput == ord('W') :
					myLabyrinth[yCoord][xCoord] = 1
					titleWin.addstr(2,1,("Changed square (y="+str(yCoord)+";x="+str(xCoord)+") to wall.").ljust(screenMaxX-2))
				elif secondInput == ord('p') or secondInput == ord('P') :
					myLabyrinth[yCoord][xCoord] = 0
					titleWin.addstr(2,1,("Changed square (y="+str(yCoord)+";x="+str(xCoord)+") to pathway.").ljust(screenMaxX-2))
				else :
					titleWin.addstr(2,1,"No changes made.".ljust(screenMaxX-2))
				titleWin.refresh()			
	
		


		if userInput == ord('t') or userInput == ord('T') :
		# this is the selection rectangle tool. 
		# press T, move the cursor to draw a rectangle, press a key to apply a command to all selected squares
			if yCoord > labyHeight-1 or xCoord > labyWidth-1 :
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
									if myLabyrinth[workingY][workingX] == 0 :
										myPad.addstr(workingY, workingX, " ")
									else :
										myPad.addstr(workingY,workingX, " ", curses.color_pair(myLabyrinth[workingY][workingX]))
							else :
								for workingX in range(originCoordX, xCoord+1) :
									if myLabyrinth[workingY][workingX] == 0 :
										myPad.addstr(workingY, workingX, " ")
									else :
										myPad.addstr(workingY,workingX, " ", curses.color_pair(myLabyrinth[workingY][workingX]))
					else :
						for workingY in range(originCoordY, yCoord+1) :			
							if originCoordX > xCoord :
								for workingX in range (xCoord, originCoordX+1) :
									if myLabyrinth[workingY][workingX] == 0 :
										myPad.addstr(workingY, workingX, " ")
									else :
										myPad.addstr(workingY,workingX, " ", curses.color_pair(myLabyrinth[workingY][workingX]))
							else :
								for workingX in range(originCoordX, xCoord+1) :
									if myLabyrinth[workingY][workingX] == 0 :
										myPad.addstr(workingY, workingX, " ")
									else :
										myPad.addstr(workingY,workingX, " ", curses.color_pair(myLabyrinth[workingY][workingX]))


					
					if userInput == curses.KEY_LEFT and xCoord > 0 :
						xCoord = xCoord -1
					if userInput == curses.KEY_RIGHT and xCoord < labyWidth-1 :
						xCoord = xCoord +1
					if userInput == curses.KEY_UP and yCoord > 0 :
						yCoord = yCoord -1
					if userInput == curses.KEY_DOWN and yCoord < labyHeight-1 :
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
							terrainToFillWith = False
							titleString = "Selection cancelled, no changes made."
						#stderr.write(str(originCoordX)+" "+str(originCoordY)+" "+str(xCoord)+" "+str(yCoord))

						if terrainToFillWith != False :
							
							if originCoordY > yCoord :
								for workingY in range(yCoord, originCoordY+1) :
									if originCoordX > xCoord :
										for workingX in range (xCoord, originCoordX+1) :
											if terrainToFillWith == -1 :
												if  myLabyrinth[workingY][workingX] == 0 :
													myLabyrinth[workingY][workingX] = 1
												elif myLabyrinth[workingY][workingX] == 1 :
													myLabyrinth[workingY][workingX] = 0
											else :
												myLabyrinth[workingY][workingX] = terrainToFillWith
											if myLabyrinth[workingY][workingX] == 0 :
												myPad.addstr(workingY,workingX, " ")
											else :
												myPad.addstr(workingY,workingX, " ", curses.color_pair(myLabyrinth[workingY][workingX]))
									else :
										for workingX in range(originCoordX, xCoord+1) :
											if terrainToFillWith == -1 :
												if  myLabyrinth[workingY][workingX] == 0 :
													myLabyrinth[workingY][workingX] = 1
												elif myLabyrinth[workingY][workingX] == 1 :
													myLabyrinth[workingY][workingX] = 0
											else :
												myLabyrinth[workingY][workingX] = terrainToFillWith
											if myLabyrinth[workingY][workingX] == 0 :
												myPad.addstr(workingY,workingX, " ")
											else :
												myPad.addstr(workingY,workingX, " ", curses.color_pair(myLabyrinth[workingY][workingX]))
							else :
								for workingY in range(originCoordY, yCoord+1) :			
									if originCoordX > xCoord :
										for workingX in range (xCoord, originCoordX+1) :
											if terrainToFillWith == -1 :
												if  myLabyrinth[workingY][workingX] == 0 :
													myLabyrinth[workingY][workingX] = 1
												elif myLabyrinth[workingY][workingX] == 1 :
													myLabyrinth[workingY][workingX] = 0
											else :
												myLabyrinth[workingY][workingX] = terrainToFillWith
											if myLabyrinth[workingY][workingX] == 0 :
												myPad.addstr(workingY,workingX, " ")
											else :
												myPad.addstr(workingY,workingX, " ", curses.color_pair(myLabyrinth[workingY][workingX]))
									else :
										for workingX in range(originCoordX, xCoord+1) :
											if terrainToFillWith == -1 :
												if  myLabyrinth[workingY][workingX] == 0 :
													myLabyrinth[workingY][workingX] = 1
												elif myLabyrinth[workingY][workingX] == 1 :
													myLabyrinth[workingY][workingX] = 0
											else :
												myLabyrinth[workingY][workingX] = terrainToFillWith
											if myLabyrinth[workingY][workingX] == 0 :
												myPad.addstr(workingY,workingX, " ")
											else :
												myPad.addstr(workingY,workingX, " ", curses.color_pair(myLabyrinth[workingY][workingX]))
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
									myPad.addstr(workingY,workingX,"#",curses.color_pair(int("1"+str(myLabyrinth[workingY][workingX]))))
							else :
								for workingX in range(originCoordX, xCoord+1) :
									myPad.addstr(workingY,workingX,"#",curses.color_pair(int("1"+str(myLabyrinth[workingY][workingX]))))
					else :
						for workingY in range(originCoordY, yCoord+1) :			
							if originCoordX > xCoord :
								for workingX in range (xCoord, originCoordX+1) :
									myPad.addstr(workingY,workingX,"#",curses.color_pair(int("1"+str(myLabyrinth[workingY][workingX]))))
							else :
								for workingX in range(originCoordX, xCoord+1) :
									myPad.addstr(workingY,workingX,"#",curses.color_pair(int("1"+str(myLabyrinth[workingY][workingX]))))

					myPad.addstr(originCoordY, originCoordX, "o", curses.color_pair(int("1"+str(myLabyrinth[originCoordY][originCoordX]))))
					myPad.addstr(yCoord, xCoord, "x", curses.color_pair(int("1"+str(myLabyrinth[yCoord][xCoord]))))

					myPad.refresh(int(yCoord-((screenMaxY-5)/2)), int(xCoord-((screenMaxX-3)/2)), 1, 1, screenMaxY-5, screenMaxX-2)	
				

	

		if userInput == ord('h') or userInput == ord('H') : # help window
			helpString0 = "HELP :"
			helpString1 = "Spacebar : switch wall/path"
			helpString2 = "R : replace block"
			helpString3 = "T : selection tool"
			helpString4 = "S : save to file"
			helpString5 = "Q : quit"
			helpString6 = "H : this help"
			helpString7 = "Press any key to close this window."

			lengthOfLongestString=max(len(helpString0),len(helpString1),len(helpString2),len(helpString3),len(helpString4),len(helpString5),len(helpString6), len(helpString7))
			helpWindow = standardScreen.subwin(10, lengthOfLongestString+2, floor(screenMaxY/2-5), floor(screenMaxX/2-(lengthOfLongestString/2)))
			helpWindow.border()
			helpWindow.addstr(1,1,helpString0.center(lengthOfLongestString))
			helpWindow.addstr(2,1,helpString1.ljust(lengthOfLongestString))
			helpWindow.addstr(3,1,helpString2.ljust(lengthOfLongestString))
			helpWindow.addstr(4,1,helpString3.ljust(lengthOfLongestString))
			helpWindow.addstr(5,1,helpString4.ljust(lengthOfLongestString))
			helpWindow.addstr(6,1,helpString5.ljust(lengthOfLongestString))
			helpWindow.addstr(7,1,helpString6.ljust(lengthOfLongestString))
			helpWindow.addstr(8,1,helpString7.center(lengthOfLongestString))			

			helpWindow.refresh()
			sleep(0.5)
			standardScreen.getch()
			
			helpWindow.clear()
			helpWindow.redrawwin()
			helpWindow.refresh()
			titleWin.border()
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
				
				fileStream = open(fileName, "w")
				for y in range(labyHeight) :
					workingLine = ""
					for x in range(labyWidth) :
						workingLine = workingLine + str(myLabyrinth[y][x])
					fileStream.write(workingLine+"\n")

				fileStream.close()
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
		#TODO : process curses.KEY_RESIZE
	

		# drawing the new cursor

		if yCoord<labyHeight and xCoord<labyWidth :
			myPad.addstr(yCoord, xCoord, "x", curses.color_pair(int("1"+str(myLabyrinth[yCoord][xCoord]))))
		else : # out of level bounds
			myPad.addstr(yCoord, xCoord, "x", curses.color_pair(4))

		standardScreen.refresh()
		myPad.refresh(int(yCoord-((screenMaxY-5)/2)), int(xCoord-((screenMaxX-3)/2)), 1, 1, screenMaxY-5, screenMaxX-2)	


errorOutput()	





