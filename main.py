# INIT
import pygame, random, time, math
import graphing
from node import *
from settings import *
import myvars
from drawScreen import *
from dataCSV import *
from nodeDistance import getDistance


myvars.susceptible = numOfNodes

for i in range(numOfNodes):
    myvars.nodes.append(Node())

# making sure there is at least one infected, if not we will make the last one infected
for index, node in enumerate(myvars.nodes):
    if node.infected:
        break
    if index + 1 == len(myvars.nodes):
        node.infected = True
        node.infectionTick = 0
        node.color = red

# checking how many are initially contagious
for node in myvars.nodes:
    if node.infected:
        myvars.susceptible -= 1
        myvars.infected += 1

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
    for index, node in enumerate(myvars.nodes):
        for node2 in myvars.nodes[index:]: # this does not loop thru nodes that already have been checked (so we have no [node1 --> node2], and then [node2 --> node1])
            getDistance(node, node2, tick)
        if node.infected:
            node.checkImmunity(tick)
        node.move()

    drawWindow(myvars.nodes, myvars.deadNodes)

    # data export stuff
    if tick % dataLogTicks == 0:
        logData()

    if myvars.infected == 0:
        break

    pygame.display.update()

logData()
createCSV(myvars.data)
graphing.graph(myvars.data)