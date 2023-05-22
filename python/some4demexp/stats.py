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
args = ap.parse_args()
config = args.config
output = args.output
country = args.country

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)
print(yaml.dump(params, default_flow_style=False))

ATTDIMS = params['attitudinal_dimensions']

ide_folder = set_output_folder_emb(params, country, output)
ide_sources, ide_targets = load_ide_embeddings(ide_folder)

ide_sources_stats = ide_sources.describe()
print(f"Ideological embeddings sources stats:\n{ide_sources_stats}")
ide_sources_stats.to_csv(os.path.join(ide_folder, "ide_sources_stats.csv"))

ide_targets_stats = ide_targets.describe()
print(f"Ideological embeddings target stats:\n{ide_targets_stats}")
ide_targets_stats.to_csv(os.path.join(ide_folder, "ide_targets_stats.csv"))

print(f"Ideological embeddings stats saved at: {ide_folder}.")

att_folder = set_output_folder_att(params, country, output)
att_sources, att_targets, att_groups = load_att_embeddings(att_folder)

att_sources_stats = att_sources.describe()
print(f"Attitudinal embeddings sources stats:\n{att_sources_stats}")
att_sources_stats.to_csv(os.path.join(att_folder, "att_sources_stats.csv"))

att_targets_stats = att_targets.describe()
print(f"Attitudinal embeddings targets stats:\n{att_targets_stats}")
att_targets_stats.to_csv(os.path.join(att_folder, "att_targets_stats.csv"))

att_groups_stats = att_groups.describe()
print(f"Attitudinal embeddings parties stats:\n{att_groups_stats}")
att_groups_stats.to_csv(os.path.join(att_folder, "att_groups_stats.csv"))


print(f"Attitudinal embeddings stats saved at: {att_folder}.")
