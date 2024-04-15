import os
import yaml
from glob import glob
import pandas as pd
from string import Template
from argparse import ArgumentParser

import seaborn as sns
import matplotlib.pyplot as plt

from some4demdb import SQLite
from some4demexp.inout import \
    get_ide_ndims, \
    set_output_folder_att, \
    load_att_embeddings, \
    set_output_folder_emb, \
    load_ide_embeddings, \
    set_output_folder, \
    csvExport, \
    excelExport


# (0) parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--country', type=str, required=True)
ap.add_argument('--output', type=str, required=False)
args = ap.parse_args()
config = args.config
output = args.output
country = args.country

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)

with open(params['params_db'], "r", encoding='utf-8') as fh:
    dbParams = yaml.load(fh, Loader=yaml.SafeLoader)

EXPORTFOLDER = params['export_folder']

LLMISSUES = dbParams['enrichments']['steps']['llm_annotations']['prompts']

SQLITE = SQLite(
    params['sqlite_db'].format(country=country),
    dbParams['output']['tables'],
    country)

PARTIESMAPPING = SQLITE.getPartiesMapping()

FOLDER = set_output_folder(params, country, output)

TARGETSTIDS = SQLITE.getTwitterIds(entity="mp", pseudo_ids=None)
SOURCESTIDS = SQLITE.getTwitterIds(entity="follower", pseudo_ids=None)


# (1a) load and export ideological embeddings

ideN = get_ide_ndims(PARTIESMAPPING, survey)
ATTFOLDER = set_output_folder_att(params, survey, country, ideN, output)
LRFOLDER = os.path.join(ATTFOLDER, 'logistic_regression')

for survey in ['ches2019']:

    ideN = get_ide_ndims(PARTIESMAPPING, survey)

    IDEFOLDER = set_output_folder_emb(
        params, country, survey, ideN, output)
    ide_sources, ide_targets = load_ide_embeddings(IDEFOLDER)

    IDEEXPORTFOLDER = os.path.join(EXPORTFOLDER, 'ideological', country)

    ide_sources = ide_sources \
        .merge(
            SOURCESTIDS,
            left_on='entity',
            right_on='pseudo_id') \
        .drop(columns=['entity', 'pseudo_id'])

    ide_sources_path = os.path.join(
        IDEEXPORTFOLDER,
        f'ide_coords_{country}_sources.csv')
    ide_sources.to_csv(ide_sources_path, index=False)

    print(f"\tfound {len(ide_sources)} sources")
    print(f"\tsaved at {ide_sources_path}")

    ide_targets = ide_targets \
        .merge(
            TARGETSTIDS,
            left_on='entity',
            right_on='pseudo_id') \
        .drop(columns=['entity', 'pseudo_id'])

    ide_targets_path = os.path.join(
        IDEEXPORTFOLDER,
        f'ide_coords_{country}_targets.csv')
    ide_targets.to_csv(ide_targets_path, index=False)

    print(f"\tfound {len(ide_targets)} targets")
    print(f"\tsaved at {ide_targets_path}")



# (1b) load and export attitudinal embeddings and descriptions

att_embeddings = dict()
for survey in ['ches2019', 'gps2019']:

    SURVEYCOL = f'{survey.upper()}_party_acronym'
    ideN = get_ide_ndims(PARTIESMAPPING, survey)

    ATTFOLDER = set_output_folder_att(
        params, survey, country, ideN, output)
    att_sources, att_targets = load_att_embeddings(ATTFOLDER)


    ATTEXPORTFOLDER = os.path.join(EXPORTFOLDER, 'attitudinal', country)

    att_sources = att_sources \
        .merge(
            SOURCESTIDS,
            left_on='entity',
            right_on='pseudo_id') \
        .drop(columns=['entity', 'pseudo_id'])

    att_sources_path = os.path.join(
        ATTEXPORTFOLDER,
        f'att_coords_{country}_{survey}_sources.csv')
    att_sources.to_csv(att_sources_path, index=False)

    las = len(att_sources)
    print(f"\tfound {las} sources with {survey} attitudinal embeddings")
    print(f"\tsaved at {att_sources_path}")

    att_targets = att_targets \
        .merge(
            TARGETSTIDS,
            left_on='entity',
            right_on='pseudo_id') \
        .drop(columns=['entity', 'pseudo_id'])

    att_targets_path = os.path.join(
        ATTEXPORTFOLDER,
        f'att_coords_{country}_{survey}_targets.csv')
    att_targets.to_csv(att_targets_path, index=False)

    lat = len(att_targets)
    print(f"\tfound {lat} targets with {survey} attitudinal embeddings")
    print(f"\tsaved at {att_targets_path}")



# (2) copy correlations

CORRFOLDER = os.path.join(EXPORTFOLDER, 'correlations', country)

for survey in ['ches2019', 'gps2019']:

    SURVEYCOL = f'{survey.upper()}_party_acronym'
    ideN = get_ide_ndims(PARTIESMAPPING, survey)

    ATTFOLDER = set_output_folder_att(
        params, survey, country, ideN, output)

    for method in ['Spearman', 'Pearson']:
        for k in ['p', 'r']:
            inpath = os.path.join(
                ATTFOLDER, f'party_corr_{method}_{country}_{survey}_{k}.csv')
            outpath = os.path.join(
                CORRFOLDER, f'party_corr_{method}_{country}_{survey}_{k}.csv')
            os.system(f'cp {inpath} {outpath}')
            print(f"File copied to {outpath}")



# (3) annotations

kwords_labels = SQLITE.getKeywordsLabels(entity='user')
labels =  [c for c in kwords_labels.columns if c.startswith('A_')]
kwords_labels = kwords_labels[labels + ['pseudo_id']]

llm_labels = SQLITE.getLLMLabels('user')
annotations = kwords_labels.merge(llm_labels, on='pseudo_id')
annotations_with_ids = annotations \
    .merge(SOURCESTIDS, on='pseudo_id') \
    .drop(columns=['pseudo_id'])

lawi = len(annotations_with_ids)
assert len(kwords_labels) == len(llm_labels) == len(annotations)  == lawi
print(f"Found {lawi} users with attitudinal embeddings and llm labels")

ANNFOLDER = os.path.join(EXPORTFOLDER, 'annotations', country)
annpath = os.path.join(
    ANNFOLDER, f'sources_annotations_{country}.csv')
annotations_with_ids.to_csv(annpath, index=False)
print(f"Annotations file saved at {annpath}")


# (4) mp annotations

mp_annotations = SQLITE.getAnnotations()
missing = set(mp_annotations.MMS_party_acronym.unique()) - set(PARTIESMAPPING.MMS_party_acronym.unique())
if missing:
    print(missing)

m0 = len(mp_annotations)
mp_with_parties = mp_annotations \
    .merge(PARTIESMAPPING, on='MMS_party_acronym')
m1 = len(mp_with_parties)

if m0 > m1:
    print(f"Drop {m0 -m1} mps with no match ")

mp_with_tids = mp_with_parties \
    .merge(TARGETSTIDS, left_on='mp_pseudo_id', right_on='pseudo_id') \
    .drop(columns=["pseudo_id"])
m2 = len(mp_with_tids)
assert m1 == m2

export_columns = [
    'firstname',
    'lastname',
    'twitter_name',
    'party_name',
    'MMS_party_acronym',
    'CHES2019_party_acronym',
    'GPS2019_party_acronym',
    'twitter_id'
]


MPFOLDER = os.path.join(EXPORTFOLDER, 'mps', country)
mpspath = os.path.join(
    MPFOLDER, f'mps_annotations_{country}.csv')
mp_with_tids[export_columns].to_csv(mpspath, index=False)
print(f"Annotations file saved at {mpspath}")


# (5) logistic regressions per country
# Note : done directaly in lr computations

# (6) logistic regressions all countries heat map


paths = glob("exports/byCountry/*/min_followers_25_min_outdegree_3/*/*/*/logistic_regression/*_logistic_regression_cross_validate_f1_score.csv")

df = pd.concat([pd.read_csv(path) for path in paths])


def kind(row):
    k = row['attitudinal_dimension_name']
    k += ": "
    k += row['label1'][2:]
    k += " vs "
    k += row['label2'][2:]
    k += " "
    k += row['strategy']
    return k.upper()

df = df.assign(kind=df.apply(lambda r:  kind(r), axis=1))

for survey in ['ches2019', 'gps2019']:

    dfp = df[df.survey==survey][["kind", "country", "f1"]]
    dfp = dfp.pivot(index="kind", columns="country", values="f1")

    df_annot = df.assign(
        annot=df.apply(
            lambda r: f"{r.train_f1_mean:.2f} ± {r.test_f1_std:.2f}", axis=1))
    df_annot = df_annot[df_annot.survey==survey][["kind", "country", "annot"]]
    df_annot = df_annot.pivot(index="kind", columns="country", values="annot")

    print("\n\n")
    for k in dfp.index:
        print(k.upper())
    print("\n\n")

    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(12, 12))


    hm = sns.heatmap(
        dfp,
        annot=df_annot,
        linewidths=0,
        ax=ax,
        cbar=False,
        vmin=0.65,
        vmax=1,
        cmap='flare')

    hm.set(xticklabels=[])
    hm.set(xlabel=None)
    hm.set(xticklabels=[])
    hm.set(ylabel=None)
    hm.set(yticklabels=[])

    ax.set(xlabel="", ylabel="")
    ax.tick_params(bottom=False)
    ax.tick_params(left=False)

    plt.show()

