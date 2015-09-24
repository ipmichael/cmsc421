"""
CMSC 421 (Intro to AI) -- Dana Nau, Sept. 22, 2015
Graph search, with breadth-first, depth-first, and uniform-cost search strategies.

This file also includes the problem definition for the Romanian Map problem.
Here are some things you can try:

gs.search('Arad', gs.neighbors, {'Bucharest'}, 'bf')
gs.search('Arad', gs.neighbors, {'Bucharest'}, 'df')
gs.search('Arad', gs.neighbors, {'Bucharest'}, 'uc')
gs.search('Arad', gs.neighbors, {'Urziceni'}, 'bf')
gs.search('Arad', gs.neighbors, {'Urziceni'}, 'df')
gs.search('Arad', gs.neighbors, {'Urziceni'}, 'uc')
"""

class Node():
	"""Class for nodes in the search tree"""
	def __init__(self,state,parent,g):
		self.state = state
		self.parent = parent
		self.g = g
		self.children = []

def getpath(y):
	"""Return the path from the root to y"""
	path = [y.state]
	while y.parent:
		y = y.parent
		path.append(y.state)
	path.reverse()
	return path

def expand(x, get_children, explored, debug):
	"""
	Return all children of x whose states aren't already in explored. 
	If debug >= 3, print a list of pruned nodes.
	"""
	pruned = []
	for (state,cost) in get_children(x.state):
		if state in explored:
			if debug >= 3:
				pruned.append(state)
		else:
			y = Node(state, x, x.g + cost)
			x.children.append(y)
	if debug >= 3:
		print '       explored:', ', '.join(explored)
		print '         pruned:', ', '.join(pruned)
	return x.children

def printnodes(nodes):
	"""For each node in nodes, print the state and g-value"""
	nodenames = ['{0} {1}'.format(y.state,y.g) for y in nodes]
	print ', '.join(nodenames)

def search(s0, get_children, goals, strategy='bf', debug=0):
	"""
	Do a graph search starting at s0, looking for a state x in goals.
	get_children is a function to compute a node's children.
	strategy may be either 'bf' (breadth-first) or 'df' (depth-first).
	On each iteration,
		if debug >= 1, print the names and g-values of the nodes in frontier;
		if debug >= 2, print the names and g-values of the expanded node's unpruned children;
		if debug >= 3, print the explored list and the names and g-values of pruned children.
	"""
	frontier = [Node(s0,False,0)]	# "False" means no parent
	explored = []
	prunes = 0
	counter = 0
	while frontier:
		counter += 1
		if debug >= 1:
			print '{:4}'.format(counter),
			printnodes(frontier)
		x = frontier.pop(0)	 # inefficient, but avoids inefficiencies elsewhere
		explored.append(x.state)
		if x.state in goals: 
			solution = getpath(x)
			if debug >= 1:
				print '=> solution', \
					'length {}, cost {}:'.format(len(solution)-1,x.g)
			return solution
		newnodes = expand(x,get_children,explored,debug)
		if debug >= 2:
			print '       children:',
			printnodes(newnodes)
		if strategy == 'bf':		# put new nodes at end of list
			frontier.extend(newnodes)
		elif strategy == 'df':		# put new nodes at start of list
			newnodes.extend(frontier)
			frontier = newnodes
		elif strategy == 'uc':		# sort all nodes by g-value
			frontier.extend(newnodes)
			frontier.sort(key=lambda x: x.g)
		else:
			raise RuntimeError("'" + strategy + "' is not a strategy")
	print "Couldn't find a solution."
	return False


##################################################
# Problem definition for the Romanian map problem.
##################################################

map = {
	'Arad':			{'Sibiu':140,'Timisoara':118,'Zerind':75},
	'Bucharest':	{'Fagaras':211,'Giurgiu':90,'Pitesti':101,'Urziceni':85},
	'Craiova':		{'Dobreta':120,'Pitesti':138,'Rimnicu Vilcea':146},
	'Dobreta':		{'Craiova':120,'Mehadia':75},
	'Eforie':		{'Hirsova':86},
	'Fagaras':		{'Bucharest':211,'Sibiu':99},
	'Giurgiu':		{'Bucharest':90},
	'Hirsova':		{'Eforie':86,'Urziceni':98},
	'Iasi':			{'Neamt':87,'Vaslui':92},
	'Lugoj':		{'Mehadia':70,'Timisoara':111},
	'Mehadia':		{'Dobreta':75,'Lugoj':70},
	'Neamt':		{'Iasi':87},
	'Oradea':		{'Sibiu':151,'Zerind':71},
	'Pitesti':		{'Bucharest':101,'Craiova':138,'Rimnicu Vilcea':97},
	'Rimnicu Vilcea': {'Craiova':146,'Pitesti':97,'Sibiu':80},
	'Sibiu':		{'Arad':140,'Fagaras':99,'Oradea':151,'Rimnicu Vilcea':80},
	'Timisoara':		{'Arad':118,'Lugoj':111},
	'Urziceni':		{'Bucharest':85,'Hirsova':98,'Vaslui':142},
	'Vaslui':		{'Iasi':92,'Urziceni':142},
	'Zerind':		{'Arad':75,'Oradea':71}}

def neighbors(city):
	"""
	get_children function for the Romanian map problem. It returns
	city's neighbors, as a list of (neighbor,distance) pairs.
	"""
	x = map[city].items()
	return x
