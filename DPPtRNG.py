land = 0
cave = 1
surf = 2
coronet = 3
walk = 40
bike = 70
natures = natures=['Hardy','Lonely','Brave','Adamant','Naughty','Bold','Docile','Relaxed','Impish','Lax','Timid','Hasty','Serious','Jolly','Naive','Modest','Mild','Quiet','Bashful','Rash','Calm','Gentle','Sassy','Careful','Quirky']
default_levels = [0,0,0,0,0,0,0,0,0,0,0,0]
class wildPoke:
    def __init__(self, slot, level, nature, ability, stats, gender, held_item, pid):
        self.slot = slot
        self.level = level
        self.nature = nature
        self.ability = ability
        self.stats = stats
        self.gender = gender
        self.held_item = held_item
        self.pid = pid
    def display(self):
        return "{}, {}, {}, {}, {}, {}, {}, {}".format(self.slot,self.level,natures[self.nature],self.ability,self.stats,self.gender,self.held_item,hex(self.pid))


class RNG:
    def __init__(self, seed, mrateModifier = 0):
        self.initial_seed = seed
        self.seed = seed
        self.frame = 0
        self.mrateModifier = mrateModifier
     
    @staticmethod
    def seed_datetime(year, month, day, hour, minute, second, frames):
        xx = day * month + minute + second
        yy = hour
        zzzz = frames + year % 2000

        seed = int(f"{xx}{yy}{zzzz}")

        return seed

    def advance(self, n=1):
        for i in range(n):
            self.seed = ((self.seed * 0x41C64E6D) + 0x6073) % (2**32)
            self.frame += 1
        return self
    
    def getRand(self):
        self.advance()
        val = self.seed
        return val >> 16
    
    def hasPokerus(self):
        if self.upper16 in [0x4000, 0x8000, 0xc000]:
            return True
        else:
            return False
    
    def getLandSlot(self):
        parts=[20, 40, 50, 60, 70, 80, 85, 90, 94, 98, 99, 100]
        sel = self.getRand()//656
        for x in range(0,12):
            if sel<parts[x]:
                return x
            
    def genPID(self):
        lowerPID = self.getRand()
        upperPID = self.getRand()
        return upperPID*0x10000+lowerPID
    
    def getIVs(self):
        ivs = []
        iv1 = self.getRand()
        iv2 = self.getRand()
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
    
    def methodJ(self,levels=default_levels,intimidate = False, lvl = 100):
        blocked = False
        init = self.frame
        slot = self.getLandSlot()
        nature = self.getRand()//0xa3e
        if intimidate == True:
            intimidateCheck = self.getRand() >> 15
            if intimidateCheck == 0 and ((lvl - levels[slot]) >= 5):
                blocked = True
        PIDFound = False
        while PIDFound == False:
            PID = self.genPID()
            if PID % 25 == nature:
                PIDFound = True
        ivs = self.getIVs()
        item_deter = self.getRand() % 100
        parts = [45,95,100]
        for x in range(0,3):
            if item_deter<parts[x]:
                item = x
                break
        item = ["No Item","Common Item","Rare Item"][x]
        gender = PID % 0x100
        if gender <= 126:
            gender = "Female"
        else:
            gender = "Male"
        self.advance(4)
        return [wildPoke(slot, levels[slot],nature, PID%2, ivs, gender, item, PID),init,self.frame,blocked]       
        
        
    def honeyLand(self,advance = False,levels = default_levels):
        if not advance:
            rng = RNG(0)
            rng.initial_seed = self.initial_seed
            rng.seed = self.seed
            rng.frame = self.frame
            return rng.methodJ(levels = levels)
        else:
            return self.methodJ(levels = levels)
    
    def checkEncounter(self,method = walk, advance = False, terrain = land, intimidate = False, lvl = 100, levels = [0,0,0,0,0,0,0,0,0,0,0,0]):
        encRate = [30, 10, 10, 15][terrain]
        rng = RNG(0)
        rng.initial_seed = self.initial_seed
        rng.seed = self.seed
        rng.frame = self.frame
        movementCheck = rng.getRand() // 0x290
        if movementCheck >= (method + self.mrateModifier):
            if advance:
                self.advance()
            return False
        terrainCheck = rng.getRand() // 0x290
        if terrainCheck >= encRate:
            if advance:
                self.advance(2)
            return False
        rng_copy = RNG(0)
        rng_copy.initial_seed = rng.initial_seed
        rng_copy.seed = rng.seed
        rng_copy.frame = rng.frame
        wild = rng_copy.methodJ(intimidate = intimidate, lvl = lvl, levels = levels)
        if intimidate and wild[3] == True:
            if advance:
                self.advance(4)
        return wild

            
                
                


            
            
        

    def jump(self,frame):
        self.reset()
        self.advance(frame)
        return self

    def next(self, n=1):
        seed = self.seed
        for i in range(n):
            seed = ((seed * 0x41C64E6D) + 0x6073) % (2**32)
        return RNG(seed)

    def upper16(self):
        return self.seed >> 16

    def reset(self):
        self.seed = self.initial_seed
        self.frame = 0

    def get_spinner_cycle(self):
        return [16, 32, 48, 64][self.upper16() % 4] 
    
    def get_walker_cycle(self):
        return [15, 31, 47, 63][self.upper16() % 4]

    def get_direction(self,dirs = 4):
        return [*range(0,dirs)][self.upper16() % dirs]
    
    def solve_cans(self):
        can_2_directions = [
            ("R", "D"),
            ("L", "R", "D"), 
            ("L", "R", "D"), 
            ("L", "R", "D"), 
            ("L", "D"),
            ("U", "R", "D"),
            ("U", "L", "D", "R"),
            ("U", "L", "D", "R"),
            ("U", "L", "D", "R"),
            ("U", "L", "D"),
            ("U", "R"),
            ("U", "L", "R"),
            ("U", "L", "R"),
            ("U", "L", "R"),
            ("U", "L")
        ]

        can_1 = self.next().upper16() % 15

        can_2_candidates = can_2_directions[can_1]
        can_2 = can_2_candidates[self.next(2).upper16() % len(can_2_candidates)]

        return f"{can_1+1}-{can_2}"

    def print(self):
        print(hex(self.seed))


