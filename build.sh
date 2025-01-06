#!/bin/bash

set -e
pip install build
python3 -m flake8
pytest
python3 -m build