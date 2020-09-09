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

Exploring all the solutions was not feasible given the large amount of exploration space available. Otherwise it would have been preferable to use a Recursive Features Elimination method [@DBLP:journals/remotesensing/PullanagariKY18, @DBLP:conf/icmla/ChenJ07].

# Application

Documentation with examples is available at [https://jbuisine.github.io/macop/](https://jbuisine.github.io/macop/).

# Acknowledgements

This work is supported by *Agence Nationale de la Recherche* : project ANR-17-CE38-0009

# References