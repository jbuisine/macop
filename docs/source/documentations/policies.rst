7. Operator choices
===================

The ``policy`` feature of **Macop** enables to choose the next operator to apply during the search process of the algorithm based on specific criterion.

7.1. Why using policy ?
~~~~~~~~~~~~~~~~~~~~~~~

Sometimes the nature of the problem and its instance can strongly influence the search results when using mutation operators or crossovers. 
Automated operator choice strategies have been developed in the literature, notably based on reinforcement learning.

.. note::
    An implementation by reinforcement has been developed as an example in the ``macop.policies.reinforcement`` module. 
    However, it will not be detailed here. You can refer to the API documentation for more details.

7.2. Custom policy
~~~~~~~~~~~~~~~~~~