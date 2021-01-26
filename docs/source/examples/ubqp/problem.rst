UBQP problem definition
=======================

Understand the UBQP Problem
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Given a collection of :math:`n` items such that each pair of items is associated with a profit value that can be positive, negative or zero, unconstrained binary quadratic programming (UBQP) seeks a subset of items that maximizes the sum of their paired values. The value of a pair is accumulated in the sum only if the two corresponding items are selected. A feasible solution to a UBQP instance can be specified by a binary string of size :math:`n`, such that each variable indicates whether the corresponding item is included in the selection or not.


Mathematical definition
~~~~~~~~~~~~~~~~~~~~~~~

More formally, the conventional and single-objective UBQP problem is to maximize the following objective function:

:math:`f(x)=x′Qx=\sum_{i=1}^{n}{\sum_{j=1}^{n}{q_{ij}⋅x_i⋅x_j}}`

where :math:`Q=(q_{ij})` is an :math:`n` by :math:`n` matrix of constant values, :math:`x` is a vector of :math:`n` binary (zero-one) variables, i.e., :math:`x \in \{0, 1\}`, :math:`i \in \{1,...,n\}`, and :math:`x'` is the transpose of :math:`x`.
