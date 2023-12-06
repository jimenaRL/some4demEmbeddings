import os
import yaml
import pandas as pd
from string import Template
from argparse import ArgumentParser

from some4demdb import SQLite
from some4demexp.inout import \
    set_output_folder_emb, \
    set_output_folder_att, \
    load_ide_embeddings, \
    load_att_embeddings, \
    set_output_folder


# (0) parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--country', type=str, required=True)
ap.add_argument('--output', type=str, required=False, default='outputs')
args = ap.parse_args()
config = args.config
output = args.output
country = args.country

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)

with open(params['params_db'], "r", encoding='utf-8') as fh:
    params_db = yaml.load(fh, Loader=yaml.SafeLoader)

SQLITE = SQLite(params['sqlite_db'], params_db['output']['tables'], country)

# (1) load attitudinal embeddings and descriptions
att_embeddings = dict()
for survey in ['ches2019', 'gps2019']:
    ATTFOLDER = set_output_folder_att(params, survey, country, output)
    att_followers, att_mps = load_att_embeddings(ATTFOLDER)
    att_mps.drop(
        columns=['MMS_party_acronym', f'{survey.upper()}_party_acronym'],
        inplace=True)
    att_embeddings[survey] = pd.concat([att_followers, att_mps])
    mssg = f"Found {len(att_embeddings[survey])} users with "
    mssg += f"attitudinal embeddings in survey {survey}"
    print(mssg)

export = att_embeddings['gps2019'].merge(
    att_embeddings['ches2019'],
    on='entity',
    how='inner'
) \
.rename(columns={'entity':'pseudo_id'})
assert len(export) == len(att_embeddings['ches2019'])

# (2) get enriched descriptions
anottations = SQLITE.getAnnotations(entity='user')

# (3) merge
export = export.merge(
    anottations,
    on='pseudo_id',
    how='inner'
)
lo = len(export)
print(f"Found {lo} users with attitudinal embeddings and anottations")

# (4) Add twitter ids and handlers
sources_twitter_ids = SQLITE.retrieveAndFormatTwitterIds(
    entity="follower", pseudo_ids=export.pseudo_id.tolist())

export = export.merge(sources_twitter_ids, on='pseudo_id')
assert len(export) == lo

metadata = SQLITE.getMetadata(
    entity="user",
    columns=['pseudo_id', 'screen_name'])

export = export.merge(metadata, on='pseudo_id')
assert len(export) == lo

# (5) export
export_path = os.path.join(
    # ATTFOLDER,
    f'{country}_att_embeddings_with_annotations_{len(export)}')

export.to_csv(
    export_path+'.csv',
    index=False,
    sep=',',
    encoding='utf-8',
    lineterminator='\n')


export.to_excel(
    export_path+'.xlsx',
    index=False,
    sheet_name=country,
    engine='openpyxl',
    float_format="%.2f")

print(
    f"Attitudinal embeddings with annotations saved with name {export_path}.")
