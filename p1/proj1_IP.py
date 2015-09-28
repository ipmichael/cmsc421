'''
Michael Ip

	I pledge on my honor that I have not given or received
any unauthorized assistance on this project.
	Michael Ip, ip.w.michael@gmail.com

	** How The Code Works **

'''

#Dana Nau's intersect function
def intersect(e1,e2):
	"""Return True if edges e1 and e2 intersect, False otherwise."""	   
	
	# First, grab all the coordinates
	((x1a,y1a), (x1b,y1b)) = e1
	((x2a,y2a), (x2b,y2b)) = e2
	dx1 = x1a-x1b
	dy1 = y1a-y1b
	dx2 = x2a-x2b
	dy2 = y2a-y2b
	
	if (dx1 == 0) and (dx2 == 0):		# both lines vertical
		if x1a != x2a: return False
		else: return collinear_point_in_edge((x1a,y1a),e2) or collinear_point_in_edge((x1b,y1b),e2)
	if (dx2 == 0):		# e2 is vertical, so m2 = infty
		x = x2a
		# compute y = m1 * x + b1, but minimize roundoff error
		y = (x2a-x1a)*dy1/float(dx1) + y1a
		return collinear_point_in_edge((x,y),e1) and collinear_point_in_edge((x,y),e2) 
	elif (dx1 == 0):		# e1 is vertical, so m1 = infty
		x = x1a
		# compute y = m2 * x + b2, but minimize roundoff error
		y = (x1a-x2a)*dy2/float(dx2) + y2a
		return collinear_point_in_edge((x,y),e1) and collinear_point_in_edge((x,y),e2) 
	else:		# neither line is vertical
		# check m1 = m2, without roundoff error:
		if dy1*dx2 == dx1*dy2:		# same slope, so either parallel or collinear
			# check b1 != b2, without roundoff error:
			if dx2*dx1*(y2a-y1a) != dy2*dx1*x2a - dy1*dx2*x1a:
				return False
			return collinear_point_in_edge((x1a,y1a),e2) or collinear_point_in_edge((x1b,y1b),e2)
		# compute x = (b2-b1)/(m1-m2) but minimize roundoff error:
		x = (dx2*dx1*(y2a-y1a) - dy2*dx1*x2a + dy1*dx2*x1a)/float(dx2*dy1 - dy2*dx1)
		# compute y = m1*x + b1 but minimize roundoff error
		y = (dy2*dy1*(x2a-x1a) - dx2*dy1*y2a + dx1*dy2*y1a)/float(dy2*dx1 - dx2*dy1)
	return collinear_point_in_edge((x,y),e1) and collinear_point_in_edge((x,y),e2) 


def collinear_point_in_edge((x,y),((xa,ya),(xb,yb))):
	"""
	Helper function for intersect.
	If (x,y) is collinear with the edge from (xa,ya) to (xb,yb), then
	(x,y) is in the edge if
		x is between xa and xb, inclusive, and
		y is between ya and yb, inclusive.
	The test of y is redundant except when line is vertical.
	"""
	if ((xa <= x <= xb) or (xb <= x <= xa)) \
	   and ((ya <= y <= yb) or (yb <= y <= ya)):
	   return True
	return False


def crash(e, w):
	'''
	Return True if edge e intersects with any wall in w
	Return False otherwise
	'''

	for wall in w:
		if intersect(e, wall):
			return True
	return False

def velocities(s, w):
	'''
	Returns set of possible choices of velocities.
	'''
	toReturn = [] #list of possible choices
	((x, y), (vx, vy)) = s
	for i in range(-1,2):
		for j in range(-1,2):
			(vxTemp, vyTemp) = (vx + i, vy + j)
			edge = ((x,y), (x+vxTemp, y+vyTemp))
			if(not crash(edge, w)):
				toReturn.append((vxTemp,vyTemp))
	return toReturn



