'''
Michael Ip

    I pledge on my honor that I have not given or received
any unauthorized assistance on this project.
    Michael Ip, ip.w.michael@gmail.com

    ** How The Code Works **
    I modified the graph search code given by the professor to implement
    an A* search. Nodes are placed into the frontier/priority queue based
    on f(x) = g(x) + h(x), which I used the heapq module to implment.
    g(x) is the depth of the node in my search tree, and h(x) is from my
    heuristic function.

    My heuristic compares vel + (vel - 1) + (vel - 2) + ... = vel(vel - 1)/2,
    where vel is current velocity, to the Euclidean distance to finish.
    This is the distance the node would be from the finish line if the node
    were to slow down by 1 every iteration until the finish line.
    My heuristic returns a value proportional to the difference in that
    comparison. I noticed that this drastically lowered my computation time
    in the huge_l case.

    My heuristic also takes into account the Euclidean distance from the
    next estimated location to the finish line, considering the nodes 
    current velocity. This lowered the number of nodes in my paths, especially
    in huge_l.

    In find_path, I implemented explored as a dictionary so that I could map
    the states to their cost, and check if a better cost path to a repeated
    state was found.
'''

import math
import heapq

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
    
    if (dx1 == 0) and (dx2 == 0):       
    # both lines vertical
        if x1a != x2a: return False
        else:   # the lines are collinear
            return (collinear_point_in_edge((x1a,y1a),e2) 
                or collinear_point_in_edge((x1b,y1b),e2) 
                or collinear_point_in_edge((x2a,y2a),e1) 
                or collinear_point_in_edge((x2b,y2b),e1))
    if (dx2 == 0):  
    # e2 is vertical (so m2 = infty), but e1 isn't vertical
        x = x2a
        # compute y = m1 * x + b1, but minimize roundoff error
        y = (x2a-x1a)*dy1/float(dx1) + y1a
        return (collinear_point_in_edge((x,y),e1) 
            and collinear_point_in_edge((x,y),e2))
    elif (dx1 == 0):  
    # e1 is vertical (so m1 = infty), but e2 isn't vertical
        x = x1a
        # compute y = m2 * x + b2, but minimize roundoff error
        y = (x1a-x2a)*dy2/float(dx2) + y2a
        return (collinear_point_in_edge((x,y),e1) 
        and collinear_point_in_edge((x,y),e2))
    else:       # neither line is vertical
        # check m1 = m2, without roundoff error:
        if dy1*dx2 == dx1*dy2: 
        # same slope, so either parallel or collinear
            # check b1 != b2, without roundoff error:
            if dx2*dx1*(y2a-y1a) != dy2*dx1*x2a - dy1*dx2*x1a:  
            # the lines aren't collinear
                return False
            # the lines are collinear
            return (collinear_point_in_edge((x1a,y1a),e2) 
                or collinear_point_in_edge((x1b,y1b),e2)
                or collinear_point_in_edge((x2a,y2a),e1) 
                or collinear_point_in_edge((x2b,y2b),e1))
        # compute x = (b2-b1)/(m1-m2) but minimize roundoff error:
        x = ((dx2*dx1*(y2a-y1a) - dy2*dx1*x2a + 
            dy1*dx2*x1a)/float(dx2*dy1 - dy2*dx1))
        # compute y = m1*x + b1 but minimize roundoff error
        y = ((dy2*dy1*(x2a-x1a) - dx2*dy1*y2a + 
            dx1*dy2*y1a)/float(dy2*dx1 - dx2*dy1))
    return (collinear_point_in_edge((x,y),e1) 
        and collinear_point_in_edge((x,y),e2))

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
    Runs intersect for edge e and every segment in w
    '''
    for wall in w:
        if intersect(e, wall):
            return True
    return False

def pointOnLine(p, line):
    '''
    Helper method that returns true if point p is on line.
    Uses cross product and collinear_point_in_edge
    '''
    (x0,y0)=p
    ((x1,y1),(x2,y2))= line
    dx0 = x0 - x1
    dy0 = y0 - y1
    dx1 = x2 - x1
    dy1 = y2 - y1
    cross = dx0 * dy1 - dy0 * dx1
    if cross != 0:
        return False
    if collinear_point_in_edge(p,line):
        return True
    return False

def velocities(s, w):
    '''
    Returns list of possible choices of velocities
    that won't make you crash into a wall (yet)
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

#using modified graph search code
class Node():
    """
    Class for nodes in the search tree
    State is in ((x,y),(vx, vy))
    Parent is parent node
    I think g is cost to this node?
    """
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
    return justPoints(path)

def expand(curr, get_children, walls):
    """
    Return all children of curr
    velocities is the get_children function
    """
    ((x,y), (vx,vy)) = curr.state
    nextPoint = (x+vx, y+vy)

    for nextVel in get_children((nextPoint,curr.state[1]), walls):
        nextState = (nextPoint,nextVel)
        curr.children.append(Node(nextState,curr,curr.g+1))
    return curr.children

def printnodes(nodes):
    """For each node in nodes, print the state and g-value"""
    nodenames = ['{0} {1}'.format(y.state,y.g) for y in nodes]
    print ', '.join(nodenames)

def find_path(pnot, finish, w, h):
    '''
    pnot is the starting point
    finish is the finish line (an edge)
    w is the list of walls (edges)
    h is heuristic function h(s, finish, w) where s is any state s = (p, v)
    A* search! i think i'm going for that
    '''
    s0 = (pnot, (0,0))
    count = 0
    explored = {} #explored is a dict that maps states to cost
    frontier = [] 

    heapq.heappush(frontier, (0, Node(s0,False,0)))
    #use heapq module to maintain as priority queue
    #heapq.heappush(frontier, (priorityNumber, data))
    #heapq.heappop(frontier)

    while frontier:
        count+=1 #number of iterations
        while True:
            (hValue,next) = heapq.heappop(frontier) #keep popping nodes off q
            if(explored.has_key(next.state)):       
                if(explored.get(next.state) > next.g):
                    break   #use this node instead if it has better cost
            else:
                break       #break if the node is not in explored
        explored[next.state] = next.g
        # print 'explored: '+ str(explored)
        # print '  SIZE OF HEAP: ' + str(len(frontier))
        # print '   CHECKING A NEW NODE: ' + str(next.state)
        # print '     H-VALUE: ' + str(hValue)
        (point, velocity) = next.state
        if pointOnLine(point, finish) and velocity == (0,0):
            solution = getpath(next)
            #print '\t\t\tnumber of iterations: ' + str(count)
            return solution
        newNodes = expand(next,velocities, w)
        for n in newNodes:
            #f(x) = g(x) + h(x), A* search! using f(x) as priority q value
            fx = n.g + h(n.state, finish, w)
            heapq.heappush(frontier, (fx, n))
    print "Couldn't find a solution."
    return False

def justPoints(stateList):
    toReturn = []
    for (p,v) in stateList:
        toReturn.append(p)
    return toReturn

def distToFin(point, finish):
    '''
    euclidean distance from point to finish
    '''
    (x,y) = point
    ((x1,y1),(x2,y2)) = finish
    d1 = dist(point, (x1,y1))
    d2 = dist(point, (x2,y2))
    
    ## If the finish line's endpoints are equidistant,
    ## then return the distance to the center of the finish line.
    ## Otherwise, return the distance to the closer endpoint.
    if d1 == d2:
        (xm,ym) = ((x1+x2)/2.0, (y1+y2)/2.0)
        return dist(point, (xm,ym))
    else:
        return min(d1,d2)

def heur(s, finish, w):
    """
    A heuristic function to be used with find_path
    """
    """Euclidean distance from state to the finish line."""

    h = 0
    #If the goal state is met, then definitely check this one next
    if pointOnLine(s[0],finish) and s[1] == (0,0):
        return 0

    (x0,y0) = s[0]
    ((x1,y1),(x2,y2)) = finish

    (vx, vy) = s[1]
    euclid = distToFin(s[0],finish)
    vel = math.sqrt(vx**2+vy**2)
    #decel is the sum of dist + (dist - 1) + (dist - 2) + ...
    decel = vel*(vel-1)/2
    #if decel is greater than euclidean distance, then we need to slow down
    if(decel > euclid):
        h += decel - euclid 
        #increase h proportionate to how much
        #we need to slow down

    #check euclidean distance of next estimated location
    x = x0+vx 
    y = y0 + vy
    # if(crash(((x0,y0),(x+2*vx,y+2*vy)),w)):
    #     h+=vel
    d1 = math.sqrt((x1-x)**2 + (y1-y)**2)
    d2 = math.sqrt((x2-x)**2 + (y2-y)**2)
    ## If the finish line's endpoints are equidistant, then return the distance
    ## to the center of the finish line. Otherwise, return the distance to the
    ## closer endpoint.
    if d1 == d2:
        (xm,ym) = ((x1+x2)/2.0, (y1+y2)/2.0)
        hVal = math.sqrt((xm-x)**2 + (ym-y)**2)
    else:
        hVal = min(d1,d2)
    return h + hVal

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

def dist(p0,p1):
    '''
    distance function
    '''
    (x0,y0) = p0
    (x1,y1) = p1
    return math.sqrt((x0-x1)**2 + (y0-y1)**2)