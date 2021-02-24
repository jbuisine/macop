# Minimalist And Customisable Optimisation Package

[![status](https://joss.theoj.org/papers/9ea7d55c4fa83808f96929cb87adff3e/status.svg)](https://joss.theoj.org/papers/9ea7d55c4fa83808f96929cb87adff3e) 
[![](https://img.shields.io/github/workflow/status/jbuisine/macop/build)](https://github.com/jbuisine/macop/actions/workflows/python-app.yml)
[![PyPI](https://img.shields.io/pypi/v/macop)](https://pypi.org/project/macop/) 
[![](https://img.shields.io/pypi/dm/macop)](https://pypi.org/project/macop/)
[![GitHub](https://img.shields.io/github/license/jbuisine/macop?style=flat)](https://github.com/jbuisine/macop/blob/master/LICENCE)

<p align="center">
    <img src="https://github.com/jbuisine/macop/blob/master/docs/source/_static/logo_macop.png" alt="" width="50%">
</p>


## Description

`Macop` is a python package for solving discrete optimisation problems in nature. Continuous optimisation can also applicable if needed. The objective is to allow a user to exploit the basic structure proposed by this package to solve a problem specific to him. The interest is that he can quickly abstract himself from the complications related to the way of evaluating, comparing, saving the progress of the search for good solutions but rather concentrate if necessary on his own algorithm. Indeed, `Macop` offers the following main and basic features: 

- **solutions:** representation of the solution;
- **validator:** such as constraint programmig, a `validator` is function which is used for validate or not a solution data state;
- **evaluator:** stores problem instance data and implement a `compute` method in order to evaluate a solution;
- **operators:** mutators, crossovers operators for update and obtain new solution;
- **policies:** the way you choose the available operators (might be using reinforcement learning);
- **algorithms:** generic and implemented optimisation research algorithms;
- **callbacks:** callbacks to automatically keep track of the search space advancement and restart from previous state if nedded.

<p align="center">
    <img src="https://github.com/jbuisine/macop/blob/master/docs/source/_static/documentation/macop_behaviour.png" alt="" width="50%">
</p>


## Motivation

Flexible discrete optimisation package allowing a quick implementation of your problems. In particular it meets the following needs:

- **Common basis:** the interaction loop during the solution finding process proposed within the package is common to all heuristics. This allows the user to modify only a part of this interaction loop if necessary without rendering the process non-functional.
- **Hierarchy:** a hierarchical algorithm management system is available, especially when an algorithm needs to manage local searches. This hierarchy remains transparent to the user. The main algorithm will be able to manage and control the process of searching for solutions.
- **Flexibility:** although the algorithms are dependent on each other, it is possible that their internal management is different. This means that the ways in which solutions are evaluated and updated, for example, may be different.
- **Abstraction:** thanks to the modular separability of the package, it is quickly possible to implement new problems, solutions representation, way to evaluate, update solutions within the package.
- **Extensible:** the package is open to extension, i.e. it does not partition the user in these developer choices. It can just as well implement continuous optimization problems if needed while making use of the main interaction loop proposed by the package.
- **Easy Setup:** as a pure Python package distributed is ``pip`` installable and easy to use.

## Target Audience 

This package would meet the expectations of people wishing to: 
- Solve a complex problem oriented evolutionary algorithm but who do not wish to develop their own framework. They can rely on what the package already proposes but also on its generic and flexible contribution in order to adapt their own content;
- Conduct research work leading to the rapid modification of meta-heuristics and the interaction of different algorithms. More precisely:
  - test new combinations of algorithms. Changing algorithms during evaluations, e.g. different local searches;
  - provide reinforcement learning during searches (e.g. adaptive operator choice strategy).
  - test new multi-objective methods quickly thanks to the proposed algorithmic hierarchy allowing to easily decompose the multi-objective problem into single-objective sub-problems.
- Take advantage of a system for launching calculations from a backup in order to avoid any loss in case of unwanted program interruption;
- Quickly model a problem that is still unknown, i.e. the type of solution and the evaluation function, while taking advantage of the interaction loop proposed by the package.

## Content

The primary advantage of using Python is that it allows you to dynamically add new members within the new implemented solution or algorithm classes. This of course does not close the possibilities of extension and storage of information within solutions and algorithms. It all depends on the need in question.

### In `macop.algorithms` module:

Both single and multi-objective algorithms have been implemented for demonstration purposes. 

A hierarchy between dependent algorithms is also available, based on a parent/child link, allowing quick access to global information when looking for solutions, such as the best solution found, the number of global evaluations.

The mono-objective Iterated Local Search algorithm which aims to perform local searches (child algorithms linked to the main algorithm) and then to explore again (explorations vs. exploitation trade-off). On the multi-objective side, the MOEA/D algorithm has been implemented by using the weighted-sum of objectives to change multi-objectives problem into a set of mono-objective (Tchebycheff approach can also be used). Hence, this algorithm aims at decomposing the multi-objective problem into `mu` single-objective problems in order to obtain the Pareto front where single-objective problems are so-called child algorithms linked to the multi-objective algorithm.

The main purpose of these developed algorithms is to show the possibilities of operational search algorithm implementations based on the minimalist structure of the library.

### In `macop.solutions` module:

Currently, only combinatorial solutions (discrete problem modelisation) are offered, with the well-known problem of the knapsack as an example. Of course, it's easy to add your own representations of solutions. Solutions modeling continuous problems can also be created by the anyone who wants to model his own problem.

### In `macop.operators` and `macop.policies` modules:

A few mutation and crossover operators have been implemented, however, it remains quite simple. What is interesting here is that it is possible to develop one's own strategy for choosing operators for the next evaluation. The available UCBPolicy class proposes this functionality as an example, since it will seek to propose the best operator to apply based on a method known as the Adaptive Operator Selection (AOS) via the use of the Upper Confidence Bound (UCB) algorithm. 

### In `macop.callbacks` module:

The use of callback instance, allows both to do an action every $k$ evaluations of information, but also to reload them once the run of the algorithm is cut. Simply inherit the abstract Callback class and implement the `apply` method to backup and `load` to restore. It is possible to add as many callbacks as required. Such as an example, implemented UCBPolicy has its own callback allowing the instance to reload previously collected statistics and restart using them.


## Documentation

Based on all of these generic and/or implemented functionalities, the user will be able to quickly develop a solution to his problem while retaining the possibility of remaining in control of his development by overloading existing functionalities if necessary.

Main idea about this Python package is that it does not which doesn't implement every algorithm in the literature but let the possibility to the user to quickly develop and test its own algorithms and strategies. The main objective of this package is to provide maximum flexibility, which allows for easy experimentation in implementation..

Fully documentation of package with examples is [available](https://jbuisine.github.io/macop). 

You can also see examples of use:
-  in the [knapsackExample.py](https://github.com/jbuisine/macop/blob/master/examples/knapsackExample.py) for mono-objective knapsack instance.
-  in the [knapsackMultiExample.py](https://github.com/jbuisine/macop/blob/master/examples/knapsackMultiExample.py) for multi-objective knapsack instance.
-  in the [qapExample.py](https://github.com/jbuisine/macop/blob/master/examples/qapExample.py) for mono-objective QAP instance.
-  in the [ubqpExample.py](https://github.com/jbuisine/macop/blob/master/examples/ubqpExample.py) for mono-objective UBQP problem instance.

## Add as dependency

```bash
git submodule add https://github.com/jbuisine/macop.git
```

## Current projects which use `Macop`:

- [@prise3d/noise-detection-attributes-optimization](https://github.com/prise-3d/noise-detection-attributes-optimization): use of a parent algorithm with the real (but very expensive) evaluation function, and then inner local searches which use a substitution model (a model that has learned to approximate the real cost function with a quick-to-evaluate function). Hence, two evaluation functions have been used in order to accelerate the search in the set of solutions.

## License

[The MIT License](LICENSE)