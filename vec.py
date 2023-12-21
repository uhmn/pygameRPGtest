import math

def div(lis, num):
    return (lis[0]/num,lis[1]/num)
    
def mult(lis, num):
    return (lis[0]*num,lis[1]*num)
    
def add(lis, num):
    return (lis[0]+num,lis[1]+num)
    
def sub(lis, num):
    return (lis[0]-num,lis[1]-num)

def abs2(lis):
    return (abs(lis[0]), abs(lis[1]))

def largest(lis):
    t1 = abs(lis[0])
    t2 = abs(lis[1])
    if t1>t2: return t1
    else: return t2

def round2(lis):
    return (round(lis[0]),round(lis[1]))


def collision(pos1, size1, pos2):
    br = add(pos1, size1)
    tl = sub(pos1, size1)
    if greater_2(pos2, tl):
        if lesser_2(pos2, br):
            return True
    return False

def div_2(t1, t2):
    return (t1[0]/t2[0],t1[1]/t2[1])
    
def mult_2(t1, t2):
    return (t1[0]*t2[0],t1[1]*t2[1])
    
def add_2(t1, t2):
    return (t1[0]+t2[0],t1[1]+t2[1])
    
def sub_2(t1, t2):
    return (t1[0]-t2[0],t1[1]-t2[1])

def greater_2(t1, t2):
    return (t1[0]>t2[0] and t1[1]>t2[1])
    
def lesser_2(t1, t2):
    return (t1[0]<t2[0] and t1[1]<t2[1])

def distance(t1, t2):
    return math.sqrt(((t1[0]-t2[0])*(t1[0]-t2[0]))+((t1[1]-t2[1])*(t1[1]-t2[1])))