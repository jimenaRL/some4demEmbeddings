#!/bin/bash

declare -a StringArray=(
    # belgium
    # france
    # germany
    # italy
    # netherlands
    # poland
    # romania
    # slovenia
    # spain
)

outputs=outputs
images=images
vizfolder=vizconfigs


for country in ${StringArray[@]}; do

    echo "################# ${country} #################"

    # configs=('configs/N2M2/*')

    configs=("configs/determined/${country}.yaml")

    # configs=('configs/N2M2/lrgen_vs_antielite_salience.yaml')

    for config in ${configs[@]}; do

        vizconfig="configs/vizconfigs/${country}.yaml"

        # python python/some4demexp/embeddings/preprocess_data.py --config=$config --country=$country --output=$outputs
        # python python/some4demexp/embeddings/create_ide_emb.py --config=$config --country=$country --output=$outputs
        # python python/some4demexp/embeddings/create_att_emb.py --config=$config  --country=$country --output=$outputs

        # python python/some4demexp/stats.py --config=$config  --country=$country --output=$outputs

        # python python/some4demexp/visualizations/matplotlib/create_ide_viz2d.py \
        #     --config=$config \
        #     --country=$country \
        #     --vizconfig=$vizconfig \
        #     --output=$outputs \
        #     --show

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

done