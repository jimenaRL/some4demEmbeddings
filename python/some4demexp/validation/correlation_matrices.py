import os
import yaml
from argparse import ArgumentParser

import numpy as np
import pandas as pd
from scipy import stats

import seaborn as sns
import matplotlib.pyplot as plt

from some4demdb import SQLite
from some4demexp.inout import \
    set_output_folder, \
    set_output_folder_att, \
    load_att_embeddings, \
    save_issues_benckmarks, \
    set_output_folder_emb, \
    load_ide_embeddings

from some4demexp.conf import \
    CHESLIMS, \
    ATTDICT

from some4demexp.correlation_coefficient import smallSamplesSpearmanr

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
NIDEDIMS = params['ideological_model']['n_latent_dimensions']
IDEDIMS = range(NIDEDIMS)

IDEDIMSNAMES = [fr'$\delta_{j+1}$' for j in IDEDIMS]
ATTDIMSNAMES = [ATTDICT[i] for i in ATTDIMS]

SQLITE = SQLite(params['sqlite_db'])


def compute_correlation_matrices(
    ide_data, att_data, info, methods, pvalue_display_th=0.05):

    for method, correlation_fn, cmap in methods:

        fig = plt.figure(figsize=(16, 8))
        ax = fig.add_subplot(1,  1,  1)

        correlations = np.empty((len(ATTDIMS), NIDEDIMS), float)
        annotations = np.empty((len(ATTDIMS), NIDEDIMS), object)

        for i, attdim in enumerate(ATTDIMS):
            for j in IDEDIMS:
                statistic, pvalue = correlation_fn(
                    ide_data[f'latent_dimension_{j}'],
                    att_data[attdim]
                )
                correlations[i, j] = statistic
                if pvalue <= pvalue_display_th:
                    annotations[i, j] = f'{statistic:.2f} (p={pvalue:.3f})'
                else:
                    annotations[i, j] = f'{statistic:.2f}'

        correlations = pd.DataFrame(
            correlations,
            index=ATTDIMSNAMES,
            columns=IDEDIMSNAMES
        ) \
        .rename_axis(
            index="Attitudinal",
            columns='Ideological'
        )

        annotations = pd.DataFrame(
            annotations,
            index=ATTDIMSNAMES,
            columns=IDEDIMSNAMES,
            dtype=str,
        ) \
        .rename_axis(
            index="Attitudinal",
            columns='Ideological'
        )



        print(f"----------------- {method} -----------------")
        print(f"----------------- {info} -----------------")
        print(annotations)

        sns.heatmap(correlations, ax=ax, annot=annotations, fmt="", cmap=cmap)
        ax.set(xlabel="", ylabel="")
        ax.xaxis.tick_top()
        _title = f"{method} Coeficient Correlation Matrix \n"
        _title += f"{country.capitalize()} N={NIDEDIMS}  M={len(ATTDIMS)}\n"
        _title += info
        _title += f"\np-values less than {pvalue_display_th} displayed"
        plt.title(_title)
        plt.tight_layout()

        figpath = os.path.join(
            att_folder,
            f"{info}_{method}_ide_vs_att_dims_correlation_matrix.png")
        plt.savefig(figpath)
        print(f"Correlation Matrix figure saved at {figpath}.")

    if show:
        plt.show()


# (0) Get embeddings
folder = set_output_folder(params, country, output)

ide_folder = set_output_folder_emb(params, country, output)
ide_sources, ide_targets = load_ide_embeddings(ide_folder)

att_folder = set_output_folder_att(params, country, output)
att_sources, att_targets = load_att_embeddings(att_folder)

cmap_s = sns.diverging_palette(145, 300, s=60, as_cmap=True)

# (1) Compute correlation matrix IDE vs CHES for parties

groups_coord_att = SQLITE.retrieveAndFormatTargetGroupsAttitudes(country, ATTDIMS)
parties_mapping = SQLITE.getPartiesMapping(country)
valid_parties = parties_mapping.ches2019_party

l0 = len(ide_targets)
ide_targets = ide_targets.merge(att_targets[["party", "entity"]])
if not l0 == len(ide_targets):
    raise ValueError(f"Target loss during merge.")

ide_targets = ide_targets[ide_targets.party.isin(valid_parties)]

estimated_groups_coord_ide = ide_targets \
    .groupby('party') \
    .mean() \
    .reset_index()

small_samples_methods = [
    ("Pearson", stats.pearsonr, "vlag"),
    ("Spearman", smallSamplesSpearmanr, cmap_s),
]

compute_correlation_matrices(
    estimated_groups_coord_ide,
    groups_coord_att,
    "PARTIES",
    small_samples_methods)


# (2) Compute correlation matrix IDE vs CHES for parties

data =  ide_sources.merge(att_sources,  on='entity',  how='inner')

large_samples_methods = [
    ("Pearson",  stats.pearsonr, "vlag"),
    ("Spearman", stats.spearmanr, cmap_s),
]

compute_correlation_matrices(
    data,
    data,
    "SOURCES",
    large_samples_methods)

