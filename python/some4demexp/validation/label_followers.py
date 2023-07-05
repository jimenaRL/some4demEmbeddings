"""
Scrip to assigne label to followers
"""
import os
import re
import yaml
from tqdm import tqdm
from itertools import combinations
from argparse import ArgumentParser

import numpy as np
import pandas as pd

import torch
from transformers import \
    AutoTokenizer, \
    AutoModelForSequenceClassification

from some4demdb import SQLite

from some4demexp.inout import \
    save_issues, \
    save_descriptions, \
    set_output_folder, \
    load_pids

from some4demexp.conf import \
    LANG

# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--country', type=str, required=True)
ap.add_argument('--output', type=str, required=True)
args = ap.parse_args()
config = args.config
country = args.country
output = args.output

issues = 'python/some4demexp/validation/issues.yaml'
with open(issues, "r", encoding='utf-8') as fh:
    issues_dict = yaml.load(fh, Loader=yaml.SafeLoader)


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
ISSUEDICT = {k: issues_dict[k][LANG[country]] for k in ISSUES}


with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)
print(yaml.dump(params, default_flow_style=False))

SQLITE = SQLite(params['sqlite_db'])

predicted_sentiment_min_rate = 3

# (0) Get embeddings and descriptions
folder = set_output_folder(params, country, output)
_, sources_pids = load_pids(folder)

entities = sources_pids

data = SQLITE.retrieveAndFormatUsersDescriptions(country, entities) \
    .rename(columns={'pseudo_id': 'entity'})


save_descriptions(folder, data)
exit()


l0 = len(data)
# (1) Find issues words in descriptions
for issue, patterns in ISSUEDICT.items():
    toprint = '\n\t'+' | '.join(patterns)+'\n'
    print(f"Checking for {toprint}patterns for issue {issue}.")
    regex = re.compile(f"(?:[\s]|^){'|'.join(patterns)}()(?=[\s]|$)")
    # for each row set 1 if issue is present in description
    data[issue] = data.description \
        .apply(lambda s: regex.search(s)) \
        .isnull() \
        .astype(int) \
        .apply(lambda n: 1 - n)

query = ' or '.join([f"{i} == 1" for i in ISSUES])
data = data.query(query)
l1 = len(data)
prop = 100 * l1 / l0
print(f"Found {l1} ({prop:.2f}%) followers with patterns in descriptions.")

# (2) Detect description language and filter out non local languages
# https://huggingface.co/papluca/xlm-roberta-base-language-detection

# #### NOTE : this should be doing at the creation of the DB by data enrichment

# model_name = "papluca/xlm-roberta-base-language-detection"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSequenceClassification.from_pretrained(model_name)

# print(f"Computing languages for {len(data)} descriptions...")

# bsize = 500
# tsize = len(data)
# batchl = [(i*bsize, (i+1)*bsize) for i in range(np.int32(tsize/bsize+1))]

# predicted_language = []
# for b in tqdm(batchl):
#     batch = data.iloc[b[0]: b[1]]
#     inputs = tokenizer(
#         batch.description.tolist(),
#         return_tensors="pt",
#         padding=True)
#     with torch.no_grad():
#         logits = model(**inputs).logits
#     predicted_class_id = logits.argmax(axis=1).numpy().tolist()
#     predicted_language.extend(
#         [model.config.id2label[i] for i in predicted_class_id]
#     )

# l0 = len(data)
# data = data \
#     .assign(predicted_language=predicted_language) \
#     .query(f"predicted_language == '{LANG[country]}'")
# l1 = len(data)

# mss = f"Dropped {l0 - l1} followers with descriptions not written in "
# mss += f"{LANG[country]}, left {l1}."
# print(mss)

# (3) Compute sentiment analysis on descriptions with
# https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment


model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

sentiment_query = ' or '.join([f"{i} == 1" for i in SENTIMENT_ISSUES])
sentiment_data = data.query(sentiment_query)

print(f"Computing sentiments for {len(sentiment_data)} descriptions...")

bsize = 500
tsize = len(sentiment_data)
batchl= [(i*bsize, (i+1)*bsize) for i in range(np.int32(tsize/bsize+1))]

predicted_sentiment = []
for b in tqdm(batchl):
    batch = sentiment_data.iloc[b[0]: b[1]]
    inputs = tokenizer(
        batch.description.tolist(),
        return_tensors="pt",
        padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_sentiment.extend(
        logits.argmax(axis=1).numpy()
    )

sentiment_data = sentiment_data.assign(predicted_sentiment=predicted_sentiment)

data = data \
    .merge(
        sentiment_data[['entity', 'predicted_sentiment']],
        on='entity',
        how='left')

data = data.assign(predicted_sentiment=data.predicted_sentiment.fillna(-1))

# (4) Get labels for axis

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


# # Europe
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

# Left-Right
ldata = data \
    .query("Left == 1") \
    .query("Left != Right") \
    .query(f"predicted_sentiment >= {predicted_sentiment_min_rate}") \
    .assign(tag='Left (+)') \
    .assign(label=0)
print(f"Found {len(ldata)} `Left-leaning` followers.")

rdata = data \
    .query("Right == 1") \
    .query("Left != Right") \
    .query(f"predicted_sentiment >= {predicted_sentiment_min_rate}") \
    .assign(tag='Rigth (+)') \
    .assign(label=1)
print(f"Found {len(rdata)} `Rigth-leaning` followers.")

# egalize sample
n = min(len(ldata), len(rdata))
ldata = ldata.sample(n=n)
rdata = rdata.sample(n=n)

print(f"Left-Right data downsampled to {n} samples of each categorie.")

save_issues(
    folder,
    pd.concat([ldata, rdata]),
    issue='Left-Right')


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

