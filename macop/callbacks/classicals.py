"""Classical Checkpoints classes implementations
"""

# main imports
import os
import logging
import numpy as np

# module imports
from macop.callbacks.base import Callback
from macop.utils.progress import macop_text, macop_line


class BasicCheckpoint(Callback):
    """
    BasicCheckpoint is used for loading previous computations and start again after loading checkpoint

    Attributes:
        algo: {:class:`~macop.algorithms.base.Algorithm`} -- main algorithm instance reference
        every: {int} -- checkpoint frequency used (based on number of evaluations)
        filepath: {str} -- file path where checkpoints will be saved
    """
    def run(self):
        """
        Check if necessary to do backup based on `every` variable
        """
        # get current best solution
        solution = self.algo.result

        currentEvaluation = self.algo.getGlobalEvaluation()

        # backup if necessary
        if currentEvaluation % self._every == 0:

            logging.info("Checkpoint is done into " + self._filepath)

            solution_data = ""
            solutionSize = len(solution.data)

            for index, val in enumerate(solution.data):
                solution_data += str(val)

                if index < solutionSize - 1:
                    solution_data += ' '

            line = str(currentEvaluation) + ';' + solution_data + ';' + str(
                solution.fitness) + ';\n'

            # check if file exists
            if not os.path.exists(self._filepath):
                with open(self._filepath, 'w') as f:
                    f.write(line)
            else:
                with open(self._filepath, 'a') as f:
                    f.write(line)

    def load(self):
        """
        Load last backup line of solution and set algorithm state (best solution and evaluations) at this backup
        """
        if os.path.exists(self._filepath):

            logging.info('Load best solution from last checkpoint')
            with open(self._filepath) as f:

                # get last line and read data
                lastline = f.readlines()[-1]
                data = lastline.split(';')

                # get evaluation  information
                globalEvaluation = int(data[0])

                if self.algo.getParent() is not None:
                    self.algo.getParent().setEvaluation(globalEvaluation)
                else:
                    self.algo.setEvaluation(globalEvaluation)

                # get best solution data information
                solution_data = list(map(int, data[1].split(' ')))

                if self.algo.result is None:
                    self.algo.result = self.algo.initialiser()

                self.algo.result.data = np.array(solution_data)
                self.algo.result.fitness = float(data[2])

            macop_line(self.algo)
            macop_text(self.algo,
                       f'Checkpoint found from `{self._filepath}` file.')
            macop_text(
                self.algo,
                f'Restart algorithm from evaluation {self.algo.getEvaluation()}.'
            )
        else:
            macop_text(
                self.algo,
                'No backup found... Start running algorithm from evaluation 0.'
            )
            logging.info(
                "Can't load backup... Backup filepath not valid in Checkpoint")

        macop_line(self.algo)


class ContinuousCheckpoint(Callback):
    """
    ContinuousCheckpoint is used for loading previous computations and start again after loading checkpoint (only continuous solution)

    Attributes:
        algo: {:class:`~macop.algorithms.base.Algorithm`} -- main algorithm instance reference
        every: {int} -- checkpoint frequency used (based on number of evaluations)
        filepath: {str} -- file path where checkpoints will be saved
    """

    def run(self):
        """
        Check if necessary to do backup based on `every` variable
        """
        # get current best solution
        solution = self.algo.result

        currentEvaluation = self.algo.getGlobalEvaluation()

        # backup if necessary
        if currentEvaluation % self._every == 0:

            logging.info("Checkpoint is done into " + self._filepath)

            solution_data = ""
            solutionSize = len(solution.data)

            for index, val in enumerate(solution.data):
                solution_data += str(val)

                if index < solutionSize - 1:
                    solution_data += ' '

            line = str(currentEvaluation) + ';' + solution_data + ';' + str(
                solution.fitness) + ';\n'

            # check if file exists
            if not os.path.exists(self._filepath):
                with open(self._filepath, 'w') as f:
                    f.write(line)
            else:
                with open(self._filepath, 'a') as f:
                    f.write(line)

    def load(self):
        """
        Load last backup line of solution and set algorithm state (best solution and evaluations) at this backup
        """
        if os.path.exists(self._filepath):

            logging.info('Load best solution from last checkpoint')
            with open(self._filepath) as f:

                # get last line and read data
                lastline = f.readlines()[-1]
                data = lastline.split(';')

                # get evaluation  information
                globalEvaluation = int(data[0])

                if self.algo.getParent() is not None:
                    self.algo.getParent().setEvaluation(globalEvaluation)
                else:
                    self.algo.setEvaluation(globalEvaluation)

                # get best solution data information
                solution_data = list(map(float, data[1].split(' ')))

                if self.algo.result is None:
                    self.algo.result = self.algo.initialiser()

                self.algo.result.data = np.array(solution_data)
                self.algo.result.fitness = float(data[2])

            macop_line(self.algo)
            macop_text(self.algo,
                       f'Checkpoint found from `{self._filepath}` file.')
            macop_text(
                self.algo,
                f'Restart algorithm from evaluation {self.algo.getEvaluation()}.'
            )
        else:
            macop_text(
                self.algo,
                'No backup found... Start running algorithm from evaluation 0.'
            )
            logging.info(
                "Can't load backup... Backup filepath not valid in Checkpoint")

        macop_line(self.algo)
