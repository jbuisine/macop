# module imports
from .Algorithm import Algorithm
from.LocalSearch import LocalSearch

class IteratedLocalSearch(Algorithm):

    def run(self, _evaluations):

        # by default use of mother method to initialize variables
        super().run(_evaluations)

        ls = LocalSearch(self.initializer, self.evaluator, self.updators, self.policy, self.validator, self.maximise)

        # local search algorithm implementation
        while self.numberOfEvaluations < self.maxEvalutations:

            # create and search solution from local search
            newSolution = ls.run(100)

            # if better solution than currently, replace it
            if self.isBetter(newSolution):
                self.bestSolution = newSolution

            # increase number of evaluations
            self.numberOfEvaluations += 100

            print(self.progress())
        print(self.information())
            

        print("End of local search algorithm..")

        return self.bestSolution
