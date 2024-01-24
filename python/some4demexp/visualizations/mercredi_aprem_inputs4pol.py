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

# (0) show by dim distributions
# distributions(
#     att_sources,
#     att_targets,
#     country,
#     survey,
#     show)

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
    if dimpair_str not in [
        # FOR TESTING
        # 'lrgen_vs_antielite_salience',
        # 'V4_Scale_vs_V6_Scale',
        # FOR MIRO VIZ
        'lrgen_vs_antielite_salience',
        # 'lrgen_vs_lrecon',
        # 'galtan_vs_environment',
        # 'eu_position_vs_immigrate_policy',
        # 'V6_Scale_vs_v14',
        # 'V4_Scale_vs_V6_Scale',
        # 'v12_vs_v13',
        # 'v10_vs_v20',
    ]:
        continue

    if dimpair_str in vizparams['attitudinal'][survey]:
        attvizparams = vizparams['attitudinal'][survey][dimpair_str]
    else:
        attvizparams = globals()[f"{survey.upper()}DEFAULTATTVIZ"]


    sources_twitter_ids = pd.read_csv('sources_twitter_ids.csv', dtype=str)

    att_sources_with_twitter_id = att_sources[['lrgen', 'antielite_salience', 'entity']] \
        .merge(sources_twitter_ids, left_on='entity', right_on='pseudo_id') \
        .drop(columns=['entity', 'pseudo_id'])


    for kind in ['liot', 'lola', 'nahel', 'stesoline']:

        print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {kind} ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        byDays = pd.read_csv(
            f'/home/jimena/Desktop/dataSprint/Nahel/inputs4pol/{kind}_input_for_politization_metrics.csv').astype(str)

        byDays = byDays \
            .reset_index() \
            .rename(columns={'index': 'line_nb'})


        byDays = byDays \
            .assign(accountsIdsSplit=byDays.accountsIds.apply(lambda s: s.split('|')))

        byDays = byDays \
            .assign(nbAccountsInit=byDays.accountsIdsSplit.apply(lambda s: len(s)))

        byDays = byDays \
            .explode('accountsIdsSplit')

        b0 = byDays.accountsIdsSplit.nunique()

        byDays = byDays.merge(att_sources_with_twitter_id, left_on='accountsIdsSplit', right_on='twitter_id')

        b1 = byDays.accountsIdsSplit.nunique()

        totalRecouvrementPerc = 100 - 100 * (b0 - b1) / b0
        print(f"Recouvrement percentage : {b0 - b1} ({totalRecouvrementPerc}%) twitter users")


        nbAccountsEnd = byDays[['line_nb', 'twitter_id']] \
            .groupby('line_nb') \
            .count() \
            .reset_index()\
            .rename(columns={'twitter_id': 'nbAccountsEnd'})

        byDays = byDays.merge(nbAccountsEnd, on='line_nb')

        b1 = byDays.accountsIdsSplit.nunique()

        byDays = byDays[['line_nb', 'lrgen', 'antielite_salience', 'nbAccountsInit', 'nbAccountsEnd']] \
            .groupby('line_nb') \
            .mean() \
            .reset_index()

        byDays = byDays.assign(recouvrementPerc=100 * byDays['nbAccountsEnd'] / byDays['nbAccountsInit'])
        byDays = byDays.assign(lrgen=byDays['lrgen']/10)
        byDays = byDays.assign(antielite_salience=byDays['antielite_salience']/10)

        print(byDays)
        path = f'/home/jimena/Desktop/dataSprint/Nahel/{kind}_politization_metrics_totalRecouvrement_{int(totalRecouvrementPerc)}perc.csv'
        byDays.to_csv(path, index=False)
        print(f"Saved at {path}")
