import os
import yaml
import json
import itertools
from tqdm import tqdm
from argparse import ArgumentParser

import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from scipy.special import expit
from sklearn.metrics import \
    precision_score, \
    recall_score, \
    f1_score

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import matplotlib.ticker as mtick
import matplotlib.patheffects as PathEffects

import seaborn as sns
import matplotlib.pyplot as plt

from some4demdb import SQLite

from corg import \
    BenchmarkDimension

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
ap.add_argument('--plot',  action='store_true', required=False)
ap.add_argument('--show',  action='store_true', required=False)

args = ap.parse_args()
config = args.config
country = args.country
survey = args.survey
output = args.output
plot = args.plot
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

SEED = 666

# (0) Get embeddings and descriptions
folder = set_output_folder(params, country, output)

att_folder = set_output_folder_att(params, survey, country, ideN, output)
att_sources, _ = load_att_embeddings(att_folder)

lrfolder = os.path.join(att_folder, 'logistic_regression')

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

# get A strategy labels
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

strategy_data = {
    'A': keywords_data,
    'C': llm_data
}


records = []

for strategy, lrdata in tqdm(
    itertools.product(strategy_data.keys(), LOGISTICREGRESSIONS)):

    egroups = {
        1:  f"{strategy}_{lrdata['group1']}",
        2:  f"{strategy}_{lrdata['group2']}",
    }

    # check that label is prsent for estrategi
    # for instance there is no 'climate denialist' for the A strategy
    if not egroups[1] in strategy_data[strategy]:
        print(f"{egroups[1]} is missing from {strategy} strategy data.")
        continue
    if not egroups[2] in strategy_data[strategy]:
        print(f"{egroups[2]} is missing from {strategy} strategy data.")
        continue

    data = {
        1: strategy_data[strategy].query(f"{egroups[1]}=='1'"),
        2: strategy_data[strategy].query(f"{egroups[2]}=='1'")
    }

    if len(data[1]) == 0:
        print(f"{country}: there is no users labeled {egroups[1]} in data.")
        continue
    if len(data[2]) == 0:
        print(f"{country}: there is no users labeled {egroups[2]} in data.")
        continue

    for attdim in lrdata[survey]:

        label1 = egroups[1]
        label2 = egroups[2]

        attdata1 = data[1][attdim]
        attdata2 = data[2][attdim]

        l1 = len(attdata1)
        l2 = len(attdata2)

        X = np.hstack([
            attdata1.values,
            attdata2.values
        ]).reshape(-1, 1)

        y = np.hstack([
            np.zeros_like(attdata1.values),
            np.ones_like(attdata2.values)
        ]).ravel()


        # egalize sample
        SEED = 666
        n = min(len(attdata1), len(attdata2))
        _data = pd.concat([
            data[1][[attdim, 'entity']].sample(n=n, random_state=SEED).assign(label=0),
            data[2][[attdim, 'entity']].sample(n=n, random_state=SEED).assign(label=1)
        ])
        X = _data[attdim].values.reshape(-1, 1)
        y = _data['label'].values.ravel()

        clf = LogisticRegression(penalty='l2', C=1e5, class_weight='balanced')
        clf.fit(X,  y)

        # evaluation
        Y_pred = clf.predict(X)

        precision = precision_score(y, Y_pred)
        recall = recall_score(y, Y_pred)
        f1 = f1_score(y, Y_pred)

        record = {
            "strategy": strategy,
            "label1": label1,
            "label2": label2,
            "nb_samples_label1": l1,
            "nb_samples_label2": l2,
            "attitudinal_dimension": attdim,
            "attitudinal_dimension_name": ATTDICT[survey][attdim],
            "survey": survey,
            "precision": precision,
            "recall": recall,
            "f1":  f1,
            "country": country
            }

        su = strategy.upper()
        os.makedirs(os.path.join(lrfolder, 'json'), exist_ok=True)
        result_path = os.path.join(
            lrfolder, 'json', f"strategy{su}_{attdim}_{label1}_{label2}.json")
        result_path_exp = os.path.join(
            f"exports/deliverableD21/validations/{country}",
            f"strategy{su}_{attdim}_{label1}_{label2}.json")
        with open(result_path, 'w') as file:
            json.dump(record, file)
        with open(result_path_exp, 'w') as file:
            json.dump(record, file)

        # add results data
        # print(record)
        records.append(record)

        # plot
        if plot:
            Xplot = np.sort(X.flatten())
            f = expit(Xplot * clf.coef_[0][0] + clf.intercept_[0]).ravel()

            if clf.intercept_[0] < 0:
                above_threshold = f > 0.5
            else:
                above_threshold = f < 0.5

            X_threshold = Xplot[above_threshold][0]

            custom_legend=[
                #densities
                Line2D([0], [0], color='white', lw=1, alpha=1, label='Users:'),
                Line2D([0], [0], color='blue', marker='o', mew=0, lw=0, alpha=0.5,
                    label=f'Labeled {label1} ({l1})'),
                Line2D([0], [0], color='red', marker='o', mew=0, lw=0, alpha=0.5,
                    label=f'Labeled {label2} ({l2})'),
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
            sns.kdeplot(data=attdata1.to_frame(), x=attdim, color='blue', ax=ax, common_norm=False)
            ax.plot(X[y==0], np.zeros(X[y==0].size), 'o', color='blue', alpha=0.02, ms=5, mew=1)

            # right/red
            sns.kdeplot(data=attdata2.to_frame(), x=attdim, color='red', ax=ax, common_norm=False)
            ax.plot(X[y==1], np.ones(X[y==1].size),  'o', color='red',  alpha=0.02, ms=5, mew=1)

            # logistic
            ax.plot(Xplot, f, color='k')
            ax.axvline(X_threshold, linestyle=':', color='k')
            ax.axhline(0.5, linestyle=':', color='k')
            ax.text(-2.3, 0.42, r'$0.5$', color='gray', fontsize=10)
            ax.text(X_threshold+0.25, -0.18, r'$%.2f$' % (X_threshold), color='gray', fontsize=10)

            # positives & negatives
            ax.text(X_threshold+0.2, 1.1, 'True pos.', color='r', fontsize=9)
            ax.text(X_threshold-3.15, 1.1, 'False neg.', color='r', fontsize=9)
            ax.text(X_threshold+0.2, -0.1, 'False pos.', color='b', fontsize=9)
            ax.text(X_threshold-3.05, -0.1, 'True neg.', color='b', fontsize=9)

            # axis
            ax.set_xlim((-2.5, 15))
            ax.set_ylim((-0.2, 1.2))
            s = ATTDICT[survey][attdim].replace(' ', '-')
            ax.set_xlabel(f"$\delta_{{{s}}}$", fontsize=13)
            ax.set_ylabel('')
            ax.legend(handles=custom_legend, loc='center left', fontsize=8.7, bbox_to_anchor=(1, 0.5))
            ax.set_xticks([0, 2.5, 5, 7.5, 10])
            ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
            title = f
            fig.suptitle(
                t=f'{country.capitalize()}: precision=%.3f,  recall=%.3f,  F1=%.3f ' % (precision, recall, f1),
                x=0.5,
                y=0.94
            )
            plt.tight_layout()

            #saving
            figname = f'lr_{country}_{strategy}_strategy_{attdim}_'
            figname += f'{egroups[1]}_vs_{egroups[2]}'
            path_png = os.path.join(lrfolder, 'png', figname+'.png')
            plt.savefig(path_png, dpi=300)
            path_pdf = os.path.join(att_folder, 'logistic_regression', 'pdf', figname+'.pdf')
            plt.savefig(path_pdf, dpi=300)

            path_pdf_exp = os.path.join(
                f"exports/deliverableD21/validations/{country}",
                f"strategy{su}_{attdim}_{label1}_{label2}.pdf")
            plt.savefig(path_pdf_exp, dpi=300)

            if show:
                plt.show()

            plt.close()

print(f"Figures saved at {lrfolder}")

records = pd.DataFrame(records).sort_values(by='f1', ascending=False)


kind = records['attitudinal_dimension_name']
kind += ": "
kind += records['label1'].apply(lambda s: s[2:])
kind += " vs "
kind += records['label2'].apply(lambda s: s[2:])
kind += " "
kind += records['strategy']
records = records.assign(kind=kind)

kind_stats = records['attitudinal_dimension_name']
kind_stats += ": "
kind_stats += records['label1'].apply(lambda s: s[2:])
kind_stats += " ("
kind_stats += records['nb_samples_label1'].astype(str)
kind_stats += ") vs "
kind_stats += records['label2'].apply(lambda s: s[2:])
kind_stats += " ("
kind_stats += records['nb_samples_label2'].astype(str)
kind_stats += ") "
kind_stats += records['strategy']
records = records.assign(kind_stats=kind_stats)
print(records)


filename = f"{country}_{survey}_logistic_regression_balanced_class_weight_f1_score"
dfpath = os.path.join(lrfolder, filename+'.csv')
records.to_csv(dfpath, index=False)
print(f"Logistic regression results (image and csv) saved at {lrfolder}")


sns.set_theme(style="whitegrid")

# Initialize the matplotlib figure
f, ax = plt.subplots(figsize=(16, 14))

# Plot the total crashes
sns.set_color_codes(palette="deep")
sns.barplot(x="f1", y="kind", data=records, label="f1", color="r")

# Add a legend and informative axis label
plt.xticks(np.arange(0, 1.1, .1, dtype=float))
ax.legend(ncol=2, loc="lower right", frameon=True, fontsize=15)
ax.set(xlim=(0, 1), ylabel="")
ax.set_xlabel(f"{country.upper()} - {survey.upper()} - LR (balanced class weight) f1 score ", fontsize=16)
ax.set_ylabel('')
ax.tick_params(axis="y", labelsize=16)

sns.despine(left=True, bottom=True)
plt.tight_layout()

figpath = os.path.join(lrfolder, filename+'.png')
plt.savefig(figpath, dpi=300)

if show:
    plt.show()
