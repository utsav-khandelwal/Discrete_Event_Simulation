# Created by - Utsav

import random
import simpy
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

WARMUP_TIME = 5000
RANDOM_SEED = 1234
NUM_MACHINES = 2         
SIM_TIME = 50000     

# Defining the various time storing arrays
timespentOP = []
waitingTimeOP = []
timespentIP = []
waitingTimeIP = []


def setup(env, num_machines):
    
    clinic = Clinic(env, num_machines)
    i=0
   
    while True:
        k = np.random.uniform(0,1)
        if(k > 5/(125)): 
            clinic.typeP = "PO"
            yield env.timeout(np.random.exponential(5))
            i += 1
            env.process(doc(env, 'PO %d' % i, clinic))
        else:
            clinic.typeP = "PI"
            yield env.timeout(np.random.exponential(120))
            i += 1
            env.process(doc(env, 'PI %d' % i, clinic))

class Clinic(object):
    
    typeP = "o"
    
    def __init__(self, env, num_machines):
        self.env = env
        self.machine = simpy.Resource(env, num_machines)

    def cure(self, doc):

        k1 = np.random.normal(4,2)
        k2 = np.random.normal(30,8)
        if k1 < 0:
            while True:
                if(k1 > 0):
                    break
                else:
                    k1 = np.random.normal(4,2)
        if k2 < 0:
            while True:
                if(k2 > 0):
                    break
                else:
                    k2 = np.random.normal(30,8)
        k=0      
        if (self.typeP == "PO"):
            k = k1
            
        else:
            k = k2
            
        yield self.env.timeout(k)


def doc(env, name, cw):
    
    k1 = env.now
    print('%s arrives at the doctor at %.2f.' % (name, k1))
    with cw.machine.request() as request:
        yield request
        k2 = env.now
        print('%s enters the doctor at %.2f.' % (name, k2))
        yield env.process(cw.cure(name))
        k3 = env.now
        print('%s leaves the doctor at %.2f.' % (name, k3))
        if(k1 > 5000):
            if(cw.typeP == "PO"):
                timespentOP.append(k3-k2)
                waitingTimeOP.append(k2-k1)
            else:
                timespentIP.append(k3-k2)
                waitingTimeIP.append(k2-k1)


# defining the seed
np.random.seed(1234)  

# creating environment
env = simpy.Environment()
env.process(setup(env, NUM_MACHINES))

env.run(until=SIM_TIME)

tspentArrayOP = np.array(timespentOP)
wtimeArrayOP = np.array(waitingTimeOP)

tspentArrayIP = np.array(timespentIP)
wtimeArrayIP = np.array(waitingTimeIP)

# Utilization of the doctor
utilization = (np.sum(tspentArrayOP)+np.sum(tspentArrayIP))/(2*(SIM_TIME-WARMUP_TIME))

# Histogram for out patients
plt.hist(wtimeArrayOP)
# Histogram for in patients
plt.hist(wtimeArrayIP)

def get_best_distribution(data):
    dist_names = ["norm", "triang", "beta", "gamma", "expon"]
    dist_results = []
    params = {}
    for dist_name in dist_names:
        dist = getattr(st, dist_name)
        param = dist.fit(data)
        params[dist_name] = param
        # Applying the Kolmogorov-Smirnov test
        D, p = st.kstest(data, dist_name, args=param)
        dist_results.append((dist_name, p))

    # select the best fitted distribution
    best_dist, best_p = (max(dist_results, key=lambda item: item[1]))
    # store the name of the best fit and its p value

    print("Best fitting distribution: "+str(best_dist))
    print("Best p value: "+ str(best_p))
    print("Parameters for the best fit: "+ str(params[best_dist]))

# Best distribution for OUT patient
print("For out-patients :")    
get_best_distribution(wtimeArrayOP)
# Best distribution for IN patient
print("For in-patients :")    
get_best_distribution(wtimeArrayIP)
print("Utilization of the doctor: ",utilization)
