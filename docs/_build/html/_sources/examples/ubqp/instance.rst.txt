UBQP Problem instance generation
================================

To define our quadratic assignment problem instance, we will use the available mUBQP_ multi-objective quadratic problem generator. 

Genration of the instance
~~~~~~~~~~~~~~~~~~~~~~~~~

We will limit ourselves here to a single objective for the purposes of this example. The available file **mubqpGenerator.R**, will be used to generate the instance (using R language).

.. code:: bash

    Rscript mubqpGenerator.R 0.8 1 100 5 42 ubqp_instance.txt

The main parameters used for generating our UBQP instance are:

- **ρ:** the objective correlation coefficient
- **M:** the number of objective functions
- **N:** the length of bit strings
- **d:** the matrix density (frequency of non-zero numbers)
- **s:** seed to use

.. _mUBQP: http://mocobench.sourceforge.net/index.php?n=Problem.MUBQP

.. _ubqp_instance.txt: https://github.com/jbuisine/macop/blob/master/examples/instances/ubqp/ubqp_instance.txt

Load data instance
~~~~~~~~~~~~~~~~~~

We are now going to load this instance via a Python code which will be useful to us later on:

.. code:: Python

    qap_instance_file = 'ubqp_instance.txt'

    n = 100 # the instance size

    # load UBQP instance
    with open(ubqp_instance_file, 'r') as f:

        lines = f.readlines()

        # get all string floating point values of matrix
        Q_data = ''.join([ line.replace('\n', '') for line in lines[8:] ])

        # load the concatenate obtained string
        Q_matrix = np.fromstring(Q_data, dtype=float, sep=' ').reshape(n, n)

    print(f'Q_matrix {Q_matrix.shape}')

.. note::
    As we know the size of our instance and the structure of the document (header size), it is quite quick to look for the lines related to the :math:`Q` matrix.