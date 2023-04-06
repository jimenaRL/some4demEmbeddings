import yaml
from utils import *
from linate import IdeologicalEmbedding, AttitudinalEmbedding

# from argparse import ArgumentParser

# parse arguments and set paths
# ap = ArgumentParser()
# ap.add_argument('--config', type=str, required=True)
# args = ap.parse_args()
# config = args.config

config = 'mooc.yaml'
# config = 'france.yaml'

with open(config, "r") as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)

COUNTRY = params['country']
DB = params['sqlite_db']


# (0) Retrive bipartite graph and target groups from sqlite database
res_graph = retrieveFollowersMpsGraph(DB, COUNTRY, limit=1e7)
res_groups = retrieveMpsParties(DB, COUNTRY)


# (1) Build adjency matrix
X, targets_ids, sources_ids = graphToAdjencyMatrix(res_graph, sparce=False)

# (2) Create and fit ideological embedding
model = IdeologicalEmbedding(**params["ideological_model"])
model.fit(X)

# (3) Get sources/targets coordinates in ideological space and add pseudo ids
sources_coords_ide = model.ideological_embedding_source_latent_dimensions_
targets_coords_ide = model.ideological_embedding_target_latent_dimensions_

# (4) Get and format target groups
targets_groups = getTargetGroups(res_groups)

# (6) Visualize ideological embedding
palette = [
        'blue',
        'red',
        'gold',
        'orange',
        'green',
        'violet',
        'cyan',
        'magenta',
        'brown',
        'gray'
]
# palette = None
visualize(
    sources_coords_ide,
    targets_coords_ide,
    targets_ids,
    sources_ids,
    targets_groups,
    palette
)
