import yaml
from itertools import combinations
from argparse import ArgumentParser

import numpy as np
import pandas as pd

from linate import AttitudinalEmbedding
from some4demdb import SQLite
from some4demexp.inout import \
    set_output_folder, \
    set_output_folder_emb, \
    set_output_folder_att, \
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
# print(yaml.dump(params, default_flow_style=False))

SQLITE = SQLite(params['sqlite_db'])
ATTDIMS = params['attitudinal_dimensions']

# Load target groups
data_folder = set_output_folder(params, country, output)

# Load data from ideological embedding
ide_folder = set_output_folder_emb(params, country, output)
ide_sources, ide_targets = load_ide_embeddings(ide_folder)
targets_groups = SQLITE.getMpsValidParties(country)

mssg = f"Find {len(targets_groups)} (out of {len(ide_targets)} in ideological "
mssg += f"embedding) mps with valid party."
print(mssg)

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
t1 = len(ide_targets_in_parties_with_valid_mapping)
if t0 > t1:
    print(
        f"Dropped {t0 - t1} targets with no group in mapping.")

# Fit regression
groups_coord_att = SQLITE.retrieveAndFormatTargetGroupsAttitudes(
    country, ATTDIMS)
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


sources_coord_att_tilda_aff = model_att.transform(ide_sources_cp.copy())
targets_coord_att_tilda_aff = model_att.transform(ide_targets.copy())


################ RIDGE REGRESSION

estimated_groups_coord_ide = estimated_groups_coord_ide.sort_values(by='party')
groups_coord_att = groups_coord_att.sort_values(by='party')

## HOT FIX !!!!
valid_parties = [f"'{p}'" for p in estimated_groups_coord_ide.party.to_list()]
groups_coord_att = groups_coord_att.query(f"party in ({','.join(valid_parties)})")
###########################

assert (estimated_groups_coord_ide.party.values != groups_coord_att.party.values).sum() == 0

X = estimated_groups_coord_ide.drop(columns=['party']).values
Y = groups_coord_att.drop(columns=['party']).values

assert (len(X) == len(Y))

from sklearn.linear_model import Ridge
clf = Ridge(alpha=1.0)
clf.fit(X, Y)

# Check affine transformation norms
ridgr_reg_coeff = clf.coef_

frobenius_norm = np.linalg.norm(ridgr_reg_coeff, ord="fro")
max_ = ridgr_reg_coeff.max()
min_ = ridgr_reg_coeff.min()
lsv = np.linalg.norm(ridgr_reg_coeff, ord=2)
ssv = np.linalg.norm(ridgr_reg_coeff, ord=-2)
print(f"Affine transformation ridgr_reg_coeff: \n\n{ridgr_reg_coeff}\n")
print(f"ridgr_reg_coeff max: {max_}")
print(f"ridgr_reg_coeff min: {min_}")
print(f"ridgr_reg_coeff largest singular value: {lsv}")
print(f"ridgr_reg_coeff smallest singular value: {ssv}")

sources_coord_att_values = clf.predict(ide_sources_cp.drop(columns=['entity']).values)
targets_coord_att_values = clf.predict(ide_targets.drop(columns=['entity']).values)

columns = groups_coord_att.drop(columns="party").columns
sources_coord_att = pd.DataFrame(
    data=sources_coord_att_values,
    columns=columns) \
    .assign(entity=ide_sources_cp.entity)
targets_coord_att = pd.DataFrame(
    data=targets_coord_att_values,
    columns=columns) \
    .assign(entity=ide_targets.entity)


#####################
# back to tilda aff
# sources_coord_att = sources_coord_att_tilda_aff
# targets_coord_att = targets_coord_att_tilda_aff

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