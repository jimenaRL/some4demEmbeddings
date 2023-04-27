import yaml
from string import Template
from itertools import combinations
from viz import *
from utils import *

from argparse import ArgumentParser

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

palette_path = Template(params['palette_path']) \
    .substitute(country=country)

with open(palette_path, "r", encoding='utf-8') as fh:
    palette = yaml.load(fh, Loader=yaml.SafeLoader)

DB = params['sqlite_db']
ATTDIMS = params['attitudinal_dimensions']

folder = set_output_folder(params, country, output)

ide_sources, ide_targets = load_ide_embeddings(folder)

targets_groups = load_targets_groups(folder)

visualize_ide(
    ide_sources,
    ide_targets,
    targets_groups,
    palette=palette,
    path=os.path.join(folder, "ideological.png")
)


for dimpair in combinations(ATTDIMS, 2):

    att_sources, att_targets, att_groups = load_att_embeddings(folder, dimpair)

    visualize_att(
        att_sources,
        att_targets,
        att_groups,
        targets_groups,
        dims=dict(zip(['x', 'y'], dimpair)),
        palette=palette,
        path=os.path.join(
            set_output_folder_dims(folder, dimpair), "attitudinal.png")
        )

# for TB viz

saveMpsMetadata(
    DB,
    country,
    pids=ide_targets.entity.tolist(),
    path=os.path.join(
            set_output_folder_dims(folder, dimpair), "mps_metadata.csv"))

if show:
    plt.show
