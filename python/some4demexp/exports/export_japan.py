import os
import yaml
from argparse import ArgumentParser

from some4demdb import SQLite
from some4demexp.graph import graphToAdjencyMatrix
from some4demexp.inout import \
    set_output_folder_emb, \
    load_ide_embeddings



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
N = params['ideological_model']['n_latent_dimensions']

# Load ideological embeddigns
ide_folder = set_output_folder_emb(params, country, output)
ide_sources, ide_targets = load_ide_embeddings(ide_folder)

s0 = len(ide_sources)

# Retrive sources annotations
sources_twitter_ids = SQLITE.retrieveAndFormatTwitterIds(
     country, kind="follower", pseudo_ids=ide_sources.entity.tolist())

dims = [f"latent_dimension_{i}" for i in range(N)]

ide_sources = ide_sources.merge(
     sources_twitter_ids,
     left_on='entity',
     right_on='pseudo_id'
)
ide_sources = ide_sources[['twitter_id']+dims]

# Retrive target annotations
targets_twitter_ids = SQLITE.retrieveAndFormatTwitterIds(
     country, kind="mp", pseudo_ids=ide_targets.entity.tolist())
targets_names = SQLITE.retrieveAndFormatMpsNames(
     country, pseudo_ids=ide_targets.entity.tolist())
mps_parties = SQLITE.retrieveAndFormatTargetGroups(country)

ide_targets = ide_targets.merge(
     targets_twitter_ids,
     left_on='entity',
     right_on='pseudo_id')
ide_targets = ide_targets.merge(
     targets_names,
     left_on='entity',
     right_on='mp_pseudo_id'
)

ide_targets = ide_targets.merge(
     mps_parties,
     left_on='entity',
     right_on='mp_pseudo_id'
)

# twitter_id,name,party,lrgen,antielite_salience
ide_targets = ide_targets[['twitter_id', 'name', 'party']+dims]

assert s0 == len(ide_sources)

print(ide_sources.columns)
print(ide_targets.columns)

ide_source_path = os.path.join(ide_folder, f'ide_sources_with_tid.csv')
ide_sources.to_csv(ide_source_path, index=False)
print(f"Source attitudinal embeddings saved at {ide_source_path}.")

ide_targets_path = os.path.join(ide_folder, f'ide_targets_with_tid.csv')
ide_targets.to_csv(ide_targets_path, index=False)
print(f"Target attitudinal embeddings saved at {ide_targets_path}.")

