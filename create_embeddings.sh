#!/bin/bash

declare -a StringArray=(france germany spain)

for country in ${StringArray[@]}; do
    python python/some4demexp/embeddings/preprocess_data.py --config=config.yaml --country=$country --output=outputs
    python python/some4demexp/embeddings/create_ide_emb.py --config=config.yaml --country=$country --output=outputs
    python python/some4demexp/embeddings/create_att_emb.py --config=config.yaml --country=$country --output=outputs
done


