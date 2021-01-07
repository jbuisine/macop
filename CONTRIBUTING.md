Contribution guidelines
=====================================

<p align="center">
    Minimalist And Customisable Optimisation Package
</p>


# Welcome !

Thank you for taking the time to read this guide for the package's contribution. I'm glad to know that you may bring a lot to the **Macop** package. This document will show you the good development practices used in the project and how you can easily participate in its evolution!

# Table of contents

1. [Naming conventions](#naming-conventions)

    1.1. [Git naming conventions](#git-naming-conventions)

    1.2. [Package modules conventions](#package-modules-conventions)

2. [Coding conventions](#coding-conventions)

    2.1. [Python conventions](#python-conventions)

    2.3. [Code documentation](#code-documentation)

    2.2. [Test implementation](#test-implementation)

3. [Submission process](#submission-process)

    3.1. [Build package](#build-package)

    3.2. [Pull request](#pull-request)

4. [Request an enhancement or report a bug](#request-an-enhancement-or-report-a-bug)

# Naming conventions

## Git naming conventions

This project uses the naming conventions of the git branches set up by the [git-flow](https://danielkummer.github.io/git-flow-cheatsheet/) interface. To make your contribution as easy as possible to inject into the project, you will need to name your git branch as follows:

```bash
git branch feature/YourFeatureBranchName
```

Using git-flow interface:

```bash
git flow feature start YourFeatureBranchName
```

## Package modules conventions

As you perhaps already saw, package contains multiples modules and submodules. It's really import to be well organized package and let it intuitive to access as possible to features.

For the moment there are no precise conventions on the naming of new modules or sub-modules, it must just in a first step respect the hierarchy already in place and avoid any redundancies.

In order to facilitate the integration of new modules, do not hesitate to let me know the name it could have beforehand.

# Coding conventions

## Python conventions

This project follows the [coding conventions](http://google.github.io/styleguide/pyguide.html) implemented by Google. To help you to format **\*.py** files, it is possible to use the [yapf](https://github.com/google/yapf/) package developed by Google.

Note that the **yapf** package is used during build process of **macop** package to format the whole code following these conventions.

## Code documentation

In order to allow quick access to the code, the project follows the documentation conventions (docstring) proposed by Google. Here an example:

```python
''' Binary integer solution class

    - store solution as a binary array (example: [0, 1, 0, 1, 1])
    - associated size is the size of the array
    - mainly use for selecting or not an element in a list of valuable objects

    Attributes:
       data: {ndarray} --  array of binary values
       size: {int} -- size of binary array values
       score: {float} -- fitness score value
'''
```

You can generate documentation and display updates using these following commands:

```
bash build.sh
firefox docs/index.html
```

Do not forget to generate new documentation output before doing a pull request.

## Test implementation

This project use the [doctest](https://docs.python.org/3/library/doctest.html) package which enables to write tests into documentation as shown in example below:

# TODO : add custom example
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
    >>> sum(solution._data) == 3
    True
    >>> # clone solution
    >>> solution_copy = solution.clone()
    >>> all(solution_copy._data == solution._data)
"""
```

Moreover, tests written are displayed into generated documentation and let examples of how to use the developed function.

# Submission process

## Build pakcage

One thing to do before submit your feature is to build the package:

```bash
python setup.py build
```

This command do a lot of thing for you:
  - Runs the tests from documentation and raise errors if there are.
  - Formats all **\*.py** inside *macop* folder using **yapf**.

Do not forget to build documentation as explained in section [2.3](#code-documentation).

Or directly use bash script which runs all you need:

```bash
bash build.sh
```

## Pull request

Once you have built the package following previous instructions. You can make a pull request using GitHub. A [documentation](https://help.github.com/articles/about-pull-requests/) about pull requests is available.

# Request an enhancement or report a bug

To enhance the package, do not hesitate to report bug or missing feature. To do that, just submit an issue using at one of this labels:

- **feature** or **idea**: for new an enhancement to develop
- **bug:** for a detected bug

You can also add your own labels too or add priority label:

- prio:**low**
- prio:**normal**
- prio:**high**

Main common required issue header:

```
Package version: X.X.X
Issue label: XXXXX
Priority: prio:**level**
Targeted modules: `macop.algorithms`, `macop.policies`
Operating System: Manjaro Linux

Description: XXXXX
```

Whatever the problem reported, I will thank you for your contribution to this project. So do not hesitate.
