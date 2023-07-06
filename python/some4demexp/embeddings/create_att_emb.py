import yaml
from itertools import combinations
from argparse import ArgumentParser

import numpy as np
from linate import AttitudinalEmbedding
from some4demdb import SQLite
from some4demexp.inout import \
    set_output_folder, \
    set_output_folder_emb, \
    set_output_folder_att, \
    load_targets_groups, \
    load_ide_embeddings, \
    save_att_embeddings

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
print(yaml.dump(params, default_flow_style=False))

SQLITE = SQLite(params['sqlite_db'])
ATTDIMS = params['attitudinal_dimensions']

# Load target groups
data_folder = set_output_folder(params, country, output)
targets_groups = load_targets_groups(data_folder)

# Load data from ideological embedding
ide_folder = set_output_folder_emb(params, country, output)
ide_sources, ide_targets = load_ide_embeddings(ide_folder)


# Estimate target groups positions in ideological space by averaging
# targets' individual positions

# add group information
t0 = len(ide_targets)
ide_targets_in_parties_with_valid_mapping = ide_targets.merge(
        targets_groups,
        left_on="entity",
        right_on="mp_pseudo_id",
        how="inner"
    ) \
    .drop(columns="mp_pseudo_id")
t1 = len(ide_targets)
if t0 > t1:
    print(
        f"Dropped {t0 - t1} targets with no group in mapping.")

# Fit regression
groups_coord_att = SQLITE.retrieveAndFormatTargetGroupsAttitudes(country, ATTDIMS)
ide_sources_cp = ide_sources.copy()

# make estimate
estimated_groups_coord_ide = ide_targets_in_parties_with_valid_mapping \
    .drop(columns=['entity']) \
    .groupby('party') \
    .mean() \
    .reset_index()

model_att = AttitudinalEmbedding(**params["attitudinal_model"])

model_att.fit(
    estimated_groups_coord_ide.rename(columns={'party': 'entity'}),
    groups_coord_att.rename(columns={'party': 'entity'})
)

# Check affine transformation norms
T_tilda_aff = model_att.T_tilda_aff_np_
frobenius_norm = np.linalg.norm(T_tilda_aff, ord="fro")
max_ = T_tilda_aff.max()
min_ = T_tilda_aff.min()
lsv = np.linalg.norm(T_tilda_aff, ord=2)
ssv = np.linalg.norm(T_tilda_aff, ord=-2)
print(f"Affine transformation T_tilda_aff: \n\n{T_tilda_aff}\n")
print(f"T_tilda_aff max: {max_}")
print(f"T_tilda_aff min: {min_}")
print(f"T_tilda_aff largest singular value: {lsv}")
print(f"T_tilda_aff smallest singular value: {ssv}")



sources_coord_att = model_att.transform(ide_sources_cp)
targets_coord_att = model_att.transform(ide_targets)

# add group information
targets_coord_att = targets_coord_att.merge(
        targets_groups,
        left_on="entity",
        right_on="mp_pseudo_id",
        how="left"
    ) \
    .drop(columns="mp_pseudo_id")

# save results
att_folder = set_output_folder_att(params, country, output)
save_att_embeddings(
    sources_coord_att,
    targets_coord_att,
    att_folder)


import pdb; pdb.set_trace()  # breakpoint d40dfd39 //
