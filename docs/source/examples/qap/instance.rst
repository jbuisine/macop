QAP Problem instance generation
===============================

To define our quadratic assignment problem instance, we will use the available mQAP_ multi-objective quadratic problem generator. 

Genration of the instance
~~~~~~~~~~~~~~~~~~~~~~~~~

We will limit ourselves here to a single objective for the purposes of this example. The file **makeQAPuni.cc**, will be used to generate the instance.

.. code:: bash

    g++ makeQAPuni.cc -o mQAPGenerator
    ./mQAPGenerator -n 100 -k 1 -f 30 -d 80 -s 42 > qap_instance.txt

with the following parameters:

- **-n** positive integer: number of facilities/locations;
- **-k** positive integer: number of objectives;
- **-f** positive integer: maximum flow between facilities;
- **-d** positive integer: maximum distance between locations;
- **-s** positive long: random seed.

The generated qap_instance.txt_ file contains the two matrices :math:`F` and :math:`D` and define our instance problem.

.. _mQAP: https://www.cs.bham.ac.uk/~jdk/mQAP/

.. _qap_instance.txt: https://github.com/jbuisine/macop/blob/master/examples/instances/qap/qap_instance.txt


Load data instance
~~~~~~~~~~~~~~~~~~


We are now going to load this instance via a Python code which will be useful to us later on:

.. code:: Python

    qap_instance_file = 'qap_instance.txt'

    n = 100 # the instance size

    with open(qap_instance_file, 'r') as f:
        file_data = f.readlines()
        print(f'Instance information {file_data[0]}')

        D_lines = file_data[1:n + 1]
        D_data = ''.join(D_lines).replace('\n', '')

        F_lines = file_data[n:2 * n + 1]
        F_data = ''.join(F_lines).replace('\n', '')

    D_matrix = np.fromstring(D_data, dtype=float, sep=' ').reshape(n, n)
    print(f'D matrix shape: {D_matrix.shape}')
    F_matrix = np.fromstring(F_data, dtype=float, sep=' ').reshape(n, n)
    print(f'F matrix shape: {F_matrix.shape}')

.. note::
    As we know the size of our instance and the structure of the document, it is quite quick to look for the lines related to the :math:`F` and :math:`D` matrices.