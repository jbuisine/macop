"""UCB policy Checkpoint class implementation
"""

# main imports
import os
import logging
import numpy as np

# module imports
from macop.callbacks.base import Callback
from macop.utils.progress import macop_text, macop_line


class UCBCheckpoint(Callback):
    """
    UCB checkpoint is used for loading previous Upper Confidence Bound data and start again after loading checkpoint
    Need to be the same operators used during previous run (see `macop.policies.reinforcement.UCBPolicy` for more details)

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
        currentEvaluation = self._algo.getGlobalEvaluation()

        # backup if necessary
        if currentEvaluation % self._every == 0:

            logging.info("UCB Checkpoint is done into " + self._filepath)

            with open(self._filepath, 'w') as f:

                rewardsLine = ''

                for i, r in enumerate(self._algo._policy._rewards):
                    rewardsLine += str(r)

                    if i != len(self._algo._policy._rewards) - 1:
                        rewardsLine += ';'

                f.write(rewardsLine + '\n')

                occurrencesLine = ''

                for i, o in enumerate(self._algo._policy._occurences):
                    occurrencesLine += str(o)

                    if i != len(self._algo._policy._occurences) - 1:
                        occurrencesLine += ';'

                f.write(occurrencesLine + '\n')

    def load(self):
        """
        Load backup lines as rewards and occurrences for UCB
        """
        if os.path.exists(self._filepath):

            logging.info('Load UCB data')
            with open(self._filepath) as f:

                lines = f.readlines()
                # read data for each line
                rewardsLine = lines[0].replace('\n', '')
                occurrencesLine = lines[1].replace('\n', '')

                self._algo._policy._rewards = [
                    float(f) for f in rewardsLine.split(';')
                ]
                self._algo._policy._occurences = [
                    float(f) for f in occurrencesLine.split(';')
                ]
            
            macop_text(self._algo, f'Load of available UCB policy data from `{self._filepath}`')
        else:
            macop_text(self._algo, 'No UCB data found, use default UCB policy')
            logging.info("No UCB data found...")

        macop_line(self._algo)
