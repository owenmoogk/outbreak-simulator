# INIT
import pygame, random, time, math
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
infectionChance = 0.4
postInfectionImmunityChance = 0.4
recoveryTime = 300 # in ticks
drawLines = True

# COLORS
white = (255,255,255)
grey = (150,150,150)
blue = (0,0,255)
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
        if self.infected:
            self.infectionTick = 0
        else:
            self.infectionTick = None

    def move(self):
        self.y += self.yVel
        self.x += self.xVel

        if self.y <= circleRadius or self.y >= windowHeight - circleRadius:
            self.yVel = -self.yVel

        if self.x <= circleRadius or self.x >= windowWidth - circleRadius:
            self.xVel = -self.xVel

    def draw(self):
        if self.infected:
            self.color = red
        elif self.immune:
            self.color = green
        else:
            self.color = grey
        pygame.draw.circle(screen, self.color, (self.x, self.y), circleRadius)

    def checkImmunity(self):
        if self.infectionTick < tick - recoveryTime:
            global infected, susceptible, immune
            self.infected = False
            self.immune = random.random() < postInfectionImmunityChance
            infected -= 1
            if self.immune:
                self.color = green
                immune += 1
            else:
                susceptible += 1
                


def drawBackground():
    screen.fill(backgroundColor)

def drawWindow(node, infected, immune, susceptible):
    for node in nodes:
        node.draw()

    # labels
    score_label = myFont.render("Susceptible: " + str(susceptible),1,white)
    screen.blit(score_label, (10, 10))
    score_label = myFont.render("Infected: " + str(infected),1,white)
    screen.blit(score_label, (10, 50))
    score_label = myFont.render("Immune: " + str(immune),1,white)
    screen.blit(score_label, (10, 90))
    
def getDistance(node1, node2):
    global infected, susceptible
    y = abs(node1.y - node2.y)
    x = abs(node1.x - node2.x)
    distance = math.sqrt(y*y + x*x)
    if distance < infectionDistance:
        if node2 in node1.connections:
            if drawLines:
                drawLine(node1, node2)
        else:
            if node1.infected and not node2.infected and not node2.immune:
                node2.infected = random.random() < infectionChance
                if node2.infected:
                    node2.infectionTick = tick
                    infected += 1
                    susceptible -= 1
            elif node2.infected and not node1.infected and not node1.immune:
                node1.infected = random.random() < infectionChance
                if node1.infected:
                    node1.infectionTick = tick
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


# main

immune = 0
susceptible = numOfNodes
infected = 0

nodes = []
for i in range(numOfNodes):
    nodes.append(Node())

# making sure there is at least one infected, if not we will make the last one infected
for index, node in enumerate(nodes):
    if node.infected:
        break
    if index + 1 == len(nodes):
        node.infected = True
        node.infectionTick = 0

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

    drawWindow(nodes, infected, immune, susceptible)

    pygame.display.update()