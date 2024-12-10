dataFile = open("day7.txt", "r")
operData = [list(map(int, x.replace(":","").strip().split())) for x in dataFile.readlines()]
dataFile.close()

def isValid(n:int,l:list):
    if(len(l)==1) : 
        return l[0]==n
    if isValid(n,[l[0]+l[1]]+l[2:]): return True
    if isValid(n,[l[0]*l[1]]+l[2:]): return True
    if isValid(n,[int(str(l[0])+str(l[1]))]+l[2:]): return True
    return False


count = 0
for row in operData:
    if (isValid(row[0], row[1:])): count+=row[0]
print(count)
