#!/bin/bash

declare -a StringArray=(
    # belgium
    france
    # germany
    # italy
    # netherlands
    # poland
    # romania
    # slovenia
    # spain
    # japan
)

outputs=outputs
images=images
vizfolder=vizconfigs


for country in ${StringArray[@]}; do

    echo "################# ${country} #################"

    configs=('configs/N2M2/lrgen_vs_antielite_salience.yaml')

    # configs=("configs/determined/${country}.yaml")

    for config in ${configs[@]}; do

        vizconfig="configs/vizconfigs/${country}.yaml"

        # [0] EMBEDDINGS CREATION
        # python python/some4demexp/embeddings/preprocess_data.py --config=$config --country=$country --output=$outputs
        # python python/some4demexp/embeddings/create_ide_emb.py --config=$config --country=$country --output=$outputs
        # python python/some4demexp/embeddings/create_att_emb.py --config=$config  --country=$country --output=$outputs

        # # [1] ANALYSIS
        # python python/some4demexp/stats.py --config=$config  --country=$country --output=$outputs
        # python python/some4demexp/validation/correlation_matrices.py --config=$config --country=$country --output=$outputs

        # # [2] EMBEDDINGS VISUALIZATION
        # python python/some4demexp/visualizations/matplotlib/create_ide_viz2d.py \
        #     --config=$config \
        #     --country=$country \
        #     --vizconfig=$vizconfig \
        #     --output=$outputs \
        #     # --show
        # python python/some4demexp/visualizations/matplotlib/create_att_viz2d.py \
        #     --config=$config --country=$country --vizconfig=$vizconfig --output=$outputs
        #     # --show

        # # [3] VALIDATION
        # python python/some4demexp/validation/label_followers.py --config=$config --country=$country --output=$outputs
        # python python/some4demexp/validation/labels_proportions.py --config=$config --country=$country --output=$outputs --show
        # python python/some4demexp/validation/benchmark.py --config=$config --country=$country --output=$outputs
        # python python/some4demexp/validation/logistic_regression.py --config=$config --country=$country --output=$outputs --show

        # # [4] EXPORTS
        # python python/some4demexp/visualizations/matplotlib/parse_images.py \
        #     --config=$config \
        #     --country=$country \
        #     --images=$images
        # python python/some4demexp/exports/export_france.py --config=$config  --country=$country --output=$outputs

    done

done