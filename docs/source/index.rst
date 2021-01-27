Minimalist And Customisable Optimisation Package
================================================

.. image:: _static/logo_macop.png
   :width: 300 px
   :align: center

What's **Macop** ?
~~~~~~~~~~~~~~~~~~

**Macop** is a discrete optimisation Python package which not which doesn't implement every algorithm in the literature but provides the ability to quickly develop and test your own algorithm and strategies. The main objective of this package is to provide maximum flexibility, which allows for easy experimentation in implementation.


Contents
~~~~~~~~

.. toctree::
   :maxdepth: 1

   description

   documentations

   api

   examples

   contributing


Motivation
~~~~~~~~~~

Flexible discrete optimisation package allowing a quick implementation of your problems. In particular it meets the following needs:

- **Common basis:** the interaction loop during the solution finding process proposed within the package is common to all heuristics. This allows the user to modify only a part of this interaction loop if necessary without rendering the process non-functional.
- **Hierarchy:** a hierarchical algorithm management system is available, especially when an algorithm needs to manage local searches. This hierarchy remains transparent to the user. The main algorithm will be able to manage and control the process of searching for solutions.
- **Flexibility:** although the algorithms are dependent on each other, it is possible that their internal management is different. This means that the ways in which solutions are evaluated and updated, for example, may be different.
- **Abstraction:** thanks to the modular separability of the package, it is quickly possible to implement new problems, solutions representation, way to evaluate, update solutions within the package.
- **Extensible:** the package is open to extension, i.e. it does not partition the user in these developer choices. It can just as well implement continuous optimization problems if needed while making use of the main interaction loop proposed by the package.
- **Easy Setup:** As a Pure Python package distributed is `pip` installable and easy to use.


Indices and tables
~~~~~~~~~~~~~~~~~~

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
