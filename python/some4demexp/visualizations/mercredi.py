import os
import yaml
import pandas as pd
from string import Template
from argparse import ArgumentParser
from itertools import combinations

from some4demdb import SQLite
from some4demexp.inout import \
    get_ide_ndims, \
    set_output_folder_att, \
    load_att_embeddings

from some4demexp.bivariate_marginal import visualize_att
from some4demexp.distributions import distributions

from some4demexp.conf import \
    CHES2019DEFAULTATTVIZ, \
    GPS2019DEFAULTATTVIZ

# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--country', type=str, required=True)
ap.add_argument('--survey', type=str, required=True)
ap.add_argument('--output', type=str, required=True)
ap.add_argument('--vizconfig', type=str, required=True)
ap.add_argument('--show',  action='store_true', required=False)
args = ap.parse_args()
config = args.config
vizconfig = args.vizconfig
survey = args.survey
output = args.output
country = args.country
show = args.show

with open(vizconfig, "r", encoding='utf-8') as fh:
    vizparams = yaml.load(fh, Loader=yaml.SafeLoader)
# print(yaml.dump(vizparams, default_flow_style=False))

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)
# print(yaml.dump(params, default_flow_style=False))

with open(params['params_db'], "r", encoding='utf-8') as fh:
    params_db = yaml.load(fh, Loader=yaml.SafeLoader)

SQLITE = SQLite(
    params['sqlite_db'].format(country=country),
    params_db['output']['tables'],
    country)
ATTDIMS = params['attitudinal_dimensions'][survey]
SURVEYCOL = f'{survey.upper()}_party_acronym'

mps_parties = SQLITE.getMpParties(['MMS', survey], dropna=True)

parties_mapping = SQLITE.getPartiesMapping()
ideN = get_ide_ndims(parties_mapping, survey)


att_folder = set_output_folder_att(
    params, survey, country, ideN, output)
att_sources, att_targets = load_att_embeddings(att_folder)


# (1) show 2d figures

# use mapping to adapt palette to the party system survey
color_data = vizparams['palette'].items()
palette = pd.DataFrame.from_dict(color_data) \
    .rename(columns={0: 'MMS_party_acronym', 1: 'color'}) \
    .merge(SQLITE.getPartiesMapping())
_zip = zip(palette[SURVEYCOL], palette['color'])
palette = {z[0]: z[1] for z in _zip}

parties_coord_att = SQLITE.getPartiesAttitudes(survey, ATTDIMS)

rename_cols = {SURVEYCOL: 'party'}
att_targets.rename(columns=rename_cols, inplace=True)
parties_coord_att.rename(columns=rename_cols, inplace=True)

# When the matchong betwwen MMS and the survey isnot injective,
# keep only one match
parties_coord_att.drop_duplicates(subset=['party'], inplace=True)

# visualize attitudinal espaces
for dimpair in combinations(ATTDIMS, 2):

    dimpair_str = '_vs_'.join(dimpair)
    #  FOR DEBUGGING
    if dimpair_str != 'lrgen_vs_antielite_salience':
        continue

    if dimpair_str in vizparams['attitudinal'][survey]:
        attvizparams = vizparams['attitudinal'][survey][dimpair_str]
    else:
        attvizparams = globals()[f"{survey.upper()}DEFAULTATTVIZ"]

    ########################################
    # MERCREDI user media wheel
    ########################################
    sources_twitter_ids = pd.read_csv('sources_twitter_ids.csv', dtype=str)

    userMedia = pd.read_csv('/home/jimena/Desktop/dataSprint/Nahel/users-medias.csv').astype(str)

    wheel = pd.read_csv(
        '/home/jimena/Desktop/dataSprint/Nahel/CorpusMediaSitesWeb/medias-v10.csv',
        encoding='utf-8',
        lineterminator='\n')

    wheel = wheel[['Label', 'clusters_legend', 'clusters_color']] \
        .rename(columns={'Label': 'media_label'})

    att_sources_with_twitter_id = att_sources[['lrgen', 'antielite_salience', 'entity']] \
        .merge(sources_twitter_ids, left_on='entity', right_on='pseudo_id') \
        .drop(columns=['entity', 'pseudo_id'])
    userMediaAtt = att_sources_with_twitter_id \
        .merge(userMedia, left_on='twitter_id', right_on='user_id') \
        .drop(columns=['user_id', 'twitter_id'])

    userMediaAttMean = userMediaAtt.groupby('media_label').mean()
    userMediaAttMean.reset_index().to_csv(
        '/home/jimena/Desktop/dataSprint/Nahel/media_mean_user_attitudinal_positions.csv', index=False)

    userMediaAttMean =  userMediaAttMean.merge(wheel, on='media_label')


    # palette = {
    #     row['clusters_legend']: row['clusters_color']
    #     for _, row in wheel[['clusters_legend', 'clusters_color']].iterrows()
    # }

    wheel = wheel.rename(columns={
        'clusters_legend': 'CHES2019_party_acronym',
        'media_label': 'entity'
        })

    title = "medias"
    path = '/home/jimena/Desktop/dataSprint/Nahel/media_mean_user_attitudinal_positions.png'
    visualize_att(
        sources_coord_att=att_sources,
        targets_coord_att=userMediaAttMean,
        parties_coord_att=parties_coord_att,
        target_groups=wheel,
        dims=dict(zip(['x', 'y'], dimpair)),
        show=show,
        palette=palette,
        survey=survey,
        title=title,
        path=path,
        **attvizparams
        )

    exit()
