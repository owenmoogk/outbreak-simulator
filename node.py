import pygame, random
from settings import *

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

    def checkImmunity(self, tick):
        import myvars
        if self.infectionTick < tick - recoveryTime:
            self.infected = False
            self.immune = random.random() < postInfectionImmunityChance
            self.dead = random.random() < deathChance
            myvars.infected -= 1
            if self.dead:
                self.color = blue
                myvars.dead += 1
                myvars.deadNodes.append(self)
                myvars.nodes.remove(self)
            else:
                if self.immune:
                    self.color = green
                    myvars.immune += 1
                else:
                    self.color = grey
                    myvars.susceptible += 1