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

from some4demexp.inout import \
    set_output_folder,  \
    set_output_folder_att,  \
    load_att_embeddings,  \
    load_issues, \
    load_issues_benckmarks

from some4demexp.conf import \
    CHESLIMS,  \
    ATTDICT

# parse arguments and set paths
ap = ArgumentParser()
ap.add_argument('--config',  type=str,  required=True)
ap.add_argument('--country',  type=str,  required=True)
ap.add_argument('--output',  type=str,  required=True)
ap.add_argument('--show',  action='store_true', required=False)

args = ap.parse_args()
config = args.config
country = args.country
output = args.output
show = args.show

with open(config,  "r",  encoding='utf-8') as fh:
    params = yaml.load(fh,  Loader=yaml.SafeLoader)
print(yaml.dump(params,  default_flow_style=False))

ATTDIMS = params['attitudinal_dimensions']
IDEDIMS = range(params['ideological_model']['n_latent_dimensions'])
ISSUES = [
    'Left', 'Right',
    # 'Elites', 'People', 'Politicians', 'StartUp', 'Entrepreneur',
    # 'Immigration',
    # 'Europe',
    # 'Environment'
]
ATTDIMISSUES = {
    'lrgen': ['Left', 'Right']
}
#########################################
# Preliminary functions and definitions #
#########################################

# Font & Latex definitions
mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['mathtext.rm'] = 'serif'
# mpl.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
plt.rc('text',  usetex=True)
plt.rc('font', family = 'sans-serif',   size=12)

################
# Loading data #
################

# attdim = "eu_position" # "antielite_salience" or "eu_position"
# labelA = 'antielite'
# labelB = 'elite'

attdim = "lrgen"  # "lrecon" or "lrgen"
labelA = 'Left'
labelB = 'Right'

issue = '-'.join(ATTDIMISSUES[attdim])

folder = set_output_folder(params,  country,  output)
att_folder = set_output_folder_att(params,  country,  output)

benchmark = load_issues_benckmarks(att_folder) \
    .query(f"dimension == '{attdim}'")

precision = benchmark.precision_train_.to_list()[0]
recall = benchmark.recall_train_.to_list()[0]
f1 = benchmark.f1_score_train_.to_list()[0]

att_sources,  _ = load_att_embeddings(att_folder)

data =  load_issues(folder,  issue) \
        .merge(att_sources,  on='entity',  how='inner')

data = data[["label",  "tag",  attdim]] \
    .sort_values(by=attdim,  ascending=True,  inplace=False)

X = data[attdim].values[:,  np.newaxis]
y = data['label'].values

clf = LogisticRegression(C=1e5)
clf.fit(X,  y)

f = expit(X * clf.coef_ + clf.intercept_).ravel()

Xplot = X[:,  0]
dfplot = data

above_threshold = f > 0.5
X_threshold = Xplot[above_threshold][0]

custom_legend=[
    #densities
    Line2D([0], [0], color='white', lw=1, alpha=1, label='Users:'),
    Line2D([0], [0], color='blue', marker='o', mew=0, lw=0, alpha=0.5,
        label=f'Labeled {labelA}'),
    Line2D([0], [0], color='red', marker='o', mew=0, lw=0, alpha=0.5,
        label=f'Labeled {labelB}'),
    #densities
    Line2D([0], [0], color='white', lw=1, alpha=1, label='\nDensities:'),
    Line2D([0], [0], color='blue', alpha=1, label=f'Labeled {labelA}'),
    Line2D([0], [0], color='red', alpha=1, label=f'Labeled {labelB}\n'),
    Line2D([0], [0], color='white', lw=1, alpha=1, label='\nLogistic Reg.:'),
    Line2D([0], [0], color='k',  alpha=1, label='Model'),
    Line2D([0], [0], color='k',  linestyle=':', alpha=1,
        label='Classification'),
    Line2D([0], [0], color='white', lw=1, alpha=1, label='cuttof'),
]

fig = plt.figure(figsize=(5,  3.3))
ax = fig.add_subplot(1,  1,  1)

# left/blue
sn.kdeplot(data=dfplot[dfplot['label']==0], x=attdim, color='blue', ax=ax, common_norm=False)
ax.plot(X[y==0], np.zeros(Xplot[y==0].size), 'o', color='blue', alpha=0.02, ms=5, mew=1)

# right/red
sn.kdeplot(data=dfplot[dfplot['label']==1], x=attdim, color='red', ax=ax, common_norm=False)
ax.plot(X[y==1], np.ones(Xplot[y==1].size),  'o', color='red',  alpha=0.02, ms=5, mew=1)

# logistic
ax.plot(Xplot, f, color='k')
ax.axvline(X_threshold, linestyle=':', color='k')
ax.axhline(0.5, linestyle=':', color='k')
ax.text(-3.6, 0.47, r'$0.5$', color='gray', fontsize=10)
ax.text(X_threshold-0.9, -0.28, r'$%.2f$'%(X_threshold), color='gray', fontsize=10)

# positives & negatives
ax.text(X_threshold+0.2, 1.1, 'True pos.', color='r', fontsize=9)
ax.text(X_threshold-3.15, 1.1, 'False neg.', color='r', fontsize=9)
ax.text(X_threshold+0.2, -0.1, 'False pos.', color='b', fontsize=9)
ax.text(X_threshold-3.05, -0.1, 'True neg.', color='b', fontsize=9)

# axis
ax.set_xlim((-2.5, 15))
ax.set_ylim((-0.2, 1.2))
s = ATTDICT[attdim][4:]
ax.set_xlabel(f"$d_{{{s}}}$" , fontsize=13)
ax.set_ylabel('')
ax.legend(handles=custom_legend, loc='center left', fontsize=8.7, bbox_to_anchor=(1, 0.5))
ax.set_xticks([0, 2.5, 5, 7.5, 10])
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
ax.set_title(f'{country.capitalize()}: precision=%.3f,  recall=%.3f,  F1=%.3f ' % (precision, recall, f1))


plt.tight_layout()

#saving
figname = f'{country}_{issue}_{attdim}.png'
path = os.path.join(att_folder, figname)
plt.savefig(path, dpi=300)
print(f"Figure saved at {path}.")

if show:
    plt.show()