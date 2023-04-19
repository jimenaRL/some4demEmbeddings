import yaml
from utils import *
from linate import IdeologicalEmbedding

from argparse import ArgumentParser

# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--output', type=str, required=True)
args = ap.parse_args()
config = args.config
output = args.output

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)
print(yaml.dump(params, default_flow_style=False))

COUNTRY = params['country']
DB = params['sqlite_db']
NB_MIN_FOLLOWERS = params['sources_min_followers']
MIN_OUTDEGREE = params['sources_min_outdegree']

folder = set_output_folder(params, output)

# Retrive source/target bipartite graph
users_metadata = retrieveAndFormatUsersMetadata(DB, COUNTRY)
valid_followers = users_metadata \
    .query(f"nb_followers >= {NB_MIN_FOLLOWERS}") \
    .pseudo_id.unique().tolist()
res_graph = retrieveGraph(DB, COUNTRY, valid_followers)

# Build adjency matrix
X, targets_ids, sources_ids = graphToAdjencyMatrix(
    res_graph, MIN_OUTDEGREE, sparce=False)

# Create and fit ideological embedding
model = IdeologicalEmbedding(**params["ideological_model"])
model.fit(X)

# Save sources/targets coordinates in ideological space and add pseudo ids
save_ide_embeddings(model, sources_ids, targets_ids, folder)
