#!/bin/bash

output=wip
config="configs/embeddings.yaml"
survey="gps2019"

echo "################# ${country} #################"

vizconfig="configs/vizconfigs/${country}.yaml"

echo ">>>>>>>>>>>>> ${survey}"

# IDELOGICAL EMBEDDINGS CREATION
python python/some4demexp/embeddings/create_ide_emb.py --config=$config --country=$country --survey=$survey --output=$output

# # # IDELOGICAL EMBEDDINGS VISUALIZATION
# python python/some4demexp/visualizations/create_ide_viz.py \
#     --config=$config \
#     --country=$country \
#     --survey=$survey \
#     --vizconfig=$vizconfig \
#     --output=$output  \
#     --show

# ATTITUDINAL EMBEDDINGS CREATION
# python python/some4demexp/embeddings/create_att_emb.py --config=$config  --country=$country --survey=$survey --output=$output

# # ATTITUDINAL EMBEDDINGS VISUALIZATION
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
# python python/some4demexp/validation/labels_proportions.py \
#     --config=$config --country=$country --survey=$survey --output=$output --show
# python python/some4demexp/validation/logistic_regression.py \
#     --config=$config --country=$country --survey=$survey --output=$output --plot  --show


# EXPORTS
# python scripts/exports.py --config=$config --country=$country --output=$output
# python scripts/exports_deliverableD21.py --config=$config --country=$country --output=$output
# python exports/some4demD21shareabledata/figures.py --config=$config --output=$output
