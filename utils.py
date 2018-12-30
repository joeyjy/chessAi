from __future__ import division

def toStr(x, y):
    return str(x) + str(y)

def mean(l):
    if len(l) > 0:
        return sum(l) / len(l)
    else:
        return 0

def vs(x, y):
    if x == None or y == None:
        return False
    if x['type'] == 7 and y['type'] == 1:
        return False
    if x['type'] < y['type']:
        return False
    return True
