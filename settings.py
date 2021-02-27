import pygame

pygame.font.init()  # init font
windowWidth = 1200
windowHeight = 675
myFont = pygame.font.SysFont("comicsans", 50)
screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Outbreak Simulation")

# SETTINGS
simSpeed = 6000 # 60 ticks / frames per second
maxNodeSpeed = 2
numOfNodes = 100
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