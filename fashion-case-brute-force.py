#######################################################

# Configurations

ROWAN_Max_Wait = 60
ROWAN_Min_Window = 20
Fashion_Case_Max_Wait = 60
Fashion_Min_Window = 64

seed = 0x82031489

#frames entering Jubilife City
low = 2140
high = 2150

stepcount = 1

#######################################################


u = 'u'
U = 'U'
d = 'd'
D = 'D'
l = 'l'
L = 'L'
r = 'r'
R = 'R'
UU = 'UU'

#17L,15U

movements_to_try = [
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,U,U,U,U,U,U,U,U,U,U,U,U,U,U,UU],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,U,L,U,U,U,U,U,U,U,U,U,U,U,U,U,UU],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,U,U,L,U,U,U,U,U,U,U,U,U,U,U,U,UU],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,U,U,U,L,U,U,U,U,U,U,U,U,U,U,U,UU],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,U,U,U,U,L,U,U,U,U,U,U,U,U,U,U,UU],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,U,U,U,U,U,L,U,U,U,U,U,U,U,U,U,UU],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,U,U,U,U,U,U,L,U,U,U,U,U,U,U,U,UU],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,l,U,U,U,U,U,U,U,U,U,U,U,U,U,U,UU],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,U,l,U,U,U,U,U,U,U,U,U,U,U,U,U,UU],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,U,U,l,U,U,U,U,U,U,U,U,U,U,U,U,UU],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,U,U,U,l,U,U,U,U,U,U,U,U,U,U,U,UU],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,U,U,U,U,l,U,U,U,U,U,U,U,U,U,U,UU],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,U,U,U,U,U,l,U,U,U,U,U,U,U,U,U,UU],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,U,U,U,U,U,U,l,U,U,U,U,U,U,U,U,UU],
]

class RNG:
    def __init__(self, seed):
        self.initial_seed = seed
        self.seed = seed
        self.frame = 0
     
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

    def next(self, n=1):
        seed = self.seed

        for i in range(n):
            seed = ((seed * 0x41C64E6D) + 0x6073) % (2**32)
        return RNG(seed)

    def upper16(self):
        return self.seed >> 16

    def reset(self):
        self.seed = self.initial_seed
        self.frame = 1

    def get_spinner_cycle(self):
        return [16, 32, 48, 64][self.upper16() % 4] 
    
    def get_walker_cycle(self):
        return [15, 31, 47, 63][self.upper16() % 4]

    def get_direction(self,dirs = 4):
        return [*range(0,dirs)][self.upper16() % dirs]
    
    def getRand(self):
        return self.upper16()
    
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

class spinner:
    def __init__(self, tick, name="", loaded = False, extra_tick=0, dirs = 4):
        self.tick = tick + extra_tick
        self.direction = 4
        self.name = name
        self.dirs = dirs
        self.loaded = loaded
    
    def advance(self,rng):
        if self.loaded:
            self.tick -= 1
            if self.tick <= 0:
                self.tick = rng.advance().get_spinner_cycle()
                self.direction = rng.advance().get_direction(self.dirs)


#npc4, little girl
class walker_3x3:
    def __init__(self, tick, name="", extra_tick=0, dirs=4,can_move = True):
        self.tick = tick + extra_tick

        self.max_x, self.max_y = 2, 2
        self.x, self.y = 1, 1

        self.name = name

        self.direction = 4
        self.chose_direction = False
        self.dirs = dirs
        self.can_move = can_move

    def move(self, direction):

        if direction == 0: 
            self.y += 1
        elif direction == 1: 
            self.y -= 1
        elif direction == 2: 
            self.x -= 1
        elif direction == 3: 
            self.x += 1

        cond = 0 <= self.x <= self.max_x and 0 <= self.y <= self.max_y
        if cond:
            self.direction = direction
        
        if self.x > self.max_x:
            self.x = self.max_x
        elif self.x < 0:
            self.x = 0

        if self.y > self.max_y:
            self.y = self.max_y
        elif self.y < 0:
            self.y = 0

        return 9 if cond else 2

    def print(self):
        print(f"{self.name}: ({self.x}, {self.y}) | tick: {self.tick} | movement history: {self.direction_history}")
    
    def advance(self, rng):
        self.tick -= 1

        if self.tick <= 0 and not self.chose_direction:
            direction = rng.advance().get_direction(self.dirs)
            if self.can_move:
                self.tick = self.move(direction)
            else:
                self.tick = 2
            self.chose_direction = True
        elif self.tick <= 0:
            self.tick = rng.advance().get_walker_cycle()
            self.chose_direction = False

#npc 7
class walker_3x3_blocked(walker_3x3):
    def move(self,direction):
        old_x = self.x
        old_y = self.y
        if direction == 0: 
            self.y += 1
        elif direction == 1: 
            self.y -= 1
        elif direction == 2: 
            self.x -= 1
        elif direction == 3: 
            self.x += 1

        if self.x == 0 and self.y == 2:
            self.x = old_x
            self.y = old_y
            cond = False
        else:
            cond = 0 <= self.x <= self.max_x and 0 <= self.y <= self.max_y
        if cond:
            self.direction = direction
        
        if self.x > self.max_x:
            self.x = self.max_x
        elif self.x < 0:
            self.x = 0

        if self.y > self.max_y:
            self.y = self.max_y
        elif self.y < 0:
            self.y = 0

        return 9 if cond else 2
    
class walker_3x1_free(walker_3x3):
    def __init__(self, tick, name="", extra_tick=0, dirs = 4,can_move = True):
        self.tick = tick + extra_tick

        self.max_x, self.max_y = 2, 0
        self.x, self.y = 1, 0

        self.name = name

        self.direction = 4
        self.chose_direction = False
        self.dirs = dirs
        self.can_move = can_move

    def move(self, direction):

        if direction == 0: 
            return 2
        elif direction == 1: 
            return 2
        elif direction == 2: 
            self.x -= 1
        elif direction == 3: 
            self.x += 1

        cond = 0 <= self.x <= self.max_x and 0 <= self.y <= self.max_y
        if cond:
            self.direction = direction
        
        if self.x > self.max_x:
            self.x = self.max_x
        elif self.x < 0:
            self.x = 0

        if self.y > self.max_y:
            self.y = self.max_y
        elif self.y < 0:
            self.y = 0

        return 9 if cond else 2
    
    def advance(self, rng):
        self.tick -= 1

        if self.tick <= 0 and not self.chose_direction:
            direction = rng.advance().get_direction(self.dirs)
            if self.can_move:
                self.tick = self.move(direction)
            else:
                self.tick = 2
            self.chose_direction = True
        elif self.tick <= 0 and self.chose_direction:
            self.tick = rng.advance().get_walker_cycle()
            self.chose_direction = False
    

class walker_3x1_hor(walker_3x1_free):
    def __init__(self, tick, name="", extra_tick=0, dirs = 2,can_move = True):
        self.tick = tick + extra_tick

        self.max_x, self.max_y = 2, 0
        self.x, self.y = 1, 0

        self.name = name

        self.direction = 4
        self.chose_direction = False
        self.dirs = 2
        self.cursor = 0
        self.can_move=can_move

    def move(self, direction):
        if direction == 0: 
            self.x -= 1
        elif direction == 1: 
            self.x += 1

        cond = 0 <= self.x <= self.max_x
        if cond:
            self.direction = direction
        
        if self.x > self.max_x:
            self.x = self.max_x
        elif self.x < 0:
            self.x = 0

        return 9 if cond else 2
    
class Player:
    def __init__(self,movements,stepcount):
        self.x = 19
        self.y = 0
        self.hitbox = [[19,0],[19,0]]
        self.tick = 4
        self.enemy = None
        self.cursor = 0
        self.movements = movements
        self.stepcount = stepcount

    def move(self,direction):

        if direction in ['u','U','UU']: 
            self.y += 1
        elif direction in ['d','D']: 
            self.y -= 1
        elif direction in ['l','L']: 
            self.x -= 1
        elif direction in ['r','R']: 
            self.x += 1
        
        if direction in ['u','d','l','r']:
            length = 8
        elif direction == 'UU':
            length = 2
        else:
            length = 4
        if self.enemy != None:
            if [self.x,self.y] in self.enemy.hitbox:
                return False
        self.hitbox[0] = self.hitbox[1]
        self.hitbox[1] = [self.x,self.y]
        self.tick = length
        self.stepcount += 1
        return True

    def advance(self,rng):
        self.tick -= 1
        if self.tick <= 0:
            if self.cursor == len(self.movements):
                return [False,True]
            res = self.move(self.movements[self.cursor])
            if res == False:
                return [False, False]
            self.cursor += 1
        elif self.tick == 1:
            if stepcount == 0:
                rng.advance()
        return [True,True]

class idiot(walker_3x1_hor):
    def __init__(self, tick, player, name="", extra_tick=0, dirs = 2, can_move = True):
        self.tick = tick + extra_tick

        self.max_x, self.max_y = 2, 1
        self.x, self.y = 1, 1

        self.hitbox = [[1,1],[1,1]]
        self.name = name

        self.direction = 4
        self.chose_direction = False
        self.dirs = 2 
        self.player = player
        self.can_move = can_move
    
    def move(self, direction):
        if direction == 0: 
            self.x -= 1
        elif direction == 1: 
            self.x += 1

        cond = 0 <= self.x <= self.max_x
        if cond:
            self.direction = direction
            self.hitbox[0] = self.hitbox[1]
            self.hitbox[1] = [self.x,self.y]
        
        if self.x > self.max_x:
            self.x = self.max_x
        elif self.x < 0:
            self.x = 0

        return 9 if cond else 2
    
    def advance(self, rng):
        self.tick -= 1

        if self.tick <= 0 and not self.chose_direction:
            direction = rng.advance().get_direction(self.dirs)
            if self.can_move:
                self.tick = self.move(direction)
            else:
                self.tick = 2
            self.chose_direction = True

        elif self.tick <= 0 and self.chose_direction:
            self.hitbox[0] = None
            self.tick = rng.advance().get_walker_cycle()
            self.chose_direction = False



class walker_1x3_ver(walker_3x1_hor):
    def __init__(self, tick, name="", extra_tick=0, dirs = 2, can_move = True):
        self.tick = tick + extra_tick

        self.max_x, self.max_y = 0, 2
        self.x, self.y = 0, 1

        self.name = name

        self.direction = 4
        self.chose_direction = False
        self.dirs = 2
        self.can_move = can_move

    def move(self, direction):
        if direction == 0: 
            self.y += 1
        elif direction == 1: 
            self.y -= 1

        cond = 0 <= self.y <= self.max_y
        if cond:
            self.direction = direction
        
        if self.y > self.max_y:
            self.y = self.max_y
        elif self.y < 0:
            self.y = 0

        return 9 if cond else 2



for enter_frame in range(low, high):
    #print(f"Enter Frame: {enter_frame}")
    for movement_type in range(0,len(movements_to_try)):

        primaryRNG = RNG(seed)
        primaryRNG.advance(enter_frame)
        #print(f"Turn left at {x}: ")


        NPCs = [None for x in range(0,12)]

        I = Player(movements_to_try[movement_type],stepcount)
        I.advance(primaryRNG)

        NPCs[2] = spinner(primaryRNG.advance().get_spinner_cycle(),"BL Nerd")
        NPCs[4] = spinner(primaryRNG.advance().get_spinner_cycle(),"Old Spinner",True)
        NPCs[7] = spinner(primaryRNG.advance().get_spinner_cycle(),"Mid Clown",True)
        NPCs[10] = spinner(primaryRNG.advance().get_spinner_cycle(),"GT Green Hair")
        NPCs[11] = spinner(primaryRNG.advance().get_spinner_cycle(),"Pond Green Hair",True)

        for x in range(0,2):
            I.advance(primaryRNG)
            for x in range(0,len(NPCs)):
                if NPCs[x] != None:
                    NPCs[x].advance(primaryRNG)

        NPCs[1] = idiot(primaryRNG.advance().get_walker_cycle(),I,"Green Hair Bonker")
        I.enemy = NPCs[1]
        NPCs[3] = walker_3x3(primaryRNG.advance().get_walker_cycle(),"Little Girl")
        NPCs[5] = walker_1x3_ver(primaryRNG.advance().get_walker_cycle(),"Nerd next to Clown")
        NPCs[6] = walker_3x3_blocked(primaryRNG.advance().get_walker_cycle(),"Old Man")
        NPCs[8] = walker_3x1_free(primaryRNG.advance().get_walker_cycle(),"Right Clown",0,4,True)

        for x in range(0,13):
            I.advance(primaryRNG)
            for x in range(0,len(NPCs)):
                if NPCs[x] != None:
                    NPCs[x].advance(primaryRNG)

        # looker cutscene activated at the end of above loop, below prints npc status during looker cutscene

        #for x in range(0,len(NPCs)):
        #    if NPCs[x] != None:
        #        print(f"{x+1}: {NPCs[x].name} {NPCs[x].tick}")

        # after looker cutscene, there will be 2F delay before you can move

        for x in range(0,2):
            #I.advance()
            for x in range(0,len(NPCs)):
                if NPCs[x] != None:
                    NPCs[x].advance(primaryRNG)

        loadingLeftClown = False

        loadingBottomLeft = False

        LCtick = 4

        BLtick = 10

        # starts moving now
        res = I.advance(primaryRNG)

        while res[0]:
            #print(f"{I.movements[I.cursor-1]}")
            #print(f"{I.enemy.hitbox}")
            #for x in range(0,len(NPCs)):
            #    if NPCs[x] != None:
            #        print(f"{x+1}: {NPCs[x].name} {NPCs[x].tick}")
            #print()
            if I.x <= 2:
                loadingLeftClown = True
                if I.y <= 6:
                    loadingBottomLeft = True
            if I.y>6:
                loadingBottomLeft = False
            if I.x>2:
                loadingLeftClown = False
                loadingBottomLeft = False
            
            if loadingLeftClown:
                LCtick -= 1
            if loadingBottomLeft:
                BLtick -= 1
            
            if NPCs[0] == None and LCtick == 0 and loadingLeftClown:
                NPCs[0] = walker_3x1_hor(primaryRNG.advance().get_walker_cycle(),"Green Hair below Left Clown",0,2,True)
                NPCs[1].advance(primaryRNG)
                NPCs[3].advance(primaryRNG)
                NPCs[4].advance(primaryRNG)
                NPCs[5].advance(primaryRNG)
                NPCs[6].advance(primaryRNG)
                NPCs[7].advance(primaryRNG)
                NPCs[8].advance(primaryRNG)
                NPCs[9] = walker_3x1_free(primaryRNG.advance().get_walker_cycle(),"Left Clown",0,4,True)
                NPCs[11].advance(primaryRNG)
            elif NPCs[2].loaded == False and BLtick == 0 and loadingBottomLeft:
                NPCs[2].loaded = True
                NPCs[10].loaded = True
                for x in range(0,len(NPCs)):
                    if NPCs[x] != None:
                        NPCs[x].advance(primaryRNG)
            else:
                for x in range(0,len(NPCs)):
                    if NPCs[x] != None:
                        NPCs[x].advance(primaryRNG)

                if I.x > 2 and NPCs[0] != None:
                    NPCs[0].can_move = False
                    NPCs[9].can_move = False
                
        
                if I.y > 6: 
                    if NPCs[8] != None:
                        NPCs[5].can_move = False
                        NPCs[8].can_move = False
                        if NPCs[8].x == 2:
                            NPCs[8] = None



            res = I.advance(primaryRNG)


            

        if res[1] == False:
            #print(f"blocked\n")
            continue

        double = primaryRNG.frame

        deloads = [2,4,5,8,10]

        for x in deloads:
            NPCs[x] = None

        for x in range(0,826):
            for y in range(0,len(NPCs)):
                if NPCs[y] != None:
                    NPCs[y].advance(primaryRNG)

        '''
        for x in range(0,len(NPCs)):
            if NPCs[x] != None:
                print(f"{x}: {NPCs[x].tick}")
        '''

        rowan_wait = 0
        while rowan_wait < ROWAN_Max_Wait:
            npc1 = NPCs[9].tick
            npc2 = NPCs[11].tick


            rowan_window = min(npc1,npc2)*2
            #print(rowan_window)

            rowan_wait += rowan_window

            if rowan_window >= ROWAN_Min_Window:
                NPCLst = [0,1,3,6,7]
                simNPCs = []
                rng_cpy = RNG(seed)
                rng_cpy.seed = primaryRNG.seed
                rng_cpy.frame = primaryRNG.frame
                simNPCs.append(walker_3x1_hor(0,"Green Hair below Left Clown",0,2,True))
                simNPCs.append(idiot(0,I,"Green Hair Bonker"))
                simNPCs.append(walker_3x3(0,"Little Girl"))
                simNPCs.append(walker_3x3_blocked(0,"Old Man"))
                simNPCs.append(spinner(0,"Mid Clown",True))
                for x in range(0,4):
                    simNPCs[x].max_x = NPCs[NPCLst[x]].max_x
                    simNPCs[x].max_y = NPCs[NPCLst[x]].max_y
                    simNPCs[x].x = NPCs[NPCLst[x]].x
                    simNPCs[x].y = NPCs[NPCLst[x]].y
                    simNPCs[x].tick = NPCs[NPCLst[x]].tick
                    simNPCs[x].chose_direction = NPCs[NPCLst[x]].chose_direction
                simNPCs[4].tick = NPCs[NPCLst[4]].tick
                
                for x in range(0,256):
                    for y in range(0,5):
                        simNPCs[y].advance(rng_cpy)

                #print("Fashions:")
                for x in range(0,int(Fashion_Case_Max_Wait/2)+1):
                    fashion_case_window = min(simNPCs[0].tick,simNPCs[1].tick,simNPCs[2].tick,simNPCs[3].tick,simNPCs[4].tick)*2
                    #print(fashion_case_window)
                    if fashion_case_window >= Fashion_Min_Window:
                        if movement_type > 6:
                            turn = movement_type - 7
                        else:
                            turn = movement_type
                        print(f"Enter Frame: {enter_frame}\nTurn at: {turn}\nWalk: {(movement_type>6)}\nGalactic Double Frame: {double}\nRowan Wait: {rowan_wait-rowan_window} ~ {rowan_wait-1}\nFashion Case: {x*2} ~ {x*2+fashion_case_window-1} ({rng_cpy.frame})\n")
                        break
                    for y in range(0,5):
                        simNPCs[y].advance(rng_cpy)
                #print("next ROWAN")

            for x in range(0,int(rowan_window/2)):
                for y in range(0,len(NPCs)):
                    if NPCs[y] != None:
                        NPCs[y].advance(primaryRNG)