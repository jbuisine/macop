# evaluator example
def evaluatorExample(solution):

    fitness = 0
    for index, elem in enumerate(solution.data):
        fitness = fitness + (elem * index)
    
    return fitness