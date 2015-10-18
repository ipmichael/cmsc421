import proj1_IP,test_probs
import time



def test(maze,h):
	(p0, finish, walls) = maze
	return proj1_IP.find_path(p0, finish, walls, h)

t = int(round(time.time() * 1000))



print "h_edist"
print "rect1",len(test(test_probs.rect1,proj1_IP.h_edist)),
t1=int(round(time.time() * 1000))
print (t1-t)/1000.0

print "rect2",len(test(test_probs.rect2,proj1_IP.h_edist)),
t2=int(round(time.time() * 1000))
print (t2-t1)/1000.0

print "wall1",len(test(test_probs.wall1,proj1_IP.h_edist)),
t3=int(round(time.time() * 1000))
print (t3-t2)/1000.0

print "wall2",len(test(test_probs.wall2,proj1_IP.h_edist)),
t4=int(round(time.time() * 1000))
print (t4-t3)/1000.0

print "zigzagwall",len(test(test_probs.zigzagwall,proj1_IP.h_edist)),
t5=int(round(time.time() * 1000))
print (t5-t4)/1000.0

print "hookwall",len(test(test_probs.hookwall,proj1_IP.h_edist)),
t6=int(round(time.time() * 1000))
print (t6-t5)/1000.0

print "rectwall",len(test(test_probs.rectwall,proj1_IP.h_edist)),
t7=int(round(time.time() * 1000))
print (t7-t6)/1000.0

print "pdes1",len(test(test_probs.pdes1,proj1_IP.h_edist)),
t8=int(round(time.time() * 1000))
print (t8-t7)/1000.0

print "pdes2",len(test(test_probs.pdes2,proj1_IP.h_edist)),
t9=int(round(time.time() * 1000))
print (t9-t8)/1000.0

print "pdes3",len(test(test_probs.pdes3,proj1_IP.h_edist)),
t10=int(round(time.time() * 1000))
print (t10-t9)/1000.0

print "spiral1",len(test(test_probs.spiral1,proj1_IP.h_edist)),
t11=int(round(time.time() * 1000))
print (t11-t10)/1000.0

print "small_l",len(test(test_probs.small_l,proj1_IP.h_edist)),
t13=int(round(time.time() * 1000))
print (t13-t11)/1000.0

print "med_l",len(test(test_probs.med_l,proj1_IP.h_edist)),
t14=int(round(time.time() * 1000))
print (t14-t13)/1000.0

print "big_l",len(test(test_probs.big_l,proj1_IP.h_edist)),
t15=int(round(time.time() * 1000))
print (t15-t14)/1000.0

print "spiral2",len(test(test_probs.spiral2,proj1_IP.h_edist)),
t16=int(round(time.time() * 1000))
print (t16-t15)/1000.0

print "huge_l",len(test(test_probs.huge_l,proj1_IP.h_edist)),
t17=int(round(time.time() * 1000))
print (t17-t16)/1000.0


print
print
print "heur"
t = int(round(time.time() * 1000))



print "rect1",len(test(test_probs.rect1,proj1_IP.heur)),
t1=int(round(time.time() * 1000))
print (t1-t)/1000.0

print "rect2",len(test(test_probs.rect2,proj1_IP.heur)),
t2=int(round(time.time() * 1000))
print (t2-t1)/1000.0

print "wall1",len(test(test_probs.wall1,proj1_IP.heur)),
t3=int(round(time.time() * 1000))
print (t3-t2)/1000.0

print "wall2",len(test(test_probs.wall2,proj1_IP.heur)),
t4=int(round(time.time() * 1000))
print (t4-t3)/1000.0

print "zigzagwall",len(test(test_probs.zigzagwall,proj1_IP.heur)),
t5=int(round(time.time() * 1000))
print (t5-t4)/1000.0

print "hookwall",len(test(test_probs.hookwall,proj1_IP.heur)),
t6=int(round(time.time() * 1000))
print (t6-t5)/1000.0

print "rectwall",len(test(test_probs.rectwall,proj1_IP.heur)),
t7=int(round(time.time() * 1000))
print (t7-t6)/1000.0

print "pdes1",len(test(test_probs.pdes1,proj1_IP.heur)),
t8=int(round(time.time() * 1000))
print (t8-t7)/1000.0

print "pdes2",len(test(test_probs.pdes2,proj1_IP.heur)),
t9=int(round(time.time() * 1000))
print (t9-t8)/1000.0

print "pdes3",len(test(test_probs.pdes3,proj1_IP.heur)),
t10=int(round(time.time() * 1000))
print (t10-t9)/1000.0

print "spiral1",len(test(test_probs.spiral1,proj1_IP.heur)),
t11=int(round(time.time() * 1000))
print (t11-t10)/1000.0

print "small_l",len(test(test_probs.small_l,proj1_IP.heur)),
t13=int(round(time.time() * 1000))
print (t13-t11)/1000.0

print "med_l",len(test(test_probs.med_l,proj1_IP.heur)),
t14=int(round(time.time() * 1000))
print (t14-t13)/1000.0

print "big_l",len(test(test_probs.big_l,proj1_IP.heur)),
t15=int(round(time.time() * 1000))
print (t15-t14)/1000.0

print "spiral2",len(test(test_probs.spiral2,proj1_IP.heur)),
t12=int(round(time.time() * 1000))
print (t12-t15)/1000.0

print "huge_l",len(test(test_probs.huge_l,proj1_IP.heur)),
t16=int(round(time.time() * 1000))
print (t16-t12)/1000.0