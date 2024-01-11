import os
import yaml
import itertools
import numpy as np
import pandas as pd
from argparse import ArgumentParser

from sklearn.linear_model import LogisticRegression
from scipy.special import expit

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import matplotlib.ticker as mtick
import matplotlib.patheffects as PathEffects
import seaborn as sn

from sklearn.metrics import \
    accuracy_score, \
    precision_score, \
    recall_score, \
    f1_score

from some4demdb import SQLite

from some4demexp.inout import \
    set_output_folder,  \
    set_output_folder_att,  \
    load_att_embeddings,  \
    load_issues, \
    get_ide_ndims
    # load_issues_benckmarks

from some4demexp.conf import \
    LOGISTICREGRESSIONS, \
    ATTDICT

# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config', type=str, required=True)
ap.add_argument('--country', type=str, required=True)
ap.add_argument('--survey', type=str, required=True)
ap.add_argument('--output', type=str, required=True)
ap.add_argument('--show',  action='store_true', required=False)

args = ap.parse_args()
config = args.config
country = args.country
survey = args.survey
output = args.output
show = args.show

with open(config, "r", encoding='utf-8') as fh:
    params = yaml.load(fh, Loader=yaml.SafeLoader)

with open(params['params_db'], "r", encoding='utf-8') as fh:
    params_db = yaml.load(fh, Loader=yaml.SafeLoader)

SQLITE = SQLite(
    params['sqlite_db'].format(country=country),
    params_db['output']['tables'],
    country)

parties_mapping = SQLITE.getPartiesMapping()
ideN = get_ide_ndims(parties_mapping, survey)


# (0) Get embeddings and descriptions
folder = set_output_folder(params, country, output)

att_folder = set_output_folder_att(params, survey, country, ideN, output)
att_sources, _ = load_att_embeddings(att_folder)


#########################################
# Preliminary functions and definitions #
#########################################

# Font & Latex definitions
mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['mathtext.rm'] = 'serif'
# mpl.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
fs = 12
# dpi = 150
plt.rc('text', usetex=True)
plt.rc('font', family='sans-serif', size=fs)

################
# Loading data #
################

# get A estrategy labels
keywords_labels = SQLITE.getKeywordsLabels(entity='user')
keywords_data = keywords_labels.merge(
    att_sources,
    left_on='pseudo_id',
    right_on='entity',
    how='inner') \
    .drop(columns=['pseudo_id'])

# get C estrategy labels
llm_labels = SQLITE.getLLMLabels('user')
llm_data = llm_labels.merge(
    att_sources,
    left_on='pseudo_id',
    right_on='entity',
    how='inner') \
    .drop(columns=['pseudo_id'])

estrategy_data = {
    'A': keywords_data,
    'C': llm_data
}

COLOR = ['red', 'blue']

for estrategy in estrategy_data.keys():

    for lrdata in LOGISTICREGRESSIONS:

        egroups = {
            1:  f"{estrategy}_{lrdata['group1']}",
            2:  f"{estrategy}_{lrdata['group2']}",
        }

        # check that label is prsent for estrategi
        # for instance there is no 'climate denialist' for the A estrategy
        if not egroups[1] in estrategy_data[estrategy]:
            print(f"{egroups[1]} is missing from {estrategy} estrategy data.")
            continue
        if not egroups[2] in estrategy_data[estrategy]:
            print(f"{egroups[2]} is missing from {estrategy} estrategy data.")
            continue

        data = {
            1: estrategy_data[estrategy].query(f"{egroups[1]}=='1'"),
            2: estrategy_data[estrategy].query(f"{egroups[2]}=='1'")
        }

        for attdim in lrdata[survey]:

            label1 = egroups[1]
            label2 = egroups[2]

            attdata1 = data[1][attdim]
            attdata2 = data[2][attdim]

            l1 = len(attdata1)
            l2 = len(attdata2)

            # to do cross validation
            if l1 > l2:
                attdata1 = attdata1.sample(n=l2, weights=None, random_state=666)
                print(f"{label1} data uniformly sample from {l1} to {l2}.")
            if l2 > l1:
                attdata2 = attdata2.sample(n=l1, weights=None, random_state=666)
                print(f"{label1} data uniformly sample from {l2} to {l1}.")

            X = np.hstack([
                attdata1.values,
                attdata2.values
            ]).reshape(-1, 1)

            y = np.hstack([
                np.zeros_like(attdata1.values),
                np.ones_like(attdata2.values)
            ]).reshape(-1, 1)

            # benchmark = load_issues_benckmarks(att_folder) \
            #     .query(f"dimension == '{attdim}'")

            # precision = benchmark.precision_train_.to_list()[0]
            # recall = benchmark.recall_train_.to_list()[0]
            # f1 = benchmark.f1_score_train_.to_list()[0]

            clf = LogisticRegression(C=1e5)
            clf.fit(X,  y)

            f = expit(X * clf.coef_ + clf.intercept_).ravel()

            above_threshold = f > 0.5
            X_threshold = X[:,  0][above_threshold][0]

            custom_legend=[
                #densities
                Line2D([0], [0], color='white', lw=1, alpha=1, label='Users:'),
                Line2D([0], [0], color='blue', marker='o', mew=0, lw=0, alpha=0.5,
                    label=f'Labeled {label1}'),
                Line2D([0], [0], color='red', marker='o', mew=0, lw=0, alpha=0.5,
                    label=f'Labeled {label2}'),
                #densities
                Line2D([0], [0], color='white', lw=1, alpha=1, label='\nDensities:'),
                Line2D([0], [0], color='blue', alpha=1, label=f'Labeled {label1}'),
                Line2D([0], [0], color='red', alpha=1, label=f'Labeled {label2}\n'),
                Line2D([0], [0], color='white', lw=1, alpha=1, label='\nLogistic Reg.:'),
                Line2D([0], [0], color='k',  alpha=1, label='Model'),
                Line2D([0], [0], color='k',  linestyle=':', alpha=1,
                    label='Classification'),
                Line2D([0], [0], color='white', lw=1, alpha=1, label='cuttof'),
            ]

            fig = plt.figure(figsize=(5,  3.3))
            ax = fig.add_subplot(1,  1,  1)

            # left/blue
            sn.kdeplot(data=attdata1.to_frame(), x=attdim, color='blue', ax=ax, common_norm=False)
            ax.plot(X[y==0], np.zeros(X[y==0].size), 'o', color='blue', alpha=0.02, ms=5, mew=1)

            # right/red
            sn.kdeplot(data=attdata2.to_frame(), x=attdim, color='red', ax=ax, common_norm=False)
            ax.plot(X[y==1], np.ones(X[y==1].size),  'o', color='red',  alpha=0.02, ms=5, mew=1)

            # logistic
            # ax.plot(X.flatten(), f, color='k')
            ax.axvline(X_threshold, linestyle=':', color='k')
            ax.axhline(0.5, linestyle=':', color='k')
            ax.text(-3.6, 0.47, r'$0.5$', color='gray', fontsize=10)
            ax.text(X_threshold-0.9, -0.28, r'$%.2f$' % (X_threshold), color='gray', fontsize=10)

            # positives & negatives
            ax.text(X_threshold+0.2, 1.1, 'True pos.', color='r', fontsize=9)
            ax.text(X_threshold-3.15, 1.1, 'False neg.', color='r', fontsize=9)
            ax.text(X_threshold+0.2, -0.1, 'False pos.', color='b', fontsize=9)
            ax.text(X_threshold-3.05, -0.1, 'True neg.', color='b', fontsize=9)

            # axis
            ax.set_xlim((-2.5, 15))
            ax.set_ylim((-0.2, 1.2))
            s = ATTDICT[survey][attdim]
            ax.set_xlabel(f"$d_{{{s}}}$" , fontsize=13)
            ax.set_ylabel('')
            ax.legend(handles=custom_legend, loc='center left', fontsize=8.7, bbox_to_anchor=(1, 0.5))
            ax.set_xticks([0, 2.5, 5, 7.5, 10])
            ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
            # ax.set_title(f'{country.capitalize()}: precision=%.3f,  recall=%.3f,  F1=%.3f ' % (precision, recall, f1))

            plt.tight_layout()

            # #saving
            # figname = f'{country}_{issue}_{attdim}.png'
            # path = os.path.join(att_folder, figname)
            # plt.savefig(path, dpi=300)
            # print(f"Figure saved at {path}.")

            if show:
                plt.show()