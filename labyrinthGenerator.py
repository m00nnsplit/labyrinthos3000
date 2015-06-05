#!/usr/bin/python3

# this is a labyrinth generator

from sys import argv, stderr
import random
from time import time
from math import floor

# argument processing

if len(argv) == 1 :
	print("The level generator wasn't given any arguments ; using 20*20 level size and outputting to a.laby. Use \""+argv[0]+" help\" for more options !\n") 

if argv.count("help") > 0 :
	print("This program generates labyrinths, in a format suitable for my labyrinth game.")
	print("Options:")
	print("help : this help")
	print("-h (followed by a number) : height of the labyrinth to be generated (default 20)")
	print("-w (followed by a number) : width of the labyrinth to be generated (default 20)")
	print("-s (followed by a string) : seed to use for the random generator")
	print("-o (followed by a string) : name of the file to write the labyrinth to (default a.laby)")
	exit()

if argv.count("-h") > 0 :
	labyHeight = int(argv[argv.index("-h")+1]) # we're taking the first one
else :
	labyHeight = 20

if argv.count("-w") > 0 :
	labyWidth = int(argv[argv.index("-w")+1])
else :
	labyWidth = 20

if argv.count("-s") > 0 :
	labySeed = argv[argv.index("-s")+1]
else :
	labySeed = str(time())

if argv.count("-o") > 0 :
	outputFile = argv[argv.index("-o")+1]
else :
	outputFile = "a.laby"


# generating a table full of 1s

myLabyrinth = []

for y in range(labyHeight) :
	newLabyLine = []
	for x in range(labyWidth) :
		newLabyLine.append(1)
	myLabyrinth.append(newLabyLine)


# picking a spawn point at random
# we're biasing the random so that spawn & objective will tend to spawn at points opposite from each other
random.seed(labySeed+str(labyHeight)+str(labyWidth)+str(labyWidth%labyHeight*3.14))
objectiveSide = random.randint(1,4)
#1 -> top left
#2 -> top right
#3 -> bottom right
#4 -> bottom left

# since I divide by four, here's how it pans out :
# x00x
# 0000
# 0000
# x00x
# where X are the parts possible for a spawn or objective

# now, the floor(...) -1 are legacy from when I didn't want it to get out of bounds.. but should they be before the division by four ? Eh, who cares I guess. Shouldn't cause problems.

if objectiveSide == 1 : # top left
	random.seed(labySeed+str(labyHeight+labyWidth))
	spawnX = random.randint(0, floor(labyWidth/4)-1)
	random.seed(labySeed+str(labyHeight-labyWidth))
	spawnY = random.randint(0, floor(labyHeight/4)-1)

elif objectiveSide == 2 : # top right
	random.seed(labySeed+str(labyHeight+labyWidth))
	spawnX = random.randint(floor(3*(labyWidth/4)), labyWidth-1)
	random.seed(labySeed+str(labyHeight-labyWidth))
	spawnY = random.randint(0, floor(labyHeight/4)-1)

elif objectiveSide == 3 : # bottom left
	random.seed(labySeed+str(labyHeight+labyWidth))
	spawnX = random.randint(0, floor(labyWidth/4)-1)
	random.seed(labySeed+str(labyHeight-labyWidth))
	spawnY = random.randint(floor(3*(labyHeight/4)), labyHeight-1)

elif objectiveSide == 4 : # bottom right
	random.seed(labySeed+str(labyHeight+labyWidth))
	spawnX = random.randint(floor(3*(labyWidth/4)), labyWidth-1)
	random.seed(labySeed+str(labyHeight-labyWidth))
	spawnY = random.randint(floor(3*(labyHeight/4)), labyHeight-1)


myLabyrinth[spawnY][spawnX] = 3

# I tried to trace a path of zeros and put an objective at its end but the results were not conclusive.. most often they ended up right next to one another

# Instead we'll pick out an objective and trace a path to it

# obviously, the objective will be placed opposite from the spawn..
if objectiveSide == 1 : # spawn is top left so we want the target bottom right
	random.seed(labySeed+str(labyHeight/labyWidth))
	objectiveX = random.randint(floor(3*(labyWidth/4)), labyWidth-1)
	random.seed(labySeed+str(labyHeight*labyWidth))
	objectiveY = random.randint(floor(3*(labyHeight/4)), labyHeight-1)

if objectiveSide == 2 : # target bottom left 
	random.seed(labySeed+str(labyHeight/labyWidth))
	objectiveX = random.randint(0, floor(labyWidth/4)-1)
	random.seed(labySeed+str(labyHeight*labyWidth))
	objectiveY = random.randint(floor(3*(labyHeight/4)), labyHeight-1)

if objectiveSide == 3 : # target top right
	random.seed(labySeed+str(labyHeight/labyWidth))
	objectiveX = random.randint(floor(3*(labyWidth/4)), labyWidth-1)
	random.seed(labySeed+str(labyHeight*labyWidth))
	objectiveY = random.randint(0, floor(labyHeight/4)-1)

if objectiveSide == 4 : # target top left
	random.seed(labySeed+str(labyHeight/labyWidth))
	objectiveX = random.randint(0, floor(labyWidth/4)-1)
	random.seed(labySeed+str(labyHeight*labyWidth))
	objectiveY = random.randint(0, floor(labyHeight/4)-1)

myLabyrinth[objectiveY][objectiveX] = 2

workingX = spawnX
workingY = spawnY
kPathfinding = 0
haveWeGoneTooFar = False
while workingX != objectiveX or workingY != objectiveY :
	random.seed(labySeed+str(workingX+workingY+kPathfinding)) #kPathfinding is the anti-infinite loop
	if kPathfinding > labyWidth*labyHeight and haveWeGoneTooFar == False :
		haveWeGoneTooFar = True
		stderr.write("Warning -- could not reach objective :\nAfter "+str(kPathfinding-1)+" loops, this program will stop messing around when trying to get to the objective, and instead go straight for it. (ie, pathfinding randomization has been disabled)\n\n")
	if haveWeGoneTooFar == True :
		whatWillWeDo = random.randint(1,6) # this ensures that if we're not making progress for too long, the thing just stops and go straight for the objective
	
	else : 
		whatWillWeDo = random.randint(1,8)	

	# basically : 
	# 1,2,3 : we go towards the objective in X axis
	# 4,5,6 : we go towards the objective in Y axis
	# 7 : we go in the direction opposite to the objective in X axis
	# 8 : we go in the direcion opposite to the objective in Y axis
	#
	# is there a chance of infinite loop this way ? I'm pretty sure there is
	# the k variable is there to make sure it's purely statistical	
	# also if it gets too high we say fuck this and exit

	if 1 <= whatWillWeDo <= 3 :
		if workingX > objectiveX :
			workingX = workingX - 1
		elif workingX < objectiveX :
			workingX = workingX + 1
		else : # we're there already
			pass
	elif 4 <= whatWillWeDo <= 6 :
		if workingY > objectiveY :
			workingY = workingY - 1
		elif workingY < objectiveY :
			workingY = workingY + 1
		else : # we're there already
			pass

	elif whatWillWeDo == 7 :	
		if workingX > objectiveX and workingX < labyWidth :
			workingX = workingX + 1
			if myLabyrinth[workingY][workingX] == 0 : # we're not backtracking
				workingX = workingX -1
		elif workingX <= objectiveX and workingX > 0 :
			workingX = workingX - 1
			if myLabyrinth[workingY][workingX] == 0 :
				workingX = workingX +1

	elif whatWillWeDo == 8 :	
		if workingY > objectiveY and workingY < labyHeight:
			workingY = workingY + 1
			if myLabyrinth[workingY][workingX] == 0 :
				workingY = workingY -1
		elif workingY <= objectiveY and workingY > 0 :
			workingY = workingY - 1
			if myLabyrinth[workingY][workingX] == 0 :
				workingY = workingY +1

	kPathfinding = kPathfinding+1
	if kPathfinding > labyWidth*labyHeight*2 : # this is a very generousy value..
		stderr.write("Error -- could not reach objective :\nAfter "+str(kPathfinding-1)+" loops trying to get to the objective, this program gave up. It will now stop tracing a path to the objective, and go to the next step. You should be able to find the resulting (likely unplayable) labyrinth as "+outputFile+".\n\n")
		break # actually this shouldn't happen anymore, I got a better idea : no more fooling around (whatWillWeDo == 7 or 8) if kPathfinding is too high

	if myLabyrinth[workingY][workingX] < 2 : # it's a 0 or 1, not an objective or spawn
		myLabyrinth[workingY][workingX] = 0


# now we blow holes at random in the 1s of the table


kPokingHoles = 0
while kPokingHoles < ((labyWidth*labyHeight)) : # labyWidth*labyHeight is an arbitrary value. Keep in mind we could pick the same square twice, and only squares with a 1 are eligible
	random.seed(labySeed+str(labyWidth)+str(kPokingHoles)+str(kPathfinding))
	randX = random.randint(0, labyWidth-1)
	random.seed(labySeed+str(labyHeight)+str(kPokingHoles))
	randY = random.randint(0, labyHeight-1)

	if myLabyrinth[randY][randX] == 1 :
		myLabyrinth[randY][randX] = 0 	
	
	kPokingHoles = kPokingHoles + 1

# now we write to file
fileStream = open(outputFile, "w")
for y in range(labyHeight) :
	workingLine = ""
	for x in range(labyWidth) :
		workingLine = workingLine + str(myLabyrinth[y][x])
	fileStream.write(workingLine+"\n")

fileStream.close()


print("Labyrinth written to "+outputFile+". It took "+str(kPathfinding)+" loops to find a way from the spawn point to the objective, plus "+str(kPokingHoles)+" loops to poke holes in the thing so it would look better. Seed was \""+labySeed+"\" with "+str(labyWidth)+" squares of width and "+str(labyHeight)+" squares of height.")
