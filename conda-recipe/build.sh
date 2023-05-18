#!/bin/bash
$PYTHON setup.py build_external -vv
$PYTHON setup.py install --single-version-externally-managed --record=record.txt