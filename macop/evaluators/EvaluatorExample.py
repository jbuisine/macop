"""Python evaluator function example
"""

import random

elements_score = [random.randint(1, 20) for _ in range(30)]


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
        fitness += elements_score[index] * elem

    return fitness
