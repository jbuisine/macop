"""Abstract Checkpoint class
"""
# main imports
import os
import logging
from abc import abstractmethod


class Callback():
    """
    Callback abstract class in order to compute some instruction every evaluation

    Attributes:
        algo: {Algorithm} -- main algorithm instance reference
        every: {int} -- checkpoint frequency used (based on number of evaluations)
        filepath: {str} -- file path where checkpoints will be saved
    """
    def __init__(self, _every, _filepath):

        self.algo = None
        self.every = _every
        self.filepath = _filepath

        # build path if not already exists
        head, _ = os.path.split(self.filepath)

        if not os.path.exists(head):
            os.makedirs(head)

    def setAlgo(self, _algo):
        """Specify the main algorithm instance reference

        Args:
            _algo: {Algorithm} -- main algorithm instance reference
        """
        self.algo = _algo

    @abstractmethod
    def run(self):
        """
        Check if necessary to do backup based on `every` variable
        """
        pass

    @abstractmethod
    def load(self):
        """
        Load last backup line of solution and set algorithm state at this backup
        """
        pass
