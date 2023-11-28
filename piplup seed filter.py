import math
import string

#Path to list of seeds
path = "\\Users\\march\\Downloads\\lonely chim r2.txt"  #Put the path to your list of seeds in the quote

mode = 1 #1 for single poke search, 2 for double

mrate = 50
encrate = 30

#stats requirement
hp = 24
atk = 30
defense = 28
spatk = 28
spdef = 13
spe = 28
ifHP = False
HPower = [3,4]
HPPower = 60

#stats requirement for secondary poke
hp2 = 0
atk2 = 0
defense2 = 0
spatk2 = 27
spdef2 = 0
spe2 = 23
ifHP2 = False
HPower2 = [3]
HPPower2 = 65

#types=["Fighting","Flying","Poison","Ground","Rock","Bug","Ghost","Steel","Fire","Water","Grass","Electric","Psychic","Ice","Dragon","Dark"]

#nature of starter
nat = ["Lonely"]
nat2 = ["Mild","Modest","Rash"]

#frame range of starter
low = 70
high = 200

#frame range of secondary poke
low2 = 2900
high2 = 4200

#pokerus?
pkrs = True #put True or False

#frame range of pkrs
pkrslow = 0
pkrshigh = 2400

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

def getPID(rng):
	rng1=rng>>16
	rng2=rngAdvance(rng)>>16
	pid=rng1+rng2*0x10000
	return pid

def getNature(pid):
	selector=pid%25
	return selector

def natureSTR(selector):
	natures=['Hardy','Lonely','Brave','Adamant','Naughty','Bold','Docile','Relaxed','Impish','Lax','Timid','Hasty','Serious','Jolly','Naive','Modest','Mild','Quiet','Bashful','Rash','Calm','Gentle','Sassy','Careful','Quirky']
	return natures[selector]

natures=['Hardy','Lonely','Brave','Adamant','Naughty','Bold','Docile','Relaxed','Impish','Lax','Timid','Hasty','Serious','Jolly','Naive','Modest','Mild','Quiet','Bashful','Rash','Calm','Gentle','Sassy','Careful','Quirky']

def seedSearch(seed,frameL,FrameH,natures,ifHP,HPower,HPPower,hp,atk,defense,spatk,spdef,spe):
	rng=rngOf(seed, frameL)
	found = False
	pokelst=[]
	for x in range(frameL,FrameH):
		rng=rngAdvance(rng)
		pid=getPID(rng)
		nature=getNature(pid)
		gender_deter = pid%0x100
		if gender_deter<=30:
		    gender = "Female"
		else:
		    gender = "Male"
		ivs=getIVs(rng)
		if natureSTR(nature) not in natures:
			continue
		if ivs[0]>=hp and ivs[1]>=atk and ivs[2]>=defense and ivs[3]>=spatk and ivs[4] >= spdef and ivs[5]>=spe:
			if ifHP == True:
				HP=getHP(ivs[0], ivs[1], ivs[2], ivs[3], ivs[4], ivs[5])
				if HP[0] in HPower and HP[1]>=HPPower:
					found = True
					poke = "{}: {} {} HP: {} {} {}".format(x, natureSTR(nature),ivs,types[HP[0]],HP[1],gender)
					pokelst.append(poke)
			else:
			 	if gender == "Female" or gender == "Male":
			 	   HP=getHP(ivs[0], ivs[1], ivs[2], ivs[3], ivs[4], ivs[5])
			 	   found = True
			 	   poke = "{}: {} {} HP: {} {} {}".format(x, natureSTR(nature),ivs,types[HP[0]],HP[1],gender)
			 	   pokelst.append(poke)
		else:
			continue
	return [found,pokelst]

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
    ivs=getWildIVs(rng)
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
    return [True,init,poke,gender,frame+4,natures[nat],ivs,items[item]]

def getWildIVs(rng):
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

def getLandSlot2(rng):
    parts=[20, 40, 50, 60, 70, 80, 85, 90, 94, 98, 99, 100]
    rng = rng >> 16
    sel = rng//656
    for x in range(0,12):
        if sel<parts[x]:
            return x

def getMetronomes(seed, low, high):
	hour = math.floor(seed/0x10000)
	hour = hour%0x100
	metronomes = []
	for x in range(low,high):
		res = checkEncwitem(seed,x)
		if hour in [2,3,19,20,21,22,23]:
		    if res[0] == True and res[2] == 2 and res[7] == "Rare Item":
			    metronomes.append(["Night",res])
		if hour in [3,4,5,6,7,8,9]:
			if res[0] == True and res[2] == 3 and res[7] == "Rare Item":
			    metronomes.append(["Morning",res])
	return metronomes

types=["Fighting","Flying","Poison","Ground","Rock","Bug","Ghost","Steel","Fire","Water","Grass","Electric","Psychic","Ice","Dragon","Dark"]

def getHP(hp,atk,defend,spatk,spdef,spe):
	a=hp%2
	b=atk%2
	c=defend%2
	d=spe%2
	e=spatk%2
	f=spdef%2
	type=math.floor(((a+2*b+4*c+8*d+16*e+32*f)*5)/21)
	if hp%4 == 2 or hp%4 ==3:
		u=1
	else:
		u=0
	if atk%4 == 2 or atk%4 ==3:
		v=1
	else:
		v=0
	if defend%4 == 2 or defend%4 ==3:
		w=1
	else:
		w=0
	if spe%4 == 2 or spe%4 ==3:
		x=1
	else:
		x=0
	if spatk%4 == 2 or spatk%4 ==3:
		y=1
	else:
		y=0
	if spdef%4 == 2 or spdef%4 ==3:
		z=1
	else:
		z=0
	power=int(((u+2*v+4*w+8*x+16*y+32*z)*40)/63)+30
	return [type, power]


def checkPokerus(seed, low, high):
	rng = rngOf(seed,low-1)
	for x in range(low,high+1):
		rng = rngAdvance(rng)
		rnd=rng>>16
		if rnd==0x4000 or rnd==0x8000 or rnd==0xc000:
			return x
	return 999999999999







seedLst = open(path, "r+")
for line in seedLst:
	seed = int(line.split("\t")[0],16)
	delay = seed%0x10000
	hour = math.floor(seed/0x10000)
	hour = hour%0x100
	if pkrs == True:
		if checkPokerus(seed, pkrslow,pkrshigh) <pkrshigh:
			pkrsFrame = checkPokerus(seed, pkrslow, pkrshigh)
			searchresult = seedSearch(seed,low,high,nat,ifHP,HPower,HPPower,hp,atk,defense,spatk,spdef,spe)
			if mode == 2:
				searchresult2 = seedSearch(seed,low2,high2,nat2,ifHP2,HPower2,HPPower2,hp2,atk2,defense2,spatk2,spdef2,spe2)
			if mode == 1:
				if searchresult[0] == True:
					metronomes = getMetronomes(seed,300,1000)
					if len(metronomes) == 0:
						continue
					print("Seed:", hex(seed))
					#print("Advance:",advance)
					print("Hour:",hour)
					print("Delay:",delay)
					print("Pokerus:",pkrsFrame)
					print("Chimchar:")
					for a in searchresult[1]:
						print(a)
					print("Metronomes:")
					for b in metronomes:
						print(b)
					print("")


