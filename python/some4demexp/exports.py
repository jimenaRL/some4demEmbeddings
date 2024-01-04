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
    set_output_folder


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

LLMISSUES = dbParams['enrichments']['steps']['llm_annotations']['prompts']

SQLITE = SQLite(
    params['sqlite_db'].format(country=country),
    dbParams['output']['tables'],
    country)

PARTIESMAPPING = SQLITE.getPartiesMapping()

# (1) load attitudinal embeddings and descriptions
att_embeddings = dict()
for survey in ['ches2019', 'gps2019']:
    SURVEYCOL = f'{survey.upper()}_party_acronym'
    ideN = get_ide_ndims(PARTIESMAPPING, survey)
    ATTFOLDER = set_output_folder_att(
        params, survey, country, ideN, output)
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
mssg = f"Found {len(export)} users with "
mssg += f"attitudinal embeddings for both surveys 'ches2019' and 'gps2019'."
print(mssg)

# (2) get enriched descriptions, keywords labels and llm annotations
enrichments = SQLITE.getEnrichments(entity='user')

keywords_labels = SQLITE.getKeywordsLabels(entity='user')

llm_labels = SQLITE.getLLMLabels('user')

# (3) merge attitudinal embeddings, enrichements and keywords annotations
export = export.merge(
    enrichments,
    on='pseudo_id',
    how='inner'
)
lo = len(export)
print(f"Found {lo} users with attitudinal embeddings and enrichments")

export = export.merge(
    keywords_labels,
    on='pseudo_id',
    how='inner'
)
lo = len(export)
print(f"Found {lo} users with attitudinal embeddings and keywords labels")


export = export.merge(
    llm_labels,
    on='pseudo_id',
    how='inner'
)
lo = len(export)
print(f"Found {lo} users with attitudinal embeddings and llm labels")


# (4) Add twitter ids and handlers
sources_twitter_ids = SQLITE.getTwitterIds(
    entity="follower", pseudo_ids=export.pseudo_id.tolist())

export = export.merge(sources_twitter_ids, on='pseudo_id')
assert len(export) == lo

metadata = SQLITE.getMetadata(
    entity="user",
    columns=['pseudo_id', 'screen_name'])

export = export.merge(metadata, on='pseudo_id')
assert len(export) == lo
print(f"Twitter ids and handlers added.")

# (5) export

FOLDER = set_output_folder(params, country, output)

export_path = os.path.join(
    FOLDER,
    f'{country}_att_embeddings_with_annotations_{len(export)}')

export.to_csv(
    export_path+'.csv',
    index=False,
    sep=',',
    encoding='utf-8',
    lineterminator='\n')

# ANOTHER HOTFIX
try:
    export.to_excel(
        export_path+'.xlsx',
        index=False,
        sheet_name=country,
        engine='xlsxwriter',
        float_format="%.2f")
except:
    export = export.assign(
        description=export.description.apply(lambda s: s.replace('nµ', '')))
    export.to_excel(
        export_path+'.xlsx',
        index=False,
        sheet_name=country,
        engine='xlsxwriter',
        float_format="%.2f")

print(
    f"Attitudinal embeddings with annotations saved with name {export_path}.")
