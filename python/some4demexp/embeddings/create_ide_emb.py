import yaml
from argparse import ArgumentParser

import numpy as np
import pandas as pd
from linate import IdeologicalEmbedding
from some4demexp.inout import \
    set_output_folder, \
    set_output_folder_emb, \
    load_experiment_data, \
    save_ide_embeddings

# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--country', type=str, required=True)
ap.add_argument('--output', type=str, required=False, default='-1')
args = ap.parse_args()
config = args.config
output = args.output
country = args.country

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)
# print(yaml.dump(params, default_flow_style=False))

data_folder = set_output_folder(params, country, output)
X, targets_pids, sources_pids, sources_map_pids = load_experiment_data(data_folder)

# Create and fit ideological embedding
model = IdeologicalEmbedding(**params["ideological_model"])
model.fit(X)

targets_embeddings = model.ideological_embedding_target_latent_dimensions_ \
    .reset_index() \
    .drop(columns=["target_id"]) \
    .assign(entity=targets_pids)

sources_embeddings = model.ideological_embedding_source_latent_dimensions_ \
    .reset_index() \
    .drop(columns=["source_id"]) \
    .assign(entity=sources_pids)

# reintegrate repeated sources
# TO DO: DOCUMENT THE PROCESS !!!!!!!
# quitte hard to explain but must be done
# ['original_columns_id', 'idx_inv']

l0 = len(sources_map_pids)
sources_map_pids = pd.DataFrame(
    data=sources_map_pids,
    columns=['original_columns_id', 'idx_inv'])
sources_map_pids = sources_map_pids.merge(
    sources_embeddings,
    left_on='idx_inv',
    right_on='entity',
    how='left') \
    .drop(columns=['idx_inv', 'entity']) \
    .rename(columns={'original_columns_id': 'entity'})

assert l0 == len(sources_map_pids)
assert sources_map_pids.latent_dimension_0.isnull().sum() == 0

sources_embeddings = sources_map_pids

assert sources_embeddings.duplicated().sum() == 0

# Save sources/targets coordinates in ideological space and add pseudo ids
emb_folder = set_output_folder_emb(params, country, output)
save_ide_embeddings(sources_embeddings, targets_embeddings, emb_folder)

