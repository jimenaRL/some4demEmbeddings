import os
import yaml
import pandas as pd
from argparse import ArgumentParser

from some4demdb import SQLite
from some4demexp.conf import CHESLIMS
from some4demexp.inout import \
    set_output_folder_att, \
    load_att_embeddings

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

SQLITE = SQLite(params['sqlite_db'], params['issues'])
ATTFOLDER = set_output_folder_att(params, country, output)

# (1) get enriched descriptions
descriptions = SQLITE.getEnrichedDescriptions(args.country)

# (2) load attitudinal embeddigns and descriptions
att_sources, _ = load_att_embeddings(ATTFOLDER)

# (3) merge
att_descript = descriptions.merge(
    att_sources,
    left_on='pseudo_id',
    right_on='entity',
    how='inner'
) \
.drop(columns=["pseudo_id"])

# (4) export
export_path = os.path.join(
    # ATTFOLDER,
    f'{country}_att_sources_with_descriptions_{len(att_descript)}.csv')

att_descript.to_csv(export_path, index=False, sep=',', encoding='utf-8', lineterminator='\n')

print(att_descript)
print(f"Source attitudinal embeddings with description saved at {export_path}.")