import os
import yaml
from argparse import ArgumentParser
from itertools import combinations

from some4demexp.inout import \
    set_output_folder, \
    set_output_folder_emb, \
    load_ide_embeddings, \
    load_targets_groups \

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
print(yaml.dump(vizparams, default_flow_style=False))

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)
print(yaml.dump(params, default_flow_style=False))

# Load ideological embeddings
ide_folder = set_output_folder_emb(params, country, output)
ide_sources, ide_targets = load_ide_embeddings(ide_folder)

# Load target groups
data_folder = set_output_folder(params, country, output)
targets_groups = load_targets_groups(data_folder)

#  ################### HOT FIX 1 ###################
targets_groups = targets_groups.assign(
    party=targets_groups.party.apply(lambda p: p.replace('&', ''))
)
#####################################################


n_dims_to_viz = min(params['ideological_model']['n_latent_dimensions'], 8)

palette = vizparams['palette']
idevizparams = vizparams['ideological']
parties_to_show = palette.keys()

# visualize ideological space
for x, y in combinations(range(n_dims_to_viz), 2):
    visualize_ide(
        sources_coord_ide=ide_sources,
        targets_coord_ide=ide_targets,
        targets_parties=targets_groups,
        latent_dim_x=x,
        latent_dim_y=y,
        parties_to_show=parties_to_show,
        output_folder=ide_folder,
        show=show,
        palette=palette,
        **idevizparams
    )
