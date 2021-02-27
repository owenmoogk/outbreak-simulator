import math, random
from settings import *
import myvars

def getDistance(node1, node2, tick):
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
                    myvars.infected += 1
                    myvars.susceptible -= 1
            elif node2.infected and not node1.infected and not node1.immune:
                node1.infected = random.random() < infectionChance
                if node1.infected:
                    node1.infectionTick = tick
                    node1.color = red
                    myvars.infected += 1
                    myvars.susceptible -= 1

            node1.connections.append(node2)
            node2.connections.append(node1)
    else:
        if node2 in node1.connections:
            node2.connections.remove(node1)
            node1.connections.remove(node2)

def drawLine(node1, node2):
    pygame.draw.line(screen, pink, (node1.x, node1.y), (node2.x, node2.y), 2)