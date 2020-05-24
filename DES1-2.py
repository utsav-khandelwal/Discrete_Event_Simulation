import random
import math
import numpy as np

# global Clock            # simulation clock
# global NextFailure      # time of next failure event
# global NextRepair       # time of next repair event
# global S                # system state
# global Slast            # previous value of the system state
# global Tlast            # time of previous state change
# global Area             # area under S(t) curve

random.seed(1254246)

def Failure():
	global Clock        
	global NextFailure  
	global NextRepair   
	global S            
	global Slast        
	global Tlast        
	global Area    	     
# Failure event
# Update state and schedule future events
	S = S-1
	if(S==1):
		NextFailure = Clock + math.ceil(6*random.random())
		NextRepair = Clock + 2.5
# Update area under the S(t) curve
	Area = Area + Slast * (Clock - Tlast)
	Tlast = Clock
	Slast = S


def Repair():
	global Clock        
	global NextFailure  
	global NextRepair   
	global S            
	global Slast        
	global Tlast        
	global Area    	     
# Repair event
# Update state and schedule future events
	S = S+1
	if(S == 1):
		if(math.ceil(random.random())<.65):
			NextRepair = Clock + 2.5
		else:
			NextRepair = Clock + 1.5			
		NextFailure = Clock + math.ceil(6*random.random())
    
# Update area under the S(t) curve
	Area = Area + Slast * (Clock - Tlast)
	Tlast = Clock
	Slast = S

def Timer():
	global Clock        
	global NextFailure  
	global NextRepair   
	global S            
	global Slast        
	global Tlast        
	global Area    	     
	Infinity = 1000000

# Determine the next event and advance time
	if (NextFailure < NextRepair):
		y = "Failure"
		Clock = NextFailure
		NextFailure = Infinity
	else:
		y = "Repair"
		Clock = NextRepair
		NextRepair = Infinity
	return y


# Program to generate a sample path for the TTF example
Infinity = 1000000

# Define and initialize replication variables
SumS = 0
SumY = 0

for Rep in range (0,100):
# Initialize the state and statistical variables
	S = 2
	Slast = 2
	Clock = 0
	Tlast = 0
	Area = 0

# Schedule the initial failure event
	NextFailure = math.ceil(6*random.random())
	NextRepair = Infinity

# Advance time and execute events until the system fails
	while(S != 0):
		NextEvent = Timer()
		if(NextEvent=="Failure"):
			Failure()
		else:
			Repair()

# Accumulate replication statistics
	SumS = SumS + Area / Clock
	SumY = SumY + Clock

# Display output
print('Average failure at time: ',SumY / 100, ', With average number of functional components: ', (SumS / 100))

# Program to generate a sample path for the TTF example
Infinity = 1000000
    
# Initialize the state and statistical variables
S = 2
Slast = 2
Clock = 0
Tlast = 0
Area = 0
    
# Schedule the initial failure event
NextFailure = math.ceil(6*random.random())
NextRepair = Infinity
    
# Advance time and execute events until the system fails
while (S != 0):
	NextEvent = Timer()
	if (NextEvent == "Failure"):
	    Failure()
	else:
	    Repair()       
    
# Display output
print('System failure at time: ', Clock,', With average number of functional components: ' , Area / Clock)