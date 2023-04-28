#!/bin/bash


declare -a StringArray=(france germany spain)

for country in ${StringArray[@]}; do
    python python/some4demexp/visualizations/matplotlib/create_2Dviz.py --config=config.yaml --country=$country --output=outputs
done


