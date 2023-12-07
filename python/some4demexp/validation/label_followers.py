"""
Scrip to assigne label to followers
"""
import os
import yaml
from argparse import ArgumentParser

import pandas as pd

from some4demdb import SQLite

from some4demexp.inout import \
    save_issues, \
    load_att_embeddings, \
    set_output_folder, \
    set_output_folder_att

from some4demexp.conf import \
LANGUAGES

# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--country', type=str, required=True)
ap.add_argument('--output', type=str, required=True)
args = ap.parse_args()
config = args.config
country = args.country
output = args.output


with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)
print(yaml.dump(params, default_flow_style=False))

FOLDER = set_output_folder(params, country, output)

SEED = params['validation']['seed']
LRMINSENT = params['validation']['leftright_sentiment_min_rate']

SQLITE = SQLite(params['sqlite_db'])

ISSUES = [
    'Left', 'Right',
    # 'Elites', 'People', 'Politicians', 'StartUp', 'Entrepreneur',
    # 'Immigration',
    # 'Europe',
    # 'Environment'
]
SENTIMENT_ISSUES = [
    'Left', 'Right',
    # 'Immigration',
    # 'Europe'
]

def computeLeftRightLabel(data, languages, predicted_sentiment_min_rate, folder):

    # filter by language
    formated = ','.join([f"'{l}'" for l in languages])
    data = data.query(f"predicted_language in [{formated}]")

    # Left-Right
    ldata = data \
        .query("Left == 1") \
        .query("Left != Right") \
        .query(f"predicted_sentiment >= {predicted_sentiment_min_rate}") \
        .assign(tag='Left (+)') \
        .assign(label=0)
    print(f"Found {len(ldata)} `Left-leaning` followers in att embedding")

    rdata = data \
        .query("Right == 1") \
        .query("Left != Right") \
        .query(f"predicted_sentiment >= {predicted_sentiment_min_rate}") \
        .assign(tag='Rigth (+)') \
        .assign(label=1)
    print(f"Found {len(rdata)} `Rigth-leaning` followers in att embedding.")

    save_issues(
        folder,
        pd.concat([ldata, rdata]),
        issue='Left-Right')

def computeMigrantionLabel(data, lang, folder):

    # # Migrantion
    # tag = 'Immigration (+)'

    # migration_plus = data \
    #     .query("Immigration == 1") \
    #     .query(f"predicted_sentiment >= {predicted_sentiment_min_rate}") \
    #     .assign(tag=tag) \
    #     .assign(label=0)
    # print(f"Found {len(migration_plus)} `{tag}` followers.")

    # tag = 'Immigration (-)'
    # migration_moins = data \
    #     .query("Immigration == 1") \
    #     .query(f"predicted_sentiment < {predicted_sentiment_min_rate}") \
    #     .assign(tag=tag) \
    #     .assign(label=0)
    # print(f"Found {len(migration_moins)} `{tag}` followers.")

    # # egalize sample
    # j = min(len(migration_plus), len(migration_moins))
    # migration_plus = migration_plus.sample(n=j)
    # migration_moins = migration_moins.sample(n=j)

    # print(f"Immigration (+)/(-) data downsampled to {j} samples of each categorie.")

    # save_issues(
    #     folder,
    #     pd.concat([migration_moins, migration_moins]),
    #     issue='Immigration')

    return

def computeEuropeLabel(data, lang, folder):
    # tag = 'Europe (+)'
    # euro_plus = data \
    #     .query("Europe == 1") \
    #     .query(f"predicted_sentiment >= {predicted_sentiment_min_rate}") \
    #     .assign(tag=tag) \
    #     .assign(label=0)
    # print(f"Found {len(euro_plus)} `{tag}` followers.")

    # tag = 'Europe (-)'
    # euro_moins = data \
    #     .query("Europe == 1") \
    #     .query(f"predicted_sentiment < {predicted_sentiment_min_rate}") \
    #     .assign(tag=tag) \
    #     .assign(label=0)
    # print(f"Found {len(euro_moins)} `{tag}` followers.")

    # # egalize sample
    # k = min(len(euro_plus), len(euro_moins))
    # euro_plus = euro_plus.sample(n=k)
    # euro_moins = euro_moins.sample(n=k)

    # print(f"Europe (+)/(-) data downsampled to {k} samples of each categorie.")

    # save_issues(
    #     folder,
    #     pd.concat([euro_plus, euro_moins]),
    #     issue='Europe')

    return

def computeAntiEliteLabel(data, lang, folder):

    # # Anti-elite

    # q1 = ' or '.join([f"{i} == 1" for i in ["Elites", "People", "Politicians"]])
    # q2 = ' and '.join([f"{i} == 0" for i in ["StartUp", "Entrepreneur"]])
    # query = f'{q1} and {q2}'
    # aedata = data \
    #     .query(query) \
    #     .assign(tag='Elites-People-Politicians') \
    #     .assign(label=1)
    # print(f"Found {len(aedata)} `Anti-elite/establishement` followers.")

    # q1 = ' or '.join([f"{i} == 1" for i in ["StartUp", "Entrepreneur"]])
    # q2 = ' and '.join([f"{i} == 0" for i in ["Elites", "People", "Politicians"]])
    # query = f'{q1} and {q2}'
    # odata = data \
    #     .query(query) \
    #     .assign(tag='StartUp-Entrepreneur') \
    #     .assign(label=0)
    # print(f"Found {len(odata)} `StartUp/Entrepreneur` followers.")

    # m = min(len(odata), len(aedata))
    # odata = odata.sample(n=m)
    # aedata = aedata.sample(n=m)
    # mssg = f"Elites-People-Politicians-StartUp-Entrepreneur data downsampled to"
    # mssg += "{m} samples of each categorie."
    # print(mssg)

    # save_issues(
    #     folder,
    #     pd.concat([aedata, odata]),
    #     issue='Elites-People-Politicians-StartUp-Entrepreneur')

    return





# (0) Get enriched (language, sentiment and matchs) descriptions

enriched_descriptions = SQLITE.getEnrichedDescriptions(country)

att_folder = set_output_folder_att(params, country, output)
att_sources, _ = load_att_embeddings(att_folder)

# use only users that are sources in attitudinal embedding
att_enriched_descriptions = enriched_descriptions.merge(
    att_sources[['entity']],
    left_on='pseudo_id',
    right_on='entity',
    how='inner'
) \
.drop(columns=['pseudo_id'])

computeLeftRightLabel(
    data=att_enriched_descriptions,
    languages=LANGUAGES[country]['languages'],
    predicted_sentiment_min_rate=LRMINSENT,
    folder=FOLDER)