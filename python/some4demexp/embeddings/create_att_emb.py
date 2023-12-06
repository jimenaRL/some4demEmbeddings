import yaml
from itertools import combinations
from argparse import ArgumentParser

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

# from linate import AttitudinalEmbedding
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
ap.add_argument('--survey', type=str, required=True)
ap.add_argument('--output', type=str, required=False, default='-1')
args = ap.parse_args()
config = args.config
output = args.output
country = args.country
survey = args.survey


with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)
# print(yaml.dump(params, default_flow_style=False))

with open(params['params_db'], "r", encoding='utf-8') as fh:
    params_db = yaml.load(fh, Loader=yaml.SafeLoader)

SQLITE = SQLite(params['sqlite_db'], params_db['output']['tables'], country)
ATTDIMS = params['attitudinal_dimensions'][survey]
SURVEYCOL = f'{survey.upper()}_party_acronym'

# Load mp groups
data_folder = set_output_folder(params, country, output)

# Load parties attitudinal coordinaets
parties_coord_att = SQLITE.retrieveAndFormatPartiesAttitudes(survey, ATTDIMS)

# Load data from ideological embedding
ide_folder = set_output_folder_emb(params, country, survey, output)
ide_followers, ide_mps = load_ide_embeddings(ide_folder)
ide_followers_cp = ide_followers.copy()
ide_mps_cp = ide_mps.copy()
mps_parties = SQLITE.retrieveAndFormatMpParties(['MMS', survey])


# drop mps with parties withou mapping and add parties to ideological positions
mps_parties = mps_parties.dropna()
mssg = f"Found {len(mps_parties)} mps (out of {len(ide_mps)} in ideological "
mssg += f"embedding) with valid party."
print(mssg)

t0 = len(ide_mps)
ide_mps_in_parties_with_valid_mapping = ide_mps.merge(
        mps_parties,
        left_on="entity",
        right_on="mp_pseudo_id",
        how="inner"
    ) \
    .drop(columns="mp_pseudo_id")
t1 = len(ide_mps_in_parties_with_valid_mapping)
if t0 > t1:
    print(
        f"Dropped {t0 - t1} mps with no party in mapping.")

# Fit ridge regression
estimated_parties_coord_ide = ide_mps_in_parties_with_valid_mapping \
    .drop(columns=['entity', 'MMS_party_acronym']) \
    .groupby(SURVEYCOL) \
    .mean() \
    .reset_index()

estimated_parties_coord_ide = estimated_parties_coord_ide.sort_values(by=SURVEYCOL)
parties_coord_att = parties_coord_att.sort_values(by=SURVEYCOL)

assert (estimated_parties_coord_ide[SURVEYCOL].values != parties_coord_att[SURVEYCOL].values).sum() == 0

X = estimated_parties_coord_ide.drop(columns=[SURVEYCOL]).values
Y = parties_coord_att.drop(columns=[SURVEYCOL, 'MMS_party_acronym']).values

assert (len(X) == len(Y))

clf = Ridge(alpha=1.0)
clf.fit(X, Y)

# Check affine transformation norms
# ridgr_reg_coeff = clf.coef_

# frobenius_norm = np.linalg.norm(ridgr_reg_coeff, ord="fro")
# max_ = ridgr_reg_coeff.max()
# min_ = ridgr_reg_coeff.min()
# lsv = np.linalg.norm(ridgr_reg_coeff, ord=2)
# ssv = np.linalg.norm(ridgr_reg_coeff, ord=-2)
# print(f"Affine transformation ridgr_reg_coeff: \n\n{ridgr_reg_coeff}\n")
# print(f"ridgr_reg_coeff max: {max_}")
# print(f"ridgr_reg_coeff min: {min_}")
# print(f"ridgr_reg_coeff largest singular value: {lsv}")
# print(f"ridgr_reg_coeff smallest singular value: {ssv}")

follower_coord_att_values = clf.predict(ide_followers_cp.drop(columns=['entity']).values)
mps_coord_att_values = clf.predict(ide_mps.drop(columns=['entity']).values)

columns = parties_coord_att.drop(
    columns=["MMS_party_acronym", SURVEYCOL]).columns
follower_coord_att = pd.DataFrame(
    data=follower_coord_att_values,
    columns=columns) \
    .assign(entity=ide_followers_cp.entity)
mps_coord_att = pd.DataFrame(
    data=mps_coord_att_values,
    columns=columns) \
    .assign(entity=ide_mps.entity)

# add group information
mps_coord_att = mps_coord_att.merge(
        mps_parties,
        left_on="entity",
        right_on="mp_pseudo_id",
        how="left"
    ) \
    .drop(columns="mp_pseudo_id") \
    .dropna()

# save results
att_folder = set_output_folder_att(params, survey, country, output)
save_att_embeddings(
    follower_coord_att,
    mps_coord_att,
    att_folder)