import csv
import myvars
from settings import dataLogTicks

def logData():
    myvars.data["immune"].append(myvars.immune)
    myvars.data["susceptible"].append(myvars.susceptible)
    myvars.data["infected"].append(myvars.infected)
    myvars.data["dead"].append(myvars.dead)

def createCSV(data):
    with open("data.csv", "w", newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["tick", "susceptible", "immune", "infected", "dead"])
        for i in range(0, len(data["immune"])):
            filewriter.writerow([i*dataLogTicks, data["susceptible"][i], data["immune"][i], data["infected"][i], data["dead"][i]])