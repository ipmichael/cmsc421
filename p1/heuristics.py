########## Examples of heuristic functions -- Dana Nau, 2015.09.25 ##########
#
# Here are three simple heuristic functions you can use to test your code.
# In my tests, h_edist usually worked best, but h_xymax was best in one case.
#
##########

# need the math module because we'll take some square roots
import math


def h_edist(state, ((x1,y1),(x2,y2)), walls):
	"""Euclidean distance from state to the finish line."""
	(x,y) = state[0]
	d1 = math.sqrt((x1-x)**2 + (y1-y)**2)
	d2 = math.sqrt((x2-x)**2 + (y2-y)**2)
	
	## If the finish line's endpoints are equidistant,
	## then return the distance to the center of the finish line.
	## Otherwise, return the distance to the closer endpoint.
	if d1 == d2:
		(xm,ym) = ((x1+x2)/2.0, (y1+y2)/2.0)
		return math.sqrt((xm-x)**2 + (ym-y)**2)
	else:
		return min(d1,d2)
		

def h_xymax(state, f_line, walls):
	"""Return the max of the x and y distances from state to center of finish line."""
	(x,y) = state[0]
	((x1,y1),(x2,y2)) = f_line
	d1 = xymax_helper((x,y),(x1,y1))
	d2 = xymax_helper((x,y),(x2,y2))
	if d1 == d2:
		(xm,ym) = ((x1+x2)/2.0, (y1+y2)/2.0)
		return xymax_helper((x,y),(xm,ym))
	return min(d1,d2)

def xymax_helper((x1,y1), (x2,y2)):
	"""
	Helper function for xymax; returns the max of the x-distance and y-distance
	between two points.
	"""
	xdist = abs(x1 - x2)	  # distance in the x direction
	ydist = abs(y1 - y2)	  # distance in the y direction
	return max(xdist, ydist)  # max distance in either direction



def h_moves0(state, f_line, walls):
	"""Number of moves it would take to reach center of finish line if stopped at current loc."""
	# get the max of the x distance and y distance to the goal
	dist = h_xymax(state, f_line, walls)
	
	# Suppose we start at speed 0, increase our speed by 1 at each move until
	# we reach some speed s, then decrease our speed by 1 at each move until
	# we're back to 0. If we don't crash into a wall, we've traveled a distance
	# of s^2. We want the largest s such that s^2 <= the distance to the goal.
	s = 0
	while s**2 <= dist:
		s += 1
	# We now have the smallest s such that s^2 >= the distance to the goal, so
	# we need to reduce s by 1.
	s -= 1
	
	# If we start at speed 0, go up to speed s, then go back down to 0, that's a
	# sequence of 2s moves. By inserting at most two more moves (of speed s or less)
	# into the sequence, we can get a sequence of moves that reaches the goal.
	difference = dist - s**2
	if difference == 0:
		return 2*s		 # no more moves, we're already at the goal
	if difference <= s:
		return 2*s+1	 # need to insert 1 more move somewhere
	else:
		return 2*s + 2	 # we need to insert 2 moves
