from random import randint, random
import math

def calculateDistance(loc1, loc2):
    return math.sqrt(pow(int(loc1[0]) - int(loc2[0]), 2) +  pow(int(loc1[1]) - int(loc2[1]), 2) +  pow(int(loc1[2]) - int(loc2[2]), 2))

def readFile(filename):
    file = open(filename)
    #skip the first line
    file.readline()
    line = file.readline()

    locations = []
    while line:
        line = line[:-1]
        lst = line.split(" ")
        locations.append(lst)
        line = file.readline()
    
    file.close()
    

    return locations

def coolDown(temp):
    return temp * 0.95

def check_repeat(populations, i, j, r):
    for u in range(j+1):
        if populations[i][u] == r:
            return True
    return False

def rand(st, ed):
    #generate random number from st to ed, st is included but ed not
    return randint(st, ed-1)


def select_parent(fitness):
    tot_fit = 0
    best_fit = 0
    for i in range(len(fitness)):
        if fitness[i] >= fitness[best_fit]:
            best_fit = i
        tot_fit += fitness[i]
    
    pop_sz = len(fitness)

    select = [0]*(pop_sz+1)
    select[0] = fitness[0] * 1.0 / tot_fit
    for i in range(pop_sz):
        select[i+1] = select[i] + fitness[i] * 1.0 / tot_fit

    r = random()
    for i in range(pop_sz):
        if select[i] >= r:
            return i
    
    return best_fit


def crossover(populations, fitness, prob, best_fit):
    pop_sz = len(populations)
    city_sz = len(populations[0]) 

    tmp = [[0]*(city_sz) for _ in range(pop_sz)]

    tmp[0] = populations[best_fit]

    for i in range(1, pop_sz):
        
        p1 = select_parent(fitness)
        p2 = select_parent(fitness) 
        
        for k in range(1000):
            if p2 == p1:
               p2 = select_parent(fitness)
            else:
                break
        
        if not p2:
            p2 = 0

        route1 = populations[p1][:-1]
        route2 = populations[p2][:-1]

        used = [0]*(city_sz-1)

        pivot = rand(1, city_sz-1)
        tmp[i][0] = pivot
        tmp[i][city_sz-1] = pivot
        used[pivot] = 1

        index_1 = 0
        index_2 = 0

        for j in range(1, city_sz-1):
            while route1[index_1] != pivot:
                index_1 += 1
                if index_1 == len(route1):
                    index_1 = 0
            while route2[index_2] != pivot:
                index_2 += 1
                if index_2 == len(route2):
                    index_2 = 0
            
            used[pivot] = 1
            
            next_1 = index_1+1 if index_1+1 != len(route1) else 0
            next_2 = index_2+1 if index_2+1 != len(route2) else 0

            while used[route1[next_1]]:
                next_1 += 1
                if next_1 == len(route1):
                    next_1 = 0
            
            while used[route2[next_2]]:
                next_2 += 1
                if next_2 == len(route2):
                    next_2 = 0


            if calculateDistance(locations[route1[next_1]], locations[route1[index_1]]) < calculateDistance(locations[route2[next_2]], locations[route2[index_2]]):
                pivot = route1[next_1]
            else:
                pivot = route2[next_2]

            tmp[i][j] = pivot
            
            index_1 = next_1
            index_2 = next_2
            

    return tmp

def calc_fitness(city):
    s = 0
    for i in range(1, len(city)):
        s += calculateDistance(locations[city[i]], locations[city[i-1]])
    return 100000.0 / s



def initPopulations(pop_size, city_sz):
    populations = [[0]*(city_sz+1) for _ in range(pop_size)]
     
    #initialize population
    for i in range(pop_size):
        populations[i][0] = 0
        populations[i][city_sz] = 0

    for i in range(pop_size):
        for j in range(1, city_sz):
            r = rand(1, city_sz)   #1-n-1
            while check_repeat(populations, i, j, r):
                r = rand(1, city_sz)
            populations[i][j] = r

    return populations

def fitness_calc(populations):
    pop_sz = len(populations)
    city_sz = len(populations[0])   #number of city + 1

    fitness = [0]*pop_sz

    fit_para = 1000000

    best_fit = 0
    for i in range(pop_sz):
        for j in range(1, city_sz):
            fitness[i] += calculateDistance(locations[populations[i][j]], locations[populations[i][j-1]])
        fitness[i] = fit_para * 1.0 / fitness[i]

        if fitness[i] >= fitness[best_fit]:
            best_fit = i

    return fitness, best_fit

def GAWork(weight):
    gen = 1
    gen_iter = 100
    pop_size = 50
    city_sz = len(weight)

    #create population
    populations = initPopulations(pop_size, city_sz)

    fitness, best_fit = fitness_calc(populations)

    temperature = 1000


    while gen < gen_iter:
        populations = crossover(populations, fitness, 0.5, best_fit)
        fitness, best_fit = fitness_calc(populations)
        gen += 1
    
    return populations[best_fit]

def output(route):
    file = open("output.txt", 'w')
    for r in range(len(route)):
        city = locations[route[r]]
        for i in range(len(city)):
            file.write(city[i])
            if i != len(city)-1:
                file.write(' ')
        if r != len(route)-1:
            file.write('\n')
    file.close()

def GA():
    #weight
    n = len(locations)
    w = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            w[i][j] = w[j][i] = calculateDistance(locations[i], locations[j])

    output(GAWork(w))


if __name__ == "__main__":
    #read all locations
    global locations 
    locations = readFile("input.txt")

    GA()
    