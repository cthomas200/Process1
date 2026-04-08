##Overview
This program simulates a processor moves instructions through memory.
It models: 
- Read
- Write
- Cache Eviction Polices (FIFO, LRU, Random)
- Clock tracked data movement
- Cache hits and misses

##Key Features
1. Memory Hierarchy
	
	It consists of:
		- SSD (largest, slowest)
		- DRAM 
		- Cache Levels: L3, L2, L1 (smallest, fastest)
	Each level has a fixed capacity, stores instructions, use an eviction policy 	when full

2. Data Movement 
	
	Data must move step by step through the hierarchy. No skipping levels 	is allowed. Movement follows SSD -> DRAM -> L3 -> L2 -> L1

3. Clock Driven Simulation

	The system operates in clock cycles. Each transfer occurs over 	time, every movement or write increments the clock.

4. Read Operation

	It searches backwards from L1 to SSD. If it's found in L1 then it's 	counted as a HIT. If found elsewhere then it's counted as a MISS. 	Data is either promoted if found in cache or loaded from the SSD.

5. Write Operation

	 Write occurs first in L1 and then flows downward to ensure data 	persistence. 

6. Cache Replacement Policy 
	
	This simulation supports:
		-LRU (least recently used, default)
		-FIFO (First in First out)
		-Random
	LRU is implemented by tracking access order and evicting the least 	recently accessed instruction. 

#OutPut

The program produces:

Memory Configuration
	Displays capacity and latency of each level

Instruction Access Trace
	Logs all operations: 
		-Read
		-Write
		-HIT/MISS

Data Movement
	Shows how instructions through the hierarchy

Cache Hits/Misses

Final Memory State


#How to Run

python ChynaTprocessor3.py 

##Author
Chyna Thomas








A command line Python program that takes a truth table as input and outputs both the canonical and simplified Boolean expressions in SOP or POS form, along with K-map grouping.

##Features
Accepts 2-4 variable variable truth tables
Generates canonical SOP and POS expressions 
Simplifies using SymPy
Validates simplified output against original truth table
Displays K-map Grouping

##Requirements
Python 3.x
SymPy
Install Sympy with pip install sympy

##Usage
Run the program from the terminal
You will be prompted to:
  1.Enter number of variables (2-4)
  2.Enter each row of the truth table
  3.Choose SOP or POS output

##Input Rules
All input values must be 0 or 1
Each row must have exactly n inputs + 1 output
No duplicate inputs allowed
Rows can be entered in any other, the program sorts them

##Author
Chyna Thomas
  
