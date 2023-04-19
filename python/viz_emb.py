import yaml
from viz import *
from utils import *

from argparse import ArgumentParser

# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--output', type=str, required=True)
args = ap.parse_args()
config = args.config
output = args.output

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)
print(yaml.dump(params, default_flow_style=False))

ATTSPACES = params['attitudinal_spaces']
PALETTE = params['palette']

folder = set_output_folder(params, output)

ide_sources, ide_targets = load_ide_embeddings(folder)

targets_groups = load_targets_groups(folder)

visualize_ide(
    ide_sources,
    ide_targets,
    targets_groups,
    palette=PALETTE,
    path=os.path.join(folder, "ideological.png")
)


for dims in ATTSPACES.values():

    att_sources, att_targets, att_groups = load_att_embeddings(folder, dims)

    visualize_att(
        att_sources,
        att_targets,
        att_groups,
        targets_groups,
        dims=dict(zip(['x', 'y'], dims)),
        palette=PALETTE,
        path=os.path.join(
            set_output_folder_dims(folder, dims), "attitudinal.png")
        )


# plt.show()
