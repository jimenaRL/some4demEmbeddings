import os
import yaml
from string import Template
from argparse import ArgumentParser
from itertools import combinations

from some4demdb import SQLite
from some4demexp.inout import \
    set_output_folder_emb, \
    set_output_folder_att, \
    load_att_embeddings, \
    load_targets_groups, \
    set_output_folder

from some4demexp.bivariate_marginal import visualize_att

# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--country', type=str, required=True)
ap.add_argument('--output', type=str, required=True)
ap.add_argument('--vizconfig', type=str, required=True)
ap.add_argument('--show',  action='store_true', required=False)
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


SQLITE = SQLite(params['sqlite_db'])

ATTDIMS = params['attitudinal_dimensions']

ide_folder = set_output_folder_emb(params, country, output)
att_folder = set_output_folder_att(params, country, output)
att_sources, att_targets = load_att_embeddings(att_folder)

palette = vizparams['palette']
parties_to_show = palette.keys()

parties_coord_att = SQLITE.retrieveAndFormatTargetGroupsAttitudes(
    country,
    ATTDIMS)

# visualize attitudinal espaces
for dimpair in combinations(ATTDIMS, 2):

    dimpair_str = '_vs_'.join(dimpair)

    # #  FOR DEBUGGING
    # if dimpair_str != 'lrgen_vs_antielite_salience':
    #     continue

    attvizparams = vizparams['attitudinal'][dimpair_str]

    visualize_att(
        sources_coord_att=att_sources,
        targets_coord_att=att_targets,
        parties_coord_att=parties_coord_att,
        dims=dict(zip(['x', 'y'], dimpair)),
        parties_to_show=parties_to_show,
        path=os.path.join(att_folder, f"{dimpair_str}.png"),
        show=show,
        palette=palette,
        **attvizparams
        )
