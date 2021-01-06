"""Abstract Checkpoint classes for callback process
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
    def __init__(self, every, filepath):

        self._algo = None
        self._every = every
        self._filepath = filepath

        # build path if not already exists
        head, _ = os.path.split(self._filepath)

        if not os.path.exists(head):
            os.makedirs(head)

    def setAlgo(self, algo):
        """Specify the main algorithm instance reference

        Args:
            algo: {Algorithm} -- main algorithm instance reference
        """
        self._algo = algo

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
