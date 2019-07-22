# define policy to choose `updator` function at current iteration
class Policy():

    # here you can define your statistical variables for choosing next operator to apply

    def __init__(self, _updators):
        self.updators = _updators

    def apply(self, solution):
        """
        Apply specific updator to solution and returns solution
        """
        raise NotImplementedError