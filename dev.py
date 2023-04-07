import yaml
from utils import *
from linate import IdeologicalEmbedding, AttitudinalEmbedding

from argparse import ArgumentParser

# parse arguments and set paths
# ap = ArgumentParser()
# ap.add_argument('--country', type=str, required=True)
# args = ap.parse_args()
# country = args.country

country = 'france'


config = f'{country}.yaml'


with open(config, "r") as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)
print(yaml.dump(params, default_flow_style=False))


COUNTRY = params['country']
DB = params['sqlite_db']
DIMS = params['attitudinal_dimensions']
PALETTE = params['palette']
MAPPING = params['mapping']

# (0) DATA RETRIEVAL
# (0.a) Retrive source/target bipartite graph and target groups from sqlite db
res_graph = retrieveGraph(DB, COUNTRY, limit=1e6)
targets_groups = retrieveAndFormatTargetGroups(DB, COUNTRY)
groups_coord_att = retrieveAndFormatTargetGroupsCoord(DB, COUNTRY, DIMS)

# (0.b) mapping

MAPPING = pd.DataFrame.from_dict({
    'parliamentary_group': MAPPING.keys(),
    'group': MAPPING.values()})

groups_coord_att = groups_coord_att \
    .merge(MAPPING, how='left', on='group') \
    .drop('parliamentary_group', axis=1)

g0 = len(targets_groups)
targets_groups = targets_groups \
    .rename(columns={'group': 'parliamentary_group'}) \
    .merge(MAPPING) \
    .drop('parliamentary_group', axis=1)
g1 = len(targets_groups)
if g0 > g1:
    print(
        f"Dropped {g0 - g1} targets with no group in mapping.")

# (1) IDEOLOGICAL SPACES
# (1.a) Build adjency matrix
X, targets_ids, sources_ids = graphToAdjencyMatrix(res_graph, sparce=False)

# (1.b) Create and fit ideological embedding
model_ide = IdeologicalEmbedding(**params["ideological_model"])
model_ide.fit(X)

# (1.c) Get sources/targets coordinates in ideological space and add pseudo ids
sources_coord_ide = model_ide.ideological_embedding_source_latent_dimensions_
targets_coord_ide = model_ide.ideological_embedding_target_latent_dimensions_


# (2) ATTITUDINAL SPACES


# (2.a) Estimate target groups positions in ideological space by averaging
# targets' positions
targets_coord_ide.index.rename('', inplace=True)
targets_coord_ide = targets_coord_ide.assign(target_id=targets_ids)


# add group information
t0 = len(targets_coord_ide)
targets_coord_ide = targets_coord_ide.merge(
        targets_groups,
        left_on="target_id",
        right_on="mp_pseudo_id",
        how="inner"
    ) \
    .drop(columns="mp_pseudo_id")
t1 = len(targets_coord_ide)
if t0 > t1:
    print(
        f"Dropped {t0 - t1} targets with no group in mapping.")

# make estimate
estimated_groups_coord_ide = targets_coord_ide \
    .drop(columns=['target_id']) \
    .groupby('group') \
    .mean() \
    .reset_index() \
    .rename(columns={'group': 'entity'})

# # (2.d) Fit regression
model_att = AttitudinalEmbedding(**params["attitudinal_model"])

model_att.fit(
    estimated_groups_coord_ide,
    groups_coord_att.rename(columns={'group': 'entity'})
)


sources_coord_ide = sources_coord_ide.assign(entity=sources_ids)
targets_coord_ide = targets_coord_ide.rename(columns={'target_id': 'entity'})

sources_coord_att = model_att.transform(sources_coord_ide)
targets_coord_att = model_att.transform(
    targets_coord_ide.drop("group", axis=1))


# add group information
targets_coord_att = targets_coord_att.merge(
        targets_groups,
        left_on="entity",
        right_on="mp_pseudo_id",
        how="inner"
    ) \
    .drop(columns="mp_pseudo_id")

# (3) VISUALIZATIONS
# (3.a) Visualize ideological embedding
visualize_ide(
    sources_coord_ide,
    targets_coord_ide,
    PALETTE,
    f'ide_{country}_20230407.png')

# (3.b) Visualize attitudinal embedding
visualize_att(
    sources_coord_att,
    targets_coord_att,
    groups_coord_att,
    dict(zip(['x', 'y'], DIMS)),
    PALETTE,
    f"att_{'vs'.join(DIMS)}_{country}_20230407.png")

plt.show()
