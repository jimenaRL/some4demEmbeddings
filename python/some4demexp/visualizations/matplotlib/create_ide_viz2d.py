import os
import yaml
from argparse import ArgumentParser
from itertools import combinations

from some4demdb import SQLite
from some4demexp.inout import \
    set_output_folder, \
    set_output_folder_emb, \
    load_ide_embeddings

from some4demexp.bivariate_marginal import visualize_ide

# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--country', type=str, required=True)
ap.add_argument('--output', type=str, required=True)
ap.add_argument('--vizconfig', type=str, required=True)
ap.add_argument('--show',  action='store_true', required=False,)
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

# Load ideological embeddings
ide_folder = set_output_folder_emb(params, country, output)
ide_sources, ide_targets = load_ide_embeddings(ide_folder)

n_dims_to_viz = min(params['ideological_model']['n_latent_dimensions'], 3)

palette = vizparams['palette']
idevizparams = vizparams['ideological']
mp_parties = SQLITE.retrieveAndFormatMpParties(['MMS', 'CHES2019'])
targets_parties = mp_parties[['mp_pseudo_id', 'MMS_party_acronym']] \
    .rename(columns={'MMS_party_acronym': 'party'})

# select parties to show
parties_to_show = mp_parties[~mp_parties['CHES2019_party_acronym'].isna()]
parties_to_show = _parties_to_show['MMS_party_acronym'].unique().tolist()

# visualize ideological space
for x, y in combinations(range(n_dims_to_viz), 2):
    visualize_ide(
        sources_coord_ide=ide_sources,
        targets_coord_ide=ide_targets,
        targets_parties=targets_parties,
        parties_to_show=parties_to_show,
        latent_dim_x=x,
        latent_dim_y=y,
        output_folder=ide_folder,
        show=show,
        palette=palette,
        **idevizparams
    )
