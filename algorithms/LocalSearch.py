# module imports
from .Algorithm import Algorithm

class LocalSearch(Algorithm):

    def run(self, _evaluations):

        # by default use of mother method to initialize variables
        super().run(_evaluations)

        solutionSize = self.bestSolution.size

        # local search algorithm implementation
        while self.numberOfEvaluations < self.maxEvalutations:

            for _ in range(solutionSize):

                # update solution using policy
                newSolution = self.update(self.bestSolution)

                # if better solution than currently, replace it
                if self.isBetter(newSolution):
                    self.bestSolution = newSolution

                # increase number of evaluations
                self.numberOfEvaluations += 1

                print(self.progress())

                # stop algorithm if necessary
                if self.numberOfEvaluations >= self.maxEvalutations:
                    break
            
            print(self.information())

        print("End of local search algorithm..")

        return self.bestSolution
