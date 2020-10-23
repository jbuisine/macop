---
title: 'Minimalist And Customizable Optimization Package'
tags:
  - Python
  - Operations Research
  - Mono-objective
  - Multi-objective
authors:
  - name: Jérôme BUISINE
    orcid: 0000-0001-6071-744X
    affiliation: 1 # (Multiple affiliations must be quoted)
affiliations:
 - name: Univ. Littoral Côte d’Opale, LISIC Calais, France, F-62100
   index: 1
date: 11 October 2020
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
#aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
#aas-journal: Astrophysical Journal <- The name of the AAS journal.
---

# Summary

Optimisation problems are frequently encountered in science and industry. Given a real-valued function $f$ defined on a set called the search space $X$, optimising the function $f$ consists of finding a point $x \in X$ en that has the optimal value $f(x)$, or at least constructing a sequence $(x_t)_{t \in \mathbf{N} \in X^\mathbf{N}$ that is close to the optimum. Depending on the search space $X$, optimisation problems can be globally classified as discrete problems (e.g. $X={0,1}^n$) or as continuous problems (e.g. $X=\mathbf{R}^n$). Tools for modelling and solving discrete and continuous problems are proposed in the literature.

In this paper, `Macop` for `Minimalist And Customizable Optimization Package`, is a proposed optimization Python package which doesn't implement the whole available algorithms in the literature, but let you the possibility to quickly develop and test your own algorithm and strategies. The main objective of this package is to be the most flexible as possible and hence, to offer a maximum of implementation possibilities.

An underlying objective is to enable this package to be used for quick implementations and in educational contexts as well. Allowing students to quickly develop their own algorithms.

# Motivation

Most of the operational research libraries developed in Python offer users either problems and algorithms where it is possible to choose parameters to obtain optimal (or near optimal) results such as [pyomo](http://www.pyomo.org/documentation), [PuLP](https://pypi.org/project/PuLP/), [pyOpt](http://www.pyopt.org/), [PySCIPOpt](https://github.com/SCIP-Interfaces/PySCIPOpt), or, libraries targeted to a specific problem or algorithm such as [simanneal](https://github.com/perrygeo/simanneal).

During thesis work, the search for a solution with complex evaluation was necessary. The assessment in question consisted of evaluating a model fitted with a selected subset of available features for a feature set. Binary solution was used as appreciation for selected or non-selected feature from the available set of features. The solution was therefore a new model obtained and its fitness which is the score obtained on the test data set. Exploring all the solutions was not feasible given the large amount of exploration space available. Otherwise, it would have been preferable to use a Recursive Features Elimination (RFE) method [@DBLP:journals/remotesensing/PullanagariKY18; @DBLP:conf/icmla/ChenJ07].

This is why it was preferred to focus on operational research methods, even if the optimal solution is not found, a good solution is still sufficient for the study case. Available libraries in the literature did not allow this kind of implementation of an evaluation function quickly and this is why the development of a Python package has been undertaken. This package was then adapted to correspond to a formalism of implementing algorithms and problems from a simple and generic structure, hence the term minimalist in Macop.

# Description

At the beginning of the development of this library, the idea of making it as modular as possible was topical. By dividing the library into sub-module forms considered to be the most important to build and solve an optimisation problem.

The package consists of main several modules:

- `algorithms`: generic and implemented OR algorithms.
- `evaluator`: contains all the implemented evaluation functions.
- `solutions`: all declared solutions classes used to represent problem data.
- `operators`: mutators, crossovers update of solution. This module also has policy classes to manage the way of update and use solution.
- `callbacks`: contains Callback classes for making callback instructions every number of evaluations.

The primary advantage of using Python is that it allows you to dynamically add new members within the new implemented solution or algorithm classes. This of course does not close the possibilities of extension and storage of information within solutions and algorithms. It all depends on the need in question.

## Implemented algorithms

Both single and multi-objective algorithms have been implemented for demonstration purposes. 

A hierarchy between dependent algorithms is also available, based on a parent/child link, allowing quick access to global information when looking for solutions, such as the best solution found, the number of global evaluations.

The mono-objective Iterated Local Search [@DBLP:books/sp/03/LourencoMS03] algorithm which aims to perform local searches (child algorithms linked to the main algorithm) and then to explore again (explorations vs. exploitation trade-off). On the multi-objective side, the MOEA/D algorithm [@DBLP:journals/tec/ZhangL07] has been implemented by using the weighted-sum of objectives to change multi-objectives problem into a set of mono-objective (Tchebycheff approach can also be used [@DBLP:journals/cor/AlvesA07]). Hence, this algorithm aims at decomposing the multi-objective problem into $mu$ single-objective problems in order to obtain the Pareto front [@kim2005adaptive] where single-objective problems are so-called child algorithms linked to the multi-objective algorithm.

The main purpose of these developed algorithms is to show the possibilities of operational search algorithm implementations based on the minimalist structure of the library.

## Available solutions

Currently, only combinatorial solutions (discrete problem modelisation) are offered, with the well-known problem of the knapsack as an example. Of course, it's easy to add your own representations of solutions. Solutions modeling continuous problems can also be created by the anyone who wants to model his own problem.

## Update solutions

A few mutation and crossover operators have been implemented, however, it remains quite simple. What is interesting here is that it is possible to develop one's own strategy for choosing operators for the next evaluation. The available UCBPolicy class proposes this functionality as an example, since it will seek to propose the best operator to apply based on a method known as the Adaptive Operator Selection (AOS) via the use of the Upper Confidence Bound (UCB) algorithm [@DBLP:journals/tec/LiFKZ14]. 

## Callback feature

The use of callback instance, allows both to do an action every $k$ evaluations of information, but also to reload them once the run of the algorithm is cut. Simply inherit the abstract Callback class and implement the `apply` method to backup and `load` to restore. It is possible to add as many callbacks as required. Such as an example, implemented UCBPolicy has its own callback allowing the instance to reload previously collected statistics and restart using them.

## Documentation

Fully documented examples for mono and multi-objectives implementations are available at [https://jbuisine.github.io/macop/](https://jbuisine.github.io/macop/).

# Conclusion

Macop aims to allow the modelling of discrete (usually combinatorial), and continuous problems. It is therefore open to expansion and not closed specifically to a problem.

Macop proposes a simple structure of interaction of the main elements (algorithms, operators, solutions, AOS, callbacks) for the resolution of operational research problems. From its generic structure, it is possible, thanks to the dynamic programming paradigm of the Python language, to easily allow the extension and development of new algorithms and problems. Based on simple concepts, this package can therefore meet the needs of the rapid problem implementation. It can also be used for quick case studies.

# Acknowledgements

This work is supported by *Agence Nationale de la Recherche* : project ANR-17-CE38-0009

# References