#!/bin/bash

# Adds empty __init__.py files to each directory in folder

for dir in ./*/
do
    touch ./$dir/__init__.py
    echo touched file: ${dir}__init__.py
done

	   

