import yaml
from itertools import combinations
from argparse import ArgumentParser

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
for dimpair in combinations(ATTDIMS, 2):

    groups_coord_att = SQLITE.retrieveAndFormatTargetGroupsAttitudes(country, dimpair)
    ide_targets_cp = ide_targets.copy()
    ide_sources_cp = ide_sources.copy()

    # make estimate
    estimated_groups_coord_ide = ide_targets_cp \
        .drop(columns=['entity']) \
        .groupby('party') \
        .mean() \
        .reset_index()

    model_att = AttitudinalEmbedding(**params["attitudinal_model"])

    model_att.fit(
        estimated_groups_coord_ide.rename(columns={'party': 'entity'}),
        groups_coord_att.rename(columns={'party': 'entity'})
    )

    sources_coord_att = model_att.transform(ide_sources_cp)
    targets_coord_att = model_att.transform(ide_targets_cp.drop("party", axis=1))

    # add group information
    targets_coord_att = targets_coord_att.merge(
            targets_groups,
            left_on="entity",
            right_on="mp_pseudo_id",
            how="inner"
        ) \
        .drop(columns="mp_pseudo_id")

    # save results
    att_folder = set_output_folder_att(ide_folder, dimpair)
    save_att_embeddings(
            sources_coord_att,
            targets_coord_att,
            groups_coord_att,
            att_folder)
