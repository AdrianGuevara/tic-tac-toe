emptyMark = '_'

def bestPlay(playerMark, grid):
	return max(possiblePlays(playerMark, grid), key=lambda play: play[1])[0]

def possiblePlays(playerMark, grid):
	return [
	(markPlay(playerMark, emptyPosition, grid),
	playScore(playerMark, emptyPosition, grid))
	for emptyPosition in emptyPositions(grid)]

def markPlay(playerMark, emptyPosition, grid):
	return {
	position: playerMark if position == emptyPosition else mark
	for position, mark in grid.items()}

def playScore(playerMark, playPosition, grid):
	return 100 if anyThreeInLine(playerMark, markPlay(playerMark, playPosition, grid)) else 0

def anyThreeInLine(playerMark, grid):
	return any([threeInLine(playerMark, line)
	for line in gridLines(grid)])

def threeInLine(playerMark, line):
	return all([mark==playerMark for mark in line.values()])

def positionLines(position, grid):
	return [line for line in gridLines(grid) if position in line]

def gridLines(grid):
	return gridRows(grid) + gridColumns(grid) + gridDiagonals(grid)

def gridRows(grid):
	return [{(i, j): grid.get((i, j)) for j in range(3)} for i in range(3)]

def gridColumns(grid):
	return [{(i, j): grid.get((i, j)) for i in range(3)} for j in range(3)]

def gridDiagonals(grid):
	return [firstDiagonal(grid), secondDiagonal(grid)]

def firstDiagonal(grid):
	return {(i, i): grid.get((i, i)) for i in range(3)}

def secondDiagonal(grid):
	return {(i, j): grid.get((i, j)) for i, j in zip(range(3), reversed(range(3)))}

def emptyPositions(grid):
	return [position for position, mark in grid.items() if mark == emptyMark]




def printGrid(grid):
	aux = ""
	for i in range(3):
		aux = "|"
		for j in range(3):
			aux+=str(grid.get((i,j)))+"|"
		print(aux)

initialGrid = {
(0,0): '_', (0,1): '_', (0,2): '_',
(1,0): 'o', (1,1): 'o', (1,2): 'x',
(2,0): 'x', (2,1): 'o', (2,2): 'x'}
for line in positionLines((1,1), initialGrid):
	print(line)
	print('=======')
