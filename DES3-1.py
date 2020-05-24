# Created by - Utsav

# importing the required libraries
import random
import simpy
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

WARMUP_TIME = 5000
RANDOM_SEED = 1234
NUM_MACHINES = 1         
SIM_TIME = 40000     

timespent = []
waitingTime = []

def doc(env, name, cw):

    k1 = env.now
    print('%s arrives at the doctor at %.2f.' % (name, k1))
    with cw.machine.request() as request:
        yield request
        k2 = env.now
        print('%s enters the doctor at %.2f.' % (name, k2))
        yield env.process(cw.wash(name))
        k3 = env.now
        print('%s leaves the doctor at %.2f.' % (name, k3))
        if(k1 > 5000):
            timespent.append(k3-k2)
            waitingTime.append(k2-k1)


class Clinic(object):

    def __init__(self, env, num_machines):
        self.env = env
        self.machine = simpy.Resource(env, num_machines)

    def wash(self, doc):
        k = np.random.normal(4,2)
        if k < 0:
            while True:
                if(k > 0):
                    break
                else:
                    k = np.random.normal(4,2)
        yield self.env.timeout(k)
        


def setup(env, num_machines):
    clinic = Clinic(env, num_machines)

    for i in range(1):
        env.process(doc(env, 'Patient %d' % i, clinic))

    while True:
        
        yield env.timeout(np.random.exponential(5))
        i += 1
        env.process(doc(env, 'Patient %d' % i, clinic))

np.random.seed(1234)  


env = simpy.Environment()
env.process(setup(env, NUM_MACHINES))

# Execute!
env.run(until=SIM_TIME)

tspentArray = np.array(timespent)
wtimeArray = np.array(waitingTime)

utilization = np.sum(tspentArray)/(SIM_TIME-WARMUP_TIME)

plt.hist(wtimeArray)
plt.show()

def best_distribution(data):
    dist_names = ["norm", "triang", "beta", "gamma", "expon"]
    dist_results = []
    params = {}
    for dist_name in dist_names:
        dist = getattr(st, dist_name)
        param = dist.fit(data)

        params[dist_name] = param
        # Applying the Kolmogorov-Smirnov test
        D, p = st.kstest(data, dist_name, args=param)
        # print("p value for "+dist_name+" = "+str(p))
        dist_results.append((dist_name, p))

    # select the best fitted distribution
    best_dist, best_p = (max(dist_results, key=lambda item: item[1]))
    # store the name of the best fit and its p value

    print("Best fit distribution: "+str(best_dist))
    print("Best p value: "+ str(best_p))
    print("Parameters (Best fit): "+ str(params[best_dist]))

best_distribution(wtimeArray)
print("Calculated Utilization of the doctor:", utilization)