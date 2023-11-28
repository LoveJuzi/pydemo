#!/bin/bash

cd $(dirname $(realpath ${BASH_SOURCE}))
export PYTHONPATH="$PWD/utils"
cd - > /dev/null
