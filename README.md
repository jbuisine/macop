# Minimalist And Customisable Optimisation Package

![](https://img.shields.io/github/workflow/status/jbuisine/macop/build?style=flat-square) ![](https://img.shields.io/pypi/v/macop?style=flat-square) ![](https://img.shields.io/pypi/dm/macop?style=flat-square)

<p align="center">
    <img src="https://github.com/jbuisine/macop/blob/master/docs/source/_static/logo_macop.png" alt="" width="50%">
</p>


## Description

`Macop` is a python package for solving discrete optimisation problems in nature. Continuous optimisation can also applicable if needed. The objective is to allow a user to exploit the basic structure proposed by this package to solve a problem specific to him. The interest is that he can quickly abstract himself from the complications related to the way of evaluating, comparing, saving the progress of the search for good solutions but rather concentrate if necessary on his own algorithm. Indeed, `Macop` offers the following main and basic features: 

- **solutions:** representation of the solution ;
- **validator:** such as constraint programmig, a `validator` is function which is used for validate or not a solution data state ;
- **evaluator:** stores problem instance data and implement a `compute` method in order to evaluate a solution ;
- **operators:** mutators, crossovers update of solution ;
- **policies:** the way you choose the available operators (might be using reinforcement learning) ;
- **algorithms:** generic and implemented optimisation research algorithms ;
- **callbacks:** callbacks to automatically keep track of the search space advancement.

<p align="center">
    <img src="https://github.com/jbuisine/macop/blob/master/docs/source/_static/documentation/macop_behaviour.png" alt="" width="50%">
</p>

Based on all of these generic and/or implemented functionalities, the user will be able to quickly develop a solution to his problem while retaining the possibility of remaining in control of his development by overloading existing functionalities if necessary.

Main idea about this Python package is that it does not which doesn't implement every algorithm in the literature but let the possibility to the user to quickly develop and test its own algorithms and strategies. The main objective of this package is to provide maximum flexibility, which allows for easy experimentation in implementation..

## Documentation

Fully documentation of package with examples is [available](https://jbuisine.github.io/macop). 

You can also see examples of use:
-  in the [knapsackExample.py](https://github.com/jbuisine/macop/blob/master/examples/knapsackExample.py) python file for mono-objective.
-  in the [knapsackMultiExample.py](https://github.com/jbuisine/macop/blob/master/examples/knapsackMultiExample.py) python file for multi-objective.

## Add as dependency

```bash
git submodule add https://github.com/jbuisine/macop.git
```

## License

[The MIT License](LICENSE)