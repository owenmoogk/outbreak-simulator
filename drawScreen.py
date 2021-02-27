import pygame, myvars
from settings import *

def drawBackground():
    screen.fill(backgroundColor)

def drawWindow(nodes, deadNodes):
    for node in nodes:
        node.draw()

    for deadNode in deadNodes:
        deadNode.draw()

    # labels
    score_label = myFont.render("Susceptible: " + str(myvars.susceptible),1,white)
    screen.blit(score_label, (10, 10))
    score_label = myFont.render("Infected: " + str(myvars.infected),1,white)
    screen.blit(score_label, (10, 50))
    score_label = myFont.render("Immune: " + str(myvars.immune),1,white)
    screen.blit(score_label, (10, 90))
    score_label = myFont.render("Dead: " + str(myvars.dead),1,white)
    screen.blit(score_label, (10, 130))