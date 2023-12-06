#!/bin/bash

declare -a Countries=(
    # belgium
    # france
    # germany
    # italy
    # netherlands
    # poland
    # romania
    slovenia
    # spain
)

declare -a Surveys=(
    # ches2019
    gps2019
)

outputs=outputs
images=images
vizfolder=vizconfigs

for country in ${Countries[@]}; do
    echo "################# ${country} #################"

    config="configs/embeddings.yaml"
    vizconfig="configs/vizconfigs/${country}.yaml"

    # PREPROCESSING
    python python/some4demexp/embeddings/preprocess_data.py --config=$config --country=$country --output=$outputs


    for survey in ${Surveys[@]}; do

        # IDELOGICAL EMBEDDINGS CREATION
        python python/some4demexp/embeddings/create_ide_emb.py --config=$config --country=$country --survey=$survey --output=$outputs

        # # IDELOGICAL EMBEDDINGS VISUALIZATION
        python python/some4demexp/visualizations/matplotlib/create_ide_viz2d.py \
            --config=$config \
            --country=$country \
            --survey=$survey \
            --vizconfig=$vizconfig \
            --output=$outputs \
            # --show


        # ATTITUDINAL EMBEDDINGS CREATION
        python python/some4demexp/embeddings/create_att_emb.py --config=$config  --country=$country --survey=$survey --output=$outputs

        # ATTITUDINAL EMBEDDINGS VISUALIZATION
        python python/some4demexp/visualizations/matplotlib/create_att_viz2d.py \
            --config=$config \
            --country=$country \
            --survey=$survey \
            --vizconfig=$vizconfig \
            --output=$outputs \
            # --show

        # # ANALYSIS
        # python python/some4demexp/stats.py --config=$config  --country=$country --output=$outputs
        # python python/some4demexp/validation/correlation_matrices.py --config=$config --country=$country --output=$outputs

        # # VALIDATION
        # python python/some4demexp/validation/labels_proportions.py --config=$config --country=$country --output=$outputs  # --show
        # python python/some4demexp/validation/benchmark.py --config=$config --country=$country --output=$outputs
        # python python/some4demexp/validation/logistic_regression.py --config=$config --country=$country --output=$outputs #  --show

    done

    # EXPORTS
    python python/some4demexp/exports.py --config=$config --country=$country

done

