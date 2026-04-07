#Chyna Thomas

import random
from collections import deque

class MemLevel:
    def __init__(self, name, capacity, policy='FIFO', lat=1):
        self.name = name 
        self.capacity = capacity #max instructions
        self.policy = policy #eviction rule
        self.storage = deque() #stores data
        self.lat = lat 
        self.accessorder = [] #tracks least recently used
       
    
    def add(self, data):
        if data in self.storage: #no duplicates
            return
        if len(self.storage) >= self.capacity: #if full, evict 
            self.evict()
        self.storage.append(data) 
        self.updata(data) #keeps accessorder current
    
    def remove(self, data):
        if data in self.storage:
            self.storage.remove(data)
            if data in self.accessorder:
                self.accessorder.remove(data)

    def evict(self):
        if self.policy == 'FIFO':
            removed = self.storage.popleft() #oldest data removed
        elif self.policy == 'LRU': 
            if self.accessorder:
                removed = self.accessorder.pop(0) #least used removed
                self.storage.remove(removed)
            else:
                removed = self.storage.popleft()
        elif self.policy == 'Random':
            removed = random.choice(list(self.storage))
            self.storage.remove(removed)
        else: 
            removed = self.storage.popleft()
        if removed in self.accessorder:
            self.accessorder.remove(removed)

        print(f'Evict: {self.name} removed 0x{removed:08x}')
        return removed

    def updata(self, data):
        if self.policy == 'LRU':
            if data in self.accessorder:
                self.accessorder.remove(data)
            self.accessorder.append(data)

    def printstr(self):
        used = len(self.storage)
        return f'{self.name}: Latency: {self.lat} Used {used} of {self.capacity} | Storage: {self.storage}'




class MemHierchy:
    def __init__(self, ssd, dram, l3, l2, l1, policy='LRU'):
        assert ssd > dram > l3 > l2 > l1 #enforces rule
        self.policy = policy
        self.ssd = MemLevel("SSD", ssd, policy=policy, lat=10)
        self.dram = MemLevel("DRAM", dram, policy=policy, lat=5)
        self.l1 = MemLevel("L1", l1, policy=policy, lat=1)
        self.l2 = MemLevel("L2", l2, policy=policy, lat=2)
        self.l3 = MemLevel("L3", l3,policy=policy, lat=3)
        self.levels = [self.ssd, self.dram, self.l3, self.l2, self.l1] #ordered from slowest to fastest
        self.clock = 0
        self.hits = 0
        self.misses = 0
        self.reads = 0
        self.writes = 0
        self.pending = []
        self.trace = []

        self.prepSSD()

    def prepSSD(self): #initializes storage
        n = min(self.ssd.capacity, 32)
        for i in range(n):
            instr = 0xADD00000 + i
            self.ssd.storage.append(instr)
        print(f'SSD seeded with {n} instructions')


    def tick(self):
        self.clock += 1
        print(f'\nClock Cycle: {self.clock}')
        self.pendingprocess()
    
    def schedule(self, data, froml, to):
        lat = self.levels[froml].lat
        ready = self.clock + lat
        self.pending.append((ready, froml, to, data))
        self._log('SCHEDULE', f'instruction=0x{data:08x} {self.levels[froml].name} to {self.levels[to].name} ready at {ready}')

    
    def read(self, instr):
        self.reads += 1
        self._log('READ', f'instr=0x{instr:08x}')

        for i in reversed(range(len(self.levels))):
            level = self.levels[i]

            if instr in level.storage:
                level.updata(instr)
                if level.name == 'L1': #Only treating L1 as a hit
                    self.hits += 1
                    self._log('HIT', f'0x{instr:08x} in {level.name}')
                    return
        
                self.misses += 1
                self._log('MISS', f'0x{instr:08x} in {level.name}')

                if level.name == 'SSD': #if not a hit then load or promote it
                    self._loadSSD(instr)
                else:
                    self.promote(i, instr)
                return
        self.misses += 1
        self._log('MISS', f'{instr} not found in any level')
        self.ssd.add(instr)
        self._loadSSD(instr)
    
    
    def write(self, instr):
        self.writes += 1
        self._log('WRITE', f'instruction 0x{instr:08x}')

        if instr not in self.l1.storage:
            self.l1.add(instr)
        if instr not in self.ssd.storage:
            self.ssd.add(instr)

        for i in reversed(range(len(self.levels)-1)):
            src = self.levels[i+1]
            dst = self.levels[i]
            self.tick()
            print(f'WRITE-BACK instruction 0x{instr:08x} from {src.name} to {dst.name}')
            dst.add(instr)
            

        self._log('WRITE',f'0x{instr:08x} persisted to SSD')
    
    def _loadSSD(self, instr): #Handles misses
        for i in range(len(self.levels)-1):
            self.tick()
            src = self.levels[i]
            dst = self.levels[i +1]

        
            dst.add(instr)
            print(f'Instruction 0x{instr:08x} sent from {src.name} to {dst.name}')

    def promote(self, indx, instr):
        for i in range(indx, len(self.levels)-1):
            src = self.levels[i]
            dst = self.levels[i + 1]
            self.tick()

            print(f'Promote {instr} {src.name} to {dst.name}')
            dst.add(instr)
    
    def _log(self, tag, msg):
        entry = f'[clock={self.clock:>3}] [{tag:<5}, {msg} ]'
        self.trace.append(entry)

    def pendingprocess(self): #transfer
        nowReady = [p for p in self.pending if p[0] <= self.clock]
        self.pending = [p for p in self.pending if p[0] > self.clock]
        
        for ready, froml, to, data in nowReady:
            dst = self.levels[to]
            dst.add(data)
            self._log('MOVE', f'0x{data:08x} sent to {dst.name}')

    def printres(self):
        print('\n--Memory Configuration--')
        for lvl in self.levels:
            print(f'{lvl.name}: capacity={lvl.capacity}, latency={lvl.lat} ')
        print('\n--Final State--')
        for lvl in self.levels:
            print(lvl.printstr())

        print('\n--Stats--')
        print(f'Reads: {self.reads}')
        print(f'Writes: {self.writes}')
        print(f'Hitss: {self.hits}')
        print(f'Misses: {self.misses}')
        print('\n--Traces--')
        for t in self.trace:
            print(t)

def  main():
    mem = MemHierchy(ssd=64, dram=32, l3=16, l2=8, l1=4, policy='LRU')
    print('--Starting--')
    instructions = [
            0xADD00001,
            0xADD00002,
            0xADD00003,
            0xADD00001,  
            0xADD00004,
            0xADD00002,
    ]

    for instr in instructions: 
        mem.read(instr)
        
    mem.write(0xFACEBEAD)
    mem.printres()

main()