#!/bin/bash

rm -rf dist/*

python setup.py sdist bdist_egg bdist_wheel
python3 setup.py bdist_egg bdist_wheel

twine upload dist/*
