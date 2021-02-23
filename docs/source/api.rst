API
=============

Modules description
~~~~~~~~~~~~~~~~~~~

**Macop** offers the following main and basic features: 

- **algorithms:** generic and implemented optimisation research algorithms;
- **callbacks:** callbacks to automatically keep track of the search space advancement and restart from previous state if nedded;
- **evaluator:** stores problem instance data and implement a `compute` method in order to evaluate a solution;
- **operators:** mutators, crossovers operators for update and obtain new solution;
- **policies:** the way you choose the available operators (might be using reinforcement learning);
- **solutions:** representation of the solution;
- **validator:** such as constraint programmig, a `validator` is function which is used for validate or not a solution data state.


Common and base modules
~~~~~~~~~~~~~~~~~~~~~~~

The modules presented in this section are common to all types of optimisation problems. The abstract classes proposed here form the basis of the package's structure.

macop.algorithms
-------------------

.. autosummary::
   :toctree: macop
   
   macop.algorithms.base
      
   macop.algorithms.mono
   macop.algorithms.multi

macop.callbacks
-------------------

.. autosummary::
   :toctree: macop
   
   macop.callbacks.base

   macop.callbacks.classicals
   macop.callbacks.multi
   macop.callbacks.policies

macop.evaluators
-------------------

.. autosummary::
   :toctree: macop
   
   macop.evaluators.base

macop.operators
-------------------

.. autosummary::
   :toctree: macop
   
   macop.operators.base

macop.policies
-------------------

.. autosummary::
   :toctree: macop
   
   macop.policies.base
      
   macop.policies.classicals
   macop.policies.reinforcement

macop.solutions
-------------------

.. autosummary::
   :toctree: macop

   macop.solutions.base

macop.utils
-------------------

.. autosummary::
   :toctree: macop

   macop.utils.progress


Discrete Optimisation
~~~~~~~~~~~~~~~~~~~~~

Some implementations of discrete optimisation problem functionalities are available. They can be used as example implementations or can simply be used by the user.

macop.evaluators
-------------------

.. autosummary::
   :toctree: macop
   
   macop.evaluators.discrete.mono
   macop.evaluators.discrete.multi

macop.operators
-------------------

.. autosummary::
   :toctree: macop
   
   macop.operators.discrete.mutators
   macop.operators.discrete.crossovers

macop.solutions
-------------------

.. autosummary::
   :toctree: macop

   macop.solutions.discrete


Continuous Optimisation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Although continuous optimization is not the priority of this package, the idea is to leave the possibility to any user to implement or even propose implementations related to this kind of problem. The modules are here for the moment nearly empty (only with Zdt functions example) but present to establish the structure relative to these types of implementations.

If a user wishes to propose these developments so that they can be added in a future version of the package, he can refer to the guidelines_ for contributions of the package.

.. _guidelines: https://github.com/prise-3d/macop/blob/master/CONTRIBUTING.md

macop.evaluators
-------------------

.. autosummary::
   :toctree: macop
   
   macop.evaluators.discrete.mono
   macop.evaluators.discrete.multi

macop.operators
-------------------

.. autosummary::
   :toctree: macop
   
   macop.operators.continuous.mutators
   macop.operators.continuous.crossovers

macop.solutions
-------------------

.. autosummary::
   :toctree: macop

   macop.solutions.continuous