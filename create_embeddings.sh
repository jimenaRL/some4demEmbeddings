#!/bin/bash


declare -a StringArray=(france, germany)

for country in ${StringArray[@]}; do
    python python/create_ide_emb.py --config=config.yaml --country=$country --output=outputs
    python python/create_att_emb.py --config=config.yaml --country=$country --output=outputs
    python python/viz_emb.py --config=config.yaml --country=$country --output=outputs
done


