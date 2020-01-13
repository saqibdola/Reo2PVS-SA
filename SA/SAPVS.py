# SA code for proofs searching and Optimization in three PVS theories.

import random
import statistics
import time
import gc
import math

import psutil
#import numpy

def acceptance_probability(temperature):
    return math.exp(temperature/(1+temperature))

def Fitness(guess):
    fitness = 0
    for i in range(len(guess)):
        if guess[i] == proof[i]:
            fitness+=1
    return fitness

def Results(guess, timings):
    timeD = time.time() - sTime
    fit = Fitness(guess)
#    print(guess, fit, timeD)
    timings.append(timeD)

def get_neighbor(parent):
    index = random.randrange(0, len(parent))
    childChars = list(parent)
    newChar, alternate = random.sample(gSet, 2)
    childChars[index] = alternate if newChar == childChars[index] else newChar
    return (childChars)


def anneal(parent, temperature, min_temp, alpha):
    geneTime = time.time()
    cc=0
    arcount=0

    best_fitness = Fitness(parent)

    if best_fitness >= optimalFitness:
        print("AR Count: ", arcount)
        return cc, parent
    T = temperature
    T_min = min_temp
    while T > T_min:
        cc = cc+1
        new_solution = get_neighbor(parent)
        new_fitness = Fitness(new_solution)
        if new_fitness == optimalFitness:
            print("AR Count: ", arcount)

            return cc, new_solution
        if new_fitness > best_fitness:
            #bestGuess = new_solution #BCBCBCBC
            parent = new_solution #BCBCBCBC
            best_fitness = new_fitness
            print(time.time() - geneTime, end=',')
            geneTime = time.time()

        else:
            ar = acceptance_probability(T)
            if ar > random.uniform(3.218,3.723): #bad one
                parent = new_solution
                best_fitness = new_fitness
                arcount = arcount + 1

        T = T*alpha
    print("AR Count: ", arcount)
    return cc, parent
random.seed()

timee = time.process_time()
fits = []
lastt = []
count=0
totalCount=0
ite = []
totalstartTime = time.time()
with open("PVSPOP.txt", 'r') as f:
    p = f.read()
    gSet = p.split()
  #  print(gSet)

with open("lp.txt", 'r') as f:
    for line in f: #all the lines in f (proofs.txt)
        timee += timee
        timings = []
        for i in range(1):
            startTime = time.time()
            proof = line.split() #tokenize each word within a line
            length = len(proof)
            #length of that word in line
            optimalFitness = len(proof)
            g1 = []

            while len(g1) < len(proof):
                sSize = min(length - len(g1), len(gSet))
                g1.extend(random.sample(gSet, sSize))
                #g2.extend(random.sample(gSet, sSize))
                randSample = list(g1)
                randSampleFit= Fitness(randSample)
            T_max = 10000
            T_min = 0.0002
            alpha = 0.9954
            count=0
            count, randSample=anneal(randSample, T_max, T_min, alpha)
            totalCount=totalCount+count
            print (count, end=',')

            print(time.time() - startTime)

print("Total Time:", time.time() - totalstartTime)
print("Total Count", totalCount)
mem = psutil.virtual_memory()  # .total / (1024.0 ** 2)
print("Memory Used in Mb:", mem.used >> 20)
