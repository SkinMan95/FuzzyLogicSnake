import logging
import random
import copy
import time
import numpy as np

grid = None


def sum_pos(a, b):
	assert len(a) == len(b)
	r = [0] * len(a)
	for i in range(len(a)):
		r[i] = a[i] + b[i]

	print("{} + {} = {}".format(a, b, r))
	return r


class Element(object):
	def __init__(self, init_pos=None):
		self.pos = init_pos if init_pos else [0,0]
		
	def get_pos(self):
		return self.pos
		
	def set_pos(self, npos):
		self.pos = npos
		return self.pos
	

class MoveElement(Element):
	directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]

	def __init__(self, init_pos, direction=None):
		super(MoveElement, self).__init__(init_pos)
		self.direction = random.choice(MoveElement.directions) if direction is None else direction
		self.lastPosition = None
		
	def move(self, dir):
		self.lastPosition = copy.deepcopy(self.pos)
		self.set_pos(sum_pos(self.pos, dir))
	

class Target(Element):
	def __repr__(self):
		return "O"


class Obstacle(Element):
	def __repr__(self):
		return "#"


class Snake(MoveElement):
	global grid

	def __init__(self, initpos):
		super(Snake, self).__init__(initpos, random.choice(MoveElement.directions))
		self.tail = None

	def grow_tail(self):
		self.tail = TailElement(init_pos=self.pos) if self.tail is None else TailElement(init_pos=self.pos, tail=self.tail)
		return self.tail

	def move(self, d):
		lpos = self.get_pos()
		super(Snake, self).move(d)
		if self.tail is not None:
			self.tail.move(lpos)

	def get_tail(self):
		return self.tail

	def get_head_pos(self):
		return self.head_pos

	def __repr__(self):
		return "*"


class TailElement(MoveElement):
	def __init__(self, init_pos=None, tail=None):
		super(TailElement, self).__init__(init_pos)
		self.tail = None

	def __repr__(self):
		return "."

	def get_next(self):
		return self.tail

	def move(self, pos):
		last_move = self.pos
		self.set_pos(pos)
		if self.tail:
			self.tail.move(last_move)
				

def gen_random_pos(lim):
	return [random.randint(2, lim-2), random.randint(2, lim-2)]


class Grid(object):
	@staticmethod
	def gen_random_grid(dimensions, snake, nobstacles, target=None):
		elements = [Obstacle() for i in range(nobstacles)]

		if target is None:
			pos = gen_random_pos(dimensions)
			while pos == snake.get_pos():
				pos = gen_random_pos(dimensions)
		target = Target(gen_random_pos(dimensions)) if target is None else target

		grid = [[None for i in range(dimensions)] for j in range(dimensions-2)]

		for i in grid:
			i[0] = Obstacle()
			i[-1] = Obstacle()
		grid.insert(0, [Obstacle() for i in range(dimensions)])
		grid.append([Obstacle() for i in range(dimensions)])

		# pos = snake.get_pos()
		# grid[pos[0]][pos[1]] = snake

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

		self.grid = Grid.gen_random_grid(dimensions=self.dimensions, snake=self.snake, nobstacles=self.nobstacles, target=None) if initial_grid is None \
			else initial_grid

	def can_move(self, pos, snake):
		can = self.grid[pos[0]][pos[1]] is None

		tail = snake.get_tail()
		while can and tail is not None:
			can = pos != tail.get_pos()
			tail = tail.get_next()

		return can

	def takeStep(self) -> bool:
		spos = self.snake.get_pos()
		dirs = MoveElement.directions[:] # copy
		random.shuffle(dirs)
		moved = False
		for d in dirs:
			npos = sum_pos(spos, d)
			if self.can_move(npos, self.snake):
				self.snake.move(d)
				moved = True

		if not moved:
			print("Can't step any further")

		return moved

	def next_move(self, iterations=None):
		assert isinstance(iterations, int) or iterations is None
		assert iterations is None or iterations > 0

		iterate = True
		while iterate and (iterations is None or iterations > 0):
			print(self)
			iterate = self.takeStep()

			iterations = iterations-1 if iterations is not None else None

		print(self)

	def __str__(self):
		r = ""
		# print("pos:", self.snake.get_pos())

		grid = self.grid
		for i in range(len(grid)):
			for j in range(len(grid[i])):
				# print((i, j))
				if [i, j] == self.snake.get_pos():
					r += "*"
				else:
					r += str(grid[i][j]) if grid[i][j] is not None else " "
			r += "\n"
		return r			


def example(grid):
	for i in range(10):
		# print(grid)
		print(i)
		grid.next_move()
		time.sleep(1)




def main():
	global grid
	grid = Grid(10)
	example(grid)


if __name__ == "__main__":
	main()