#!/bin/bash
set -e
pip install twine
python3 -m twine upload dist/*