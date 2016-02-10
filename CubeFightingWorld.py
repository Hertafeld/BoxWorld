#Simulates a given individual and saves his replay

from graphics import *
import random
import Tkinter
import pickle
import time


#dna properties
actions = 3
gScale = (5, 5, 5, 5, 5)
testX = 10
#global properties
playSpeed = .03
gravity = 1
jumpV = 10
draw = True
jumpHeight = 20
speed = 3
playerSize = 20
treatSize = 10
treatSpeed = 2
floorY = 180
xStart1 = 90
xStart2 = 170

#global variables
tx = 0
treatCount1 = 0
treatCount2 = 0
ty = 0
x1 = 0
y1= 0
v1 = 0
x2 = 0
y2 = 0
v2 = 0

#drawing stuff
win = 0
p1 = Rectangle(Point(x1, floorY), Point(x1+playerSize, floorY+playerSize))
p2 = Rectangle(Point(x2, floorY), Point(x2+playerSize, floorY+playerSize))
treat = Rectangle(Point(tx, ty), Point(tx + treatSize, ty + treatSize))
treat.setFill('yellow')
p1.setFill('blue')
p2.setFill('red')



#Main method
def main():
    strat1 = initializeStrat()
    strat2 = initializeStrat()
    simulateCompetition(strat1, strat2, display = True, filename = 'multiplayerTest')
    print("Done")
 


#Simulates an individual    
def simulateCompetition(strategy1, strategy2, display = False, recordThis = False, filename = '', time = 1000):
    if recordThis:
        replay = []
    initVars()
    if display:
        initDraw()
    for i in range(time):
        act(getStratP1(strategy1), getStratP2(strategy2), display)
        if recordThis:
            replay.append((x1, y1, x2, y2, tx, ty))
    if recordThis:
        result = (treatCount1, treatCount2, replay)
        if filename != '':
            filename = filename + '.replay2'
            replayFile = open(filename, 'wb')
            pickle.dump(replay, replayFile)
            replayFile.close()
    else:
        result = (treatCount1, treatCount2, [])
    if display:
        global win
        win.close()
    
    return result

#Initialization of global variables and drawing structures
def initVars():
    global x1, y1, v1, treatCount1, tx, ty, x2,y2, treatCount2
    tx = random.randint(0, 190)
    treatCount1 = 0
    ty = 0
    x1 = xStart1
    y1=floorY
    v1 = 0
    x2 = xStart2
    y2 = floorY
    v2 = 0
    treatCount2 = 0
    
def initDraw():
    global win, p1, p2, treat
    win = GraphWin()
    win.autoflush = False
    p1 = Rectangle(Point(x1, floorY), Point(x1+playerSize, y1+playerSize))
    p2 = Rectangle(Point(x2, floorY), Point(x2+playerSize, y2+playerSize))
    treat = Rectangle(Point(tx, ty), Point(tx + treatSize, ty + treatSize))
    treat.setFill('yellow')
    p1.setFill('blue')
    p2.setFill('red')
    p1.draw(win)
    p2.draw(win)
    treat.draw(win)

#Helper methods for simulation
def act(action1, action2, display):        
    global x1
    global p1
    global p2
    global v1
    global y1
    global x2
    global y2
    global v2
    tempx1 = x1
    tempy1 = y1
    tempx2 = x2
    tempy2 = y2
    #Perform action
    if action1 == 1:
        x1 = x1+speed
    elif action1 == 2:
        x1 = x1-speed
    elif action1 == 3 and v1 == -jumpV:
        v1 = jumpV
        
    if action2 == 1:
        x2 = x2+speed
    elif action2 == 2:
        x2 = x2-speed
    elif action2 == 3 and v2 == -jumpV:
        v2 = jumpV
    
    #Handle jumping
    if v1 != -jumpV:
        v1 = v1 - gravity
    y1 = y1 - v1
    if y1 > floorY:
        y1 = floorY

    if v2 != -jumpV:
        v2 = v2 - gravity
    y2 = y2 - v2
    if y2 > floorY:
        y2 = floorY

    #check for pins and pushes
    xOver = xOverlap()
    if xOver != 0:
        if tempy1 <= tempy2 - playerSize:
            v2 = v1
            x2 = tempx2
            y2 = tempy2 - v2
            if y2 > floorY:
                y2 = floorY
            y1 = y2 - playerSize
        elif tempy2 <= tempy1 - playerSize:
            v1 = v2
            x1 = tempx1
            y1 = tempy1 - v1
            if y1 > floorY:
                y1 = floorY
            y2 = y1 - playerSize
        else:
            if action1 == 1:
                x2 = x2 + speed
            if action1 == 2:
                x2 = x2 - speed
            if action2 == 1:
                x1 = x1 + speed
            if action2 == 2:
                x1 = x1 - speed
            
    
        
    #Handle wrapping
    x1 = x1 % 200
    x2 = x2 % 200
    
    manageTreat(display)
    
    #draw character
    if display:
        p1.move(x1-tempx1, y1-tempy1)
        p2.move(x2-tempx2, y2-tempy2)
        win.flush()
        time.sleep(playSpeed)
     

def initializeStrat():
    strat = [[[[[random.randint(1, 3) for i in range(gScale[4])] for j in range(gScale[3])] for k in range(gScale[2])] for l in range(gScale[1])] for m in range(gScale[0])]
    return strat

def scaleTen(min, max, val):
    return int(((val-min)*10)/(max-min))

def scaleX(scale, min, max, val):
    return int(((val-min)*scale)/(max-min))

def getStratP1(strat):
    var1 = scaleX(gScale[0], 0, 200, (x1-tx)%200)
    var2 = scaleX(gScale[1], 0, 180, (y1-ty)%180)
    var3 = scaleX(gScale[2], -jumpV, jumpV, v1)
    var4 = scaleX(gScale[3], 0, 200, (x1-x2)%200)
    var5 = scaleX(gScale[4], -jumpV, jumpV, v2)
    return strat[var1][var2][var3][var4][var5]

def getStratP2(strat):
    var1 = scaleX(gScale[0], 0, 200, (x2-tx)%200)
    var2 = scaleX(gScale[0], 0, 180, (y2-ty)%180)
    var3 = scaleX(gScale[0], -jumpV, jumpV, v2)
    var4 = scaleX(gScale[0], 0, 200, (x2-x1)%200)
    var5 = scaleX(gScale[0], -jumpV, jumpV, v1)
    return strat[var1][var2][var3][var4][var5]

   
def manageTreat(display):
    global tx
    global ty
    tempx = tx
    tempy = ty
    global treatCount1
    global treatCount2
    ty = ty+treatSpeed
    if ty >= 200:
        ty = 0
        tx = random.randint(0, 190)
    temp1 = intersectsTreatP1()
    temp2 = intersectsTreatP2()
    if temp1 and temp2:
        if random.random() < .5:
            temp1 = False
        else:
            temp2 = False
    if intersectsTreatP1():
        ty = 0
        tx = random.randint(0, 190)
        treatCount1 = treatCount1 + 1
        #print("Got it!")
    if intersectsTreatP2():
        ty = 0
        tx = random.randint(0, 190)
        treatCount2 = treatCount2 + 1
    if display:
        treat.move(tx-tempx, ty-tempy)
    
def intersectsTreatP1():
    if x1 > tx + treatSize or tx > x1 + playerSize:
        return False
    if y1 > ty + treatSize or ty > y1 + playerSize:
        return False
    return True

def intersectsTreatP2():
    if x2 > tx + treatSize or tx > x2 + playerSize:
        return False
    if y2 > ty + treatSize or ty > y2 + playerSize:
        return False
    return True

def wouldCrash(dx1, dy1, dx2, dy2):
    if (x1+dx1) > (x2 + dx2) + playerSize or (x2+dx2) > (x1 + dx1) + playerSize:
        return 0
    if (y1+dy1) > (y2 + dy2) + playerSize or (y2+dy2) > (y1 + dy1) + playerSize:
        return 0
    return min(x1+playerSize-x2, x2+playerSize-x1)

def xOverlap():
    return wouldCrash(0, 0, 0, 0)
#Shows a replay - takes either filename or tuple list
def showReplay(filename):
    replay = []
    if type(filename) is str:
        filename = filename + '.replay2'
        fileReplay = open(filename, 'rb')
        replay = pickle.load(fileReplay)
        fileReplay.close()
    else:
        replay = filename
    firstFrame = replay[0]
    winReplay = GraphWin('Replay Window')
    x1Replay = firstFrame[0]
    y1Replay = firstFrame[1]
    x2Replay = firstFrame[2]
    y2Replay = firstFrame[3]
    txReplay = firstFrame[4]
    tyReplay = firstFrame[5]
    treatReplay = Rectangle(Point(txReplay, tyReplay), Point(txReplay + treatSize, tyReplay + treatSize))
    treatReplay.setFill('yellow')
    p1Replay = Rectangle(Point(x1Replay,y1Replay), Point(x1Replay+playerSize, y1Replay+playerSize))
    p1Replay.setFill('blue')
    p1Replay.draw(winReplay)
    p2Replay = Rectangle(Point(x2Replay,y2Replay), Point(x2Replay+playerSize, y2Replay+playerSize))
    p2Replay.setFill('red')
    p2Replay.draw(winReplay)
    treatReplay.draw(winReplay)
    winReplay.autoflush = False


    leftEye1= Circle(Point(x1Replay + .25 * playerSize, y1Replay + .4*playerSize), .25*playerSize)
    leftEye1.setFill('white')
    leftEye1.setOutline('black')
    leftEye1.setWidth(0)
    leftEye1.draw(winReplay)
    
    rightEye1= Circle(Point(x1Replay + .75 * playerSize, y1Replay + .4*playerSize), .25*playerSize)
    rightEye1.setFill('white')
    rightEye1.setOutline('black')
    rightEye1.setWidth(0)
    rightEye1.draw(winReplay)

    leftEyeP1= Circle(Point(x1Replay + .25 * playerSize, y1Replay + .4*playerSize), .1*playerSize)
    leftEyeP1.setFill('black')
    leftEyeP1.setWidth(0)
    leftEyeP1.draw(winReplay)

    rightEyeP1= Circle(Point(x1Replay + .75 * playerSize, y1Replay + .4*playerSize), .1*playerSize)
    rightEyeP1.setFill('black')
    rightEyeP1.setWidth(0)
    rightEyeP1.draw(winReplay)

    leftEye2= Circle(Point(x2Replay + .25 * playerSize, y2Replay + .4*playerSize), .25*playerSize)
    leftEye2.setFill('white')
    leftEye2.setOutline('black')
    leftEye2.setWidth(0)
    leftEye2.draw(winReplay)
    
    rightEye2= Circle(Point(x2Replay + .75 * playerSize, y2Replay + .4*playerSize), .25*playerSize)
    rightEye2.setFill('white')
    rightEye2.setOutline('black')
    rightEye2.setWidth(0)
    rightEye2.draw(winReplay)

    leftEyeP2= Circle(Point(x2Replay + .25 * playerSize, y2Replay + .4*playerSize), .1*playerSize)
    leftEyeP2.setFill('black')
    leftEyeP2.setWidth(0)
    leftEyeP2.draw(winReplay)

    rightEyeP2= Circle(Point(x2Replay + .75 * playerSize, y2Replay + .4*playerSize), .1*playerSize)
    rightEyeP2.setFill('black')
    rightEyeP2.setWidth(0)
    rightEyeP2.draw(winReplay)
    for i in range(len(replay) - 1):
        frame = replay[i+1]
        leftEye1.move(-x1Replay + frame[0], -y1Replay + frame[1])
        rightEye1.move(-x1Replay + frame[0], -y1Replay + frame[1])
        leftEyeP1.move(-x1Replay + frame[0], -y1Replay + frame[1])
        rightEyeP1.move(-x1Replay + frame[0], -y1Replay + frame[1])

        leftEye2.move(-x2Replay + frame[2], -y2Replay + frame[3])
        rightEye2.move(-x2Replay + frame[2], -y2Replay + frame[3])
        leftEyeP2.move(-x2Replay + frame[2], -y2Replay + frame[3])
        rightEyeP2.move(-x2Replay + frame[2], -y2Replay + frame[3])
        
        p1Replay.move(-x1Replay + frame[0], -y1Replay + frame[1])
        p2Replay.move(-x2Replay + frame[2], -y2Replay + frame[3])
        treatReplay.move(-txReplay + frame[4], -tyReplay + frame[5])
        winReplay.flush()
        time.sleep(playSpeed)
        x1Replay = frame[0]
        y1Replay = frame[1]
        x2Replay = frame[2]
        y2Replay = frame[3]
        txReplay = frame[4]
        tyReplay = frame[5]
        if winReplay.checkMouse() != None:
            break;
    winReplay.close()

    
#main()
