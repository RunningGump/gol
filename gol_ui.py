#!/usr/bin/python

import copy
import pygame
from pygame.locals import *


# Colors
GRAY	= (127, 127, 127)
MAGENTA	= (255, 0, 255)
WHITE	= (255, 255, 255)
YELLOW	= (255, 255, 0)

# Constants
WORLD_SIZE = 100
CELL_SIZE = 5
VIEW_GRID = 0
WRAP_EDGES = True

# Spaceships
GLIDER = [
	[0, 1, 0],
	[0, 0, 1],
	[1, 1, 1],
]

# Oscillators
BLINKER = [
	[1, 1, 1],
]

# Methuselahs
R_PENTOMINO = [
	[0, 1, 1],
	[1, 1, 0],
	[0, 1, 0]
]

TEST = [
    [0,0,1,1,1,0,0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [0,0,1,1,1,0,0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,0],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,0]
]

class Cell(object):
	alive = False

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __repr__(self):
		return "(%d, %d)" % (self.x, self.y)

	def draw(self, screen):
		rect = [self.x * CELL_SIZE + 1, self.y * CELL_SIZE + 1, CELL_SIZE - 1, CELL_SIZE - 1]
		pygame.draw.rect(screen, YELLOW, rect)

	def isAlive(self):
		return self.alive

	def isDead(self):
		return not self.alive

def buildGrid(screen):
	# Fill grid background
	grid = pygame.Surface(screen.get_size())
	grid = grid.convert()
	grid.fill(GRAY)

	# Draw grid lines
	if VIEW_GRID:
		for i in range(0, WORLD_SIZE * CELL_SIZE + 1, CELL_SIZE):
			pygame.draw.line(grid, WHITE, (i, 0), (i, WORLD_SIZE * CELL_SIZE))
			pygame.draw.line(grid, WHITE, (0, i), (WORLD_SIZE * CELL_SIZE, i))

	return grid

def layCells():
	cells = []
	for i in range(WORLD_SIZE):
		row = []
		for j in range(WORLD_SIZE):
			row.append(Cell(j, i))
		cells.append(row)

	#for cell in GLIDER:
	#	cells[cell[0]][cell[1]].alive = True

	pattern = TEST
	pos = (WORLD_SIZE / 2 - 1, WORLD_SIZE / 2 - 1)

	for row in range(len(pattern)):
		for col in range(len(pattern[row])):
			if pattern[row][col]:
				cells[int(pos[1] + row)][int(pos[0] + col)].alive = True

	return cells

def countLiveNeighbours(cell, cells):
	total = 0
	for i in range(cell.y - 1, cell.y + 2):
		for j in range(cell.x - 1, cell.x + 2):
			if not (i == cell.y and j == cell.x):
				if WRAP_EDGES:
					if cells[i % WORLD_SIZE][j % WORLD_SIZE].isAlive():
						total += 1
				else:
					if 0 <= i and i < WORLD_SIZE and \
					   0 <= j and j < WORLD_SIZE:
						if cells[i][j].isAlive():
							total += 1
	return total

def main():
	# Initialise screen
	pygame.init()
	pygame.display.set_caption('Game of Life')
	screen = pygame.display.set_mode((WORLD_SIZE * CELL_SIZE + 1, WORLD_SIZE * CELL_SIZE + 1))
	clock = pygame.time.Clock()

	grid = buildGrid(screen)
	cells = layCells()

	# Event loop
	while 1:
		# -- Update --

		clock.tick(100)

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return
			elif event.type == QUIT:
				return

		# Updating cells
		newCells = copy.deepcopy(cells)

		for i, row in enumerate(cells):
			for j, cell in enumerate(row):
				liveNeighbours = countLiveNeighbours(cell, cells)
				if cell.isAlive():
					if liveNeighbours < 2 or \
					   liveNeighbours > 3:
						newCells[i][j].alive = False
				elif cell.isDead():
					if liveNeighbours == 3:
						newCells[i][j].alive = True

		cells = newCells

		# -- Render --

		# Draw grid
		screen.blit(grid, (0, 0))

		# Draw cells
		for row in cells:
			for cell in row:
				if cell.isAlive():
					cell.draw(screen)

		screen.blit(screen, (0, 0))
		pygame.display.flip()


if __name__ == '__main__': main()
