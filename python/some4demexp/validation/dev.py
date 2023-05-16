import re
import yaml
import pandas as pd
from itertools import combinations
from some4demdb import SQLite
from some4demexp.inout import \
    set_output_folder_emb, \
    load_ide_embeddings, \
    set_output_folder_att, \
    load_att_embeddings

# parse arguments and set paths
# ap = ArgumentParser()
# ap.add_argument('--config', type=str, required=True)
# ap.add_argument('--country', type=str, required=True)
# ap.add_argument('--output', type=str, required=True)
# args = ap.parse_args()
# config = args.config
# country = args.country
# output = args.output

country = 'france'
config = 'config15D.yaml'
output = 'outputs'

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)
print(yaml.dump(params, default_flow_style=False))

SQLITE = SQLite(params['sqlite_db'])
ATTDIMS = params['attitudinal_dimensions']


ide_folder = set_output_folder_emb(params, country, output)
ide_sources, ide_targets = load_ide_embeddings(ide_folder)

entities = pd.concat([
        ide_sources['entity'],
        ide_targets['entity']]) \
    .drop_duplicates()

descriptions = SQLITE.retrieveAndFormatUsersDescriptions(country, entities)

print(descriptions)

dimpair = ('lrgen', 'antielite_salience')
att_folder = set_output_folder_att(ide_folder, dimpair)
att_sources, att_targets, att_groups = load_att_embeddings(att_folder)

data = att_sources \
    .merge(descriptions, left_on='entity', right_on='pseudo_id') \
    .drop(columns=['entity'])

print(data.head())

issues = 'issues.yaml'
with open(issues, "r", encoding='utf-8') as fh:
    issues = yaml.load(fh, Loader=yaml.SafeLoader)


for issue in issues:
    for k in issues[issue]['fr']:
        regex = re.compile(k)
        data[f'{issue}'] = data.description.apply(lambda d: regex.search(d)))