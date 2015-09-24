"""
File: mdraw.py -- Dana Nau, Sept. 22, 2015
A drawing module you can use while developing your code for Project 1.

---------------------------------------------------------------------------
IMPORTANT: BEFORE SUBMITTING YOUR CODE FOR PROJECT 1,
		   REMOVE EVERYTHING THAT DEPENDS ON THIS MODULE!
If you submit code that needs this module, we won't be able to run it
correctly on the grace machines, so you'll get points taken off.
---------------------------------------------------------------------------

To use this code, you'll need to install matplotlib on your machine.
If you have installed python 2 (I used 2.7.10, but I think other versions
will probably work too) and matplotlib, here's what to do:

- Launch python, in the same directory where you have this file.

- Type "import mdraw" to import this file.

- Call mdraw.draw_problem(walls,start,goal) to tell mdraw to draw a
  route-finding problem. If you don't want a coordinate grid,
  you can specify False as an optional fourth argument.

- Call mdraw.draw_move(move,'expand') each time you expand a node, and
  mdraw.draw_move(move,'re-expand') each time you re-expand a node, to tell
  mdraw to draw the expansions and reexpansions.

- Call mdraw.draw_path(path) to tell mdraw to draw a path.

- Call mdraw.show() to display what you've drawn.

If you created the above file on grace.umd.edu, you'll need to copy it to 
your own machine. Then, on your own machine, launch python 2 and import the
file. If everything works correctly, this will open a python graphics window
and draw everything that you specified. 

This file includes an example that you can try out, like this:

import mdraw
mdraw.draw_problem(mdraw.example_walls,mdraw.example_start,mdraw.example_finish)
mdraw.draw_path(mdraw.example_path)
mdraw.show()
"""
import matplotlib.pyplot as plt



def draw_problem(walls,start=None,finish=None,grid=True):
	"""
	draw_problem first set_scale to set the plotting scale,
	then it draws walls, start, and goal.
	The grid argument tells whether or not to draw a grid behind the problem.
	"""
	set_scale(walls,grid)
	draw_lines(walls,width=2)
	if start: draw_start(start)
	if finish: draw_finish(finish)

def draw_path(path):
	"""draw a path"""
	x0 = False
	for (x1,y1) in path:
		if x0:
			plt.plot((x0,x1), (y0,y1), color='r', linewidth=2, marker='o')
		(x0,y0) = (x1,y1)


def draw_move(move,status):
	"""
	Draw the line for an individual move. Use status to tell whether the
	move is one that you're generating, expanding, or re-expanding.
	"""
	if status=='generate':
		draw_lines([move], width=1, color='orange')
	elif status=='expand':
		draw_lines([move], width=2, color='cyan')
	elif status=='re-expand':
		draw_lines([move], width=2, color='purple')
	elif status=='goal':
		# this doesn't really do much, but here it is anyway:
		draw_lines([move], width=3, color='r')
	else:
		raise RuntimeError("'" + status + "' is not a move status")

def show():
	plt.show()

################## Primitives #######################
# These get called by the above functions.
# You probably won't need to call any of them directly.
	
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
	mmin = lowerleft-margin
	mmax = upperright+margin
	plt.axis([mmin, mmax, mmin, mmax])
	if grid: draw_grid(lowerleft,upperright)

def draw_lines(lines, color='black', width=2, marker=None):
	"""draw every line in lines"""
	for ((x0,y0), (x1,y1)) in lines:
		plt.plot((x0,x1), (y0,y1), color=color, linewidth=width, marker=marker)
		

def draw_start(loc,color='b',size=10):
	"""put a dot at location loc"""
	(x,y) = loc
	plt.plot((x), (y), color=color, linewidth=size, marker='D',markeredgewidth=2,markeredgecolor='b')

def draw_finish(finish,color='g',width=2):
	"""draw the finish line"""
	((x0,y0), (x1,y1)) = finish
	plt.plot((x0,x1), (y0,y1), color=color, linewidth=width, marker=None)

def draw_grid(ll,ur):
	size = ur - ll
	for gridsize in [1, 2, 5, 10, 20, 50, 100 ,200, 500]:
		lines = (ur-ll)/gridsize
		# print('gridsize', gridsize, '->', int(lines)+1, 'lines')
		if lines <= 11: break
	x = ll
	while x <= ur:
		if int(x/gridsize)*gridsize == x:
			plt.plot((x,x), (ll,ur), color=".75")
			plt.plot((ll,ur), (x,x), color=".75")
		x += 1

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
