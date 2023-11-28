#####################################################

#range of frames to check for lucky egg
start = 4040
end = 4446

#seed you are checking
seed = 0x82031489

#movement rate you are checking cues
mrate = 60

#movement rate when you are advancing
advanceMRate = 60
#30 for grass, 10 for water and cave
encounterRate = 30

immunity = 5
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
     
def checkItem(rng):
    rng = rngAdvance(rng)
    rng = rngAdvance(rng)
    rnd = rng>>16
    nat = rnd//0xa3e
    PIDFound = False
    while PIDFound == False:
        rng=rngAdvance(rng)

        lowerPID = rng>>16
        rng=rngAdvance(rng)

        upperPID=rng>>16
        PID=upperPID*0x10000+lowerPID
        if PID%25 == nat:
           PIDFound = True

    rng = rngAdvance(rng)
    rng = rngAdvance(rng)
    rng = rngAdvance(rng)
    item_deter = rng>>16
    item_deter = item_deter%100
    parts = [45,95,100]
    for x in range(0,3):
        if item_deter<parts[x]:
            item = x
            break
    return item
    
def getLandSlot(rng):
    parts=[20, 40, 50, 60, 70, 80, 85, 90, 94, 98, 99, 100]
    rng = rng >> 16
    sel = rng//656
    for x in range(0,12):
        if sel<parts[x]:
            return x

def getLE(seed,start,end):
    target = [9,11]
    lst = []
    found = False
    rng = rngOf(seed,start)
    for x in range(start,end):
        slot = getLandSlot(rngAdvance(rng))
        if slot not in target:
            rng = rngAdvance(rng)
            continue
        else:
            res=checkItem(rng)
            rng = rngAdvance(rng)
            if res == 2:
                lst.append(x)
    return lst


table = ["Roselia L19", "Bibarel L18", "Staravia L19", "Ralts L17", "Staravia L18", "Bibarel L19","Ralts L18","Roselia L20","Ralts L19", "Chansey L17","Ralts L19","Chansey L19"]

def checkEnc(seed,frame):
    init = frame
    rng = rngOf(seed,init)
    rng = rngAdvance(rng)
    frame+=1
    movementCheck = rng >> 16
    rng = rngAdvance(rng)
    frame+=1
    encounterCheck = rng >> 16
    if movementCheck//0x290 >=mrate or encounterCheck//0x290 >= 30:
        return [False]
    rng = rngAdvance(rng)
    frame+=1
    poke=getLandSlot(rng)
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
    rng = rngAdvance(rng)
    ivs=getIVs(rng)
    rng = rngAdvance(rng)
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
    return [True,init,table[poke],gender,frame+4,natures[nat],ivs,items[item]]


targets = getLE(seed,start,end+1)
print(targets)
for x in range(start,end-1):
     res = checkEnc(seed,x)
     if res[0]:
        init = res[1]
        poke = res[2]
        gender = res[3]
        occid = res[4]
        target = False
        for x in range(0,len(targets)):
            if occid < targets[x]:
                target = targets[x]
                break
        if target == False:
             print("{}\t{}\t{}\t{}\tRIP".format(init,poke,gender,occid))
        else:
            frame = occid
            sinceLast = 0
            steps = 0
            rng = rngOf(seed,frame)
            while frame < target:
                steps+=1
                if sinceLast < 5:
                    rng = rngAdvance(rng)
                    frame+=1
                    immunityCheck = rng >> 16
                    sinceLast+=1
                    if immunityCheck//0x290 >= immunity:
                        continue
                if sinceLast >=5:
                     sinceLast += 1
                rng = rngAdvance(rng)
                frame += 1
                movementCheck = rng >> 16
                if movementCheck//0x290 < advanceMRate:
                    rng = rngAdvance(rng)
                    frame += 1
                    encounterCheck = rng >> 16
                    if encounterCheck//0x290 < encounterRate:
                        rng = rngAdvance(rng)
                        frame += 1
                        sinceLast = 0
                        continue
                    else:
                        continue
                else:
                    continue
            if frame == target:
                 print("{}\t{}\t{}\t{}\t{: <3d} Steps\t Target: {}".format(init,poke,gender,occid,steps,target))
            else:
                 print("{}\t{}\t{}\t{}\tSkipped\t".format(init,poke,gender,occid))

