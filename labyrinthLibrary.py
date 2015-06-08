# this library contains the Labyrinth class
#
# a Labyrinth has a bunch of attributes :
# name (string)
# author (string)
# colors : dictionary binding color ID (0 to 3) to a list of 6 RGB values between 0 and 1000 (three for the foreground, two for the background, one to keep people asking)
# highscores : list of [score:int, player:string] couples
# nextLevel : filename for the level to follow (the game asks if you want to go to the next level at the end of the current one)
# levelMap : a rectangular, 2D table representing the level with 0, 1, 2 and 3s



class Labyrinth :
		
	def __init__(self, fileName=None) :
		if fileName == None :
			# by default we'll create a default level
		
			self.name = "Default Level"
			self.author = "Olivier"
			# we won't set colours

			self.highscores = [[18,"olivier"],[22,"olivier"]]
			
			# we won't set a level to follow

			self.levelMap = [
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
		
		else :
			# init where it reads a labyrinth from a file.
			
			try :
				fileStream = open(fileName)
			except OSError as readError :
				return("readError")
			
			workingLine = fileStream.readline()
			
			while workingLine.strip() != "end" :
				words = workingLine.split(" ")
				
				if workingLine.strip() == "" :
					pass
				elif workingLine[0] == "#" :
					pass
				elif words[0] == "name" :
					self.name = ""
					for i in range(1, len(words)) :
						self.name = self.name + words[i]
						if i < len(words)-1 :
							self.name = self.name + " "
				
				elif words[0] == "author" :
					self.author = ""
					for i in range(1, len(words)) :
						self.author = self.author + words[i]
						if i < len(words)-1 :
							self.author = self.author + " "

				elif words[0] == "color" :
					
					try : # Python is a dynamic language except when you need to declare things so you can append stuff to them
						self.colors
					except AttributeError :
						self.colors = {}
					colorTable = []
					for i in range (2, 8) :
						colorTable.append(int(words[i]))
					self.colors[int(words[1])] = colorTable

				elif words[0] == "highscore" :
					try :
						self.highscores
					except AttributeError :
						self.highscores = []
					self.highscores.append([int(words[1]),words[2]])

				elif words[0] == "nextlevel" :
					self.nextLevel = words[1]

				elif words[0] == "map" :
					# under the assumption we have only one map in the file (eh) I'll allow myself not to use a try/except block
					self.levelMap=[]

					workingLine = fileStream.readline().strip()
					while workingLine != "end" :
						newLabyLine = []
						for i in range(len(workingLine)) :
							newLabyLine.append(int(workingLine[i]))
						self.levelMap.append(newLabyLine)
						workingLine = fileStream.readline().strip()
					break

				workingLine = fileStream.readline().strip()






	def writeLabyrinth(fileName) :
		# saves a labyrinth as a .laby file..
		# TODO
		pass
