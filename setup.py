from setuptools import setup
import distutils.command.check

class TestCommand(distutils.command.check.check):
    """Custom test command."""

    def run(self):

        # run tests using doctest
        import doctest
        
        # discrete solutions module
        from macop.solutions import discrete
        from macop.solutions import continuous
        

        # run all doctest
        print("==============================")
        print("Runs test command...")
        
        # discrete solutions module
        doctest.testmod(discrete)
        doctest.testmod(continuous)

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
