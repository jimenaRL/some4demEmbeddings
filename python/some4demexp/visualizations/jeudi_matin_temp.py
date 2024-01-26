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
    # JEUDI MATIN
    ########################################

    from glob import glob
    from tqdm import tqdm
    from datetime import datetime, timedelta, timezone

    import seaborn as sns
    sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
    import matplotlib.pyplot as plt

    # sources_twitter_ids = pd.read_csv('sources_twitter_ids.csv').astype(str)
    # att_sources_with_twitter_id = att_sources.merge(sources_twitter_ids, left_on='entity', right_on='pseudo_id')
    # att_sources_with_twitter_id = att_sources_with_twitter_id[['lrgen', 'antielite_salience', 'twitter_id']]

    # files = glob('/home/jimena/Desktop/dataSprint/Nahel/users/users-time_*.csv')

    # records = []
    # all_users_time = []
    # for file in files:

    #     kind = file.split('users-time_')[-1].split('.csv')[0]
    #     users_time = pd.read_csv(file)
    #     users_time = users_time.sort_values(by='local_time')

    #     l0 = len(users_time)

    #     users_time = att_sources_with_twitter_id.merge(
    #         users_time[['user_id', 'local_time']].astype('str'),
    #         left_on='twitter_id',
    #         right_on='user_id') \
    #         .rename(columns={'twitter_id': 'entity'})

    #     title = kind

    #     path = os.path.join(
    #         "/home/jimena/Desktop/dataSprint/Nahel/figs/users-time",
    #        f'{kind}.png')


    #     record = {
    #         "nb_total": l0,
    #         "nb_coincidences": len(users_time),
    #         "prop_coincidences": 100 * float(len(users_time) / l0),
    #         "type": kind,
    #         }

    #     print(record)
    #     records.append(record)

    #     all_users_time.append(
    #         users_time \
    #             .assign(type=title) \
    #             .rename(columns={'user_id': 'twitter_id'}) \
    #             .drop(columns='entity') \
    #             .reset_index() \
    #             .drop(columns="index"))


    # records = pd.DataFrame.from_records(records)

    # all_users_time = pd.concat(all_users_time)

    # all_users_time = all_users_time.sort_values(by='local_time')

    # print(records)
    # print(all_users_time)


    # # make buckets

    # min_date = all_users_time['local_time'].min()
    # max_date = all_users_time['local_time'].max()

    # start_date_a = datetime(2023, 6, 27, 00)
    # start_date_b = datetime(2023, 6, 27, 12)
    # end_date = datetime(2023, 7, 18, 23, 59)

    # def between(date, init, end):
    #     return init < date and date < end

    # format_dates = [datetime.strptime(s, '%Y-%m-%dT%H:%M:%S') for s in all_users_time['local_time'].tolist()]

    # bucket = 0
    # dfbuckets = []
    # while start_date_a < end_date:
    #     dfbucket = all_users_time[[between(f, start_date_a, start_date_b) for f in format_dates]]
    #     dfbucket = dfbucket.assign(bucket=bucket)
    #     print(dfbucket)
    #     print("-----------------")
    #     dfbuckets.append(dfbucket)
    #     bucket += 1
    #     start_date_a += timedelta(hours=12)
    #     start_date_b += timedelta(hours=12)

    # dfbuckets = pd.concat(dfbuckets)


    # dfbuckets.to_csv('/home/jimena/Desktop/dataSprint/Nahel/users/users-time_all_withBucket_withAtt.csv', index=False)

    dfbuckets = pd.read_csv('/home/jimena/Desktop/dataSprint/Nahel/users/users-time_all_withBucket_withAtt.csv')

    buckets = dfbuckets.bucket.unique()
    types = dfbuckets.type.unique().tolist()

    # sources_twitter_ids = pd.read_csv('sources_twitter_ids.csv').astype(str)
    # att_sources_with_twitter_id = att_sources.merge(sources_twitter_ids, left_on='entity', right_on='pseudo_id')
    # att_sources_with_twitter_id = att_sources_with_twitter_id[['lrgen', 'antielite_salience', 'twitter_id']]

    att_sources = att_sources.rename(columns={'entity': 'twitter_id'})

    for typ in types:

        for bucket in buckets:

            df = dfbuckets[dfbuckets.bucket == bucket]

            df = df[df.type==typ]

            df = pd.concat([
                df,
                att_sources.assign(type='base')[['lrgen', 'type', 'twitter_id']]])

            # ------------------------------------------------------------------
            # ----------------------- type vs base distr -----------------------
            # ------------------------------------------------------------------

            # df = df[['lrgen', 'type', 'twitter_id']].rename(columns={'lrgen':'x', 'type':'g'})

            # df = df.sort_values(by='g')

            # # df.drop_duplicates(inplace=True)

            # # Initialize the FacetGrid object
            # pal = sns.cubehelix_palette(2, rot=-.25, light=.7)
            # g = sns.FacetGrid(df, row="g", hue="g", aspect=15, height=.5, palette=pal)

            # # Draw the densities in a few steps
            # g.map(sns.kdeplot, "x",
            #       bw_adjust=.5, clip_on=False,
            #       fill=True, alpha=1, linewidth=1.5)
            # g.map(sns.kdeplot, "x", clip_on=False, color="w", lw=2, bw_adjust=.5)

            # # passing color=None to refline() uses the hue mapping
            # g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)

            # # Define and use a simple function to label the plot in axes coordinates
            # def label(x, color, label):
            #     ax = plt.gca()
            #     ax.text(0, .2, label, fontweight="bold", color=color,
            #             ha="left", va="center", transform=ax.transAxes)

            # g.map(label, "x")

            # # Set the subplots to overlap
            # g.figure.subplots_adjust(hspace=-.25)

            # # Remove axes details that don't play well with overlap
            # g.set_titles("")
            # g.set(yticks=[], ylabel="")
            # g.despine(bottom=True, left=True)

            # plt.savefig(f'/home/jimena/Desktop/dataSprint/Nahel/figs/buckets_user_time/{typ}/{bucket}.png')
            # # plt.show()

            # ------------------------------------------------------------------
            # ----------------------- lrgen vs antielite -----------------------
            # ------------------------------------------------------------------

            df = df[['lrgen', 'antielite_salience', 'type', 'twitter_id']]

            os.makedirs(f"/home/jimena/Desktop/dataSprint/Nahel/figs/buckets_user_time_dense/{typ}", exist_ok=True)
            visualize_att(
                sources_coord_att=att_sources,
                targets_coord_att=df[df.type==typ].rename(columns={'twitter_id': 'entity'}),
                parties_coord_att=parties_coord_att,
                target_groups=mps_parties,
                dims=dict(zip(['x', 'y'], dimpair)),
                show=show,
                palette=palette,
                survey=survey,
                title=f"{typ} - {bucket}",
                path=f"/home/jimena/Desktop/dataSprint/Nahel/figs/buckets_user_time_dense/{typ}/{bucket}.png",
                **attvizparams
                )

