#!/usr/bin/env python
# coding: utf-8

# # Total time Function
# 
# this is the Function calculating the total time required for manufactiring and its Assembly for all model

# In[1]:


def totalTime(timeMappings , order):
    timeMan =0
    timeAss =0
    idleTime =0
    timeManStart =[]
    timeAssStart =[]
    for i in order:
        timeManStart.append(timeMan)
        timeMan += int(timeMappings[i]['man'])
        if timeMan>=timeAss:
            currIdle = timeMan - timeAss
            idleTime += currIdle
            timeAssStart.append(timeAss+currIdle)
            timeAss += (currIdle+ int(timeMappings[i]['ass']))
        else:
            timeAssStart.append(timeAss)
            timeAss += timeMappings[i]['ass']
            
    totalTime = 0
    if timeMan>timeAss:
        totalTime = timeMan
    else:
        totalTime = timeAss
    return totalTime,idleTime,timeManStart,timeAssStart


# # Importing files and data preprocessing
# 
# this is the section where we import data from the file and do some preprocessing stuffs

# In[2]:


file = open("input.txt").read().split("\n")
data = {}
for i in file:
    record = i.split(" / ")
    data[int(record[0])]={
            'man' : int(record[1]),
            'ass': int(record[2])
        }
print(data)
keys = data.keys()
model =[]
man =[]
#ass =[]
for i in keys:
    model.append(i)
for i in range(0,len(model)):
    man.append(data[model[i]]['man'])
    #ass.append(data[model[i]]['ass'])


# # Finding the Order of the Manufacturing Using Greedy Programming Techneque

# In[3]:


n = len(model)
for i in range(n):
    for j in range(0, n-i-1):
        if man[j] > man[j+1] :
            model[j], model[j+1] = model[j+1], model[j]
            man[j], man[j+1] = man[j+1], man[j]


import numpy as np

order = np.copy(model)
print(order)


# In[4]:


totalTime,idleTime,manStartTimes,assStartTimes = totalTime(data,order)
with open('output.txt', 'w') as f:
    print("Order of Manufacturung:" +str(order) , file =f)
    print("Total production time for all mobiles is: "+str(totalTime) , file =f)
    print("Idle Time: "+ str(idleTime), file=f)


# In[6]:


# Importing the matplotlb.pyplot 
def Union(lst1, lst2,list3): 
    final_list = lst1 + lst2+list3 
    return final_list 
import matplotlib.pyplot as plt 

fig, gnt = plt.subplots() 

# Setting Y-axis limits 
gnt.set_ylim(0, 15)  
gnt.set_xlim(0, totalTime) 
gnt.set_xlabel('Time') 
gnt.set_ylabel('Assembly Line')  
gnt.set_yticks([5, 10])
gnt.set_xticks(Union(manStartTimes,assStartTimes,[totalTime]))
gnt.set_yticklabels(['Manufacturing', 'Assembly']) 
gnt.grid(True)
alt = True
for i in range(0,len(order)):
    if(alt):
        alt = False
        gnt.broken_barh([(manStartTimes[i], data[order[i]]['man'])], (3, 4), facecolors =('tab:blue'))
        gnt.broken_barh([(assStartTimes[i], data[order[i]]['ass'])], (8, 4),facecolors ='tab:blue')
    else:
        alt = True
        gnt.broken_barh([(manStartTimes[i], data[order[i]]['man'])], (3, 4), facecolors =('tab:orange'))
        gnt.broken_barh([(assStartTimes[i], data[order[i]]['ass'])], (8, 4),facecolors ='tab:orange')
plt.savefig("outputImage.png")
print("\n\nOrder of Manufacturung:" +str(order))
print("Total production time for all mobiles is: "+str(totalTime))
print("Idle Time: "+ str(idleTime))


# # Implementing Genetic Algorithm for Optimisation

# In[7]:


"""
Importing Required Library

"""
import numpy as np
import matplotlib.pyplot as plt
import random


# In[8]:


def fittnessFunction(timeMappings , order):
    timeMan =0
    timeAss =0
    idleTime =0
    for i in order:
        timeMan += int(timeMappings[i]['man'])
        if timeMan>=timeAss:
            currIdle = timeMan - timeAss
            idleTime += currIdle
            timeAss += (currIdle+ int(timeMappings[i]['ass']))
        else:
            timeAss += timeMappings[i]['ass']
            
    totalTime = 0
    if timeMan>timeAss:
        totalTime = timeMan
    else:
        totalTime = timeAss
    return totalTime,idleTime


# In[9]:


"""
Population Initialization

"""
population =[]
for i in  range(10):
    order =np.random.choice(range(1,len(model)+1), len(model), replace=False)
    time,idle =fittnessFunction(data,order)
    indevidual = {'chromosomes':order,'fittness':time**2,'time':time}
    population.append(indevidual)


# In[10]:


"""
Sorting the population aith fittness

"""
def sortPopulation(population):
    n = 10
    for i in range(n):
        for j in range(0, n-i-1):
            if population[j]['fittness'] > population[j+1]['fittness'] :
                population[j], population[j+1] = population[j+1], population[j]
    return population


# In[11]:


population = sortPopulation(population)
for i in range(10):
    print(population[i])


# In[12]:


"""
Natural Selection
"""
def get_probability_list():
    total_fit =0
    for i in population:
        total_fit +=i['fittness']
    relative_fitness = [f['fittness']/total_fit for f in population]
    probabilities = [1-sum(relative_fitness[:i+1]) 
                     for i in range(len(relative_fitness))]
    return probabilities
def roulette_wheel_pop(population, probabilities, number):
    chosen = []
    for n in range(number):
        r = random.random()
        while True:
            index = random.randrange(10)
            if r <= probabilities[index]:
                chosen.append(population[index]['chromosomes'])
                break
    return chosen


# In[ ]:





# In[13]:


"""
Crossover

"""
def pointCrossover(selection):
    newIndevidual1 =[]
    newIndevidual2 =[]
    ind1 = np.copy(selection[0])
    ind2 = np.copy(selection[1])
    point = random.randint(2,len(model)-2)
    print(point)
    arrayAfterPoint = np.copy(ind1[point :])
    fullArray = np.copy(ind2)
    delete =[]
    for i in range(len(fullArray)):
        for j in arrayAfterPoint:
            if fullArray[i] == j:
                delete.append(i)
    resArray = np.delete(fullArray,delete ,axis =0)
    #print(arrayAfterPoint)
    #print(resArray)
    newIndevidual1 = np.hstack((np.copy(resArray),arrayAfterPoint))
    
    arrayBeforePoint = np.copy(ind2[: point])
    fullArray = np.copy(ind1)
    delete =[]
    for i in range(len(fullArray)):
        for j in arrayBeforePoint:
            if fullArray[i] == j:
                delete.append(i)
    resArray = np.delete(fullArray,delete ,axis =0)
    newIndevidual2 = np.hstack((arrayBeforePoint,np.copy(resArray)))
    return newIndevidual1,newIndevidual2


# In[14]:


"""
Mutation

"""

def pointMutation(indevidual,prob):
    decisonVariable =random.randrange(101)
    if decisonVariable<=prob:
        point1 =random.randint(0,len(model)-1)
        point2 = random.randint(0,len(model)-1)
        temp1 = indevidual[point1]
        temp2 = indevidual[point2]
        indevidual[point1] =temp2
        indevidual[point2] =temp1
    return indevidual


# In[15]:



for i in range(1000):
    print("generation"+str(i))
    #print(population[0])
    probablities = get_probability_list()
    selection = roulette_wheel_pop(population, probablities, 2)
    ind1,ind2 =pointCrossover(selection)
    mut1 = pointMutation(ind1,50)
    mut2 = pointMutation(ind2,50)
    time,idle =fittnessFunction(data,mut1)
    indevidual_1 = {'chromosomes':mut1,'fittness':time**2,'idle':time}
    time,idle =fittnessFunction(data,mut2)
    indevidual_2 = {'chromosomes':mut2,'fittness':time**2,'idle':time}
    print(indevidual_1)
    print(indevidual_2)
    population[8] = indevidual_1
    population[9]= indevidual_2
    population = sortPopulation(population)


# In[15]:


def totalTime1(timeMappings , order):
    timeMan =0
    timeAss =0
    idleTime =0
    timeManStart =[]
    timeAssStart =[]
    for i in order:
        timeManStart.append(timeMan)
        timeMan += int(timeMappings[i]['man'])
        if timeMan>=timeAss:
            currIdle = timeMan - timeAss
            idleTime += currIdle
            timeAssStart.append(timeAss+currIdle)
            timeAss += (currIdle+ int(timeMappings[i]['ass']))
        else:
            timeAssStart.append(timeAss)
            timeAss += timeMappings[i]['ass']
            
    totalTime = 0
    if timeMan>timeAss:
        totalTime = timeMan
    else:
        totalTime = timeAss
    return totalTime,idleTime,timeManStart,timeAssStart
order1 = np.copy(population[0]['chromosomes'])
totalTime1,idleTime1,manStartTimes1,assStartTimes1 = totalTime1(data,order1)


# In[16]:


def Union(lst1, lst2,list3): 
    final_list = lst1 + lst2+list3 
    return final_list 
import matplotlib.pyplot as plt 

fig, gnt = plt.subplots() 

# Setting Y-axis limits 
gnt.set_ylim(0, 15)  
gnt.set_xlim(0, totalTime) 
gnt.set_xlabel('Time') 
gnt.set_ylabel('Assembly Line')  
gnt.set_yticks([5, 10])
gnt.set_xticks(Union(manStartTimes,assStartTimes,[totalTime]))
gnt.set_yticklabels(['Manufacturing', 'Assembly']) 
gnt.grid(True)
alt = True
for i in range(0,len(order1)):
    if(alt):
        alt = False
        gnt.broken_barh([(manStartTimes[i], data[order1[i]]['man'])], (3, 4), facecolors =('tab:blue'))
        gnt.broken_barh([(assStartTimes[i], data[order1[i]]['ass'])], (8, 4),facecolors ='tab:blue')
    else:
        alt = True
        gnt.broken_barh([(manStartTimes[i], data[order1[i]]['man'])], (3, 4), facecolors =('tab:orange'))
        gnt.broken_barh([(assStartTimes[i], data[order1[i]]['ass'])], (8, 4),facecolors ='tab:orange')
plt.savefig("outputImage.png")
print("\n\nOrder of Manufacturung:" +str(order1))
print("Total production time for all mobiles is: "+str(totalTime1))
print("Idle Time: "+ str(idleTime1))


# In[488]:





# In[ ]:




