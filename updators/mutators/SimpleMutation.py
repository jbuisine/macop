# main imports
import random
import sys

# module imports
from ...solutions import *

def SimpleBinaryMutation(solution):
    size = solution.size

    cell = random.randint(0, size - 1)

    # copy data of solution
    currentData = solution.data.copy()

    # swicth values
    if currentData[cell]:
        currentData[cell] = 0
    else:
        currentData[cell] = 1

    # create solution of same kind with new data
    return globals()[type(solution).__name__](currentData, size)


def SimpleMutation(solution):

    size = solution.size

    firstCell = 0
    secondCell = 0

    # copy data of solution
    currentData = solution.data.copy()

    while firstCell == secondCell:
        firstCell = random.randint(0, size - 1) 
        secondCell = random.randint(0, size - 1)

    temp = currentData[firstCell]

    # swicth values
    currentData[firstCell] = currentData[secondCell]
    currentData[secondCell] = temp
    
    # create solution of same kind with new data
    return globals()[type(solution).__name__](currentData, size)

