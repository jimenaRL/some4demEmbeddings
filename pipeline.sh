#!/bin/bash

declare -a StringArray=(france)

config=config2D.yaml
outputs=outputs

for country in ${StringArray[@]}; do
    # python python/some4demexp/embeddings/preprocess_data.py --config=$config --country=$country --output=$outputs
    # python python/some4demexp/embeddings/create_ide_emb.py --config=$config --country=$country --output=$outputs
    # python python/some4demexp/embeddings/create_att_emb.py --config=$config  --country=$country --output=$outputs
    python python/some4demexp/visualizations/matplotlib/create_2Dviz.py \
        --config=$config \
        --country=$country \
        --vizconfig="vizconfigs/$country.yaml" \
        --output=$outputs \
        --show
done