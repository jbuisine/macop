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
        print("Runs test command...")

        # pass test using doctest
        #doctest.testmod(Algorithm)

        distutils.command.check.check.run(self)


setup(
    name='macop',
    version='0.3.3',
    description='Minimalist And Customizable Optimization Package',
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
        'macop.algorithms.mono', 
        'macop.algorithms.multi', 
        'macop.callbacks', 
        'macop.evaluators', 
        'macop.operators',  
        'macop.operators.mutators',  
        'macop.operators.crossovers',  
        'macop.operators.policies', 
        'macop.solutions', 
        'macop.utils'],
    install_requires=[
        'numpy',
    ],
    cmdclass={
        'test': TestCommand,
    },
    zip_safe=False)
