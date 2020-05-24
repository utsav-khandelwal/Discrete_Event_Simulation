import random
import math
from scipy.stats import ttest_1samp 

# global Clock            # simulation clock
# global NextFailure      # time of next failure event
# global NextRepair       # time of next repair event
# global S                # system state
# global Slast            # previous value of the system state
# global Tlast            # time of previous state change
# global Area             # area under S(t) curve

random.seed(125456)		# To maintain consistency among various runs
# above line can be removed in order to get randomisation

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
		NextRepair = Clock + 2.5
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
time=[]
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
	time.append(Clock)
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


tset, pval = ttest_1samp(time, 13.67)

if pval < 0.05:
	print("Null hypothesis rejected")
else:
	print("Null hypothesis accepted")