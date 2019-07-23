# define policy to choose `operator` function at current iteration
class Policy():

    # here you can define your statistical variables for choosing next operator to apply

    def __init__(self, _operators):
        self.operators = _operators

    def apply(self, solution):
        """
        Apply specific operator to solution and returns solution
        """
        raise NotImplementedError