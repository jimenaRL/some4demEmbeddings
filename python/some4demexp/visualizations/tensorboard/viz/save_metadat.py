import yaml
from string import Template
from itertools import combinations
from bivariate_marginal import visualize_att, visualize_ide

from some4demexp.utils import \

from some4demexp.utils import \
    set_output_folder, \
    set_output_folder_dims, \
    load_ide_embeddings, \
    load_targets_groups \

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
folder_dims = set_output_folder_dims(folder, dimpair)

_, ide_targets = load_ide_embeddings(folder)


# for TB viz

saveMpsMetadata(
    DB,
    country,
    pids=ide_targets.entity.tolist(),
    path=os.path.join(folder_dims, "mps_metadata.csv"))

if show:
    plt.show
