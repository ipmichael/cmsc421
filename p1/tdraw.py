"""
File: draw.py -- Dana Nau, Sept. 22, 2015
A drawing module you can use while developing your code for Project 1.

---------------------------------------------------------------------------
IMPORTANT: BEFORE SUBMITTING YOUR CODE FOR PROJECT 1,
		   REMOVE EVERYTHING THAT DEPENDS ON THIS MODULE!
If you submit code that needs this module, we won't be able to run it
correctly on the grace machines, so you'll get points taken off.
---------------------------------------------------------------------------

Here's how to use this module:
- Launch python, in the same directory where you have this file.
- Type "import tdraw" to import this file.
- To initialize a graphics window, call tdraw.init().
- Each time you want to display a route-finding problem, call
  tdraw.draw_problem(walls,start,finish). You can add True as an optional
  4th argument if you want the drawing to include a coordinate grid.
- To overlay your path onto the drawing of the problem, call
  tdraw.draw_path(path).

This file includes an example that you can try out, like this:
tdraw.init()
tdraw.draw_problem(tdraw.example_walls,tdraw.example_start,tdraw.example_finish,True)
tdraw.draw_path(tdraw.example_path)
"""

import turtle

def init():
	"""Call this to initialize the drawing package."""
	turtle.reset()

def draw_problem(walls,start=None,finish=None,grid=False):
	"""
	draw_problem first set_scale to set the plotting scale,
	then it draws walls, start, and finish line.
	The grid argument tells whether or not to draw a grid behind the problem.
	"""
	clear()
	set_scale(walls,grid)
	draw_lines(walls)
	if start: draw_dot(start,color='blue',size=12)
	if finish: draw_lines([finish], color='green', width=2, dots=0)

def draw_path(path):
	"""draw a path"""
	x0 = False
	for (x1,y1) in path:
		if x0:
			draw_lines([((x0,y0),(x1,y1))], color='red', width=2, dots=8)
		(x0,y0) = (x1,y1)

def draw_move(move,status):
	"""
	Draw the line for an individual move. Use status to tell whether the
	move is one that you're generating, expanding, or re-expanding.
	"""
	if status=='generate':
		draw_lines([move], width=1, color='orange')
	elif status=='expand':
		draw_lines([move], width=2, color='blue', visible=True)
		draw_lines([move], width=2, color='cyan')
	elif status=='re-expand':
		draw_lines([move], width=2, color='blue', visible=True)
		draw_lines([move], width=3, color='purple')
	elif status=='finish':
		# this doesn't really do much, but here it is anyway:
		draw_lines([move], width=3, color='red')
	else:
		raise RuntimeError("'" + status + "' is not a move status")


################## Primitives #######################
# These get called by the above functions.
# You probably won't need to call any of them directly.
	
def clear():
	"""Clear the graphics window."""
	turtle.clear()

def set_scale(lines,grid=False):
	"""This sets the coordinate scale so that lines will nearly fill
	the window that you're drawing in. It doesn't actually draw anything.
	If grid=True, it will then draw a grid.
	"""
	global lowerleft
	global upperright
	lowerleft = min([min(x0,y0,x1,y1) for ((x0,y0),(x1,y1)) in lines])
	upperright = max([max(x0,y0,x1,y1) for ((x0,y0),(x1,y1)) in lines])
	size = upperright - lowerleft
	margin = size*.1
	turtle.setworldcoordinates(lowerleft-margin,lowerleft-margin,upperright+margin,upperright+margin)
	turtle.pen(speed=10,shown=False)
	if grid: draw_grid(lowerleft,upperright)

def draw_lines(lines, color='black', width=3, dots=0, visible=False):
	"""draw every line in lines"""
	turtle.pen(speed=10,shown=False)
	turtle.color(color)
	turtle.width(width)
	for line in lines:
		((x0,y0),(x1,y1)) = list(line)
		turtle.penup()
		turtle.goto((x0,y0))
		turtle.pendown()
		if dots>0: turtle.dot(dots)
		if visible:
#			 turtle.pen(speed=10,shown=True)
			turtle.goto((x1,y1))
#			 turtle.pen(speed=10,shown=False)
		else:
			turtle.goto((x1,y1))


def draw_dot(loc,color='red',size=10):
	"""put a dot at location loc"""
	(x,y) = loc
	turtle.penup()
	turtle.goto((x,y))
	turtle.dot(size,color)

def draw_finish(loc,color='red',size=10):
	"""put a dot at location loc"""
	(x,y) = loc
	turtle.penup()
	turtle.goto((x,y))
	turtle.dot(size,color)

def draw_grid(ll,ur):
	size = ur - ll
	for gridsize in [1, 2, 5, 10, 20, 50, 100 ,200, 500]:
		lines = (ur-ll)/gridsize
		# print('gridsize', gridsize, '->', int(lines)+1, 'lines')
		if lines <= 11: break
	turtle.color('gray')
	turtle.width(1)
	x = ll
	while x <= ur:
		if int(x/gridsize)*gridsize == x:
			turtle.penup()
			turtle.goto(x, ll-.25*gridsize)
			turtle.write(str(x),align="center",font=("Arial",12,"normal"))
			turtle.goto(x,ll)
			turtle.pendown()
			turtle.goto(x,ur)
			# print(x,ll,'to',x,ur)
		x += 1
	y = ll
	while y <= ur:
		# horizontal grid lines:
		if int(y/gridsize)*gridsize == y:
			turtle.penup()
			turtle.goto(ll-.1*gridsize, y - .06*gridsize)
			turtle.write(str(y),align="right",font=("Arial",12,"normal"))
			turtle.goto(ll,y)
			turtle.pendown()
			turtle.goto(ur,y)
			# print(ll,y,'to',ur,y)
		y += 1

########## Test data ##########

# Here's the problem in the project description, and a path that solves it.

example_walls=[
	{(0,0), (10,0)}, {(10,0),(10,10)},	{(10,10),(20,10)},{(20,10),(30,0)},
	{(30,0),(30,10)}, {(30,10),(10,20)}, {(10,20),(0,20)}, {(0,20),(0,0)}, 
	{(3,14),(10,14)}, {(10,14),(10,16)}, {(10,16),(3,16)}, {(3,16),(3,14)}]

example_start = (4, 5)

example_finish = ((24,8), (26,11))

example_path=[
	(4, 5), (5, 6), (7, 8), (10, 11), (14, 13), (18, 14), (21, 14),
	(23, 13), (25, 11), (26, 10), (26, 9), (26, 9)]
