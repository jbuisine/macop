2. Problem instance
===================


In this tutorial, we introduce the way of using `macop` and running your algorithm quickly.

2.1 Problem definition
~~~~~~~~~~~~~~~~~~~~~~

.. image:: ../_static/documentation/knapsack_problem.png
   :width:  300 px
   :align: center





2.2 Problem implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hence, we define our problem in Python:

- value of each component of knapsack
- weight associated to each of these components (objects)

.. code:: python
    
    """
    imports part
    """
    import random

    """
    Problem definition
    """
    random.seed(42)

    elements_score = [ random.randint(1, 20) for _ in range(30) ] # value of each object
    elements_weight = [ random.randint(5, 25) for _ in range(30) ] # weight of each object

First of all we need to define the kind of solution which best represent the problem. As example, we use the well known knapsack problem using 30 objects (solution size of 30).

