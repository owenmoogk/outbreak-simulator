# INIT
import pygame, random, time, math
import graphing
pygame.font.init()  # init font
windowWidth = 1200
windowHeight = 675
myFont = pygame.font.SysFont("comicsans", 50)
screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Outbreak Simulation")

# SETTINGS
simSpeed = 60 # 60 ticks / frames per second
maxNodeSpeed = 2
numOfNodes = 200
circleRadius = 7
infectionDistance = 50
initInfectionChance = 0 # init infection change, if 0 there will be exactly one node that is infected
infectionChance = 0.1
postInfectionImmunityChance = 0.3
recoveryTime = 600 # in ticks
deathChance = 0.05
drawLines = True
transmissionLinesOnly = True # limits lines to only connect between infected dots, only matters if drawlines is true
dataLogTicks = 20 # log the data every 100 ticks

# COLORS
white = (255,255,255)
grey = (150,150,150)
blue = (51,153,255)
red = (255,0,0)
pink = (254,127,156)
green = (0,255,0)
backgroundColor = (30,30,30)

class Node:

    def __init__(self):
        self.x = random.randint(circleRadius,windowWidth-circleRadius)
        self.y = random.randint(circleRadius,windowHeight-circleRadius)
        self.xVel = random.randint(-maxNodeSpeed,maxNodeSpeed)
        self.yVel = random.randint(-maxNodeSpeed,maxNodeSpeed)
        self.connections = []
        self.infected = random.random() < initInfectionChance
        self.immune = False
        self.color = grey
        self.dead = False
        if self.infected:
            self.infectionTick = 0
        else:
            self.infectionTick = None

    def move(self):
        if self.dead:
            return

        self.y += self.yVel
        self.x += self.xVel

        if self.y <= circleRadius or self.y >= windowHeight - circleRadius:
            self.yVel = -self.yVel

        if self.x <= circleRadius or self.x >= windowWidth - circleRadius:
            self.xVel = -self.xVel

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), circleRadius)

    def checkImmunity(self):
        global nodes, deadNodes
        if self.infectionTick < tick - recoveryTime:
            global infected, susceptible, immune, dead
            self.infected = False
            self.immune = random.random() < postInfectionImmunityChance
            self.dead = random.random() < deathChance
            infected -= 1
            if self.dead:
                self.color = blue
                dead += 1
                deadNodes.append(self)
                nodes.remove(self)
            else:
                if self.immune:
                    self.color = green
                    immune += 1
                else:
                    self.color = grey
                    susceptible += 1


def drawBackground():
    screen.fill(backgroundColor)

def drawWindow(nodes, deadNodes):
    global immune, susceptible, infected, dead

    for node in nodes:
        node.draw()

    for deadNode in deadNodes:
        deadNode.draw()

    # labels
    score_label = myFont.render("Susceptible: " + str(susceptible),1,white)
    screen.blit(score_label, (10, 10))
    score_label = myFont.render("Infected: " + str(infected),1,white)
    screen.blit(score_label, (10, 50))
    score_label = myFont.render("Immune: " + str(immune),1,white)
    screen.blit(score_label, (10, 90))
    score_label = myFont.render("Dead: " + str(dead),1,white)
    screen.blit(score_label, (10, 130))
    
def getDistance(node1, node2):
    global infected, susceptible
    y = abs(node1.y - node2.y)
    x = abs(node1.x - node2.x)
    distance = math.sqrt(y*y + x*x)
    if distance < infectionDistance:
        if node2 in node1.connections:
            if drawLines:
                if transmissionLinesOnly:
                    if node1.infected or node2.infected:
                        drawLine(node1, node2)
                else:
                    drawLine(node1, node2)

        else:
            if node1.infected and not node2.infected and not node2.immune:
                node2.infected = random.random() < infectionChance
                if node2.infected:
                    node2.infectionTick = tick
                    node2.color = red
                    infected += 1
                    susceptible -= 1
            elif node2.infected and not node1.infected and not node1.immune:
                node1.infected = random.random() < infectionChance
                if node1.infected:
                    node1.infectionTick = tick
                    node1.color = red
                    infected += 1
                    susceptible -= 1

            node1.connections.append(node2)
            node2.connections.append(node1)
    else:
        if node2 in node1.connections:
            node2.connections.remove(node1)
            node1.connections.remove(node2)

def drawLine(node1, node2):
    pygame.draw.line(screen, pink, (node1.x, node1.y), (node2.x, node2.y), 2)

def logData():
    global data
    data["immune"].append(immune)
    data["susceptible"].append(susceptible)
    data["infected"].append(infected)
    data["dead"].append(dead)

# main
data = {
    "susceptible": [],
    "immune": [],
    "infected": [],
    "dead": [],
}
immune = 0
susceptible = numOfNodes
infected = 0
dead = 0

nodes = []
deadNodes = []
for i in range(numOfNodes):
    nodes.append(Node())

# making sure there is at least one infected, if not we will make the last one infected
for index, node in enumerate(nodes):
    if node.infected:
        break
    if index + 1 == len(nodes):
        node.infected = True
        node.infectionTick = 0
        node.color = red

# checking how many are initially contagious
for node in nodes:
    if node.infected:
        susceptible -= 1
        infected += 1

clock = pygame.time.Clock()
tick = 0
while True:
    tick += 1
    clock.tick(simSpeed)
    drawBackground()

    # quit function
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # proxmitiy detection (and transmission)
    for index, node in enumerate(nodes):
        for node2 in nodes[index:]: # this does not loop thru nodes that already have been checked (so we have no [node1 --> node2], and then [node2 --> node1])
            getDistance(node, node2)
        if node.infected:
            node.checkImmunity()
        node.move()

    drawWindow(nodes, deadNodes)

    # data export stuff
    if tick % dataLogTicks == 0:
        logData()

    if infected == 0:
        break

    pygame.display.update()

logData()

import csv
def createCSV(data):
    with open("data.csv", "w", newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["tick", "susceptible", "immune", "infected", "dead"])
        for i in range(0, len(data["immune"])):
            filewriter.writerow([i*dataLogTicks, data["susceptible"][i], data["immune"][i], data["infected"][i], data["dead"][i]])

createCSV(data)
graphing.graph(data)