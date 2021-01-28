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
        solution = self._algo.result

        currentEvaluation = self._algo.getGlobalEvaluation()

        # backup if necessary
        if currentEvaluation % self._every == 0:

            logging.info("Checkpoint is done into " + self._filepath)

            solution.data = ""
            solutionSize = len(solution.data)

            for index, val in enumerate(solution.data):
                solution.data += str(val)

                if index < solutionSize - 1:
                    solution.data += ' '

            line = str(currentEvaluation) + ';' + solution.data + ';' + str(
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

                if self._algo.getParent() is not None:
                    self._algo.getParent().setEvaluation(globalEvaluation)
                else:
                    self._algo.setEvaluation(globalEvaluation)

                # get best solution data information
                solution.data = list(map(int, data[1].split(' ')))

                if self._algo.result is None:
                    self._algo.result(self._algo.initialiser())

                self._algo.result.data = np.array(solution.data)
                self._algo.result.fitness = float(data[2])

            macop_line(self._algo)
            macop_text(self._algo,
                       f'Checkpoint found from `{self._filepath}` file.')
            macop_text(
                self._algo,
                f'Restart algorithm from evaluation {self._algo.getEvaluation()}.'
            )
        else:
            macop_text(
                self._algo,
                'No backup found... Start running algorithm from evaluation 0.'
            )
            logging.info(
                "Can't load backup... Backup filepath not valid in Checkpoint")

        macop_line(self._algo)
