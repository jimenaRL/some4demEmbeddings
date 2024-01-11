#!/bin/bash

declare -a Countries=(
    # belgium
    france
    # germany
    # italy
    # netherlands
    # poland
    # romania
    # slovenia
    # spain
)

declare -a Surveys=(
    ches2019
    # gps2019
)

output=exports
deliverable=deliverableD21
config="configs/embeddings.yaml"

for country in ${Countries[@]}; do

    echo "################# ${country} #################"

    vizconfig="configs/vizconfigs/${country}.yaml"

    # # # # PREPROCESSING
    # python python/some4demexp/embeddings/preprocess_data.py --config=$config --country=$country --output=$output

    for survey in ${Surveys[@]}; do

        # # IDELOGICAL EMBEDDINGS CREATION
        # python python/some4demexp/embeddings/create_ide_emb.py --config=$config --country=$country --survey=$survey --output=$output

        # # IDELOGICAL EMBEDDINGS VISUALIZATION
        # python python/some4demexp/visualizations/create_ide_viz.py \
        #     --config=$config \
        #     --country=$country \
        #     --survey=$survey \
        #     --vizconfig=$vizconfig \
        #     --output=$output \
        #     --show

        # # ATTITUDINAL EMBEDDINGS CREATION
        # python python/some4demexp/embeddings/create_att_emb.py --config=$config  --country=$country --survey=$survey --output=$output

        # ATTITUDINAL EMBEDDINGS VISUALIZATION
        # python python/some4demexp/visualizations/create_att_viz.py \
        #     --config=$config \
        #     --country=$country \
        #     --survey=$survey \
        #     --vizconfig=$vizconfig \
        #     --output=$output \
        #     --show

        # # ANALYSIS
        # python python/some4demexp/validation/correlation_matrices.py --config=$config --country=$country --survey=$survey --output=$output

        # VALIDATION
        # python python/some4demexp/validation/labels_proportions.py --config=$config --country=$country --survey=$survey --output=$output  # --show
        python python/some4demexp/validation/logistic_regression.py --config=$config --country=$country --survey=$survey --output=$output --show

    done

    # EXPORTS
    # python python/some4demexp/exports.py --config=$config --country=$country --output=$output

done

