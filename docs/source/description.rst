Description
=====================================

.. image:: _static/logo_macop.png
   :width: 350 px
   :align: center


Context
------------

Based on its generic behaviour, each **Macop** algorithm runs can be represented as an interactive loop where you can interact with and specify your needs at each step:

.. image:: _static/documentation/macop_behaviour.png
   :width: 450 px
   :align: center

The package is strongly oriented on combinatorial optimisation (hence discrete optimisation) but it remains possible to extend for continuous optimisation.

Motivation
~~~~~~~~~~

Flexible discrete optimisation package allowing a quick implementation of your problems. In particular it meets the following needs:

- **Common basis:** the interaction loop during the solution finding process proposed within the package is common to all heuristics. This allows the user to modify only a part of this interaction loop if necessary without rendering the process non-functional.
- **Hierarchy:** a hierarchical algorithm management system is available, especially when an algorithm needs to manage local searches. This hierarchy remains transparent to the user. The main algorithm will be able to manage and control the process of searching for solutions.
- **Flexibility:** although the algorithms are dependent on each other, it is possible that their internal management is different. This means that the ways in which solutions are evaluated and updated, for example, may be different.
- **Abstraction:** thanks to the modular separability of the package, it is quickly possible to implement new problems, solutions representation, way to evaluate, update solutions within the package.
- **Extensible:** the package is open to extension, i.e. it does not partition the user in these developer choices. It can just as well implement continuous optimization problems if needed while making use of the main interaction loop proposed by the package.
- **Easy Setup:** As a Pure Python package distributed is ``pip`` installable and easy to use.



Installation
------------

Just install package using `pip` Python package manager: 

.. code:: bash
   
   pip install macop
