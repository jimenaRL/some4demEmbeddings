import yaml
from argparse import ArgumentParser

import numpy as np
import pandas as pd

from linate import IdeologicalEmbedding
from some4demdb import SQLite
from some4demexp.inout import \
    get_ide_ndims, \
    set_output_folder, \
    set_output_folder_emb, \
    set_output_folder_att, \
    load_ide_embeddings, \
    load_att_embeddings, \
    load_experiment_data, \
    save_ide_embeddings

# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--output', type=str, required=False)
args = ap.parse_args()
config = args.config
output = args.output

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)

with open(params['params_db'], "r", encoding='utf-8') as fh:
    params_db = yaml.load(fh, Loader=yaml.SafeLoader)


COUNTRIES = [
    # 'belgium',
    'france',
    # 'germany',
    # 'italy',
    # 'netherlands',
    # 'poland',
    # 'romania',
    'slovenia',
    # 'spain',
]



# 1. PRE FILTERING DATA (SQLITE)

def get_count(sqlite, query, country):
    return SQLITE.retrieve(query.format(country))[0][0]

def get_discarded_count(sqlite, query, keyTrue, country):
    return SQLITE.retrieve(query.format(country, keyTrue))[0][0]

def get_annotation_count(sqlite, query, keyTrue, keyFalse, country):
    query = query.format(country, keyTrue, keyFalse)
    return SQLITE.retrieve(query)[0][0]


qMpGraph = """
    SELECT COUNT(DISTINCT(mp_pseudo_id))
    FROM mp_follower_graph_{}
    """

qMpLut = """
    SELECT COUNT(pseudo_id)
    FROM mp_lut_{}
    """

qMpAnnotation = """
    SELECT COUNT(mp_pseudo_id)
    FROM mp_annotation_{}
    """

qMpParty = """
    SELECT COUNT(mp_pseudo_id)
    FROM mp_party_{}
    """

qMpMetadata = """
    SELECT COUNT(pseudo_id)
    FROM mp_metadata_{}
    """

qFollowerGraph = """
    SELECT COUNT(DISTINCT(follower_pseudo_id))
    FROM mp_follower_graph_{}
    """

qFollowerLut = """
    SELECT COUNT(pseudo_id)
    FROM follower_lut_{}
    """

qUsersMetadata = """
    SELECT COUNT(pseudo_id)
    FROM user_metadata_{}
    """

qUsersEnrichedMetadata = """
    SELECT COUNT(pseudo_id)
    FROM user_enriched_metadata_{}
    """

qUsersKeywordsLabels = """
    SELECT COUNT(pseudo_id)
    FROM user_keywords_labels_{}
    """
qUsersLlmLabels = """
    SELECT COUNT(pseudo_id)
    FROM user_llm_labels_{}
    """

qAnnotNbTrue = """
    SELECT COUNT(*)
    FROM user_llm_labels_{}
    WHERE C_{}='1'
    AND C_{}!='1'
    """


qAnnotNbDiscarded = """
    SELECT COUNT(*)
    FROM user_llm_labels_{}
    WHERE C_{} NOT IN ('0', '1')
    """


nb_mps_lut = []
nb_mps_graph = []
nb_mps_annotation = []
nb_mps_party = []
nb_mps_metadata = []

nb_followers_lut = []
nb_followers_graph = []

nb_users_metadata = []
nb_users_enriched_metadata = []
nb_users_keywords_labels = []
nb_users_llm_labels = []

llm_labels_left = []
llm_labels_right = []
llm_labels_populist = []
llm_labels_elite = []

llm_labels_discarded_left = []
llm_labels_discarded_right = []
llm_labels_discarded_populist = []
llm_labels_discarded_elite = []

for country in COUNTRIES:

    print(f"----- {country} -----")

    SQLITE = SQLite(
        params['sqlite_db'].format(country=country),
        params_db['output']['tables'],
        country)

    nb_mps_graph.append(get_count(SQLITE, qMpGraph, country))
    nb_mps_lut.append(get_count(SQLITE, qMpLut, country))
    nb_mps_annotation.append(get_count(SQLITE, qMpAnnotation, country))
    nb_mps_party.append(get_count(SQLITE, qMpParty, country))
    nb_mps_metadata.append(get_count(SQLITE, qMpMetadata, country))

    nb_followers_graph.append(get_count(SQLITE, qFollowerGraph, country))
    nb_followers_lut.append(get_count(SQLITE, qFollowerLut, country))

    nb_users_metadata.append(get_count(SQLITE, qUsersMetadata, country))
    nb_users_enriched_metadata.append(get_count(SQLITE, qUsersEnrichedMetadata, country))
    nb_users_keywords_labels.append(get_count(SQLITE, qUsersKeywordsLabels, country))
    nb_users_llm_labels.append(get_count(SQLITE, qUsersLlmLabels, country))

    llm_labels_left.append(get_annotation_count(SQLITE, qAnnotNbTrue, 'left', 'right', country))
    llm_labels_right.append(get_annotation_count(SQLITE, qAnnotNbTrue, 'right', 'left', country))
    llm_labels_populist.append(get_annotation_count(SQLITE, qAnnotNbTrue, 'populist', 'elite', country))
    llm_labels_elite.append(get_annotation_count(SQLITE, qAnnotNbTrue, 'elite', 'populist' ,country))


    llm_labels_discarded_left.append(get_discarded_count(SQLITE, qAnnotNbDiscarded, 'left', country))
    llm_labels_discarded_right.append(get_discarded_count(SQLITE, qAnnotNbDiscarded, 'right', country))
    llm_labels_discarded_populist.append(get_discarded_count(SQLITE, qAnnotNbDiscarded, 'populist', country))
    llm_labels_discarded_elite.append(get_discarded_count(SQLITE, qAnnotNbDiscarded, 'elite' ,country))


data = [
    nb_mps_graph,
    nb_mps_lut,
    nb_mps_annotation,
    nb_mps_party,
    nb_mps_metadata,
    nb_followers_lut,
    nb_followers_graph,
    nb_users_metadata,
    nb_users_enriched_metadata,
    nb_users_keywords_labels,
    nb_users_llm_labels,
    llm_labels_left,
    llm_labels_right,
    llm_labels_populist,
    llm_labels_elite,
    llm_labels_discarded_left,
    llm_labels_discarded_right,
    llm_labels_discarded_populist,
    llm_labels_discarded_elite,
]

index = [
    '# mps graph',
    '# mps lut',
    '# mps annotation',
    '# mps party',
    '# mps metadata',
    '# followers graph',
    '# followers lut',
    '# users metadata',
    '# users enriched metadata',
    '# users keywords labels',
    '# users llm labels',
    '# sources llm left',
    '# sources llm right',
    '# sources llm populist',
    '# sources llm elite',
    '# sources llm discarded left',
    '# sources llm discarded right',
    '# sources llm discarded populist',
    '# sources llm discarded elite',
]

df = pd.DataFrame(data=data, index=index, columns=COUNTRIES).T


print(df[[
    '# sources llm left',
    '# sources llm right',
    '# sources llm populist',
    '# sources llm elite',
]].T)

# print(df[[
#     '# sources llm left',
#     '# sources llm right',
#     '# sources llm populist',
#     '# sources llm elite',
# ]].to_latex())


print(df[[
    '# mps graph',
    '# mps lut',
    '# mps annotation',
    '# mps party',
    '# mps metadata',
]])
print(df[[
    '# followers graph',
    '# followers lut',
]])
print(df[[
    '# users metadata',
    '# users enriched metadata',
    '# users keywords labels',
    '# users llm labels',
]])



print(df[[
    '# sources llm discarded left',
    '# sources llm discarded right',
    '# sources llm discarded populist',
    '# sources llm discarded elite',
]])




perc_discarded_left = 100 * df[['# sources llm discarded left']].T.values.flatten() / df[['# users llm labels']].T.values.flatten()
perc_discarded_right = 100 * df[['# sources llm discarded right']].T.values.flatten() / df[['# users llm labels']].T.values.flatten()
perc_discarded_populist = 100 * df[['# sources llm discarded populist']].T.values.flatten() / df[['# users llm labels']].T.values.flatten()
perc_discarded_elite = 100 * df[['# sources llm discarded elite']].T.values.flatten() / df[['# users llm labels']].T.values.flatten()


dfperc = pd.DataFrame(
    data=[
        100 * df[['# sources llm discarded right']].T.values.flatten() / df[['# users llm labels']].T.values.flatten(),
        100 * df[['# sources llm discarded left']].T.values.flatten() / df[['# users llm labels']].T.values.flatten(),
        100 * df[['# sources llm discarded populist']].T.values.flatten() / df[['# users llm labels']].T.values.flatten(),
        100 * df[['# sources llm discarded elite']].T.values.flatten() / df[['# users llm labels']].T.values.flatten(),

    ],
    index=[
        "% not labelled left",
        "% labelled right",
        "% labelled populist",
        "% labelled elite",
        ],
    columns=COUNTRIES)

print(dfperc)
# print(dfperc.to_latex())
df_preprocessing = df.copy()



# 2. POST FILTERING (csv)

for survey in ['ches2019', 'gps2019']:

    print(f">>>>> {survey} <<<<<")

    nb_targets_postp = []
    nb_targets_ide = []
    nb_targets_att = []

    nb_sources_postp = []
    nb_sources_ide = []
    nb_sources_att = []

    nb_users_keywords_labels_postp = []
    nb_users_llm_labels_postp = []

    for country in COUNTRIES:

        print(f"----- {country} -----")

        SQLITE = SQLite(
            params['sqlite_db'].format(country=country),
            params_db['output']['tables'],
            country)

        PARTIESMAPPING = SQLITE.getPartiesMapping()

        FOLDER = set_output_folder(params, country, output)

        SURVEYCOL = f'{survey.upper()}_party_acronym'
        ideN = get_ide_ndims(PARTIESMAPPING, survey)

        # Load mp groups
        FOLDER = set_output_folder(params, country, output)
        _, targets_pids, sources_pids, _ = load_experiment_data(
            FOLDER)
        nb_sources_postp.append(len(sources_pids))
        nb_targets_postp.append(len(targets_pids))

        # Load data from ideological embedding
        IDEFOLDER = set_output_folder_emb(
            params, country, survey, ideN, output)
        ide_followers, ide_mps = load_ide_embeddings(IDEFOLDER)
        nb_targets_ide.append(len(ide_mps))
        nb_sources_ide.append(len(ide_followers))


        # Load att data
        ATTFOLDER = set_output_folder_att(
            params, survey, country, ideN, output)
        att_sources, att_targets = load_att_embeddings(ATTFOLDER)
        nb_targets_att.append(len(att_targets))
        nb_sources_att.append(len(att_sources))

        # Load labels

        keywords_labels = SQLITE.getKeywordsLabels(entity='user')
        keywords_data = keywords_labels.merge(
            att_sources,
            left_on='pseudo_id',
            right_on='entity',
            how='inner') \
            .drop(columns=['pseudo_id'])

        # get C strategy labels
        llm_labels = SQLITE.getLLMLabels('user')
        llm_data = llm_labels.merge(
            att_sources,
            left_on='pseudo_id',
            right_on='entity',
            how='inner') \
            .drop(columns=['pseudo_id'])

        nb_users_keywords_labels_postp.append(len(keywords_data))
        nb_users_llm_labels_postp.append(len(llm_data))


    data = [
        nb_targets_postp,
        nb_targets_ide,
        nb_targets_att,
        nb_sources_postp,
        nb_sources_ide,
        nb_sources_att,
        nb_users_keywords_labels_postp,
        nb_users_llm_labels_postp,
    ]

    index = [
        '# targets post processing',
        '# targets ideologial',
        '# targets attitudinal',
        '# sources post processing',
        '# sources ideologial',
        '# sources attitudinal',
        '# sources keywords labels',
        '# sources llm labels',
    ]

    df = pd.DataFrame(data=data, index=index, columns=COUNTRIES).T

    print(df[[
        '# targets post processing',
        '# sources post processing',
    ]])

    print(df[[
        '# targets ideologial',
        '# sources ideologial',
    ]])

    print(df[[
        '# targets attitudinal',
        '# sources attitudinal',
    ]])


    print(df[[
        '# sources keywords labels',
        '# sources llm labels',
    ]])

df_postprocessing = df.copy()


# 3. COMPARAISONS
lost_mps = df_preprocessing[['# mps graph']].values \
- df_postprocessing[['# targets post processing']].values
data = np.array([
    df_preprocessing[['# mps graph']].values.flatten(),
    df_postprocessing[['# targets post processing']].values.flatten(),
    lost_mps.flatten()]).T
columns = ['# mps graph', '# targets post processing', '# lost mps']
lost_mps = pd.DataFrame(data=data, index=COUNTRIES, columns=columns)
print(lost_mps)

fg = df_preprocessing[['# followers graph']].values.flatten()
spp = df_postprocessing[['# sources post processing']].values.flatten()
lost_fls =  (fg - spp).flatten()
lost_fls_p = (100 * (fg - spp) / fg).flatten()
kept_fls_p = (100 - 100 * (fg - spp) / fg).flatten()
data = np.array([fg, spp, lost_fls, lost_fls_p, kept_fls_p]).T
columns = [
    '# followers graph',
    '# sources post processing',
    '# lost followers',
    '% lost followers',
    '% kept followers'
]
lost_fls = pd.DataFrame(data=data, index=COUNTRIES, columns=columns)
lost_fls = lost_fls.astype({
    '# followers graph': int,
    '# sources post processing': int,
    '# lost followers': int,
    '% lost followers': float,
    '% kept followers': float,
    })
print(lost_fls)

a = df_preprocessing[['# users keywords labels']].values.flatten()
b = df_preprocessing[['# users llm labels']].values.flatten()
c = df_postprocessing[['# sources keywords labels']].values.flatten()
d = df_postprocessing[['# sources llm labels']].values.flatten()
e = a - c
f = b - d
data = np.array([a, b, c, d, e, f]).T
columns = [
    '# users keywords labels',
    '# users llm labels',
    '# sources keywords labels',
    '# sources llm labels',
    '# lost keywords labels',
    '# lost llm labels',
]

lost_meta = pd.DataFrame(data=data, index=COUNTRIES, columns=columns)


print(lost_meta)
