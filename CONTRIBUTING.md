How to contribute
=====================================

<p align="center">
    <img src="https://github.com/jbuisine/macop/blob/master/docs/source/_static/logo_macop.png" alt="" width="40%">
</p>



# Welcome !

Thank you for taking the time to read this guide for the package's contribution. I'm glad to know that you may bring a lot to the **Macop** package. This document will show you the good development practices used in the project and how you can easily participate in its evolution!

# Table of contents

1. [Submission processes](#submission-process)

    1.1. [Submit an issue](#submit-an-issue)

    1.2. [Pull request](#pull-request)

    1.3. [Seek support](#seek-support)

2. [Coding conventions](#coding-conventions)

    2.1. [Python conventions](#python-conventions)

    2.2. [Code documentation](#code-documentation)

    2.3. [Testing](#test-implementation)


# Submission process

## Submit an issue

Do not hesitate to report bug or issue in [https://github.com/jbuisine/macop/issues](https://github.com/jbuisine/macop/issues) with the common template header:

```
**Package version:** X.X.X
**Issue label:** XXXXX
**Targeted modules:** `macop.algorithms`, `macop.policies`
**Operating System:** Manjaro Linux

**Description:** XXXXX
```

## Pull request

If you have made changes to the project you have forked, you can submit a pull request in [https://github.com/jbuisine/macop/pulls](https://github.com/jbuisine/macop/pulls) in order to have your changes added inside new version of the `Macop` package. A [GitHub documentation](https://help.github.com/articles/about-pull-requests/) about pull requests is available if necessary.

To enhance the package, do not hesitate to fix bug or missing feature. To do that, just submit your pull request with this common template header:

```
**Package version:** X.X.X
**Enhancements label:** XXXXX
**Targeted modules:** `macop.algorithms`, `macop.policies`
**New modules:** `macop.XXXX`, `macop.algorithms.XXXX`

**Description:** XXXXX
```

**Note:** the code conventions required for the approval of your changes are described below.

Whatever the problem reported, I will thank you for your contribution to this project. So do not hesitate.

## Seek support

If you have any problem with the use of the package, issue or pull request submission, do not hesitate to let a message to [https://github.com/jbuisine/macop/discussions](https://github.com/jbuisine/macop/discussions). Especially in the question and answer section. 

You can also contact me at the following email address: `contact@jeromebuisine.fr`.

# Coding conventions

## Python conventions

This project follows the [coding conventions](http://google.github.io/styleguide/pyguide.html) implemented by Google. To help you to format **\*.py** files, it is possible to use the [yapf](https://github.com/google/yapf/) Python package developed by Google.

```
yapf -ir -vv macop
```

**Note:** you need at least Python version >=3.7.0.

## Package modules conventions

As you perhaps already saw, package contains multiples modules and submodules. It's really import to be well organized package and let it intuitive to access as possible to features.

`Macop` is mainly decompose into discrete and continuous optimisation. Especially if you want to offer continuous optimisation problems, modules are already available for this purpose. You can refer to the [documentation](https://jbuisine.github.io/macop) if necessary.

In order to facilitate the integration of new modules, do not hesitate to let me know the name it could have beforehand in your pull request.

## Code documentation

In order to allow quick access to the code, the project follows the documentation conventions (docstring) proposed by Google. Here an example:

```python
class BinarySolution():
"""Binary integer solution class

    - store solution as a binary array (example: [0, 1, 0, 1, 1])
    - associated size is the size of the array
    - mainly use for selecting or not an element in a list of valuable objects

    Attributes:
       data: {ndarray} --  array of binary values
       size: {int} -- size of binary array values
       score: {float} -- fitness score value
"""
```

For method:
```python
class BinarySolution():

...

def random(self, validator):
    """
    Intialize binary array with use of validator to generate valid random solution

    Args:
        size: {int} -- expected solution size to generate
        validator: {function} -- specific function which validates or not a solution (if None, not validation is applied)

    Returns:
        {:class:`~macop.solutions.discrete.BinarySolution`}: new generated binary solution
    """
    ...
```

You can generate documentation and display updates using these following commands:

```
bash build.sh
firefox docs/build/index.html
```

## Test implementation

This project uses the [doctest](https://docs.python.org/3/library/doctest.html) package which enables to write tests into documentation as shown in example below:

```python
""" Initialise binary solution using specific data

    Args:
        data: {ndarray} --  array of binary values
        size: {int} -- size of binary array values

    Example:

    >>> from macop.solutions.discrete import BinarySolution
    >>> # build of a solution using specific data and size
    >>> data = [0, 1, 0, 1, 1]
    >>> solution = BinarySolution(data, len(data))
    >>> # check data content
    >>> sum(solution.data) == 3
    True
    >>> # clone solution
    >>> solution_copy = solution.clone()
    >>> all(solution_copy._data == solution.data)
"""
```

Moreover, tests written are displayed into generated documentation and show examples of how to use the developed features.
