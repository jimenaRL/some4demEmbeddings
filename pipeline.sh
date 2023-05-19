#!/bin/bash

declare -a StringArray=(
    # belgium
    # france
    # germany
    # italy
    # netherlands
    # poland
    # # romania  # create_ide_emb fails on SVD computation with prince
    # slovenia
    # spain
)

outputs=outputs
images=images
vizfolder=vizconfigs

for country in ${StringArray[@]}; do

    config="detconfigs/${country}.yaml"
    vizconfig="vizconfigs/${country}.yaml"

    echo "################# ${country} #################"

    python python/some4demexp/embeddings/preprocess_data.py --config=$config --country=$country --output=$outputs
    python python/some4demexp/embeddings/create_ide_emb.py --config=$config --country=$country --output=$outputs
    python python/some4demexp/embeddings/create_att_emb.py --config=$config  --country=$country --output=$outputs

    python python/some4demexp/stats.py --config=$config  --country=$country --output=$outputs

    python python/some4demexp/visualizations/matplotlib/create_ide_viz2d.py \
        --config=$config \
        --country=$country \
        --vizconfig=$vizconfig \
        --output=$outputs \
        # --show

    python python/some4demexp/visualizations/matplotlib/create_att_viz2d.py \
        --config=$config \
        --country=$country \
        --vizconfig=$vizconfig \
        --output=$outputs \
        # --show

    python python/some4demexp/visualizations/matplotlib/parse_images.py \
        --config=$config \
        --country=$country \
        --images=$images

done