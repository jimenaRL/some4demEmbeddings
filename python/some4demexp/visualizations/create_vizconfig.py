import os
import yaml
import copy
import pandas as pd
from glob import glob
from itertools import combinations

from argparse import ArgumentParser


# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--country', type=str, required=True)
ap.add_argument('--vizfolder', type=str, required=True)
args = ap.parse_args()
config = args.config
vizfolder = args.vizfolder
country = args.country

COLORS = {
    'mediumvioletred',
    'tab:purple',
    'tab:pink',
    'cornflowerblue',
    'tab:green',
    'orangered',
    'red',
    'tab:blue',
    'black',
    'tab:brown',
    'navy',
    'gold',
    'magenta'
}


# don't create vizualtion config if it already exists
vizconfig_path = os.path.join("vizconfigs", config.replace("config", country))
if os.path.exists(vizconfig_path):
    print(f"Vizualisation config found at: {vizconfig_path}")
    exit()

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)


template_path = os.path.join(vizfolder, "template.yaml")
with open(template_path, "r", encoding='utf-8') as fh:
    template = yaml.load(fh, Loader=yaml.SafeLoader)

vizparams = copy.deepcopy(template)

attitudes_path = os.path.join(
    os.environ["DATA"],
    "some4dem/annotations",
    country,
    f"{country.upper()}_group_attitudes.csv"
)
attitudes = pd.read_csv(attitudes_path)
parties = attitudes.party.unique()

vizparams["palette"] = dict(zip(parties, COLORS))

vizparams["ideological"]["nudges"] = {p: [0, 0] for p in parties}


ATTDIMS = params['attitudinal_dimensions']
for dimpair in combinations(ATTDIMS, 2):

    vizparams['attitudinal']['_vs_'.join(dimpair)] = template["attitudinal"]["att1_vs_att2"]
    vizparams['attitudinal']['_vs_'.join(dimpair)]["nudges"] = {p: [0, 0] for p in parties}

del vizparams['attitudinal']['att1_vs_att2']

with open(vizconfig_path, "w", encoding='utf-8') as fh:
    yaml.dump(vizparams, fh)

print(f"Vizualisation config created at: {vizconfig_path}")
