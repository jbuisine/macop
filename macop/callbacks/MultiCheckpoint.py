"""Multi Checkpoint class implementation
"""

# main imports
import os
import logging
import numpy as np

# module imports
from .Callback import Callback
from ..utils.color import macop_text, macop_line


class MultiCheckpoint(Callback):
    """
    MultiCheckpoint is used for loading previous computations and start again after loading checkpoint

    Attributes:
        algo: {Algorithm} -- main algorithm instance reference
        every: {int} -- checkpoint frequency used (based on number of evaluations)
        filepath: {str} -- file path where checkpoints will be saved
    """
    def run(self):
        """
        Check if necessary to do backup based on `every` variable
        """
        # get current population
        population = self._algo._population

        currentEvaluation = self._algo.getGlobalEvaluation()

        # backup if necessary
        if currentEvaluation % self._every == 0:

            logging.info("Checkpoint is done into " + self._filepath)

            with open(self._filepath, 'w') as f:

                for solution in population:
                    solutionData = ""
                    solutionSize = len(solution.data)

                    for index, val in enumerate(solution.data):
                        solutionData += str(val)

                        if index < solutionSize - 1:
                            solutionData += ' '

                    line = str(currentEvaluation) + ';'

                    for i in range(len(self._algo.evaluator)):
                        line += str(solution.scores[i]) + ';'

                    line += solutionData + ';\n'

                    f.write(line)

    def load(self):
        """
        Load backup lines as population and set algorithm state (population and pareto front) at this backup
        """
        if os.path.exists(self._filepath):

            logging.info('Load best solution from last checkpoint')
            with open(self._filepath) as f:

                # read data for each line
                for i, line in enumerate(f.readlines()):

                    data = line.replace(';\n', '').split(';')

                    # only the first time
                    if i == 0:
                        # get evaluation  information
                        globalEvaluation = int(data[0])

                        if self._algo.parent is not None:
                            self._algo.parent.numberOfEvaluations = globalEvaluation
                        else:
                            self._algo.numberOfEvaluations = globalEvaluation

                    nObjectives = len(self._algo.evaluator)
                    scores = [float(s) for s in data[1:nObjectives + 1]]

                    # get best solution data information
                    solutionData = list(map(int, data[-1].split(' ')))

                    # initialize and fill with data
                    self._algo.population[i] = self._algo.initializer()
                    self._algo.population[i].data = np.array(solutionData)
                    self._algo.population[i].scores = scores

                    self._algo.pfPop.append(self._algo.population[i])

            print(macop_line())
            print(
                macop_text('Load of available population from `{}`'.format(
                    self._filepath)))
            print(
                macop_text('Restart algorithm from evaluation {}.'.format(
                    self._algo.numberOfEvaluations)))

        else:
            print(
                macop_text(
                    'No backup found... Start running algorithm from evaluation 0.'
                ))
            logging.info(
                "Can't load backup... Backup filepath not valid in Checkpoint")

        print(macop_line())
