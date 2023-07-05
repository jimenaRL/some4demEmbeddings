import os
import yaml
from argparse import ArgumentParser

from some4demdb import SQLite
from some4demexp.graph import graphToAdjencyMatrix
from some4demexp.inout import \
    set_output_folder_att, \
    load_att_embeddings



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
NB_MIN_FOLLOWERS = params['sources_min_followers']
MIN_OUTDEGREE = params['sources_min_outdegree']

dims = ['lrgen', 'antielite_salience']

# Load attitudinal embeddigns
att_folder = set_output_folder_att(params, country, output)
att_sources, att_targets = load_att_embeddings(att_folder)

s0 = len(att_sources)
t0 = len(att_targets)

# Retrive sources annotations
sources_twitter_ids = SQLITE.retrieveAndFormatTwitterIds(
     country, kind="follower", pseudo_ids=att_sources.entity.tolist())

att_sources = att_sources.merge(sources_twitter_ids, left_on='entity', right_on='pseudo_id')
att_sources = att_sources[['twitter_id']+dims]

# Retrive target annotations
targets_twitter_ids = SQLITE.retrieveAndFormatTwitterIds(
     country, kind="mp", pseudo_ids=att_targets.entity.tolist())
targets_names = SQLITE.retrieveAndFormatMpsNames(
     country, pseudo_ids=att_targets.entity.tolist())

att_targets = att_targets.merge(targets_twitter_ids, left_on='entity', right_on='pseudo_id')
att_targets = att_targets.merge(targets_names, left_on='entity', right_on='mp_pseudo_id')
att_targets = att_targets[['twitter_id', 'name', 'party']+dims]

assert s0 == len(att_sources)
assert t0 == len(att_targets)

print(att_sources.head())
print(att_targets.head())

att_folder = set_output_folder_att(params, country, output)

dims_str = '_vs_'.join(dims)

att_source_path = os.path.join(att_folder, f'att_sources_{dims_str}.csv')
att_sources.to_csv(att_source_path, index=False)
print(f"Source attitudinal embeddings saved at {att_source_path}.")

att_targets_path = os.path.join(att_folder, f'att_targets_{dims_str}.csv')
att_targets.to_csv(att_targets_path, index=False)
print(f"Target attitudinal embeddings saved at {att_targets_path}.")

