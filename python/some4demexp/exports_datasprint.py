import os
import yaml
import pandas as pd
from string import Template
from argparse import ArgumentParser

from some4demdb import SQLite
from some4demexp.inout import \
    get_ide_ndims, \
    set_output_folder_att, \
    load_att_embeddings, \
    set_output_folder, \
    load_experiment_data

# (0) parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--country', type=str, required=True)
ap.add_argument('--output', type=str, required=False)
args = ap.parse_args()
config = args.config
output = args.output
country = args.country

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)

with open(params['params_db'], "r", encoding='utf-8') as fh:
    dbParams = yaml.load(fh, Loader=yaml.SafeLoader)

SQLITE = SQLite(
    params['sqlite_db'].format(country=country),
    dbParams['output']['tables'],
    country)

PARTIESMAPPING = SQLITE.getPartiesMapping()

# (1) load attitudinal embeddings and descriptions
survey = 'ches2019'
SURVEYCOL = f'{survey.upper()}_party_acronym'
ideN = get_ide_ndims(PARTIESMAPPING, survey)
ATTFOLDER = set_output_folder_att(
    params, survey, country, ideN, output)
att_sources, att_targets = load_att_embeddings(ATTFOLDER)

mssg = f"Found {len(att_targets)} targets with "
mssg += f"attitudinal embeddings in survey {survey}"
print(mssg)

mssg = f"Found {len(att_sources)} sources with "
mssg += f"attitudinal embeddings in survey {survey}"
print(mssg)

# (2) get twitter ids and graph
sources_twitter_ids = SQLITE.getTwitterIds(
    entity="follower", pseudo_ids=att_sources.entity.tolist())

targets_twitter_ids = SQLITE.getTwitterIds(
    entity="mp", pseudo_ids=att_targets.entity.tolist())

res_graph = SQLITE.retrieveGraph(
    'follower', valid=att_sources['entity'].tolist())
graph = pd.DataFrame(res_graph, columns=['targets_pids', 'sources_pids'])


# (3) prepare exports

export_sources = att_sources[['entity', 'lrgen', 'antielite_salience']] \
    .merge(sources_twitter_ids, left_on='entity', right_on='pseudo_id') \
    .drop(columns=["entity", "pseudo_id"]) \
    .rename(columns={"twitter_id": "sources_twitter_id"})
assert(len(export_sources) == len(sources_twitter_ids))

export_targets = att_targets[['entity', 'lrgen', 'antielite_salience']] \
    .merge(targets_twitter_ids, left_on='entity', right_on='pseudo_id') \
    .drop(columns=["entity", "pseudo_id"]) \
    .rename(columns={"twitter_id": "targets_twitter_id"})
assert(len(export_targets) == len(targets_twitter_ids))


graph = graph.merge(
        sources_twitter_ids,
        right_on='pseudo_id',
        left_on='sources_pids') \
    .drop(columns=["pseudo_id", "sources_pids"]) \
    .rename(columns={"twitter_id": "sources_twitter_id"})
assert graph.sources_twitter_id.nunique() == len(export_sources)

graph = graph.merge(
        targets_twitter_ids,
        right_on='pseudo_id',
        left_on='targets_pids')\
    .drop(columns=["pseudo_id", "targets_pids"]) \
    .rename(columns={"twitter_id": "targets_twitter_id"})
assert graph.targets_twitter_id.nunique() == len(export_targets)
assert graph.sources_twitter_id.nunique() == len(export_sources)

vstid = set(graph['sources_twitter_id'].tolist())
export_sources = export_sources[export_sources.sources_twitter_id.isin(vstid)]
assert graph.sources_twitter_id.nunique() == len(export_sources)


# (4) save
graph.astype(str).to_csv(
    'MedialexDatasprint/france_bipartite_graph.csv', index=False)
export_targets.astype(str).to_csv(
    'MedialexDatasprint/france_mps_attitudinal_embeddings.csv', index=False)
export_sources.astype(str).to_csv(
    'MedialexDatasprint/france_followers_attitudinal_embeddings.csv', index=False)
