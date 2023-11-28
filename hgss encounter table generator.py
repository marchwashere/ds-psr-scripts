import math
import string


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
	rng=rngAdvance(rng)
	rng=rngAdvance(rng)
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



natures=['Hardy','Lonely','Brave','Adamant','Naughty','Bold','Docile','Relaxed','Impish','Lax','Timid','Hasty','Serious','Jolly','Naive','Modest','Mild','Quiet','Bashful','Rash','Calm','Gentle','Sassy','Careful','Quirky']

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
    if rnd1/0x290 <= mrate and rnd2/0x290 <=30:
        return True
    else:
        return False

def getLandSlot(seed,frame):
    parts=[20, 40, 50, 60, 70, 80, 85, 90, 94, 98, 99, 100]
    rng = rngOf(seed,frame+1)>>16
    sel = rng%100
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






seed = 0xDA0C0BEC


table = ["Rattata\t14", "Koffing\t14", "Rattata\t14", "Koffing\t14", "Koffing\t16", "Koffing\t16","Magmar\t16","Magmar\t16","Zubat\t15", "Rattata\t14","Zubat\t15","Rattata\t14"]

def checkEnc(seed,frame):
    init = frame
    f1 = rngOf(seed,frame+1)
    f2 = rngOf(seed,frame+2)
    rnd1 = f1>>16
    rnd2 = f2>>16
    rnd11 = rnd1%100
    rnd21=rnd2%100
    if rnd1%100 >=20 or rnd2%100 >= 30:
        return 0
    frame = frame+2
    poke=getLandSlot(seed,frame)
    frame = frame+2
    rng=rngOf(seed,frame)
    rnd = rng>>16
    nat = rnd%25
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
    if poke == 6 or poke == 7:
        gender_deter = PID%0x100
        if gender_deter <=63:
            gender = "F"
        else:
            gender = "M"
    else:
        gender_deter = PID%0x100
        if gender_deter<=126:
            gender ="F"
        else:
            gender="M"
    print (str(init)+"\t"+table[poke]+"\t"+gender+"\t"+str(rnd1%100)+"\t"+str(frame+4)+"\t"+natures[nat]+"\t"+str(ivs))


def findEnc(seed,frame,slots):
    init = frame
    f1 = rngOf(seed,frame+1)
    f2 = rngAdvance(f1)
    rnd1 = f1>>16
    rnd2 = f2>>16
    if rnd1%100 >=100 or rnd2%100 >= 25:
        return 0
    frame = frame+2
    poke=getLandSlot(seed,frame)
    if poke not in slots:
        return 0
    frame = frame+2
    rng=rngOf(seed,frame)
    rnd = rng>>16
    nat = rnd%25
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
        gender_deter = PID%0x100
        if gender_deter <=63:
            gender = "F"
        else:
            gender = "M"
    else:
        gender_deter = PID%0x100
        if gender_deter<=126:
            gender ="Female"
        else:
            gender="Male"
    print (str(init)+"\t"+str(poke)+"\t"+gender+"\t"+str(frame+4)+"\t"+natures[nat]+"\t"+str(ivs)+"\t"+str(rnd1%100))

#print(rngOf(seed,4536)>>16)
seed= 0x59110d6b
for x in range(70,4000):
    checkEnc(seed,x)

    #1 3 6 7 hg l2/3 sentret
    #1 3 6

