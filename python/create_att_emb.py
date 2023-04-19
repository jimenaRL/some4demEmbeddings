import yaml
from utils import *
from linate import AttitudinalEmbedding

from argparse import ArgumentParser

# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--output', type=str, required=False, default='-1')
args = ap.parse_args()
config = args.config
output = args.output

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)
print(yaml.dump(params, default_flow_style=False))

COUNTRY = params['country']
DB = params['sqlite_db']
ATTSPACES = params['attitudinal_spaces']

# Retrieve target groups from sqlite db
ches_mapping = retrieveAndFormatPartiesMapping(DB, COUNTRY)
targets_groups = retrieveAndFormatTargetGroups(DB, COUNTRY, ches_mapping)

# Load data from ideological embedding
folder = set_output_folder(params, output)
ide_sources, ide_targets = load_ide_embeddings(folder)

# Estimate target groups positions in ideological space by averaging
# targets' positions

# add group information
t0 = len(ide_targets)
ide_targets = ide_targets.merge(
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
for dims in ATTSPACES.values():

    groups_coord_att = retrieveAndFormatTargetGroupsCoord(DB, COUNTRY, dims)
    ide_targets_cp = ide_targets.copy()
    ide_sources_cp = ide_sources.copy()

    # make estimate
    estimated_groups_coord_ide = ide_targets_cp \
        .drop(columns=['entity']) \
        .groupby('group') \
        .mean() \
        .reset_index() \
        .rename(columns={'group': 'entity'})

    model_att = AttitudinalEmbedding(**params["attitudinal_model"])

    model_att.fit(
        estimated_groups_coord_ide,
        groups_coord_att.rename(columns={'group': 'entity'})
    )

    sources_coord_att = model_att.transform(ide_sources_cp)
    targets_coord_att = model_att.transform(ide_targets_cp.drop("group", axis=1))

    # add group information
    targets_coord_att = targets_coord_att.merge(
            targets_groups,
            left_on="entity",
            right_on="mp_pseudo_id",
            how="inner"
        ) \
        .drop(columns="mp_pseudo_id")

    # save results
    save_att_embeddings(
            sources_coord_att,
            targets_coord_att,
            groups_coord_att,
            targets_groups,
            folder,
            dims)
