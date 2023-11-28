import json
import pathlib
dir = str(pathlib.Path(__file__).parent.resolve())
path = dir+r"\moveData.json"
metronome = 1
dslap = 2
mimic = 3
fwcrit = 4

#display fights with what move (or you crit fw t1)
mode = metronome

#real time (DS Clock)
minute = 56
second = 27

#center of the cluster
center = 0x533f

banned = ["ENCORE","COUNTER", "MIMIC", "METRONOME", "MIRROR MOVE", "STRUGGLE", "SKETCH","THIEF","PROTECT","DESTINY BOND","DETECT","ENDURE","SLEEP TALK","MIRROR COAT","FOCUS PUNCH","FOLLOW ME","HELPING HAND","TRICK","ASSIST","SNATCH","COVET","FEINT","ME FIRST","COPY CAT","SWITCHEROO","CHATTER", "DOUBLE SLAP","MIMIC"]

def rngAdvance(prev):
    next=(1103515245*prev)+24691
    return next%0x100000000

def rngOf(seed,frame):
    prev=seed
    for x in range(0,frame):
        prev=rngAdvance(prev)
    return prev

def advanceBy(seed,x):
    for x in range(0,x):
        seed = rngAdvance(seed)
    return seed

moveData = open(path, "r+", encoding="UTF-8")
moveLst = moveData.read()
moveLst = moveLst.split("},")


for x in range(0,len(moveLst)):
    moveLst[x] = moveLst[x].split("\n")
    moveLst[x].pop(0)
    moveLst[x].pop(0)
    moveLst[x].pop()
    for y in range(0,len(moveLst[x])):
        moveLst[x][y] = moveLst[x][y].split(":")[1]
        moveLst[x][y] = moveLst[x][y].strip(",")
        moveLst[x][y] = moveLst[x][y].strip()
        moveLst[x][y] = moveLst[x][y].strip("\"")
    moveLst[x][0] = moveLst[x][0].split("MOVE_")[1]
    moveLst[x][0] = moveLst[x][0].replace("_", " ")

def unkBLookup(name):
    for x in moveLst:
        if x[0] == name:
            print("{0:016b}".format(int(x[10])))

def getMetronome(rng):
    moveSel= rng >> 16
    maximum = len(moveLst)
    maximum = maximum - 1
    move = moveSel%maximum
    move += 1
    return move

rolls = [33, 33, 33, 33, 34, 34, 34, 34, 36, 36, 36, 36, 37, 37, 37, 39]
FWrolls = [25, 27, 27, 27, 27, 27, 28, 28, 28, 28, 28, 30, 30, 30, 30, 31]
stomprolls = [16, 16, 16, 16, 16, 16, 16, 16, 18, 18, 18, 18, 18, 18, 18, 19]
stompcrit = [33, 33, 33, 33, 34, 34, 34, 34, 36, 36, 36, 36, 37, 37, 37, 39]



upper = (1*1 + minute+second)*0x1000000 + 0xc0000

miltank = ["Attract","Stomp"]

for x in range(center-130,center+131):
    seed = upper+x
    rng = rngOf(seed,11)
    move = (rng >> 16)%3
    identifier = [0,0,0,[]]
    rng = advanceBy(rng,5)
    fwCrit = (rng >> 16)%16
    if fwCrit == 0:
        identifier[0] = 1
        if mode != fwcrit:
            continue
        else:
            #frame29
            rng = advanceBy(rng,13)
            t1 = (rng>>16)%2
            if t1 == 0:
                #f50
                rng = advanceBy(rng,21)
                #f55
                rng = advanceBy(rng,5)
                move = (rng>>16)%2
                if move == 0:
                    rng = advanceBy(rng, 3)
                    crit = (rng>>16)%16
                    rng = rngAdvance(rng)
                    if crit != 0:
                        t2 = "Fully {}".format(56-stomprolls[15-((rng>>16)%16)])
                    else:
                        t2 = "Fully {}".format(56-stompcrit[15-((rng>>16)%16)])
                    print(hex(seed),"\t","Attract","\t",t2)
                else:
                    rng = advanceBy(rng, 6)
                    crit = (rng>>16)%16
                    rng = rngAdvance(rng)
                    if crit != 0:
                        t2 = "Through {}".format(56-stomprolls[15-((rng>>16)%16)])
                    else:
                        t2 = "Through {}".format(56-stompcrit[15-((rng>>16)%16)])
                    print(hex(seed),"\t","Attract","\t",t2)
            else:
                #f39
                rng = advanceBy(rng, 10)
                crit = (rng>>16)%16
                #f40
                rng = rngAdvance(rng)
                if crit != 0:
                    dmg = 56-stomprolls[15-((rng>>16)%16)]
                else:
                    dmg = 56-stompcrit[15-((rng>>16)%16)]
                rng = advanceBy(rng,13)
                t2 = (rng>>16)%2
                if t2 == 0:
                    t2 = miltank[t2]
                else:
                    rng = advanceBy(rng, 10)
                    crit = (rng>>16)%16
                    rng = rngAdvance(rng)
                    if crit != 0:
                        t2 = "Stomp {}".format(dmg-stomprolls[15-((rng>>16)%16)])
                    else:
                        t2 = "Stomp {}".format(dmg-stompcrit[15-((rng>>16)%16)])
                print(hex(seed),"\t","Stomp",dmg,"\t",t2)
    rng = rngAdvance(rng)
    dmg = FWrolls[15-((rng>>16)%16)]
    rng = advanceBy(rng,2)
    burn = (rng>>16)%100
    if burn < 10:
        identifier[1] = 1
    rng = rngAdvance(rng)
    cutecharm = (rng>>16)%10
    if cutecharm < 3:
        identifier[2] = 1
    if move%3 == 0:
        if mode!= dslap:
            continue
        rng = rngOf(seed,25)
        counter = 25
        
        turns = (rng>>16) & 3
        if turns>1:
            rng = rngAdvance(rng)
            turns = ((rng>>16) & 3)+2
        else:
            turns = turns + 2
        
        firstturn=True
        while turns!=0:
            rng = advanceBy(rng,1)
            counter+=1
            if not firstturn:
                rng = advanceBy(rng,2)
                counter+=2
            
            critCheck = (rng>>16)%16
            rng = rngAdvance(rng)
            damageCheck = (rng>>16)%16
            if identifier[1] == 0:
                if critCheck == 0:
                    if damageCheck == 0:
                        identifier[3].append(9)
                    else:
                        identifier[3].append(7)
                else:
                    if damageCheck == 0:
                        identifier[3].append(4)
                    else:
                        identifier[3].append(3)
            else:
                if critCheck == 0:
                    if damageCheck == 0:
                        identifier[3].append(6)
                    else:
                        identifier[3].append(4)
                else:
                    if damageCheck == 0:
                        identifier[3].append(3)
                    else:
                        identifier[3].append(1)
            if firstturn:
                rng = rngAdvance(rng)
                counter +=1
            if firstturn:
                acc = (rng>>16)%100+1
                if acc>85:
                    identifier[3][0]="Miss"
                    break
                firstturn=False
            turns = turns - 1
        print(hex(seed),end="\t")
        for x in range(1,3):
            print(identifier[x],end="\t")
        print(dmg,end="\t")
        print(str(identifier[3]).strip("[]'").replace(",","").replace("'","").replace(" ",""),end=" ")
        if identifier[3][0] == "Miss":
            print()
        else:
            print(56-sum(identifier[3]))
    elif move%3 == 1:
        if mode != mimic:
            continue
        identifier[3].append("Mimic")
        print(hex(seed),end ="\t")
        for x in range(1,3):
            print(identifier[x],end="\t")
        print(dmg,end="\t")
        if identifier[2]:
            #frame 35
            rng = advanceBy(rng,18)
            move = (rng>>16)%2
            if move:
                if dmg == 25:
                    rng = advanceBy(rng,4)
                    dmg = FWrolls[15-((rng>>16)%16)]
                    if dmg == 25:
                        print("Miss range")
                        continue
                    else:
                        rng = advanceBy(rng,10)
                else:
                    rng = advanceBy(rng,14)
                move = (rng>>16)%2
                if move == 0:
                    print("Attract")
                else:
                    rng = advanceBy(rng, 10)
                    crit = (rng>>16)%16
                    rng = rngAdvance(rng)
                    if crit != 0:
                        dmg = 56-stomprolls[15-((rng>>16)%16)]
                    else:
                        dmg = 56-stompcrit[15-((rng>>16)%16)]
                    print("Stomp",dmg)
            else:
                print("fully")
            
        else:
            if dmg == 25:
                #frame 41
                rng = advanceBy(rng,21)
                dmg = FWrolls[15-((rng>>16)%16)]
                if dmg == 25:
                    print("Miss range")
                    continue
                else:
                    rng = advanceBy(rng,10)
            else:
                rng = advanceBy(rng,31)
            move = (rng>>16)%2
            if move == 0:
                print("Attract")
            else:
                rng = advanceBy(rng, 10)
                crit = (rng>>16)%16
                rng = rngAdvance(rng)
                if crit != 0:
                    dmg = 56-stomprolls[15-((rng>>16)%16)]
                else:
                    dmg = 56-stompcrit[15-((rng>>16)%16)]
                print("Stomp",dmg)               
    else:
        if mode!=metronome:
            continue
        rng = rngOf(seed,25)
        move = getMetronome(rng)
        while moveLst[move][0] in banned:
            rng = rngAdvance(rng)
            move = getMetronome(rng)
        print(hex(seed),end="\t")
        for x in range(1,3):
            print(identifier[x],end="\t")
        print(dmg,end="\t")
        print(moveLst[move][0])







