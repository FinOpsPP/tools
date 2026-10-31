# FinOps++ Style Guide

Style can mean a lot. It may provide a sense of structure, can act as a mark of quality, enable understanding for new user, or even aid in recognition of a project. In may ways, style is the beating heart of the FinOps++ streaming from the desire to produce exactly these outcomes.

To help with this, when designing the structure of the Assessments project, we looked closely at how to provide a style scaffolding via time-tested specifications and popular linters.

## Linting

It is strongly recommended to use [pylint](https://www.pylint.org/) for linting for python code.

There are built-in configuration files for these in the top-level directory of this project that will help make sure your code is compliant with the project's standards. These packages can be pretty easily installed in [CLI Tool](/src/README.md) with the following modification to the pip install command `python -m pip install -e ".[validation]"`.

## Python

All python modules and code with the `.py` extension generally hold to the [PEP 8](https://peps.python.org/pep-0008/) standard. Deviations generally are around things like line-length, where much like the Markdown change, we allow 120 character lines. We also use PascalCase for local variables rather than the standard UPPER_CASE format.

The full list of changes (honestly, the full list of configuration even including basic defaults) can be found in [.pylintrc](/.pylintrc). This might be a bit hard to read, and if you are really interested in seeing the differences, would suggest running `pylint --generate-rcfile > .pylintrc2` in another directory and compare the differences using a tool like `diff` in *nix like environments or something like `Compare-Object` in PowerShell.
