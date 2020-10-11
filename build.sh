#! bin/bash

# Format code
echo "Use of yapf package to format code.."
yapf -ir -vv macop

# Build rawls package
echo "Build package..."
python setup.py build
python setup.py test

echo "Build documentation..."
rm -r docs/source/macop
cd docs && make clean && make html