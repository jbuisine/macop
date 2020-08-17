"""Abstract Checkpoint class
"""
# main imports
import os
import logging


class Checkpoint():
    """
    Local Search used as exploitation optimization algorithm

    Attributes:
        algo: {Algorithm} -- main algorithm instance reference
        every: {int} -- checkpoint frequency used (based on number of evaluations)
        filepath: {str} -- file path where checkpoints will be saved
    """
    def __init__(self, _algo, _every, _filepath):
        self.algo = _algo
        self.every = _every
        self.filepath = _filepath

        # build path if not already exists
        head, _ = os.path.split(self.filepath)

        if not os.path.exists(head):
            os.makedirs(head)

    def run(self):
        """
        Check if necessary to do backup based on `every` variable
        """
        pass

    def load(self):
        """
        Load last backup line of solution and set algorithm state at this backup
        """
        pass
