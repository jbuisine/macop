"""Multi-objective Checkpoints classes implementations
"""

# main imports
import os
import logging
import numpy as np

# module imports
from macop.callbacks.base import Callback
from macop.utils.progress import macop_text, macop_line


class MultiCheckpoint(Callback):
    """
    MultiCheckpoint is used for loading previous computations and start again after loading checkpoint

    Attributes:
        algo: {:class:`~macop.algorithms.base.Algorithm`} -- main algorithm instance reference
        every: {int} -- checkpoint frequency used (based on number of evaluations)
        filepath: {str} -- file path where checkpoints will be saved
    """
    def run(self):
        """
        Check if necessary to do backup based on `every` variable
        """
        # get current population
        population = self._algo.population

        currentEvaluation = self._algo.getGlobalEvaluation()

        # backup if necessary
        if currentEvaluation % self._every == 0:

            logging.info("Checkpoint is done into " + self._filepath)

            with open(self._filepath, 'w') as f:

                for solution in population:
                    solution.data = ""
                    solutionSize = len(solution.data)

                    for index, val in enumerate(solution.data):
                        solution.data += str(val)

                        if index < solutionSize - 1:
                            solution.data += ' '

                    line = str(currentEvaluation) + ';'

                    for i in range(len(self._algo.evaluator)):
                        line += str(solution.scores[i]) + ';'

                    line += solution.data + ';\n'

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

                        if self._algo.getParent() is not None:
                            self._algo.getParen(
                            )._numberOfEvaluations = globalEvaluation
                        else:
                            self._algo._numberOfEvaluations = globalEvaluation

                    nObjectives = len(self._algo.evaluator)
                    scores = [float(s) for s in data[1:nObjectives + 1]]

                    # get best solution data information
                    solution.data = list(map(int, data[-1].split(' ')))

                    # initialise and fill with data
                    self._algo.population[i] = self._algo.initialiser()
                    self._algo.population[i].data = np.array(solution.data)
                    self._algo.population[i].scores = scores

                    self._algo._pfPop.append(self._algo.population[i])

            macop_line(self._algo)
            macop_text(
                self._algo,
                f'Load of available population from `{self._filepath}`')
            macop_text(
                self._algo,
                f'Restart algorithm from evaluation {self._algo._numberOfEvaluations}.'
            )
        else:
            macop_text(
                self._algo,
                'No backup found... Start running algorithm from evaluation 0.'
            )
            logging.info(
                "Can't load backup... Backup filepath not valid in Checkpoint")

        macop_line(self._algo)


class ParetoCheckpoint(Callback):
    """
    Pareto checkpoint is used for loading previous computations and start again after loading checkpoint

    Attributes:
        algo: {:class:`~macop.algorithms.base.Algorithm`} -- main algorithm instance reference
        every: {int} -- checkpoint frequency used (based on number of evaluations)
        filepath: {str} -- file path where checkpoints will be saved
    """
    def run(self):
        """
        Check if necessary to do backup based on `every` variable
        """
        # get current population
        pfPop = self._algo.result

        currentEvaluation = self._algo.getGlobalEvaluation()

        # backup if necessary
        if currentEvaluation % self._every == 0:

            logging.info("Checkpoint is done into " + self._filepath)

            with open(self._filepath, 'w') as f:

                for solution in pfPop:
                    solution.data = ""
                    solutionSize = len(solution.data)

                    for index, val in enumerate(solution.data):
                        solution.data += str(val)

                        if index < solutionSize - 1:
                            solution.data += ' '

                    line = ''

                    for i in range(len(self._algo.evaluator)):
                        line += str(solution.scores[i]) + ';'

                    line += solution.data + ';\n'

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

                    nObjectives = len(self._algo.evaluator)
                    scores = [float(s) for s in data[0:nObjectives]]

                    # get best solution data information
                    solution.data = list(map(int, data[-1].split(' ')))

                    self._algo.result[i].data = solution.data
                    self._algo.result[i].scores = scores

            macop_text(
                self._algo,
                f'Load of available pareto front backup from `{ self._filepath}`'
            )
        else:
            macop_text(
                self._algo,
                'No pareto front found... Start running algorithm with new pareto front population.'
            )
            logging.info("No pareto front backup used...")

        macop_line(self._algo)
