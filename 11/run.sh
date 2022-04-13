#!/bin/bash
cd $1
for file in *.jack;
do
	python ../compiler.py $file
done
cd ..
