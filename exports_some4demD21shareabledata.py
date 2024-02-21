import os
import yaml
from argparse import ArgumentParser

import numpy as np
import pandas as pd

from some4demdb import SQLite
from some4demexp.inout import \
    get_ide_ndims, \
    set_output_folder, \
    set_output_folder_emb, \
    set_output_folder_att, \
    load_ide_embeddings, \
    load_att_embeddings

# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--input', type=str, required=False)
ap.add_argument('--output', type=str, required=False)
args = ap.parse_args()
config = args.config
INPUTFOLDER = args.input
EXPORTFOLDER = args.output

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)

with open(params['params_db'], "r", encoding='utf-8') as fh:
    params_db = yaml.load(fh, Loader=yaml.SafeLoader)

COUNTRIES = [
    'belgium',
    'france',
    'germany',
    'italy',
    'netherlands',
    'poland',
    'romania',
    'slovenia',
    'spain',
]

RENAME = {
    'lrgen': 'left_right',
    'antielite_salience': 'antielite',
    'C_left': 'labeled_left',
    'C_right': 'labeled_right',
    'C_populist': 'labeled_populist',
    'C_elite': 'labeled_elite'
}

SURVEY = 'ches2019'
print(f">>>>> {SURVEY} <<<<<")

nb_targets_ide = []
nb_targets_att = []

nb_sources_ide = []
nb_sources_att = []

nb_users_llm_labels_postp = []

nb_targets_final = []
nb_sources_final = []


def format_ide(df):
    return df[['entity', 'latent_dimension_0', 'latent_dimension_1']] \
        .rename(columns={
            "latent_dimension_0": "delta_1",
            "latent_dimension_1": "delta_2"
        })

def format_att(df):
    return df[['entity', 'lrgen', 'antielite_salience']]

def format_llm(df):
    return df[['entity', 'C_left', 'C_right', 'C_populist', 'C_elite']] \
        .replace({'': '0'})

def format_parties(df):
     return df \
        .rename(columns={
            'mp_pseudo_id': 'entity',
            'MMS_party_acronym': 'party'}) \
        .drop(columns=[f'{SURVEY.upper()}_party_acronym'])

for country in COUNTRIES:

    print(f"----- {country} -----")

    SQLITE = SQLite(
        params['sqlite_db'].format(country=country),
        params_db['output']['tables'],
        country)

    PARTIESMAPPING = SQLITE.getPartiesMapping()

    FOLDER = set_output_folder(params, country, INPUTFOLDER)

    SURVEYCOL = f'{SURVEY.upper()}_party_acronym'
    ideN = get_ide_ndims(PARTIESMAPPING, SURVEY)


    # mps parties
    mps_parties = SQLITE.getMpParties(['MMS', SURVEY], dropna=False)
    mps_parties = format_parties(mps_parties)

    # ideological embedding data
    IDEFOLDER = set_output_folder_emb(
        params, country, SURVEY, ideN, INPUTFOLDER)
    ide_followers, ide_mps = load_ide_embeddings(IDEFOLDER)
    nb_targets_ide.append(len(ide_mps))
    nb_sources_ide.append(len(ide_followers))

    # att data
    ATTFOLDER = set_output_folder_att(
        params, SURVEY, country, ideN, INPUTFOLDER)
    att_sources, att_targets = load_att_embeddings(ATTFOLDER)
    nb_targets_att.append(len(att_targets))
    nb_sources_att.append(len(att_sources))

    # C strategy labels
    llm_labels = SQLITE.getLLMLabels('user')
    llm_data = llm_labels.merge(
        att_sources,
        left_on='pseudo_id',
        right_on='entity',
        how='inner') \
        .drop(columns=['pseudo_id'])
    nb_users_llm_labels_postp.append(len(llm_data))

    att_sources = format_att(att_sources)
    att_targets = format_att(att_targets)
    ide_mps = format_ide(ide_mps)
    ide_followers = format_ide(ide_followers)
    llm_data = format_llm(llm_data)

    m0 = len(ide_mps)
    mps = ide_mps \
        .merge(att_targets, on='entity') \
        .merge(mps_parties, on='entity') \
        .drop('entity', axis=1)
    assert m0 == len(mps)

    f0 = len(ide_followers)
    followers = ide_followers \
        .merge(att_sources, on='entity') \
        .merge(llm_data, on='entity', how='left') \
        .fillna('0') \
        .drop('entity', axis=1)
    assert f0 == len(followers)

    nb_targets_final.append(len(mps))
    nb_sources_final.append(len(followers))


    mps_path = os.path.join(EXPORTFOLDER, f'{country}_mps.csv')
    mps \
        .rename(columns=RENAME) \
        .astype(str) \
        .to_csv(mps_path, index=False)

    followers_path = os.path.join(EXPORTFOLDER, f'{country}_users.csv')
    followers \
        .rename(columns=RENAME) \
        .astype(str) \
        .to_csv(followers_path, index=False)

    print(f"mps data saved at {mps_path}")
    print(f"followers data saved at {followers_path}")


data = [
    nb_targets_ide,
    nb_targets_att,
    nb_targets_final,
    nb_sources_ide,
    nb_sources_att,
    nb_users_llm_labels_postp,
    nb_sources_final,
]

index = [
    '# targets ideologial',
    '# targets attitudinal',
    '# targets final',
    '# sources ideologial',
    '# sources attitudinal',
    '# sources llm labels',
    '# sources final',
]

dfCounts = pd.DataFrame(data=data, index=index, columns=COUNTRIES).T

print(dfCounts)

print(" & ".join(dfCounts['# sources llm labels'].astype(str).values.tolist()))

