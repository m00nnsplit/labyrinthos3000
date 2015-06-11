# this library contains the Labyrinth class
#
# a Labyrinth has a bunch of attributes directly taken from the save file :
# name (string)
# author (string)
# colors : dictionary binding color ID (0 to 3) to a list of 6 RGB values between 0 and 1000 (three for the foreground, two for the background, one to keep people asking)
# highscores : list of [score:int, player:string] couples
# nextLevel : filename for the level to follow (the game asks if you want to go to the next level at the end of the current one)
# levelMap : a rectangular, 2D table representing the level with 0, 1, 2 and 3s

# Plus some stuff :
# levelSizeX and levelSizeY = two ints representing the map at its largest
# writeComment = a string written as a comment when the labyrinth is saved

# Methods :
# default constructor : returns a sample labyrinth
# constructor with (fileName) argument : reads <fileName> and returns the resulting labyrinth, or False if it couldn't be read
# write(fileName) : writes the Labyrinth as <fileName>

from datetime import datetime

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

			self.levelSizeX = 10
			self.levelSizeY = 10
		
		else :
			# init where it reads a labyrinth from a file.
			
			try :
				fileStream = open(fileName)
			except OSError as readError :
				return(False)
			
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

					self.levelSizeX = 0
					self.levelSizeY = 0
					workingLine = fileStream.readline().strip()
					while workingLine != "end" :
						newLabyLine = []
						for i in range(len(workingLine)) :
							newLabyLine.append(int(workingLine[i]))
							if i+1>self.levelSizeX :
								self.levelSizeX = i+1
						self.levelSizeY = self.levelSizeY + 1
						self.levelMap.append(newLabyLine)
						workingLine = fileStream.readline().strip()
					break

				workingLine = fileStream.readline().strip()






	def write(self, fileName) :
		# saves a labyrinth as <fileName>

		fileStream = open(fileName, "w")

		fileStream.write("# Written : "+datetime.now().isoformat(' ')+"\n")
		
		try :
			fileStream.write("# "+self.writeComment+"\n")
		except AttributeError :
			pass		
	
		try :
			fileStream.write("name "+self.name+"\n")
		except AttributeError :
			pass

		try :
			fileStream.write("author "+self.author+"\n")
		except AttributeError :
			pass
		
		# we only have 4 colours maximum so that's not really a problem

		for i in [0,1,2,3] :
			try :
				cols = self.colors[i]
				
				fileStream.write("color "+str(i)+" "+str(cols[0])+" "+str(cols[1])+" "+str(cols[2])+" "+str(cols[3])+" "+str(cols[4])+" "+str(cols[5])+"\n")
			except KeyError : # ie that color isn't customized
				pass
			except AttributeError :
				pass

		try :
			for i in range(len(self.highscores)) :
				fileStream.write("highscore "+str(self.highscores[i][0])+" "+self.highscores[i][1]+"\n")
		except AttributeError :
			pass

		try :
			fileStream.write("nextlevel "+self.nextLevel+"\n")
		except AttributeError :
			pass


		# and now for the hard part

		fileStream.write("map\n")
		for y in range(len(self.levelMap)) :
			workingLine = ""
			for x in range(len(self.levelMap[y])) :
				workingLine = workingLine + str(self.levelMap[y][x])
			fileStream.write(workingLine+"\n")
		
		fileStream.write("end")

		fileStream.close()
