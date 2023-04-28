import os
import yaml
from string import Template
from argparse import ArgumentParser
from itertools import combinations

from some4demexp.inout import \
    set_output_folder, \
    set_output_folder_dims, \
    load_ide_embeddings, \
    load_att_embeddings, \
    load_targets_groups \

from some4demexp.bivariate_marginal import \
    visualize_ide, \
    visualize_att


# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--output', type=str, required=True)
ap.add_argument('--country', type=str, required=True)
ap.add_argument('--show', type=str, required=False, default=False)
args = ap.parse_args()
config = args.config
output = args.output
country = args.country
show = args.show


with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)
print(yaml.dump(params, default_flow_style=False))

ATTDIMS = params['attitudinal_dimensions']

palette_path = Template(params['palette_path']).substitute(country=country)
with open(palette_path, "r", encoding='utf-8') as fh:
    palette = yaml.load(fh, Loader=yaml.SafeLoader)

folder = set_output_folder(params, country, output)

ide_sources, ide_targets = load_ide_embeddings(folder)

targets_groups = load_targets_groups(folder)

# visualize ideological space
visualize_ide(
    ide_sources,
    ide_targets,
    targets_groups,
    palette=palette,
    path=os.path.join(folder, "ideological.png")
)

# visualize attitudinal espaces
for dimpair in combinations(ATTDIMS, 2):

    att_sources, att_targets, att_groups = load_att_embeddings(folder, dimpair)

    folder_dims = set_output_folder_dims(folder, dimpair)
    visualize_att(
        att_sources,
        att_targets,
        att_groups,
        targets_groups,
        dims=dict(zip(['x', 'y'], dimpair)),
        palette=palette,
        path=os.path.join(folder_dims, "attitudinal.png")
        )

if show:
    plt.show
