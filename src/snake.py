import logging
import random
import copy
import time
import threading
grid = None

class Element(object):
	def __init__(self, init_pos=None):
		self.pos = init_pos if init_pos else [0,0]
		
	def get_pos(self):
		return self.pos
		
	def set_pos(self, npos):
		self.pos = npos
		return self.pos
	

class MoveElement(Element):
	directions = [(1,0),(0,-1),(-1,0),(0,1)]

	def __init__(self, init_pos,direction):
		super(MoveElement, self).__init__(init_pos)
		self.direction = random.choice(MoveElement.directions)
		self.lastPosition  = None
		
	def move(self, dir):
		lastPosition = copy.deepcopy(self.pos)
		npos = self.pos
		for i in range(len(dir)):
			npos[i] += dir[i]
		self.pos = npos  
	

class Target(Element):
	def __repr__(self):
		return "O"

class Obstacle(Element):
	def __repr__(self):
		return "#"


class Snake(MoveElement):
	global grid
	def __init__(self, initpos):
		# super(Snake, self).__init__(*args)) # stemen que inventa :v
		super(Snake, self).__init__(initpos, random.choice(MoveElement.directions))
		self.tail = None

	def grow_tail(self):
		self.tail = TailElement(initPos=self.pos) if self.tail is None else TailElement(initPos=self.pos, tail=self.tail)
		return self.tail

	def move(self):  	
		# super(Snake, self).move(dir)
		if self.tail != None:
			self.tail.set

	def get_tail(self):
		return self.tail

	def get_head_pos(self):
		return self.head_pos

	def __repr__(self):
		return "*"
				
class TailElement(MoveElement):
	def __init__(self, initPos=None, tail=None):
		super(TailElement, self).__init__(initPos)
		self.tail=None

	def __repr__(self):
		return "."

	def move(self, pos):
		lastMove = self.pos
		self.set_pos(pos)
		if tail:
			self.tail.move(lastMove)
				

def gen_random_pos(lim):
	return [random.randint(2, lim-2), random.randint(2, lim-2)]

class Grid(object):
  
	def gen_random_grid(self, dimensions, snake, nobstacles, target=None):
		elements = [Obstacle() for i in range(nobstacles)]

		if target is None:
			pos = gen_random_pos(dimensions)
			while pos == snake.get_pos():
				pos = gen_random_pos(dimensions)
		target = Target(gen_random_pos(dimensions)) if target is None else target

		grid = [[None for i in range(dimensions)] for j in range(dimensions-2)]

		for i in grid:
			i[0]=Obstacle()
			i[dimensions-1]=Obstacle()
		grid.insert(0,[Obstacle() for i in range(dimensions)])
		grid.append([Obstacle() for i in range(dimensions)])

		pos = snake.get_pos()
		grid[pos[0]][pos[1]] = snake

		pos = target.get_pos()
		grid[pos[0]][pos[1]] = target

		while len(elements) > 0:
			pos = gen_random_pos(dimensions)
			while grid[pos[0]][pos[1]] is not None:
				pos = gen_random_pos(dimensions)
			
			e = elements.pop()
			e.set_pos(pos)
			grid[pos[0]][pos[1]] = e

		return grid


	def __init__(self, dimensions, initial_grid=None, nobstacles=None, snake=None):
		assert isinstance(dimensions, int)
		assert (nobstacles is None) or (nobstacles < dimensions**2)

		self.dimensions = dimensions
		self.nobstacles = random.randint(1, dimensions//2) if nobstacles is None else nobstacles
		self.snake = snake if snake is not None else Snake(gen_random_pos(self.dimensions))

		self.grid = self.gen_random_grid(self.dimensions, self.snake, self.nobstacles) if initial_grid is None else initial_grid

	def nextMove(self):
		self.snake.move()
		# cords = self.snake.get_head_pos()
		# print(cords)
		pass

	def __str__(self):
		r = ""
		for i in self.grid:
			for j in i:
				r += str(j) if j != None else " "
			r += "\n"
		return r			

def example(grid):
	for i in range(10):
		print(grid)
		print(i)
	grid.nextMove()
	time.sleep(1)


def main():
	global grid
	grid = Grid(10)
	threading.Thread(target=example(grid)).start()
if __name__ == "__main__":
	main()