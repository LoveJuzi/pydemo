#!/bin/bash

cd $(dirname $(realpath ${BASH_SOURCE}))
export PYTHONPATH="$PWD/utils:$PWD/resource"
cd - > /dev/null
