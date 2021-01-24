from setuptools import setup
import distutils.command.check

class TestCommand(distutils.command.check.check):
    """Custom test command."""

    def run(self):

        # run tests using doctest
        import doctest

        # set specific seed for pseudo-random process
        import random
        import numpy as np

        # discrete and continuous solutions module
        from macop.solutions import discrete
        from macop.solutions import continuous

        # operators module
        from macop.operators.discrete import mutators as discrete_mutators
        from macop.operators.discrete import crossovers as discrete_crossovers

        # policies module
        from macop.policies import classicals
        from macop.policies import reinforcement

        # evaluators module
        from macop.evaluators.discrete import mono as discrete_mono
        from macop.evaluators.discrete import multi as discrete_multi

        # algorithms
        from macop.algorithms import mono as algo_mono
        from macop.algorithms import multi as algo_multi

        # run all doctest
        print("==============================")
        print("Runs test command...")

        random.seed(42)
        np.random.seed(42)
        # discrete solutions module
        doctest.testmod(discrete)
        doctest.testmod(continuous)

        random.seed(42)
        np.random.seed(42)
        # operators module
        doctest.testmod(discrete_mutators)
        doctest.testmod(discrete_crossovers)

        random.seed(42)
        np.random.seed(42)
        # policies module
        doctest.testmod(classicals)
        doctest.testmod(reinforcement)

        random.seed(42)
        np.random.seed(42)
        # policies module
        doctest.testmod(discrete_mono)
        doctest.testmod(discrete_multi)

        random.seed(42)
        np.random.seed(42)
        # policies module
        doctest.testmod(algo_mono)
        doctest.testmod(algo_multi)

        # pass test using doctest
        distutils.command.check.check.run(self)


setup(
    name='macop',
    version='1.0.8',
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
        'macop.evaluators.discrete',
        'macop.evaluators.continuous',
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
