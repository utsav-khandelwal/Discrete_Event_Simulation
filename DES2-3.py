import simpy
import random

env = simpy.Environment()		# Specifying the environment
random.seed(1234)		# Defining the seed value

def car(env):
	while True:
		print('Start parking at %d' % env.now)		# Printing each time at which a car parks
		parking_duration = random.normal(20,1)		# Car's parking time chosen at random from given normal distribution
		yield env.timeout(parking_duration)

		print('Start driving at %d' % env.now)		# Printing each time when a the car is driven
		trip_duration = random.exponential(30)		# Car's trip duration time chosen at random from given exponential distribution
		yield env.timeout(trip_duration)


env.process(car(env))

env.run(until=1000)			# Simulate process until 1000 units have elapsed