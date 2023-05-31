import yaml
import pandas as pd
from argparse import ArgumentParser

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from some4demexp.inout import \
    set_output_folder, \
    set_output_folder_emb, \
    load_ide_embeddings, \
    set_output_folder_att, \
    load_att_embeddings, \
    load_issues_descriptions

from some4demexp.conf import \
    ATTDIMISSUES, \
    CHESLIMS, \
    ATTDICT

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

ATTDIMS = params['attitudinal_dimensions']
IDEDIMS = range(params['ideological_model']['n_latent_dimensions'])
ISSUES = sum([d['issues'] for d in ATTDIMISSUES.values()], [])

# (0) Get embeddings and descriptions
folder = set_output_folder(params, country, output)

ide_folder = set_output_folder_emb(params, country, output)
ide_sources, _ = load_ide_embeddings(ide_folder)

att_folder = set_output_folder_att(params, country, output)
att_sources, _, _ = load_att_embeddings(att_folder)

data = {}
for attdim in ATTDIMISSUES.keys():

    issue = '-'.join(ATTDIMISSUES[attdim]['issues'])
    data[attdim] = load_issues_descriptions(folder, issue) \
        .merge(att_sources, on='entity', how='inner') \
        .merge(ide_sources, on='entity', how='inner')

# (3) visualizations attitudinal
fig, axes = plt.subplots(3, 3, figsize=(12, 8), sharey=True)

for i in [0, 1, 2]:

    idedim = f'latent_dimension_{i}'
    ax = axes[0, i]
    aedata = data['antielite_salience'].query("tag == 'Elites-People-Politicians'")
    g = sns.histplot(
        aedata,
        x=idedim, hue='tag', stat="percent", fill=False, element="poly", bins=20,
        ax=ax
    )
    fmt = '%.0f%%'
    pticks = ticker.FormatStrFormatter(fmt)
    ax.yaxis.set_major_formatter(pticks)
    ax.set_xlabel(idedim)
    ax.set_ylabel('`Density')

    ax = axes[1, i]
    odata = data['antielite_salience'].query("tag == 'StartUp-Entrepreneur'")
    g = sns.histplot(
        odata,
        x=idedim, hue='tag', stat="percent", fill=False, element="poly", bins=20,
        ax=ax
    )
    pticks = ticker.FormatStrFormatter(fmt)
    ax.yaxis.set_major_formatter(pticks)
    ax.set_xlabel(idedim)
    ax.set_ylabel('`Density')

    ax = axes[2, i]
    adata = data['antielite_salience'].assign(tag='All')
    g = sns.histplot(
        adata,
        x=idedim, hue='tag', stat="percent", fill=False, element="poly", bins=20,
        ax=ax
    )
    fmt = '%.0f%%'
    pticks = ticker.FormatStrFormatter(fmt)
    ax.yaxis.set_major_formatter(pticks)
    ax.set_xlabel(idedim)
    ax.set_ylabel('`Density')



plt.tight_layout()


fig, axes = plt.subplots(3, 3, figsize=(12, 8), sharey=True)

for i in [0, 1, 2]:

    idedim = f'latent_dimension_{i}'
    ax = axes[0, i]
    aedata = data['lrgen'].query("tag == 'Left (+)'")
    g = sns.histplot(
        aedata,
        x=idedim, hue='tag', stat="percent", fill=False, element="poly", bins=20,
        ax=ax
    )
    fmt = '%.0f%%'
    pticks = ticker.FormatStrFormatter(fmt)
    ax.yaxis.set_major_formatter(pticks)
    ax.set_xlabel(idedim)
    ax.set_ylabel('`Density')

    ax = axes[1, i]
    odata = data['lrgen'].query("tag == 'Rigth (+)'")
    g = sns.histplot(
        odata,
        x=idedim, hue='tag', stat="percent", fill=False, element="poly", bins=20,
        ax=ax
    )
    fmt = '%.0f%%'
    pticks = ticker.FormatStrFormatter(fmt)
    ax.yaxis.set_major_formatter(pticks)
    ax.set_xlabel(idedim)
    ax.set_ylabel('`Density')

    ax = axes[2, i]
    adata = data['lrgen'].assign(tag='All')
    g = sns.histplot(
        adata,
        x=idedim, hue='tag', stat="percent", fill=False, element="poly", bins=20,
        ax=ax
    )
    fmt = '%.0f%%'
    pticks = ticker.FormatStrFormatter(fmt)
    ax.yaxis.set_major_formatter(pticks)
    ax.set_xlabel(idedim)
    ax.set_ylabel('`Density')

plt.tight_layout()


# (4) visualizations attitudinal
fig, axes = plt.subplots(3, 2, figsize=(12, 8), sharey=True)

# ------------------- CHES Anti-elite Salience -------------------
ax = axes[0, 0]
aedata = data['antielite_salience'].query("tag == 'Elites-People-Politicians'")
g = sns.histplot(
    aedata.query(f"{CHESLIMS[attdim][0]} < {attdim} < {CHESLIMS[attdim][1]}"),
    x=attdim, hue='tag', stat="percent", fill=False, element="poly", bins=20,
    ax=ax,
    palette=sns.color_palette("Set2",  aedata.label.nunique()))
fmt = '%.0f%%'
pticks = ticker.FormatStrFormatter(fmt)
ax.yaxis.set_major_formatter(pticks)
ax.set_xlabel(ATTDICT[attdim])
ax.set_ylabel('`Density')

ax = axes[1, 0]
odata = data['antielite_salience'].query("tag == 'StartUp-Entrepreneur'")
g = sns.histplot(
    odata.query(f"{CHESLIMS[attdim][0]} < {attdim} < {CHESLIMS[attdim][1]}"),
    x=attdim, hue='tag', stat="percent", fill=False, element="poly", bins=20,
    ax=ax,
    palette=sns.color_palette("husl",  aedata.label.nunique()))
fmt = '%.0f%%'
pticks = ticker.FormatStrFormatter(fmt)
ax.yaxis.set_major_formatter(pticks)
ax.set_xlabel(ATTDICT[attdim])
ax.set_ylabel('`Density')

ax = axes[2, 0]
adata = data['antielite_salience'].assign(tag='All')
g = sns.histplot(
    adata.query(f"{CHESLIMS[attdim][0]} < {attdim} < {CHESLIMS[attdim][1]}"),
    x=attdim, hue='tag', stat="percent", fill=False, element="poly", bins=20,
    ax=ax
)
fmt = '%.0f%%'
pticks = ticker.FormatStrFormatter(fmt)
ax.yaxis.set_major_formatter(pticks)
ax.set_xlabel(ATTDICT[attdim])
ax.set_ylabel('`Density')


# ------------------- CHES Left – Right -------------------
attdim = 'lrgen'

# add label
ax = axes[0, 1]
ldata = data['lrgen'].query("tag == 'Left (+)'")
g = sns.histplot(
    ldata.query(f"{CHESLIMS[attdim][0]} < {attdim} < {CHESLIMS[attdim][1]}"),
    x=attdim, hue='tag', stat="percent", fill=False, element="poly", bins=20,
    ax=ax,
    palette=sns.color_palette("husl", ldata.label.nunique()))
fmt = '%.0f%%'
pticks = ticker.FormatStrFormatter(fmt)
ax.yaxis.set_major_formatter(pticks)
ax.set_xlabel(ATTDICT[attdim])


ax = axes[1, 1]
rdata = data['lrgen'].query("tag == 'Rigth (+)'")
g = sns.histplot(
    rdata.query(f"{CHESLIMS[attdim][0]} < {attdim} < {CHESLIMS[attdim][1]}"),
    x=attdim, hue='tag', stat="percent", fill=False, element="poly", bins=20,
    ax=ax,
    palette=sns.color_palette("Paired", rdata.label.nunique()))
fmt = '%.0f%%'
pticks = ticker.FormatStrFormatter(fmt)
ax.yaxis.set_major_formatter(pticks)
ax.set_xlabel(ATTDICT[attdim])

ax = axes[2, 1]
adata = data['lrgen'].assign(tag='All')
g = sns.histplot(
    adata.query(f"{CHESLIMS[attdim][0]} < {attdim} < {CHESLIMS[attdim][1]}"),
    x=attdim, hue='tag', stat="percent", fill=False, element="poly", bins=20,
    ax=ax,
    color='k')
fmt = '%.0f%%'
pticks = ticker.FormatStrFormatter(fmt)
ax.yaxis.set_major_formatter(pticks)
ax.set_xlabel(ATTDICT[attdim])

plt.tight_layout()


plt.show()

