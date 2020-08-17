"""Python evaluator function example
"""


# evaluator example
def evaluatorExample(_solution):
    """
    Evaluator's example of solution to compute fitness

    Args:
        _solution: {Solution} -- solution to evaluate

    Returns:
        {float} -- fitness score of solution
    """
    fitness = 0
    for index, elem in enumerate(_solution.data):
        fitness = fitness + (elem * index)

    return fitness
