import numpy
from matplotlib import pyplot as PLT

def graph(data):
    dead = numpy.array(data["dead"])
    susceptible = numpy.array(data["susceptible"])
    infected = numpy.array(data["infected"])
    immune = numpy.array(data["immune"])

    myArray = numpy.row_stack((susceptible, infected, immune, dead))
    x = numpy.arange(len(dead))
    y_stack = numpy.cumsum(myArray, axis=0)

    fig = PLT.figure()
    ax1 = fig.add_subplot(111)

    ax1.fill_between(x, 0, y_stack[0,:], facecolor="#808080", alpha=.7)
    ax1.fill_between(x, y_stack[0,:], y_stack[1,:], facecolor="#FF0000", alpha=.7)
    ax1.fill_between(x, y_stack[1,:], y_stack[2,:], facecolor="#00FF00")
    ax1.fill_between(x, y_stack[2,:], y_stack[3,:], facecolor="#0000ff")

    PLT.show()