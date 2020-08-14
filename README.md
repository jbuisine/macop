# Minimalist And Customizable Optimizations Package

![](https://github.com/prise-3d/macop/workflows/build/badge.svg) ![](https://github.com/prise-3d/macop/workflows/pypi/badge.svg)

<p align="center">
    <img src="https://github.com/prise-3d/macop/blob/master/logo_macop.png" alt="" width="50%">
</p>


## Description

Optimisation generic framework built for optimization problem during thesis

## Modules

- **algorithms:** generic and implemented OR algorithms
- **evaluator:** example of an evaluation function to use (you have to implement your own evaluation function)
- **solutions:** solutions used to represent problem data
- **operators:** mutators, crossovers update of solution. This folder also had `policies` folder to manage the way of update and use solution.
- **checkpoints:** checkpoints folder where `Checkpoint` class is available for making checkpoint every number of evaluations.
  
**Note:** you can pass a custom `validator` function to the algorithm in order to check is solution is always correct for your needs after an update.

## How to use ?

You can see an example of use in the `mainExample.py` python file.

## Add as dependency

```bash
git submodule add https://github.com/prise-3d/macop.git
```

## License

[The MIT License](LICENSE)