#Simulates a given individual and saves his replay

from graphics import *
import random
import Tkinter
import pickle
import time
#dna properties
g1Scale = 5
g2Scale = 5
g3Scale = 5
actions = 3

#global properties
playSpeed = .03
gravity = 1
jumpV = 10
draw = True
speed = 3
playerSize = 20
treatSize = 10
treatSpeed = 5
floorY = 180
xStart = 90

#global variables
tx = 0
treatCount1 = 0
ty = 0
x1 = 0
y1= 0
v1 = 0


#drawing stuff
win = 0
p1 = Rectangle(Point(xStart, floorY), Point(x1+playerSize, y1+playerSize))
treat = Rectangle(Point(tx, ty), Point(tx + treatSize, ty + treatSize))
treat.setFill('yellow')
p1.setFill('blue')



#Main method
def main():
    for i in range(100):
        strat = initializeStrat()
        filename = 'test' + str(i)
        simulateIndividual(strat, True, filename)
    print("Done")
 


#Simulates an individual    
def simulateIndividual(strategy, display = False, recordThis = False, filename = '', time = 1000):
    if recordThis:
        replay = []
    initVars()
    if display:
        initDraw()
    for i in range(time):
        act(getStrat(strategy), display)
        if recordThis:
            replay.append((x1, y1, tx, ty))
    if recordThis:
        result = (treatCount1, replay)
        if filename != '':
            filename = filename + '.replay'
            replayFile = open(filename, 'wb')
            pickle.dump(replay, replayfile)
            replayFile.close()
    else:
        result = (treatCount1, [])
    if display:
        win.close()
    
    return result

#Initialization of global variables and drawing structures
def initVars():
    global x1, y1, v1, treatCount1, tx, ty
    tx = random.randint(0, 190)
    treatCount1 = 0
    ty = 0
    x1 = xStart
    y1=floorY
    v1 = 0
    
def initDraw():
    win = GraphWin()
    p1 = Rectangle(Point(xStart, floorY), Point(x1+playerSize, y1+playerSize))
    treat = Rectangle(Point(tx, ty), Point(tx + treatSize, ty + treatSize))
    treat.setFill('yellow')
    p1.setFill('blue')

    p1.draw(win)
    treat.draw(win)

#Helper methods for simulation
def act(action, display):        
    global x1
    global p1
    global p2
    global v1
    global y1
    tempx = x1
    tempy = y1
    
    #Perform action
    if action == 1:
        x1 = x1+speed
    elif action == 2:
        x1 = x1-speed
    elif action == 3 and v1 == -jumpV:
        v1 = jumpV

    #Handle jumping
    if v1 != -jumpV:
        v1 = v1 - gravity
    y1 = y1 - v1
    if y1 > floorY:
        y1 = floorY
    #Handle wrapping
    x1 = x1 % 200
    
    manageTreat(display)
    
    #draw character
    if display:
        p1.move(x1-tempx, y1-tempy)
 

def initializeStrat():
    strat = [[[random.randint(1, actions) for i in range(g3Scale)] for j in range(g2Scale)] for k in range(g1Scale)]
    return strat

def scaleTen(min, max, val):
    return int(((val-min)*10)/(max-min))

def scaleX(scale, min, max, val):
    return int(((val-min)*scale)/(max-min))

def getStrat(strat):
    var1 = scaleX(g1Scale, 0, 200, (x1-tx)%200)
    var2 = scaleX(g2Scale, 0, 180, (y1-ty)%180)
    var3 = scaleX(g3Scale, -jumpV, jumpV, v1)
    return strat[var1][var2][var3]

   
def manageTreat(display):
    global tx
    global ty
    tempx = tx
    tempy = ty
    global treatCount1
    ty = ty+treatSpeed
    if ty >= 200:
        ty = 0
        tx = random.randint(0, 190)
    if intersectsTreat():
        ty = 0
        tx = random.randint(0, 190)
        treatCount1 = treatCount1 + 1
        #print("Got it!")
    if display:
        treat.move(tx-tempx, ty-tempy)
    
def intersectsTreat():
    if x1 > tx + treatSize or tx > x1 + playerSize:
        return False
    if y1 > ty + treatSize or ty > y1 + playerSize:
        return False
    return True

#Shows a replay - takes either filename or tuple list
def showReplay(filename):
    if type(filename) is str:
        filename = filename + '.replay'
        fileReplay = open(filename, 'rb')
        replay = pickle.load(fileReplay)
        fileReplay.close()
    else:
        replay = filename
    firstFrame = replay[0]
    winReplay = GraphWin('Replay Window')
    winReplay.autoflush = False
    x1Replay = firstFrame[0]
    y1Replay = firstFrame[1]
    txReplay = firstFrame[2]
    tyReplay = firstFrame[3]
    treatReplay = Rectangle(Point(txReplay, tyReplay), Point(txReplay + treatSize, tyReplay + treatSize))
    treatReplay.setFill('yellow')
    p1Replay = Rectangle(Point(x1Replay,y1Replay), Point(x1Replay+playerSize, y1Replay+playerSize))
    p1Replay.setFill('blue')
    p1Replay.draw(winReplay)
    
    leftEye= Circle(Point(x1Replay + .25 * playerSize, y1Replay + .4*playerSize), .25*playerSize)
    leftEye.setFill('white')
    leftEye.setOutline('black')
    leftEye.setWidth(0)
    leftEye.draw(winReplay)
    
    rightEye= Circle(Point(x1Replay + .75 * playerSize, y1Replay + .4*playerSize), .25*playerSize)
    rightEye.setFill('white')
    rightEye.setOutline('black')
    rightEye.setWidth(0)
    rightEye.draw(winReplay)

    leftEyeP= Circle(Point(x1Replay + .25 * playerSize, y1Replay + .4*playerSize), .1*playerSize)
    leftEyeP.setFill('black')
    leftEyeP.setWidth(0)
    leftEyeP.draw(winReplay)

    rightEyeP= Circle(Point(x1Replay + .75 * playerSize, y1Replay + .4*playerSize), .1*playerSize)
    rightEyeP.setFill('black')
    rightEyeP.setWidth(0)
    rightEyeP.draw(winReplay)

    treatReplay.draw(winReplay)
    print(len(replay))
    for i in range(len(replay) - 1):
        frame = replay[i+1]
        leftEye.move(-x1Replay + frame[0], -y1Replay + frame[1])
        rightEye.move(-x1Replay + frame[0], -y1Replay + frame[1])
        leftEyeP.move(-x1Replay + frame[0], -y1Replay + frame[1])
        rightEyeP.move(-x1Replay + frame[0], -y1Replay + frame[1])
        p1Replay.move(-x1Replay + frame[0], -y1Replay + frame[1])
        treatReplay.move(-txReplay + frame[2], -tyReplay + frame[3])
        winReplay.flush()
        time.sleep(playSpeed)
        x1Replay = frame[0]
        y1Replay = frame[1]
        txReplay = frame[2]
        tyReplay = frame[3]
        if winReplay.checkMouse() != None:
            break;
    winReplay.close()

    
#main()
