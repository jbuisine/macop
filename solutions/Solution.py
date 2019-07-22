# Generic solution class 
class Solution():

    def __init__(self, _data, _size):
        """
        Initialize data of solution using specific data

        Note : `data` field can be anything, such as array/list of integer
        """
        self.data = _data
        self.size = _size
        self.score = None
    

    def apply(self, _updator):
        """
        Apply custom modification of solution and return the transformed solution
        """
        return _updator(self)


    def isValid(self, _validator):
        """
        Use of custom method which validates if solution is valid or not
        """
        return _validator(self)


    def evaluate(self, _evaluator):
        """
        Evaluate function using specific `_evaluator`
        """
        self.score = _evaluator(self)
        return self.score


    def fitness(self):
        """
        Returns fitness score
        """
        return self.score


    def random(self):
        """
        Initialize solution using random data
        """
        raise NotImplementedError


    def __str__(self):
        print("Generic solution with ", self.data)
