import os
import yaml
import numpy as np
import pandas as pd
from argparse import ArgumentParser

import statsmodels.api as sm

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
ap.add_argument('--show',  action='store_true', required=False)

args = ap.parse_args()
config = args.config
country = args.country
output = args.output
show = args.show

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
att_sources, _ = load_att_embeddings(att_folder)

NBINS = 11

fig = plt.figure(figsize=(12, 8))

tags = {
    'lrgen': ["Left (+)", "Rigth (+)"],
    'lrecon': ["Left (+)", "Rigth (+)"],
    'eu_position': ["Elites-People-Politicians", "StartUp-Entrepreneur"],
    'antielite_salience': ["Elites-People-Politicians", "StartUp-Entrepreneur"],
    'immigrate_policy': ["Immigration (+)", "Immigration (-)"],
}

nb_plot = 0
for attdim, color in zip(tags, sns.color_palette("husl", len(tags))):

    issue = '-'.join(ATTDIMISSUES[attdim]['issues'])
    data = load_issues_descriptions(folder, issue) \
        .merge(att_sources[['entity', attdim]], on='entity', how='inner')

    bins = np.linspace(CHESLIMS[attdim][0], CHESLIMS[attdim][1], NBINS)
    baseline, _ = np.histogram(
        att_sources[attdim],
        range=CHESLIMS[attdim],
        bins=bins)

    for tag in tags[attdim]:

        labeled_data = data.query(f"tag == '{tag}'")

        hist, bin_edges = np.histogram(
            labeled_data[attdim],
            range=CHESLIMS[attdim],
            bins=bins)

        p = hist / baseline
        p_lower, p_upper = sm.stats.proportion_confint(
            hist, baseline, method='beta', alpha=0.05)

        nb_plot += 1
        ax = fig.add_subplot(4, 2, nb_plot)

        half_step = np.mean(bin_edges[0:2])
        plot_x = (bin_edges+half_step)[:-1]
        ax.plot(
            plot_x,
            100.0*p,
            color=color
        )
        ax.fill_between(
            plot_x,
            100.0*p_lower,
            100.0*p_upper,
            color=color,
            alpha=0.25
        )
        ax.set_xlim(CHESLIMS[attdim])
        ax.set_ylim((0, 200.0 * np.nanmax(p)))
        ax.set_title(f"Labeled {tag}")
        ax.set_xlabel(ATTDICT[attdim])
        fmt = '%.02f%%'
        pticks = ticker.FormatStrFormatter(fmt)
        ax.yaxis.set_major_formatter(pticks)
        plt.tight_layout()

#saving
figname = f'{country}_users labeled_stats_with_confidence.png'
path = os.path.join(att_folder, figname)
plt.savefig(path)
print(f"Figure saved at {path}.")

if show:
    plt.show()