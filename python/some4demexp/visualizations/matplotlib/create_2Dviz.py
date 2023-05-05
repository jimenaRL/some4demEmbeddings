import os
import yaml
from string import Template
from argparse import ArgumentParser
from itertools import combinations

from some4demexp.inout import \
    set_output_folder, \
    set_output_folder_emb, \
    set_output_folder_att, \
    load_ide_embeddings, \
    load_att_embeddings, \
    load_targets_groups \

from some4demexp.bivariate_marginal import \
    visualize_ide, \
    visualize_att

# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--country', type=str, required=True)
ap.add_argument('--output', type=str, required=True)
ap.add_argument('--vizconfig', type=str, required=True)
ap.add_argument('--show', type=bool, required=False)
args = ap.parse_args()
config = args.config
vizconfig = args.vizconfig
output = args.output
country = args.country
show = args.show

with open(vizconfig, "r", encoding='utf-8') as fh:
    vizparams = yaml.load(fh, Loader=yaml.SafeLoader)[country]
print(yaml.dump(vizparams, default_flow_style=False))

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)
print(yaml.dump(params, default_flow_style=False))

ATTDIMS = params['attitudinal_dimensions']

ide_folder = set_output_folder_emb(params, country, output)
ide_sources, ide_targets = load_ide_embeddings(ide_folder)
ide_images_folder = os.path.join(ide_folder, 'pairwise_latent_dimensions_images')
os.makedirs(ide_images_folder, exist_ok=True)

# Load target groups
data_folder = set_output_folder(params, country, output)
targets_groups = load_targets_groups(data_folder)

# visualize ideological space
ide_dims = range(params['ideological_model']['n_latent_dimensions'])
for x, y in combinations(ide_dims, 2):
    visualize_ide(
        ide_sources,
        ide_targets,
        targets_groups,
        latent_dim_x=x,
        latent_dim_y=y,
        output_folder=ide_images_folder,
        show=show,
        **vizparams
    )

exit()

# visualize attitudinal espaces
for dimpair in combinations(ATTDIMS, 2):

    att_folder = set_output_folder_att(ide_folder, dimpair)
    att_sources, att_targets, att_groups = load_att_embeddings(att_folder)

    visualize_att(
        att_sources,
        att_targets,
        att_groups,
        targets_groups,
        dims=dict(zip(['x', 'y'], dimpair)),
        palette=palette,
        path=os.path.join(att_folder, "attitudinal.png")
        )