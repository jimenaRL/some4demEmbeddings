import os
import os.path as op
import yaml
from utils import *
from viz import *
from linate import IdeologicalEmbedding, AttitudinalEmbedding

from argparse import ArgumentParser

# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--output', type=str, required=False, default='-1')
ap.add_argument('--limit', type=str, required=False, default='-1')
args = ap.parse_args()
config = args.config
limit = args.limit
output = args.output

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)
print(yaml.dump(params, default_flow_style=False))

COUNTRY = params['country']
DB = params['sqlite_db']
DIMS = params['attitudinal_dimensions']
PALETTE = params['palette']
NB_MIN_FOLLOWERS = params['sources_min_followers']
MIN_OUTDEGREE = params['sources_min_outdegree']

OUTPUT = args.output


# (0) DATA RETRIEVAL
# (0.a) Retrive source/target bipartite graph and target groups from sqlite db

groups_coord_att = retrieveAndFormatTargetGroupsCoord(DB, COUNTRY, DIMS)
ches_mapping = retrieveAndFormatPartiesMapping(DB, COUNTRY)
targets_groups = retrieveAndFormatTargetGroups(DB, COUNTRY, ches_mapping)

users_metadata = retrieveAndFormatUsersMetadata(DB, COUNTRY)
valid_followers = users_metadata \
    .query(f"nb_followers >= {NB_MIN_FOLLOWERS}") \
    .pseudo_id.unique().tolist()
res_graph = retrieveGraph(DB, COUNTRY, valid_followers, limit=float(limit))

# (1) IDEOLOGICAL SPACES
# (1.a) Build adjency matrix
X, targets_ids, sources_ids = graphToAdjencyMatrix(
    res_graph, MIN_OUTDEGREE, sparce=False)

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


# (3) SAVE RESULTS

today = date.today().strftime("%b-%d-%Y")
attitudes = '_vs_'.join(DIMS)

emb_folder = f"{COUNTRY}"
emb_folder += f"_sources_min_followers_{NB_MIN_FOLLOWERS}"
emb_folder += f"_sources_min_outdegree_{MIN_OUTDEGREE}"
emb_folder += f"_{limit}_links"
emb_folder += f"_{today}"
emb_folder = os.path.join(OUTPUT, 'embeddings', emb_folder)
ide_output_folder = os.path.join(emb_folder, 'ide')
att_output_folder = os.path.join(emb_folder, 'att', attitudes)

save_embeddings(
    embeddings={
        "sources_coord_ide": sources_coord_ide,
        "targets_coord_ide": targets_coord_ide,
        "sources_coord_att": sources_coord_att,
        "targets_coord_att": targets_coord_att,
        "groups_coord_att": groups_coord_att
    },
    ide_output_folder=ide_output_folder,
    att_output_folder=att_output_folder
)

# (4) VISUALIZATIONS

img_folder = f"{COUNTRY}"
img_folder += f"_sources_min_followers_{NB_MIN_FOLLOWERS}"
img_folder += f"_sources_min_outdegree_{MIN_OUTDEGREE}"
img_folder += f"_{limit}_links"
img_folder += f"_{today}"
img_folder = os.path.join(OUTPUT, 'images', img_folder)
ide_output_folder = os.path.join(img_folder, 'ide')
att_output_folder = os.path.join(img_folder, 'att', attitudes)

ide_name = f'ide_{COUNTRY}_{today}.png'
att_name = f"att_{attitudes}_{COUNTRY}_{today}.png"

viz2dEmb(
    sources_coord_ide,
    targets_coord_ide,
    sources_coord_att,
    targets_coord_att,
    groups_coord_att,
    DIMS,
    PALETTE,
    ide_output_folder,
    att_output_folder,
    ide_name,
    att_name
)
plt.show()
