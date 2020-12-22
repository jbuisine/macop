from setuptools import setup
import distutils.command.check

class TestCommand(distutils.command.check.check):
    """Custom test command."""

    def run(self):

        # run tests using doctest
        import doctest
        
        # folders
        # from macop.algorithms import Algorithm
        print("==============================")
        print("Run test program...")
        from macop.solutions.discrete import BinarySolution
        from macop.evaluators.knapsacks import KnapsackEvaluator

        from macop.operators.discrete.mutators import SimpleMutation
        from macop.operators.discrete.mutators import SimpleBinaryMutation
        from macop.operators.discrete.crossovers import SimpleCrossover
        from macop.operators.discrete.crossovers import RandomSplitCrossover

        from macop.policies.classicals import RandomPolicy
        from macop.policies.reinforcement import UCBPolicy

        from macop.algorithms.mono import IteratedLocalSearch as ILS
        from macop.callbacks.classicals import BasicCheckpoint
        import random

        random.seed(42)

        elements_score = [ random.randint(1, 20) for _ in range(30) ]
        elements_weight = [ random.randint(2, 5) for _ in range(30) ]

        def knapsackWeight(solution):

            weight_sum = 0
            for index, elem in enumerate(solution._data):
                weight_sum += elements_weight[index] * elem

            return weight_sum

        # default validator
        def validator(solution):

            if knapsackWeight(solution) <= 80:
                return True
            else:
                False

        # define init random solution
        def init():
            return BinarySolution([], 30).random(validator)

        evaluator = KnapsackEvaluator(data={'worths': elements_score})
        operators = [SimpleBinaryMutation(), SimpleMutation(), SimpleCrossover(), RandomSplitCrossover()]
        policy = UCBPolicy(operators)
        # callback = BasicCheckpoint(_every=5, _filepath=filepath)

        algo = ILS(init, evaluator, operators, policy, validator, maximise=True, verbose=False)
        
        # add callback into callback list
        # algo.addCallback(callback)
        algo.run(200)

        print("==============================")
        print("Run test using doctest...")

        # pass test using doctest
        distutils.command.check.check.run(self)


setup(
    name='macop',
    version='1.0.5',
    description='Minimalist And Customisable Optimisation Package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Utilities'
    ],
    url='https://github.com/prise-3d/macop',
    author='Jérôme BUISINE',
    author_email='jerome.buisine@univ-littoral.fr',
    license='MIT',
    packages=['macop', 
        'macop.algorithms', 
        'macop.callbacks', 
        'macop.evaluators',  
        'macop.operators',  
        'macop.operators.discrete',
        'macop.operators.continuous',  
        'macop.policies', 
        'macop.solutions', 
        'macop.utils'],
    install_requires=[
        'numpy',
    ],
    cmdclass={
        'test': TestCommand,
    },
    zip_safe=False)
