import yaml
from argparse import ArgumentParser

from linate import IdeologicalEmbedding
from some4demexp.inout import \
    set_output_folder, \
    set_output_folder_emb, \
    load_experiment_data, \
    save_ide_embeddings

# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--country', type=str, required=True)
ap.add_argument('--output', type=str, required=False, default='-1')
args = ap.parse_args()
config = args.config
output = args.output
country = args.country

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)
print(yaml.dump(params, default_flow_style=False))

data_folder = set_output_folder(params, country, output)
X, targets_pids, sources_pids = load_experiment_data(data_folder)

# Create and fit ideological embedding
model = IdeologicalEmbedding(**params["ideological_model"])
model.fit(X)

# Save sources/targets coordinates in ideological space and add pseudo ids
emb_folder = set_output_folder_emb(params, country, output)
save_ide_embeddings(model, sources_pids, targets_pids, emb_folder)
