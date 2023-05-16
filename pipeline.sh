#!/bin/bash

declare -a StringArray=(
    belgium
    france
    germany
    italy
    netherlands
    poland
    # romania  # create_ide_emb fails on SVD computation with prince
    slovenia
    spain
)

outputs=outputs
suffix=15D.yaml
images=images
vizfolder=vizconfigs

for country in ${StringArray[@]}; do

    echo "################# ${country} #################"

    python python/some4demexp/embeddings/preprocess_data.py --config=config$suffix --country=$country --output=$outputs
    python python/some4demexp/embeddings/create_ide_emb.py --config=config$suffix --country=$country --output=$outputs
    python python/some4demexp/embeddings/create_att_emb.py --config=config$suffix  --country=$country --output=$outputs

    python python/some4demexp/visualizations/matplotlib/create_vizconfig.py  \
        --config=config$suffix \
        --country=$country \
        --vizfolder=$vizfolder
    python python/some4demexp/visualizations/matplotlib/create_2Dviz.py \
        --config=config$suffix \
        --country=$country \
        --vizconfig="vizconfigs/$country$suffix" \
        --output=$outputs \
        --show
    python python/some4demexp/visualizations/matplotlib/parse_images.py \
        --config=config$suffix \
        --country=$country \
        --images=$images

done
