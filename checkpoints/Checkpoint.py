# main imports
import os
import logging

class Checkpoint():

    def __init__(self, _algo, _every, _filepath):
        self.algo = _algo
        self.every = _every
        self.filepath = _filepath

    def run(self):
        """
        Check if necessary to do backup based on `_every` variable
        """
        pass

    def load(self):
        """
        Load last backup line of solution and set algorithm state at this backup
        """
        pass