"""Pareto front Checkpoint class implementation
"""

# main imports
import os
import logging
import numpy as np
import pkgutil

# module imports
from .Callback import Callback
from ..utils.color import macop_text, macop_line

# import all available solutions
for loader, module_name, is_pkg in pkgutil.walk_packages(
        path=['macop/solutions'], prefix='macop.solutions.'):
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module


class ParetoCheckpoint(Callback):
    """
    Pareto checkpoint is used for loading previous computations and start again after loading checkpoint

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
        pfPop = self.algo.pfPop

        currentEvaluation = self.algo.getGlobalEvaluation()

        # backup if necessary
        if currentEvaluation % self.every == 0:

            logging.info("Checkpoint is done into " + self.filepath)

            with open(self.filepath, 'w') as f:

                for solution in pfPop:
                    solutionData = ""
                    solutionSize = len(solution.data)

                    for index, val in enumerate(solution.data):
                        solutionData += str(val)

                        if index < solutionSize - 1:
                            solutionData += ' '

                    line = ''

                    for i in range(len(self.algo.evaluator)):
                        line += str(solution.scores[i]) + ';'

                    line += solutionData + ';\n'

                    f.write(line)

    def load(self):
        """
        Load backup lines as population and set algorithm state (population and pareto front) at this backup
        """
        if os.path.exists(self.filepath):

            logging.info('Load best solution from last checkpoint')
            with open(self.filepath) as f:

                # reinit pf population
                self.algo.pfPop = []

                # retrieve class name from algo
                class_name = type(self.algo.population[0]).__name__

                # read data for each line
                for line in f.readlines():

                    data = line.replace(';\n', '').split(';')

                    nObjectives = len(self.algo.evaluator)
                    scores = [float(s) for s in data[0:nObjectives]]

                    # get best solution data information
                    solutionData = list(map(int, data[-1].split(' ')))

                    newSolution = getattr(
                        globals()['macop.solutions.' + class_name],
                        class_name)(solutionData, len(solutionData))
                    newSolution.scores = scores

                    self.algo.pfPop.append(newSolution)

            print(
                macop_text(
                    'Load of available pareto front backup from `{}`'.format(
                        self.filepath)))

        else:
            print(
                macop_text(
                    'No pareto front found... Start running algorithm with new pareto front population.'
                ))
            logging.info("No pareto front backup used...")

        print(macop_line())
