def rngAdvance(prev):
	next=(1103515245*prev)+24691
	return next%0x100000000

def rngOf(seed,frame):
	prev=seed
	for x in range(0,frame):
		prev=rngAdvance(prev)
	return prev

def advanceBy(previous,frame):
	prev=previous
	for x in range(0,frame):
		prev=rngAdvance(prev)
	return prev

leerful = [[6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8],[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6],[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4],[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4],[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3]]
pound = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5]
leerless = [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6],[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4],[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]]

scratch = leerful

upper = 0x85030000
target = ["G","G","G","G","G","P5","G"]
target2 = ["P4","G","G","G","P4"]
def rival(seed):
    growl = 0
    piplup = 20
    turns = []

    rng = rngOf(seed,10)
    rng = rngAdvance(rng)
    firstCall = rng>>16
    rng = rngAdvance(rng)
    secondCall = rng>>16
    rng = advanceBy(rng,5)
    if scratch == leerless:
        roll = scratch[growl][15-(rng>>16)%16]
        rng = advanceBy(rng,1)
        piplup -= roll

    if firstCall % 256 > 99:
        turns.append("G")
        rng=advanceBy(rng,5)
        growl +=1

    else:
        if secondCall %2 == 1:
            turns.append("G")
            rng=advanceBy(rng,5)
            growl +=1
        else:
            rng = advanceBy(rng,5)
            roll = pound[15-(rng>>16)%16]
            rng = advanceBy(rng,1)
            turns.append("P{}".format(roll))
        
        

    while piplup >0:
        rng=advanceBy(rng,10)
        rng = rngAdvance(rng)
        firstCall = rng>>16
        rng = rngAdvance(rng)
        secondCall = rng>>16
        #print(frame,piplup)
        rng = advanceBy(rng,5)
        roll = scratch[growl][15-(rng>>16)%16]
        rng = advanceBy(rng,1)
        piplup -= roll
        
        if piplup <= 0:
            break
        
        else:
            if firstCall % 256 > 99 and growl <6:
                turns.append("G")
                rng=advanceBy(rng,5)
                growl +=1
            else:
                if secondCall %2 == 1 and growl<6:
                    turns.append("G")
                    rng=advanceBy(rng,5)
                    growl +=1
                else:
                    rng = advanceBy(rng,5)
                    roll = pound[15-(rng>>16)%16]
                    rng = advanceBy(rng,1)
                    turns.append("P{}".format(roll))
    return turns

upper = 0x85030000

for x in range(0x42ae-60,0x42ae+300):
     fight = rival(upper+x)
     turns = len(fight)+1
     print("{}\t{}\t{}".format(hex(upper+x),turns,fight))
