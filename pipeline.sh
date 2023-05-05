#!/bin/bash

declare -a StringArray=(spain)

config=config.yaml
outputs=outputs
vizconfig=vizconfig.yaml
show=False

for country in ${StringArray[@]}; do
    python python/some4demexp/embeddings/preprocess_data.py --config=$config --country=$country --output=$outputs
    python python/some4demexp/embeddings/create_ide_emb.py --config=$config --country=$country --output=$outputs
    python python/some4demexp/embeddings/create_att_emb.py --config=$config  --country=$country --output=$outputs
    python python/some4demexp/visualizations/matplotlib/create_2Dviz.py \
        --config=$config \
        --country=$country \
        --vizconfig=$vizconfig \
        --output=$outputs \
        --show=$show
done



