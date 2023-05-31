"""
Scrip to assigne label to followers
"""
import os
import re
import yaml
import pandas as pd
from itertools import combinations
from argparse import ArgumentParser

import torch
from transformers import \
    AutoTokenizer, \
    AutoModelForSequenceClassification

from some4demdb import SQLite
from some4demexp.inout import \
    save_issues_descriptions, \
    set_output_folder, \
    load_pids

from some4demexp.conf import \
    ATTDIMISSUES, \
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

ISSUES = sum([d['issues'] for d in ATTDIMISSUES.values()], [])
ISSUEDICT = {k: issues_dict[k][LANG[country]] for k in ISSUES}

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)
print(yaml.dump(params, default_flow_style=False))

SQLITE = SQLite(params['sqlite_db'])

# (0) Get embeddings and descriptions
folder = set_output_folder(params, country, output)
_, sources_pids = load_pids(folder)

entities = sources_pids

data = SQLITE.retrieveAndFormatUsersDescriptions(country, entities) \
    .rename(columns={'pseudo_id': 'entity'})

l0 = len(data)
print(f"Found {l0} followers attitudinal embeddings.")

# (1) Find issues words in descriptions
for issue, patterns in ISSUEDICT.items():
    regex = re.compile(f"(?:[\s]|^){'|'.join(patterns)}()(?=[\s]|$)")
    # for each row set 1 if issue is present in description
    data[issue] = data.description \
        .apply(lambda s: regex.search(s)) \
        .isnull() \
        .astype(int) \
        .apply(lambda n: 1 - n)

l1 = len(data.query(' or '.join([f"{i} == 1" for i in ISSUES])))
prop = 100 * l1 / l0
print(f"Found {l1} ({prop:.2f}%) followers with patterns in descriptions.")

for issue in ISSUES:
    query = f"{issue} == 1"
    print(f"{issue}: {len(data.query(query))}")

query = ' or '.join([f"{i} == 1" for i in ISSUES])
data = data.query(query)

# (2) Detect description language and filter out non local languages
# https://huggingface.co/papluca/xlm-roberta-base-language-detection

print(f"Computing languages for {len(lrdata)} descriptions...")

model_name = "papluca/xlm-roberta-base-language-detection"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
inputs = tokenizer(
    data.description.tolist(),
    return_tensors="pt",
    padding=True)

with torch.no_grad():
    logits = model(**inputs).logits

predicted_class_id = logits.argmax(axis=1).numpy().tolist()
predicted_language = [model.config.id2label[i] for i in predicted_class_id]

l0 = len(data)
data = data \
    .assign(predicted_language=predicted_language) \
    .query(f"predicted_language == '{LANG[country]}'")
l1 = len(data)

mss = f"Dropped {l0 - l1} followers with descriptions not written in "
mss += f"{LANG[country]}, left {l1}."
print(mss)


# (3) Compute sentiment analysis on descriptions with
# https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment

query = ' or '.join([f"{i} == 1" for i in ATTDIMISSUES['lrgen']['issues']])
lrdata = data.query(query)

print(f"Computing sentiments for {len(lrdata)} descriptions...")

model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

inputs = tokenizer(
    lrdata.description.tolist(),
    return_tensors="pt",
    padding=True)

with torch.no_grad():
    logits = model(**inputs).logits
predicted_sentiment=logits.argmax(axis=1).numpy()

lrdata = lrdata.assign(predicted_sentiment=predicted_sentiment)

print("done.")

data = data.merge(
    lrdata[['entity', 'predicted_sentiment']], on='entity', how='left')

data = data.assign(predicted_sentiment=data.predicted_sentiment.fillna(-1))


# (4) Get labels for axis

# CHES Left – Right

ldata = data \
    .query("Left == 1") \
    .query("Left != Right") \
    .query("predicted_sentiment >= 3") \
    .assign(tag='Left (+)') \
    .assign(label=0)
print(f"Found {len(ldata)} `Left-leaning` followers.")

rdata = data \
    .query("Right == 1") \
    .query("Left != Right") \
    .query("predicted_sentiment >= 3") \
    .assign(tag='Rigth (+)') \
    .assign(label=1)
print(f"Found {len(rdata)} `Rigth-leaning` followers.")

n = min(len(ldata), len(rdata))
ldata = ldata.sample(n=n)
rdata = rdata.sample(n=n)

save_issues_descriptions(
    folder,
    pd.concat([ldata, rdata]),
    issue='Left-Right')


# CHES Anti-elite Salience

attdim = 'antielite_salience'

q1 = ' or '.join([f"{i} == 1" for i in ["Elites", "People", "Politicians"]])
q2 = ' and '.join([f"{i} == 0" for i in ["StartUp", "Entrepreneur"]])
query = f'{q1} and {q2}'
aedata = data \
    .query(query) \
    .assign(tag='Elites-People-Politicians') \
    .assign(label=1)
print(f"Found {len(aedata)} `Anti-elite/establishement` followers.")

q1 = ' or '.join([f"{i} == 1" for i in ["StartUp", "Entrepreneur"]])
q2 = ' and '.join([f"{i} == 0" for i in ["Elites", "People", "Politicians"]])
query = f'{q1} and {q2}'
odata = data \
    .query(query) \
    .assign(tag='StartUp-Entrepreneur') \
    .assign(label=0)
print(f"Found {len(odata)} `StartUp/Entrepreneur` followers.")

save_issues_descriptions(
    folder,
    pd.concat([aedata, odata]),
    issue='Elites-People-Politicians-StartUp-Entrepreneur')
