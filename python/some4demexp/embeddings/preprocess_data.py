import yaml
from argparse import ArgumentParser

from some4demdb import SQLite
from some4demexp.graph import graphToAdjencyMatrix
from some4demexp.inout import \
    set_output_folder, \
    save_experiment_data



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
NB_MIN_FOLLOWERS = params['sources_min_followers']
MIN_OUTDEGREE = params['sources_min_outdegree']

# set data folder
folder = set_output_folder(params, country, output)

# # Retrive source/target bipartite graph
valid_followers = SQLITE.retrieveFollowersMinIndegree(
    country,
    min_indegree=NB_MIN_FOLLOWERS
)

res_graph = SQLITE.retrieveGraph('follower', country, valid_followers)

# Build adjency matrix
X, targets_pids, sources_pids, sources_map_pids = graphToAdjencyMatrix(
    res_graph, MIN_OUTDEGREE, sparce=False)

# Save social graph and target/source pseudo ids
save_experiment_data(
    X, targets_pids, sources_pids, sources_map_pids, folder)