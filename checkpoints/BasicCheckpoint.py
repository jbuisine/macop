# main imports
import os
import logging

# module imports
from .Checkpoint import Checkpoint

class BasicCheckpoint(Checkpoint):

    def __init__(self, _algo, _every, _filepath):
        self.algo = _algo
        self.every = _every
        self.filepath = _filepath


    def run(self):

        # get current best solution
        solution = self.algo.bestSolution

        currentEvaluation = self.algo.getGlobalEvaluation()

        # backup if necessary
        if currentEvaluation % self.every == 0:

            logging.info("Checkpoint is done into " + self.filepath)

            cleanSolution =  str(solution.data).replace('[', '').replace(']', '')
            line = str(currentEvaluation) + ';' + cleanSolution + ';' + str(solution.fitness()) + ';\n'

            # check if file exists
            if not os.path.exists(self.filepath):
                with open(self.filepath, 'w') as f:
                    f.write(line)
            else:
                with open(self.filepath, 'a') as f:
                    f.write(line)


    def load(self):

        if os.path.exists(self.filepath):

            logging.info('Load best solution from last checkpoint')
            with open(self.filepath) as f:

                # get last line and read data
                lastline = f.readlines()[-1]
                data = lastline.split(';')
                
                # get evaluation  information 
                globalEvaluation = int(data[0])

                print(globalEvaluation, data)

                if self.algo.parent is not None:
                    self.algo.parent.numberOfEvaluations = globalEvaluation
                else:
                    self.algo.numberOfEvaluations = globalEvaluation

                print(self.algo.numberOfEvaluations)
                # get best solution data information
                solutionData = list(map(int, data[1].split(' ')))

                print(solutionData)
                self.algo.bestSolution.data = solutionData
                self.algo.bestSolution.score = float(data[2])
        else:
            logging.info("Can't load backup... Backup filepath not valid in Checkpoint")
