2. Problem instance
===================

In this tutorial, we introduce the way of using `macop` and running your algorithm quickly using a well the known `knapsack` problem.

2.1 Problem definition
~~~~~~~~~~~~~~~~~~~~~~

The **knapsack problem** is a problem in combinatorial optimization: Given a set of items, each with a weight and a value, determine the number of each item to include in a collection so that the total weight is less than or equal to a given limit and the total value is as large as possible.


The image below provides an illustration of the problem:

.. image:: ../_static/documentation/knapsack_problem.png
   :width:  300 px
   :align: center


In this problem, we try to optimise the value associated with the objects we wish to put in our backpack while respecting the capacity of the bag (weight constraint).

It is a combinatorial and therefore discrete problem. `Macop` decomposes its package into two parts, which is related to discrete optimisation on the one hand, and continuous optimisation on the other hand. This will be detailed later.


2.2 Problem implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hence, we define our problem in Python:

- values of each objects 
- weight associated to each of these objects

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

Once we have defined the instance of our problem, we will need to define the representation of a solution to that problem.
