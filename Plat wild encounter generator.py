import math
import string

#####################################################
seed = 0x5a06169f

start = 300
end = 1550

mrate=35
encrate=30
#####################################################
def rngAdvance(prev):
	next=(1103515245*prev)+24691
	return next%0x100000000

def rngOf(seed,frame):
	prev=seed
	for x in range(0,frame):
		prev=rngAdvance(prev)
	return prev

def getIVs(rng):
	ivs=[]
	#rng=rngAdvance(rng)
	#rng=rngAdvance(rng)
	iv1=rng>>16
	rng=rngAdvance(rng)
	iv2=rng>>16
	ivs.append(iv1%0b100000)
	iv1=iv1//0b100000
	ivs.append(iv1%0b100000)
	iv1=iv1//0b100000
	ivs.append(iv1%0b100000)
	ivs.append(iv2%0b100000)
	iv2=iv2//0b100000
	ivs.insert(3,iv2%0b100000)
	iv2=iv2//0b100000
	ivs.insert(4,iv2%0b100000)
	return ivs

def getPID(rng):
	rng1=rng>>16
	rng2=rngAdvance(rng)>>16
	pid=rng1+rng2*0x10000
	return pid

def getNature(pid):
	selector=pid%25
	return selector

natures=['Hardy','Lonely','Brave','Adamant','Naughty','Bold','Docile','Relaxed','Impish','Lax','Timid','Hasty','Serious','Jolly','Naive','Modest','Mild','Quiet','Bashful','Rash','Calm','Gentle','Sassy','Careful','Quirky']

def natureSTR(selector):
	natures=['Hardy','Lonely','Brave','Adamant','Naughty','Bold','Docile','Relaxed','Impish','Lax','Timid','Hasty','Serious','Jolly','Naive','Modest','Mild','Quiet','Bashful','Rash','Calm','Gentle','Sassy','Careful','Quirky']
	return natures[selector]




#this is for land only
def checkItem(seed,frame):
	frame = frame+2
	rng=rngOf(seed,frame)
	rnd = rng>>16
	nat = rnd//0xa3e
	PIDFound = False
	while PIDFound == False:
		rng=rngAdvance(rng)
		frame+=1
		lowerPID = rng>>16
		rng=rngAdvance(rng)
		frame+=1
		upperPID=rng>>16
		PID=upperPID*0x10000+lowerPID
		if PID%25 == nat:
			PIDFound = True
	item_deter = rngOf(seed,frame+3)>>16
	item_deter = item_deter%100
	if item_deter < 45:
	    item = "No Item"
	elif item_deter >=45 and item_deter < 95:
		item = "Common Item"
	elif item_deter>=95:
		item = "Rare Item"
	ivs=getIVs(rngOf(seed,frame-1))
	return [item,frame+4,nat,ivs]


def checkEncounter(seed,frame):
    f1 = rngOf(seed,frame-1)
    f2 = rngOf(seed,frame-0)
    rnd1 = f1>>16
    rnd2 = f2>>16
    if rnd1/0x290 <= mrate and rnd2/0x290 <=encrate:
        return True
    else:
        return False

def getLandSlot(seed,frame):
    parts=[20, 40, 50, 60, 70, 80, 85, 90, 94, 98, 99, 100]
    rng = rngOf(seed,frame+1)>>16
    sel = rng//656
    for x in range(0,12):
        if sel<parts[x]:
            return x

def checkLE(seed):
    target = [9,11]
    metroLST = []
    found = False
    for x in range(start,end):
        if getLandSlot(seed,x) not in target:
            continue
        else:
            res=checkItem(seed,x)
            if res[0] == "Rare Item":
                found = True
                metroLST.append([x,res[1],natures[res[2]],res[3]])
    return [found,metroLST]







table = ["Roselia L19", "Bibarel L18", "Staravia L19", "Ralts L17", "Staravia L18", "Bibarel L19","Ralts L18","Roselia L20","Ralts L19", "Chansey L17","Ralts L19","Chansey L19"]
table2 = ["Starly","Shinx","Starly","Bidoof","Bidoof","Abra","Abra","Shinx","Starly L2","Bidoof L2","Starly L2","Bidoof L2"]
table3 = ["Shinx L3","Bidoof L3","Starly L4","Kricketot L3","Shinx L4","Bidoof L3","Starly L4","Bidoof L4","Starly L2","Bidoof L2","Starly L2","Bidoof L2"]
table4 = ["Budew L18","Bidoof L18","Budew L19","Ralts L17","Roselia L19","Bibarel L18","Ralts L18", "Bibarel L19","Roselia L20","Bibarel L20","Roselia L20","Bibarel L20"]
table5 = ["Starly L4","Shinx L4","Kricketot L5","Zubat L4","Bidoof L5","Abra L4","Abra L5","Shinx L5","Starly L6","Bidoof L6","Starly L7","Bidoof L7"]
def checkEnc(seed,frame):
    init = frame
    f1 = rngOf(seed,frame+1)
    f2 = rngOf(seed,frame+2)
    rnd1 = f1>>16
    rnd2 = f2>>16
    if rnd1//0x290 >= mrate or rnd2//0x290 >= encrate:
        return 0
    frame = frame+2
    poke=getLandSlot(seed,frame)
    frame = frame+2
    rng=rngOf(seed,frame)
    rnd = rng>>16
    nat = rnd//0xa3e
    PIDFound = False
    while PIDFound == False:
        rng=rngAdvance(rng)
        frame+=1
        lowerPID = rng>>16
        rng=rngAdvance(rng)
        frame+=1
        upperPID=rng>>16
        PID=upperPID*0x10000+lowerPID
        if PID%25 == nat:
           PIDFound = True
    ivs=getIVs(rngOf(seed,frame-1))
    if poke == 9 or poke == 11:
        gender = "Female"
    else:
        gender_deter = PID%0x100
        if gender_deter<=126:
            gender ="Female"
        else:
            gender="Male"
    #if table2[poke] == "Abra":
    return [poke,(str(init)+"\t"+str(poke)+"\t"+gender+"\t"+str(frame+4)+"\t"+natures[nat]+"\t"+str(ivs))+"\t"+str(rnd1//0x290)+"\t"+str(rnd2//0x290)]

def checkEncIntimidate(seed,frame):
    init = frame
    f1 = rngOf(seed,frame+1)
    f2 = rngOf(seed,frame+2)
    rnd1 = f1>>16
    rnd2 = f2>>16
    if rnd1//0x290 >=70 or rnd2//0x290 >= 30:
        return 0
    frame = frame+2
    poke=getLandSlot(seed,frame)
    frame = frame+2
    intim_deter = rngOf(seed,frame)>>16>>15
    if intim_deter==1:
       frame+=1
       rng=rngOf(seed,frame)
       rnd = rng>>16
       nat = rnd//0xa3e
       PIDFound = False
       while PIDFound == False:
	       rng=rngAdvance(rng)
	       frame+=1
	       lowerPID = rng>>16
	       rng=rngAdvance(rng)
	       frame+=1
	       upperPID=rng>>16
	       PID=upperPID*0x10000+lowerPID
	       if PID%25 == nat:
	           PIDFound = True
       ivs=getIVs(rngOf(seed,frame-1))
       if poke == 9 or poke == 11:
        gender = "Female"
       else:
        gender_deter = PID%0x100
        if gender_deter<=126:
            gender ="Female"
        else:
            gender="Male"
       print (str(init)+"\t"+table[poke]+"\t"+gender+"\t"+str(frame+4)+"\t"+natures[nat]+"\t"+str(ivs))
    else:
    	print(str(init)+"\t"+"blocked")
#4533
#print(rngOf(seed,4536)>>16)

for x in range(1070,1100):
    checkEnc(seed,x)

def findEnc(seed, frame):
    init = frame
    f1 = rngOf(seed,frame+1)
    f2 = rngOf(seed,frame+2)
    rnd1 = f1>>16
    rnd2 = f2>>16
    if rnd1//0x290 >=40 or rnd2//0x290 >= 30:
        return False
    else:
         return True



def checkEncwitem(seed,frame):
    init = frame
    rng = rngOf(seed,init)
    rng = rngAdvance(rng)
    frame+=1
    movementCheck = rng >> 16
    rng = rngAdvance(rng)
    frame+=1
    encounterCheck = rng >> 16
    if movementCheck//0x290 >=mrate or encounterCheck//0x290 >= encrate:
        return [False]
    rng = rngAdvance(rng)
    frame+=1
    poke=getLandSlot2(rng)
    rng = rngAdvance(rng)
    frame+=1
    rnd = rng>>16
    nat = rnd//0xa3e
    PIDFound = False
    while PIDFound == False:
        rng=rngAdvance(rng)
        frame+=1
        lowerPID = rng>>16
        rng=rngAdvance(rng)
        frame+=1
        upperPID=rng>>16
        PID=upperPID*0x10000+lowerPID
        if PID%25 == nat:
           PIDFound = True
           break
    rng = rngAdvance(rng)
    ivs=getIVs(rng)
    rng = rngAdvance(rng)
    rng = rngAdvance(rng)
    item_deter = rng>>16
    item_deter = item_deter%100
    parts = [45,95,100]
    for x in range(0,3):
        if item_deter<parts[x]:
            item = x
            break
    items = ["No Item","Common Item","Rare Item"]
    if poke == 9 or poke == 11:
        gender = "Female"
    else:
        gender_deter = PID%0x100
        if gender_deter<=126:
            gender ="Female"
        else:
            gender="Male"
    return [True,init,str(poke),gender,frame+4,natures[nat],ivs,items[item],frame+4-init]

def getLandSlot2(rng):
    parts=[20, 40, 50, 60, 70, 80, 85, 90, 94, 98, 99, 100]
    rng = rng >> 16
    sel = rng//656
    for x in range(0,12):
        if sel<parts[x]:
            return x


for x in range(start,end):
     res = checkEncwitem(seed,x)
     if res[0] == True:
          print(res)


