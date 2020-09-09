---
title: 'Minimalist And Customizable Optimization Package'
tags:
  - Python
  - Operations Research
  - Multi-objective
authors:
  - name: Jérôme BUISINE
    orcid: 0000-0001-6071-744X
    affiliation: 1 # (Multiple affiliations must be quoted)
affiliations:
 - name: Univ. Littoral Côte d’Opale, LISIC Calais, France, F-62100
   index: 1
date: 9 September 2020
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
#aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
#aas-journal: Astrophysical Journal <- The name of the AAS journal.
---

# Summary

`Macop` for `Minimalist And Customizable Optimization Package` is an optimization Python package which not implement the whole available algorithms in the literature but let you the possibility to quickly develop and test your own algorithm and strategies. The main objective of this package is to be the most flexible as possible and hence, to offer a maximum of implementation possibilities.

An underlying objective is to enable this package to be used in educational contexts as well. Allowing students to quickly develop their own algorithms.

# Motivation

During thesis work, the search for a solution with complex evaluation was necessary. The assessment in question consisted of evaluating a model fited with selected subset of available features from a features set. The solution was therefore the new model obtained and its fitness, the score obtained on this test basis.

Exploring all the solutions was not feasible given the large amount of exploration space available. Otherwise it would have been preferable to use a Recursive Features Elimination method [@DBLP:journals/remotesensing/PullanagariKY18; @DBLP:conf/icmla/ChenJ07].

This is why it was preferred to focus on operational research and to develop this python package. Even if the optimal solution is not found, a good solution is still sufficient.

# Description

At the beginning of the development of this tool, the idea of making it as modular as possible was topical.

The package consists of several modules:

- `algorithms`: generic and implemented OR algorithms.
- `evaluator`: contains all the implemented evaluation functions.
- `solutions`: all declared solutions classes used to represent problem data.
- `operators`: mutators, crossovers update of solution. This module also has policies classes to manage the way of update and use solution.
- `callbacks`: contains Callback class implemenration for making callback instructions every number of evaluations.


## Implemented algorithms

Both single and multi-objective algorithms have been implemented for demonstration purposes. The mono-objective Iterated Local Search [@DBLP:books/sp/03/LourencoMS03] algorithm which aims to perform local searches and then to explore again (explorations vs. exploitation trade-off). On the multi-objective side, the MOEA/D algorithm [@DBLP:journals/tec/ZhangL07] has been implemented using the weighted-sum of objectives method (Tchebycheff approach can also be used [@DBLP:journals/cor/AlvesA07]). This algorithm aims at decomposing the multi-objective problem into $mu$ under single-objective problem in order to obtain the pareto front.

## Available solutions

Currently, only combinatorial solutions are offered, with the well-known problem of the knapsack as an example. Of course, it's easy to add your own representations of solutions.

## Update solutions

A few mutation and crossover operators have been implemented, however it remains quite simple. What is interesting here is that it is possible to develop one's own strategy for choosing operators for the next evaluation. The available UCBPolicy class proposes this functionality as an example, since it will seek to propose the best operator to apply based on a method known as Adaptive Operator Selection (AOS) via the use of the Upper Confidence Bound (UCB) algorithm [@DBLP:journals/tec/LiFKZ14]. 

## Backup feature

The use of callback instance allows both to save all the $k$ evaluations of the information but also to reload them once the run of the algorithm is cut. Simply inherit the abstract Callback class and implement the `apply` method to backup and `load` to restore. It is possible to add as many callbacks as required.

## Documentation

Documentation with examples for mono and multi objective implemenration is available at [https://jbuisine.github.io/macop/](https://jbuisine.github.io/macop/).

# Acknowledgements

This work is supported by *Agence Nationale de la Recherche* : project ANR-17-CE38-0009

# References