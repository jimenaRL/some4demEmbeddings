import os
import yaml
import pandas as pd
from string import Template
from argparse import ArgumentParser
from itertools import combinations

from some4demdb import SQLite
from some4demexp.inout import \
    set_output_folder_emb, \
    set_output_folder_att, \
    load_att_embeddings, \
    set_output_folder

from some4demexp.bivariate_marginal import visualize_att

# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--country', type=str, required=True)
ap.add_argument('--output', type=str, required=True)
ap.add_argument('--vizconfig', type=str, required=True)
ap.add_argument('--show',  action='store_true', required=False)
args = ap.parse_args()
config = args.config
vizconfig = args.vizconfig
output = args.output
country = args.country
show = args.show

with open(vizconfig, "r", encoding='utf-8') as fh:
    vizparams = yaml.load(fh, Loader=yaml.SafeLoader)
# print(yaml.dump(vizparams, default_flow_style=False))

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)
print(yaml.dump(params, default_flow_style=False))

with open(params['params_db'], "r", encoding='utf-8') as fh:
    params_db = yaml.load(fh, Loader=yaml.SafeLoader)

SQLITE = SQLite(params['sqlite_db'], params_db['output']['tables'], country)
ATTDIMS = params['attitudinal_dimensions']

ide_folder = set_output_folder_emb(params, country, output)
att_folder = set_output_folder_att(params, country, output)
att_sources, att_targets = load_att_embeddings(att_folder)

# use mapping to adapt palette to the party system survey
color_data = vizparams['palette'].items()
palette = pd.DataFrame.from_dict(color_data) \
    .rename(columns={0: 'MMS_party_acronym', 1: 'color'}) \
    .merge(SQLITE.getPartiesMapping())
_zip = zip(palette['CHES2019_party_acronym'], palette['color'])
palette = {z[0]: z[1] for z in _zip}

# select parties to show
mp_parties = SQLITE.retrieveAndFormatMpParties(['MMS', 'CHES2019'])
_parties_to_show = mp_parties[~mp_parties['CHES2019_party_acronym'].isna()]
parties_to_show = _parties_to_show['CHES2019_party_acronym'].unique().tolist()

parties_coord_att = SQLITE.retrieveAndFormatPartiesAttitudes('CHES2019', ATTDIMS)

rename_cols = {'CHES2019_party_acronym': 'party'}
att_targets.rename(columns=rename_cols, inplace=True)
parties_coord_att.rename(columns=rename_cols, inplace=True)

# visualize attitudinal espaces
for dimpair in combinations(ATTDIMS, 2):

    dimpair_str = '_vs_'.join(dimpair)

    #  FOR DEBUGGING
    if dimpair_str not in [
        'lrgen_vs_antielite_salience',
        'lrgen_vs_lrecon',
        'galtan_vs_environment',
        'eu_position_vs_immigrate_policy',
    ]:
        continue

    attvizparams = vizparams['attitudinal'][dimpair_str]

    visualize_att(
        sources_coord_att=att_sources,
        targets_coord_att=att_targets,
        parties_coord_att=parties_coord_att,
        dims=dict(zip(['x', 'y'], dimpair)),
        parties_to_show=parties_to_show,
        path=os.path.join(att_folder, f"{dimpair_str}.png"),
        show=show,
        palette=palette,
        **attvizparams
        )
