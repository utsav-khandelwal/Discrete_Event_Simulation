import random
import math
import numpy as np

S = 5                                       # system state
Sinit = 5                                   # Initial system state
Slast = S                                   # previous value of the system state
Clock = 0                                   # simulation clock
Tlast = 0                                   # time of previous state change
Area = 0.0                                  # area under S(t) curve
NextFailure = 2      # time of next failure event
# NextRepair = 1000000                        # time of next repair event
Timer = "Failure"

t = np.zeros(100)          
comp = np.zeros(100)            

random.seed(1234)

def Failure():
    global S
    global Slast
    global Tlast
    global Area
    global NextFailure
    global NextRepair
    global Clock
    global Sinit
    # Failure event
    # Update State and Schedule future events
    S = S - 1
    x = np.argmax(NextRepair)
    y = np.argmin(NextRepair)
    if (S<Sinit and S>0):
        NextFailure = Clock + 2*(math.ceil(5*random.random()))
        if(math.ceil(random.random())<.4):
            NextRepair[y] = NextRepair[x] + 3.5
        else:
            NextRepair[y] = NextRepair[x] + 2.5
   
    # Update area under the S(t) curve
    Area = Area + Slast * (Clock-Tlast)
    Tlast = Clock
    Slast = S
   
def Repair():
    global S
    global Slast
    global Tlast
    global Area
    global NextFailure
    global NextRepair
    global Clock
    global Timer
   
    # Repair Event
    # Update state and schedule future events
    S = S + 1
   
    if (S == 1):
        if(math.ceil(random.random())<.4):
            NextRepair = Clock + 3.5
        else:
            NextRepair = Clock + 2.5
        NextFailure = Clock + 2*(math.ceil(5*random.random()))
   

    # Update area under the S(t) curve
    Area = Area + Slast * (Clock-Tlast)
    Tlast = Clock
    Slast = S
   
def Timerfunc():
    global NextFailure
    global NextRepair
    global Clock
    global Timer

    z = 0
    repair = np.zeros(Sinit)
    i = 0
    while (i < Sinit):
        repair[i] = abs(NextRepair[z])
        i=i+1
    z = np.argmin(repair)
   
    # Determine the next event and advance time
    if (NextFailure < abs(NextRepair[z])):
        Timer = "Failure"
        Clock = NextFailure
        NextFailure = 1000000
    else:
        Timer = "Repair"
        Clock = NextRepair[z]
        NextRepair[z] = 1000000
    # return result
   
   

def TTF(n):
    random.seed(1234)
    global S
    global Slast
    global Tlast
    global Area
    global NextFailure
    global NextRepair
    global Clock
    global Timer

    # Define and initialize replication variables
    SumS = 0
    SumY = 0
    Rep = 0

    S = n
    Sinit = n
    Slast = S
    Clock = 0
    Tlast = 0
    Area = 0.0

    NextFailure = 2*(math.ceil(5*random.random()))
    NextRepair = np.full(n, ((-1)*1000000), dtype=float)

    while (Rep<=100):
# Advance time and execute events until the system fails
        while (S > 0):
            Timerfunc()
            if Timer == "Failure":
                Failure()
            elif Timer == "Repair":
                Repair()
        # Accumulate replication statistics
        Average = Area/Clock
        SumS= SumS + Average
        SumY = SumY + Clock
        Rep = Rep + 1
       
        # Display output  
    print("Average System Failure is at Time", SumY/100)

TTF(5)