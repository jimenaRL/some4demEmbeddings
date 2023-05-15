#!/bin/bash

declare -a StringArray=(
    # france
    # germany
    # spain
    # italy
    # belgium
    # netherlands
    # # romania  # create_ide_emb fails on SVD computation with prince
    # slovenia
    # poland
)

outputs=outputs
suffix=15D.yaml

for country in ${StringArray[@]}; do

    echo "################# ${country} #################"

    # python python/some4demexp/embeddings/preprocess_data.py --config=config$suffix --country=$country --output=$outputs
    # python python/some4demexp/embeddings/create_ide_emb.py --config=config$suffix --country=$country --output=$outputs
    # python python/some4demexp/embeddings/create_att_emb.py --config=config$suffix  --country=$country --output=$outputs
    python python/some4demexp/visualizations/matplotlib/create_2Dviz.py \
        --config=config$suffix \
        --country=$country \
        --vizconfig="vizconfigs/$country$suffix" \
        --output=$outputs \
        # --show
done