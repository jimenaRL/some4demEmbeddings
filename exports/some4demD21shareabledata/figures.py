"""
2. Para cada país generar la imagen bonita 2D con las dos dimensiones latentes left_right y antielite con densidad en azul, MPs +, partidos (centroide) o.
** Para las figuras 2D, delete users with duplicate coordinates ?
3. Nomenclatura para los ejes de las imágenes 2D:
    3a. dimensiones ideológicas: ‘First latent dimension $\delta_1$’ y ‘Second latent dimension $\delta_2$’
    3b. dimensiones CHES: ‘Left – Right’ and ‘Anti-elite rhetoric’
    3c. Hay que correr las cajitas de los nombres de los partidos para que sean visibles las posiciones de los partidos.
4. Calcular una tabla de países versus labels 9 x 4 para mostrar la cantidad de labels: (index y columns) exportado a csv y latex
4. Calcular los F1 (con std para N=100 subsampling minoritario) 2 x 9, exportado a csv y latex
5. Para cada país y para left_right y antielite, calcular una figura de regresión logística (18 figuras):
    5a. la regresión logística es con los parámetros promedio
    5b. los KDE son sobre la totalidad de las muestras labelled
"""

import os
import yaml
import pandas as pd
import seaborn as sns

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patheffects as PathEffects

plt.rc('text', usetex=True)
plt.rc('font', family='sans-serif', size=12)

DPI = 300
FONTSIZE = 12
LIMS = [0, 10]

legend_mps = Line2D(
    [0],
    [0],
    label='MPs',
    marker='+',
    markersize=5,
    linewidth=0,
    markeredgecolor='black',
)
legend_parties = Line2D(
    [0],
    [0],
    label='Parties',
    marker='o',
    markersize=5,
    linewidth=0,
    markeredgecolor='black',
    markerfacecolor='white',
)
legend_followers = Line2D(
    [0],
    [0],
    label='Followers',
    marker='h',
    markersize=5,
    linewidth=0,
    markeredgecolor='deepskyblue',
    markerfacecolor="deepskyblue"
)
CUSTOMLEGEND = [legend_mps, legend_parties, legend_followers]

COUNTRIES = [
    'belgium',
    'france',
    'germany',
    'italy',
    'netherlands',
    'poland',
    'romania',
    'slovenia',
    'spain',
]


IDEFIG = False
ATTFIG = False

SHOW = False

for country in COUNTRIES:

    print(f"----- {country} -----")

    vizconfig = os.path.join("vizconfigs", f"{country}.yaml")
    with open(vizconfig, "r", encoding='utf-8') as fh:
        vizparams = yaml.load(fh, Loader=yaml.SafeLoader)

    palette = vizparams['palette']

    sources_coord = pd.read_csv(f"{country}_users.csv")
    targets_coord = pd.read_csv(f"{country}_mps.csv")

     # I. Ideological embeddings visualizations
    if IDEFIG:

        nudges = vizparams['ideological']['nudges']
        limits = vizparams['ideological']['limits']
        cbar_rect = vizparams['ideological']['cbar_rect']
        legend_loc = vizparams['ideological']['legend_loc']

        plot_df = pd.concat([
            sources_coord[['delta_1', 'delta_2']],
            targets_coord[['delta_1', 'delta_2']]
            ]) \
            .reset_index() \
            .drop(columns="index") \
            .rename(columns={'delta_1': 'x', 'delta_2': 'y'})

        kwargs = {
            'x': 'x',
            'y': 'y',
            'space': 0,
            'ratio': 10,
            'height': 5,
            'color': "deepskyblue",
            'gridsize': 100,
            'kind': 'hex',
            'data': plot_df,
        }

        g = sns.jointplot(**kwargs)

        ax = g.ax_joint
        texts = []
        for party in palette:

            sample = targets_coord[targets_coord.party == party]
            sample = sample[['delta_1', 'delta_2', 'party']] \
                .rename(columns={'delta_1': 'x', 'delta_2': 'y'})

            if len(sample) == 0:
                continue

            ax.scatter(
                sample['x'],
                sample['y'],
                marker='+',
                s=20,
                alpha=0.5,
                color=palette[party],
                label=party
            )

            mean_group_estimated = sample[['x', 'y']].mean()

            ax.plot(
                mean_group_estimated['x'],
                mean_group_estimated['y'],
                marker='o',
                markeredgecolor='black',
                markeredgewidth=1.0,
                markersize=5,
                color=palette[party],
            )

            text = ax.text(
                mean_group_estimated['x']+nudges[party][0],
                mean_group_estimated['y']+nudges[party][1],
                party.replace("&", ""),
                color='white',
                bbox=dict(
                    boxstyle="round",
                    ec='black',
                    fc=palette[party],
                    alpha=1),
                fontsize=9)
            texts.append(text)

        xl = fr'1st latent dimension $\delta_1$'
        yl = fr'2nd latent dimension $\delta_2$'
        ax.set_xlabel(xl, fontsize=FONTSIZE)
        ax.set_ylabel(yl, fontsize=FONTSIZE)

        ax.legend(handles=CUSTOMLEGEND, loc=legend_loc)
        ax.tick_params(axis='x', labelsize=FONTSIZE)
        ax.tick_params(axis='x', labelsize=FONTSIZE)

        ax.set_xlim(limits['x'])
        ax.set_ylim(limits['y'])

        cbar_ax = g.fig.add_axes(cbar_rect)
        cbar = plt.colorbar(cax=cbar_ax)

        path = f"{country}_delta_1_vs_delta_2.pdf"
        plt.savefig(path, dpi=DPI)
        print(f"Figure saved at {path}.")

        if SHOW:
            plt.show()


    # II. Ideological embeddings visualizations
    if ATTFIG:

        attparams =  vizparams['attitudinal']['ches2019']['lrgen_vs_antielite_salience']
        nudges = attparams['nudges']
        limits = attparams['limits']
        cbar_rect = attparams['cbar_rect']
        legend_loc = attparams['legend_loc']

        plot_df = pd.concat([
            sources_coord[['left_right', 'antielite']],
            targets_coord[['left_right', 'antielite']]
            ]) \
            .reset_index() \
            .drop(columns="index") \
            .rename(columns={'left_right': 'x', 'antielite': 'y'})

        kwargs = {
            'x': 'x',
            'y': 'y',
            'color': "deepskyblue",
            'space': 2,
            'ratio': 10,
            'height': 5,
            'kind': 'hex',
            'data': plot_df,
        }

        # plot sources and targets embeddings
        g = sns.jointplot(**kwargs)

        ax = g.ax_joint

        # plot square showing CHES limits

        lowlim_x = 0
        upperlim_x = 10
        lowlim_y = 0
        upperlim_y = 10
        A = [lowlim_x, lowlim_x, upperlim_x, upperlim_x, lowlim_x]
        B = [lowlim_y, upperlim_y, upperlim_y, lowlim_y, lowlim_y]
        ax.plot(A, B, color='white', linestyle='-')
        ax.plot(A, B, color='black', linestyle='--')
        txt = ax.text(2, 10.25, f'CHES survey bounds', fontsize=12)
        txt.set_path_effects(
            [PathEffects.withStroke(linewidth=2, foreground='w')])

        # plot colored by parties targets attitudinal embeddings
        texts = []

        for party in palette:

            # plot colored by parties target embeddings
            mps_coord_att = targets_coord[targets_coord['party'] == party] \
                .rename(columns={'left_right': 'x', 'antielite': 'y'})

            ax.scatter(
                mps_coord_att['x'],
                mps_coord_att['y'],
                marker='+',
                s=20,
                alpha=0.5,
                color=palette[party],
                label=party
            )

            group_positions = mps_coord_att[['x', 'y']].mean()
            ax.plot(
                group_positions.iloc[0],
                group_positions.iloc[1],
                marker='o',
                markeredgecolor='black',
                markeredgewidth=1.0,
                markersize=5,
                color=palette[party],
        )

            text = ax.text(
                group_positions.iloc[0]+nudges[party][0],
                group_positions.iloc[1]+nudges[party][1],
                party.replace("&", ""),
                color='white',
                bbox=dict(
                    boxstyle="round",
                    ec='black',
                    fc=palette[party],
                    alpha=1),
                fontsize=9)
            texts.append(text)

        ax.set_xlabel('Left – Right', fontsize=FONTSIZE)
        ax.set_ylabel('Anti-elite rhetoric', fontsize=FONTSIZE)

        ax.legend(
            handles=CUSTOMLEGEND,
            loc=legend_loc,
            fontsize=FONTSIZE-2,
            framealpha=0.98
        )

        ax.tick_params(axis='x', labelsize=FONTSIZE)
        ax.tick_params(axis='x', labelsize=FONTSIZE)

        # setting lims
        ax.set_xlim(limits)
        ax.set_ylim(limits)

        cbar_ax = g.fig.add_axes(cbar_rect)
        cbar = plt.colorbar(cax=cbar_ax)

        path = f"{country}_left_right_vs_antielite.pdf"
        plt.savefig(path, dpi=DPI)
        print(f"Figure saved at {path}.")

        if SHOW:
            plt.show()



