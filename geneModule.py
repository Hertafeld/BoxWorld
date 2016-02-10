#Generates and breeds cubes
import CubeGrabbingWorld, CubeFightingWorld
import random
import operator
import pickle
import pylab

class Cube:

    def __init__(self, strat):
        self.dna = strat
        self.fitness = 0
        self.replay = []
    def getFitness(self):
        return self.fitness
    def simulate(self, time = 1000):
        result = CubeGrabbingWorld.simulateIndividual(self.dna, False, '', time = time)
        self.fitness = result[0]
        return self.fitness
    def simulateAndRecord(self, f= '', time = 1000):
        result = CubeGrabbingWorld.simulateIndividual(self.dna, display = False, recordThis = True, filename = f, time = time)
        self.fitness = result[0]
        self.replay = result[1]
        return self.fitness
    def play(self):
        CubeGrabbingWorld.showReplay(self.replay)
    def saveReplay(self, filename):
        filename = filename + '.replay'
        replayFile = open(filename, 'wb')
        pickle.dump(self.replay, replayFile)
        replayFile.close()
    def saveDna(self, filename):
        filename = filename + '.dna'
        dnaFile = open(filename, 'wb')
        pickle.dump(self.dna, dnaFile)
        dnaFile.close()
    def loadDna(self, filename):
        filename = filename + '.dna'
        dnaFile = open(filename, 'rb')
        self.dna = pickle.load(dnaFile)
        dnaFile.close()
    def mutateDna(self, rate):
        mutate(rate, self.dna)
        
def saveReplay2(replay, filename):
        filename = filename + '.replay2'
        replayFile = open(filename, 'wb')
        pickle.dump(replay, replayFile)
        replayFile.close()
        
def mutate(rate, dna):
    for i in range(CubeGrabbingWorld.g1Scale):
        for j in range(CubeGrabbingWorld.g2Scale):
            for k in range(CubeGrabbingWorld.g3Scale):
                if rate > random.random():
                    dna[i][j][k] = random.randint(1, CubeGrabbingWorld.actions)
def mutate2(rate, dna):
    for i in range(CubeFightingWorld.gScale[0]):
        for j in range(CubeFightingWorld.gScale[1]):
            for k in range(CubeFightingWorld.gScale[2]):
                for l in range(CubeFightingWorld.gScale[3]):
                    for m in range(CubeFightingWorld.gScale[4]):
                        if rate > random.random():
                            dna[i][j][k][l][m] = random.randint(1, CubeFightingWorld.actions)
def createChild(parent1, parent2, crossoverPoints, mutationRate):
    spots = []
    dnaFromParent1 = True
    newDna = []
    count = 0
    for i in range(crossoverPoints):
        spots.append(random.randint(0, CubeGrabbingWorld.g1Scale * CubeGrabbingWorld.g2Scale*CubeGrabbingWorld.g3Scale))
    for i in range(CubeGrabbingWorld.g1Scale):
        newDna.append([])
        for j in range(CubeGrabbingWorld.g2Scale):
            newDna[i].append([])
            for k in range(CubeGrabbingWorld.g3Scale):
                if count in spots:
                    dnaFromParent1 = not dnaFromParent1
                if dnaFromParent1:
                    newDna[i][j].append(parent1.dna[i][j][k])
                else:
                    newDna[i][j].append(parent2.dna[i][j][k])

                count = count + 1
    mutate(mutationRate, newDna)
    return Cube(newDna)

def createChild2(parent1, parent2, crossoverPoints, mutationRate):
    spots = []
    dnaFromParent1 = True
    newDna = []
    count = 0
    for i in range(crossoverPoints):
        spots.append(random.randint(0, reduce(lambda x,y:x*y,CubeFightingWorld.gScale)))
    for i in range(CubeFightingWorld.gScale[0]):
        newDna.append([])
        for j in range(CubeFightingWorld.gScale[1]):
            newDna[i].append([])
            for k in range(CubeFightingWorld.gScale[2]):
                newDna[i][j].append([])
                for l in range(CubeFightingWorld.gScale[3]):
                    newDna[i][j][k].append([])
                    for m in range(CubeFightingWorld.gScale[4]):
                        #print newDna
                        if count in spots:
                            dnaFromParent1 = not dnaFromParent1
                        if dnaFromParent1:
                            newDna[i][j][k][l].append(parent1.dna[i][j][k][l][m])
                        else:
                            newDna[i][j][k][l].append(parent2.dna[i][j][k][l][m])
                        count = count + 1
    mutate2(mutationRate, newDna)
    return Cube(newDna)

def getRandomDNA():
    strat = [[[random.randint(1, 3) for i in range(10)] for j in range(10)] for k in range(10)]
    return strat

def getRandomDNA2():
    strat = [[[[[random.randint(1, 3) for i in range(10)] for j in range(10)] for k in range(10)] for l in range(10)] for m in range(10)]
    return strat

def playReplay(filename):
    CubeGrabbingWorld.showReplay(filename)
    
def playReplay2(filename):
    CubeFightingWorld.showReplay(filename)

def sortPopulation(population):
    population = sorted(population, key=operator.attrgetter('fitness'))
    population.reverse()
    return population
    
def selectFromFitnessWheel(population, sum):
    value = random.randint(1, sum)
    sum = 0
    for i in range(len(population)):
        sum = sum + population[i].fitness
        if value <= sum:
            return population[i]
        
        
def getChildren(population, crossoverPoints, mutationRate):
    newPop = []
    sortPopulation(population)
    sum = 0
    for i in range(len(population)):
        sum = sum + population[i].fitness
    
    for i in range(len(population) - 1):
        p1 = selectFromFitnessWheel(population, sum)
        p2 = selectFromFitnessWheel(population, sum)
        newPop.append(createChild(p1, p2, crossoverPoints, mutationRate))
    population[0].fitness = 0
    newPop.append(population[0])
    return newPop
def getChildren2(population, crossoverPoints, mutationRate):
    newPop = []
    sortPopulation(population)
    sum = 0
    for i in range(len(population)):
        sum = sum + population[i].fitness
    
    for i in range(len(population) - 1):
        p1 = selectFromFitnessWheel(population, sum)
        p2 = selectFromFitnessWheel(population, sum)
        newPop.append(createChild2(p1, p2, crossoverPoints, mutationRate))
    population[0].fitness = 0
    newPop.append(population[0])
    return newPop

def getNewPopulation(size):
    pop = []
    for i in range(size):
        pop.append(Cube(getRandomDNA()))
    return pop
def getNewPopulation2(size):
    pop = []
    for i in range(size):
        pop.append(Cube(getRandomDNA2()))
    return pop
        
def simulatePopulation(pop, time = 1000):
    for agent in pop:
        agent.simulateAndRecord("", time)

def recordPopulation(pop, filePrefix, gen, doPrint = True, doRecord = True, gb = 0):
    sum = 0
    for i in range(len(pop)):
        sum = sum + pop[i].fitness
    avg = float(sum)/(len(pop))
    if doPrint:
        print("Generation " + str(gen) + ":")
        print("Best has fitness of " + str(pop[0].fitness))
        print("Average fitness is " + str(avg))
        print("Best so far is " + str(gb))
    if doRecord:
        pop[0].saveReplay(filePrefix + "_gen_" + str(gen))
        pop[0].saveDna(filePrefix + ' gen ' + str(gen))

    return avg

def generationDetailPrintout(pop):
    for i in range(len(pop)):
        print("Agent " + str(i) + ": " + str(pop[i].fitness))
        
def savePlot(history, filePrefix):
    for i in range(2):
        pylab.plot(range(len(history)), extractNth(history, i))
    pylab.xlabel('Generation')
    pylab.ylabel('Fitness')
    pylab.title(filePrefix + ' Fitness Plot')
    pylab.savefig(filePrefix + '_plot.png')



# def savePlot(filePrefix):
#     histFile = open(filePrefix + '.history', 'rb')
#     history = pickle.load(histFile)
#     for i in range(2):
#         pylab.plot(range(len(history)), extractNth(history, i))
#     pylab.xlabel('Generation')
#     pylab.ylabel('Fitness')
#     pylab.title(filePrefix + ' Fitness Plot')
#     pylab.savefig(filePrefix + '_plot.png')

def savePlot2(history, filePrefix):
    pylab.plot(range(len(history)), extractNth(history, 0), 'b')
    pylab.plot(range(len(history)), extractNth(history, 1), 'b')
    pylab.plot(range(len(history)), extractNth(history, 2), 'r')
    pylab.plot(range(len(history)), extractNth(history, 3), 'r')
    pylab.xlabel('Generation')
    pylab.ylabel('Fitness')
    pylab.title(filePrefix + ' Fitness Plot')
    pylab.savefig(filePrefix + '_plot.png')
    
def savePlot2(filePrefix):
    histFile = open(filePrefix + '.history2', 'rb')
    history = pickle.load(histFile)
    pylab.plot(range(len(history)), extractNth(history, 0), 'b')
    pylab.plot(range(len(history)), extractNth(history, 1), 'b')
    pylab.plot(range(len(history)), extractNth(history, 2), 'r')
    pylab.plot(range(len(history)), extractNth(history, 3), 'r')
    pylab.xlabel('Generation')
    pylab.ylabel('Fitness')
    pylab.title(filePrefix + ' Fitness Plot')
    pylab.savefig(filePrefix + '_plot.png')

def runSimulation(generations, popSize, crossoverPoints, mutationRate, filePrefix, printEvery = 1, recordEvery = 1, time = 1000):
    history = []
    globalBest = 0
    globalBestBot = 0
    pop = getNewPopulation(popSize)
    for i in range(generations):
        simulatePopulation(pop, time)
        pop = sortPopulation(pop)
        best = pop[0].fitness
        worst = pop[len(pop) - 1].fitness        
        if i % printEvery == 0:
            p = True
            #generationDetailPrintout(pop)
        else:
            p = False
        if i % recordEvery == 0:
            r = True
        else:
            r= False
        if best > globalBest:
             globalBest = best
             globalBestBot = pop[0]
             #r=True
             #p=True
        avg = recordPopulation(pop, filePrefix, i, p, r, globalBest)
        history.append((best, avg))
        pop = getChildren(pop, crossoverPoints, mutationRate)
        if p:
            savePlot(history, filePrefix)
            globalBestBot.saveDna(filePrefix + 'Best')
            globalBestBot.saveReplay(filePrefix + 'Best')
    simulatePopulation(pop, time)
    sortPopulation(pop)
    recordPopulation(pop, filePrefix, i, True, True)
    globalBestBot.saveDna(filePrefix + 'Best')
    globalBestBot.saveReplay(filePrefix + 'Best')
    savePlot(history, filePrefix)
    return globalBestBot
    

def extractNth(seq, index):
    return map(lambda x : x[index], seq)

def getAverage(bot, trials, t = 1000):
    sum = 0
    for i in range(trials):
        bot.simulate(t)
        sum = sum + bot.fitness
    return float(sum) / trials
        
def ffSimple(a, b):
    return (a, b)

def ffRed(a, b):
    return(b, b)
    
def ffTeam(a, b):
	return(a+b, a+b)

def compete(p1, p2, display = False, recordThis = False, filename = '', time = 1000, fitnessFunction = ffSimple):
    result = CubeFightingWorld.simulateCompetition(p1.dna, p2.dna, display, recordThis, filename, time)
    fits = fitnessFunction(result[0], result[1])
    p1.fitness = p1.fitness + fits[0]
    p2.fitness = p2.fitness + fits[1]
    return (fits[0], fits[1], result[2])
        

def getHistoryPoint(pop1, pop2):
    sum1 = 0
    sum2 = 0
    for bot in pop1:
        sum1 = sum1 + bot.fitness
    for bot in pop2:
        sum2 = sum2 + bot.fitness
    return (float(pop1[0].fitness)/len(pop2), float(sum1)/(len(pop2)*len(pop1)), float(pop2[0].fitness)/len(pop1), float(sum2)/(len(pop1)*len(pop2)))
    
def runCompetition(generations, popSize1, popSize2, crossoverPoints, mutationRate, filePrefix, printEvery = 10, recordEvery = 100, time = 1000, fitnessFunction = ffSimple):
    history = []
    globalBest = 0
    globalBestReplay = 0
    printThis = False
    pop1 = getNewPopulation2(popSize1)
    pop2 = getNewPopulation2(popSize2)
    for i in range(generations):
        printThis = i % printEvery == 0
        for j in range(popSize1):
            for k in range(popSize2):
                temp = compete(pop1[j], pop2[k], False, True, '', time, fitnessFunction)
                if temp[0] > globalBest or temp[1] > globalBest:
                    saveReplay2(temp[2], filePrefix + '_gen_' + str(i))
                    globalBest = max(temp[0], temp[1])
                    globalBestReplay = temp[2]
                    printThis = True
        pop1 = sortPopulation(pop1)
        pop2 = sortPopulation(pop2)
        point = getHistoryPoint(pop1, pop2)
        history.append(point)
        if printThis:
            print("Generation " + str(i))
            print("Best blue: " + str(point[0])) 
            print("Average blue: " + str(point[1])) 
            print("Best red: " + str(point[2])) 
            print("Average red: " + str(point[3]))
            generationDetailPrintout(pop1)
            generationDetailPrintout(pop2)
        pop1 = getChildren2(pop1, crossoverPoints, mutationRate)
        pop2 = getChildren2(pop2, crossoverPoints, mutationRate)
    saveReplay2(globalBestReplay, filePrefix + 'Best')
        
    
def main():
    bot = runSimulation(200, 100, 3, .01, 'soloTest', 10, 100)
    playReplay('soloTestBest')
    #runCompetition(100, 10, 10, 3, .04, 'teamworkTest', 1, 1, time = 750, fitnessFunction = ffRed)
    #playReplay2('teamworkTestBest')    
    
main()
