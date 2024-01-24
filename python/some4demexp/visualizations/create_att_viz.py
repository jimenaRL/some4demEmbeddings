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


    ########################################
    # LUNDI
    ########################################


    # from glob import glob
    # from tqdm import tqdm

    # sources_twitter_ids = SQLITE.getTwitterIds(
    #     entity="follower", pseudo_ids=att_sources.entity.tolist())

    # att_sources = att_sources.merge(sources_twitter_ids, left_on='entity', right_on='pseudo_id')
    # att_sources = att_sources[['lrgen', 'antielite_salience', 'twitter_id']]

    # ce = pd.read_csv('/home/jimena/Desktop/dataSprint/Nahel/classementEvenements - classementEvenements.csv')
    # folder = '/home/jimena/Desktop/dataSprint/Nahel/2023-06-27_2023-07_0.75_1_files'
    # thread_ids = ce.Événement.unique()
    # records = []



    # for thread_id in tqdm(thread_ids):
    #     file = os.path.join(folder, f"{thread_id}.csv")
    #     df = pd.read_csv(file)
    #     thread_id = int(file.split('/')[-1].split('.csv')[0])
    #     description = ce[ce.Événement == thread_id]['Description'].values[0]
    #     att_sources2 = att_sources.merge(
    #         df[['user_id']].astype('str'),
    #         left_on='twitter_id',
    #         right_on='user_id')
    #     record = {
    #         "nb_coincidences": len(att_sources2),
    #         "prop_coincidences": 100 * float(len(att_sources2) / len(df)),
    #         "description": description,
    #         "thread_id": thread_id,
    #         }
    #     records.append(record)

    #     print(record)

    # # title = "all"
    # title =  f"{thread_id}"


    ########################################
    # MARDI cagnotte
    ########################################

    from tqdm import tqdm
    from datetime import datetime, timedelta, timezone

    sources_twitter_ids = pd.read_csv('sources_twitter_ids.csv').astype(str)

    att_sources_with_twitter_id = att_sources.merge(sources_twitter_ids, left_on='entity', right_on='pseudo_id')
    att_sources_with_twitter_id = att_sources_with_twitter_id[['lrgen', 'antielite_salience', 'twitter_id']]

    ce = pd.read_csv('/home/jimena/Desktop/dataSprint/Nahel/classementEvenements - classementEvenements.csv')
    folder = '/home/jimena/Desktop/dataSprint/Nahel/2023-06-27_2023-07_0.75_1_files'
    records = []

    ce = ce[ce['Motif'] == 'Cagnotte']
    thread_ids = ce.Événement.unique()

    df = pd.concat([
            pd.read_csv(os.path.join(folder, f"{thread_id}.csv"))
                for thread_id in thread_ids])

    df = df.reset_index().drop(columns='index')

    df = df.sort_values(by='timestamp_utc')

    format_dates = [
        datetime.strptime(s.replace(' ', 'T'), '%Y-%m-%dT%H:%M:%S')
            for s in df['local_time'].tolist()]

    start_date_a = datetime(2023, 6, 29, 12)
    start_date_b = datetime(2023, 6, 30, 00)
    end_date = datetime(2023, 7, 16, 23, 59)

    def between(date, init, end):
        return init < date and date < end

    bucket = 0
    buckets = []
    while start_date_a < end_date:
        dfbucket = df[[between(f, start_date_a, start_date_b) for f in format_dates]]
        print(dfbucket)
        print("-----------------")
        buckets.extend([bucket for i in range(len(dfbucket))])
        bucket += 1
        start_date_a += timedelta(hours=12)
        start_date_b += timedelta(hours=12)

    assert len(df) == len(buckets)

    df = df.assign(buckets=buckets)

    for bucket in tqdm(list(set(buckets))):

        bucket_users = df[df.buckets == bucket]

        bucket_users = att_sources_with_twitter_id.merge(
            bucket_users[['user_id']].astype('str'),
            left_on='twitter_id',
            right_on='user_id')

        record = {
            "nb_coincidences": len(bucket_users),
            "prop_coincidences": 100 * float(len(bucket_users) / len(df)),
            "bucket": bucket,
            "initDate": str(datetime(2023, 6, 29, 12) + bucket * timedelta(hours=12))
            }

        lrgen_stats =  {f"lrgen_{k}":v for k,v in bucket_users["lrgen"].describe().to_dict().items()}
        antielite_salience_stats =  {f"antielite_salience_{k}":v for k,v in bucket_users["lrgen"].describe().to_dict().items()}

        record.update(lrgen_stats)
        record.update(antielite_salience_stats)
        records.append(record)

        description = str(bucket)
        title = record['initDate']

        print(record)

        path = os.path.join(
            "/home/jimena/Desktop/dataSprint/Nahel/figs/buckets",
           f'{bucket}.png')

        attvizparams['path'] = path


        visualize_att(
            sources_coord_att=att_sources,
            targets_coord_att=bucket_users,
            parties_coord_att=parties_coord_att,
            target_groups=mps_parties,
            dims=dict(zip(['x', 'y'], dimpair)),
            show=show,
            palette=palette,
            survey=survey,
            title=title,
            **attvizparams
            )

    stats = pd.DataFrame.from_records(records)
    stats.to_csv('stats.csv')
    print(stats)


    exit()
    ########################################
    # MARDI days viso
    ########################################

    sources_twitter_ids = pd.read_csv('sources_twitter_ids.csv', dtype=str)

    att_sources_with_twitter_id = att_sources[['lrgen', 'antielite_salience', 'entity']] \
        .merge(sources_twitter_ids, left_on='entity', right_on='pseudo_id') \
        .drop(columns=['entity', 'pseudo_id'])

    byDays = pd.read_csv(
        '/home/jimena/Desktop/dataSprint/Nahel/input_for_politization_metrics.csv').astype(str)

    byDays = byDays \
        .reset_index() \
        .rename(columns={'index': 'line_nb'})

    byDays = byDays \
        .assign(accountsIdsSplit=byDays.accountsIds.apply(lambda s: s.split('|'))) \
        .explode('accountsIdsSplit')

    b0 = byDays.accountsIdsSplit.nunique()

    byDays = byDays.merge(att_sources_with_twitter_id, left_on='accountsIdsSplit', right_on='twitter_id')

    b1 = byDays.accountsIdsSplit.nunique()

    print(f"Missing {b0 - b1} ({100 * (b0 - b1) / b0}) twitter users")

    byDays = byDays[['line_nb', 'lrgen', 'antielite_salience']] \
        .groupby('line_nb') \
        .mean() \
        .reset_index()

    byDays = byDays.assign(lrgen=byDays['lrgen']/10)
    byDays = byDays.assign(antielite_salience=byDays['antielite_salience']/10)

    byDays.to_csv(
        '/home/jimena/Desktop/dataSprint/Nahel/politization_metrics.csv',
        index=False)

    ########################################
    # MARDI user media
    ########################################
    sources_twitter_ids = pd.read_csv('sources_twitter_ids.csv', dtype=str)

    userMedia = pd.read_csv('/home/jimena/Desktop/dataSprint/Nahel/users-medias.csv').astype(str)
    att_sources_with_twitter_id = att_sources[['lrgen', 'antielite_salience', 'entity']] \
        .merge(sources_twitter_ids, left_on='entity', right_on='pseudo_id') \
        .drop(columns=['entity', 'pseudo_id'])
    userMediaAtt = att_sources_with_twitter_id \
        .merge(userMedia, left_on='twitter_id', right_on='user_id') \
        .drop(columns=['user_id', 'twitter_id'])

    userMediaAttMean = userMediaAtt.groupby('media_label').mean()
    userMediaAttMean.reset_index().to_csv(
        '/home/jimena/Desktop/dataSprint/Nahel/media_mean_user_attitudinal_positions.csv', index=False)

    title = "medias"
    path = '/home/jimena/Desktop/dataSprint/Nahel/media_mean_user_attitudinal_positions.png'
    visualize_att(
        sources_coord_att=att_sources,
        targets_coord_att=userMediaAttMean,
        parties_coord_att=parties_coord_att,
        target_groups=mps_parties,
        dims=dict(zip(['x', 'y'], dimpair)),
        show=show,
        palette=palette,
        survey=survey,
        title=title,
        path=path,
        **attvizparams
        )

    ########################################
    # MARDI user events
    ########################################


    from glob import glob
    from tqdm import tqdm

    # sources_twitter_ids = SQLITE.getTwitterIds(
    #     entity="follower", pseudo_ids=att_sources.entity.tolist())
    # sources_twitter_ids.to_csv('sources_twitter_ids.csv', index=False)
    sources_twitter_ids = pd.read_csv('sources_twitter_ids.csv').astype(str)

    att_sources_with_twitter_id = att_sources.merge(sources_twitter_ids, left_on='entity', right_on='pseudo_id')
    att_sources_with_twitter_id = att_sources_with_twitter_id[['lrgen', 'antielite_salience', 'twitter_id']]

    ce = pd.read_csv('/home/jimena/Desktop/dataSprint/Nahel/classementEvenements - classementEvenements.csv')
    folder = '/home/jimena/Desktop/dataSprint/Nahel/2023-06-27_2023-07_0.75_1_files'
    thread_ids = ce.Événement.unique()
    records = []

    for thread_id in tqdm(thread_ids):
        file = os.path.join(folder, f"{thread_id}.csv")
        df = pd.read_csv(file)
        thread_id = int(file.split('/')[-1].split('.csv')[0])
        description = ce[ce.Événement == thread_id]['Description'].values[0]
        event_users = att_sources_with_twitter_id.merge(
            df[['user_id']].astype('str'),
            left_on='twitter_id',
            right_on='user_id')

        record = {
            "nb_coincidences": len(event_users),
            "prop_coincidences": 100 * float(len(event_users) / len(df)),
            "description": description,
            "thread_id": thread_id,
            }

        lrgen_stats =  {f"lrgen_{k}":v for k,v in event_users["lrgen"].describe().to_dict().items()}
        antielite_salience_stats =  {f"antielite_salience_{k}":v for k,v in event_users["lrgen"].describe().to_dict().items()}

        record.update(lrgen_stats)
        record.update(antielite_salience_stats)
        records.append(record)

        description = str(description).replace('\xa0', ' ').replace('«', '"').replace('»', '"')
        title = f"{thread_id} - {description}"

        if thread_id != 61406:
            continue

        print(record)

        path = os.path.join(
            "/home/jimena/Desktop/dataSprint/Nahel/figs",
           f'{thread_id}.png')

        attvizparams['path'] = path


        visualize_att(
            sources_coord_att=att_sources,
            targets_coord_att=event_users,
            parties_coord_att=parties_coord_att,
            target_groups=mps_parties,
            dims=dict(zip(['x', 'y'], dimpair)),
            # path=os.path.join(att_folder, f"{dimpair_str}.png"),
            show=show,
            palette=palette,
            survey=survey,
            title=title,
            **attvizparams
            )

    stats = pd.DataFrame.from_records(records)
    stats.to_csv('stats.csv')
    print(stats)

    ########################################


