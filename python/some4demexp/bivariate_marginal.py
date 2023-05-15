import os
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patheffects as PathEffects
from adjustText import adjust_text

plt.rc('text', usetex=True)
plt.rc('font', family='sans-serif', size=12)

fs = 12
dpi = 150

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
custom_legend = [legend_mps, legend_parties, legend_followers]


ATT_DICT = {
    'lrgen': 'Left- Right',
    'eu_position': 'EU integration',
    'antielite_salience': 'Anti-elite salience',
    'lrecon': 'Left- Right economy',
    'immigrate_policy': 'Immigration',
    'galtan': 'Liberal - Traditional',
    'environment': 'Importance of ecology'
}

def get_ordinal(n):
    if n < 0 or not isinstance(n, int):
        raise ValueError(f"Input must be a strictly positive interger.")
    if n == 1:
        return "1st"
    elif n == 2:
        return "2nd"
    else:
        return f"{n}th"


def visualize_ide(
    sources_coord_ide,
    targets_coord_ide,
    targets_parties,
    latent_dim_x,
    latent_dim_y,
    palette,
    nudges,
    limits,
    cbar_rect,
    legend_loc,
    output_folder=None,
    show=False
):

    # preprocessing
    colrename = {
        f'latent_dimension_{latent_dim_x}': 'x',
        f'latent_dimension_{latent_dim_y}': 'y'
    }
    sources_coord_ide = sources_coord_ide.rename(columns=colrename)
    targets_coord_ide = targets_coord_ide.rename(columns=colrename)
    targets_parties = targets_parties.rename(columns=colrename)

    plot_df = pd.concat([sources_coord_ide, targets_coord_ide]) \
        .reset_index() \
        .drop(columns="index")

    l0 = len(plot_df)
    plot_df = plot_df.drop_duplicates()
    l1 = len(plot_df)
    if (l0 > l1):
        print(f"Dropped {l1 -l0} repeated embeddings points.")

    # setting lims
    pad = 0.35
    dx = plot_df['x'].max()-plot_df['x'].min()
    dy = plot_df['y'].max()-plot_df['y'].min()
    xlims = (plot_df['x'].min()-pad*dx, plot_df['x'].max()+pad*dx)
    ylims = (plot_df['y'].min()-pad*dy, plot_df['y'].max()+pad*dy)

    # This turned out to be 6x6 figsize
    kwargs = {
        'x': 'x',
        'y': 'y',
        'space': 0,
        'ratio': 10,
        'height': 5,
        'color': "deepskyblue",
        'kind': 'hex',
        'data': plot_df,
    }

    # plot sources and targets ideological embeddings
    g = sns.jointplot(**kwargs)

    # get unique parties and build color dictionary
    unique_parties = targets_parties.party.unique().tolist()
    nunique_parties = len(set(unique_parties))

    targets_coord_ide = targets_coord_ide.merge(
            targets_parties,
            left_on="entity",
            right_on="mp_pseudo_id",
            how="inner"
        ) \
        .drop(columns="mp_pseudo_id")

    # plot colored by parties target embeddings
    ax = g.ax_joint
    texts = []
    for party in unique_parties:

        sample = targets_coord_ide[targets_coord_ide.party == party]

        ax.scatter(
            sample['x'],
            sample['y'],
            marker='+',
            s=20,
            alpha=0.5,
            color=palette[party],
            label=party
        )

        # plot estimated parties mean
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
            party,
            color='white',
            bbox=dict(
                boxstyle="round",
                ec='black',
                fc=palette[party],
                alpha=1),
            fontsize=9)
        texts.append(text)

    adjust_text(texts)

    xl = fr'{get_ordinal(latent_dim_x+1)} latent dimension '
    xl += fr'$\delta_{latent_dim_x+1}$'
    yl = fr'{get_ordinal(latent_dim_y+1)} latent dimension '
    yl += fr'$\delta_{latent_dim_y+1}$'
    ax.set_xlabel(xl, fontsize=fs)
    ax.set_ylabel(yl, fontsize=fs)

    ax.legend(handles=custom_legend, loc=legend_loc)
    ax.tick_params(axis='x', labelsize=fs)
    ax.tick_params(axis='x', labelsize=fs)

    ax.set_xlim(limits['x'])
    ax.set_ylim(limits['y'])

    cbar_ax = g.fig.add_axes(cbar_rect)
    cbar = plt.colorbar(cax=cbar_ax)

    plt.tight_layout()

    if output_folder:
        figname = f"latent_dims_{latent_dim_x}_vs_{latent_dim_y}.png"
        path = os.path.join(output_folder, figname)
        plt.savefig(path, dpi=dpi)
        print(f"Figure saved at {path}.")

    if show:
        plt.show()


def visualize_att(
    sources_coord_att,
    targets_coord_att,
    parties_coord_att,
    targets_parties,
    dims,
    palette,
    nudges,
    limits,
    cbar_rect,
    legend_loc,
    path=None,
    show=False,
    **kwargs
):

    plot_df = pd.concat([sources_coord_att, targets_coord_att]) \
        .reset_index() \
        .drop(columns="index")

    l0 = len(plot_df)
    plot_df = plot_df.drop_duplicates()
    l1 = len(plot_df)
    if (l0 > l1):
        print(f"Dropped {l1 -l0} repeated embeddings points.")

    # setting lims
    pad = 0.35
    dx = plot_df[dims['x']].max()-plot_df[dims['x']].min()
    dy = plot_df[dims['y']].max()-plot_df[dims['y']].min()
    xlims = (plot_df[dims['x']].min()-pad*dx, plot_df[dims['x']].max()+pad*dx)
    ylims = (plot_df[dims['y']].min()-pad*dy, plot_df[dims['y']].max()+pad*dy)

    # This turned out to be 6x6 figsize
    kwargs = {
        'x': dims['x'],
        'y': dims['y'],
        'space': 0,
        'ratio': 10,
        'height': 5,
        'color': "deepskyblue",
        'kind': 'hex',
        'data': plot_df,
    }

    # plot sources and targets embeddings
    g = sns.jointplot(**kwargs)

    # get unique parties and build color dictionary
    unique_parties = targets_coord_att.party.unique().tolist()
    nunique_parties = targets_coord_att.party.nunique()


    # plot colored by parties targets attitudinal embeddings
    ax = g.ax_joint
    texts = []
    for party in unique_parties:

        # plot colored by parties target embeddings
        sample = targets_coord_att[targets_coord_att.party == party]

        ax.scatter(
            sample[dims['x']],
            sample[dims['y']],
            marker='+',
            s=20,
            alpha=0.5,
            color=palette[party],
            label=party
        )

        # plot parties attitudinal coordinates
        group_positions = parties_coord_att[parties_coord_att.party == party]
        if len(group_positions) > 1:
            raise ValueError("Bizarre")
        if len(group_positions) == 1:
            ax.plot(
                group_positions.iloc[0][dims['x']],
                group_positions.iloc[0][dims['y']],
                marker='o',
                markeredgecolor='black',
                markeredgewidth=1.0,
                markersize=5,
                color=palette[party],
        )

        text = ax.text(
            group_positions.iloc[0][dims['x']]+nudges[party][0],
            group_positions.iloc[0][dims['y']]+nudges[party][1],
            party,
            color='white',
            bbox=dict(
                boxstyle="round",
                ec='black',
                fc=palette[party],
                alpha=1),
            fontsize=9)
        texts.append(text)

    adjust_text(texts)

    # the next lines plot the [0, 10]^2 square showing CHES limits
    ax.plot([0, 10, 10, 0, 0], [0, 0, 10, 10, 0], color='white', linestyle='-')
    ax.plot([0, 10, 10, 0, 0], [0, 0, 10, 10, 0], color='black', linestyle='--')
    txt = ax.text(2, 10.25, 'CHES survey bounds', fontsize=12)
    txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='w')])

    xl = f"CHES {ATT_DICT[dims['x']]}"
    yl = f"CHES {ATT_DICT[dims['y']]}"
    ax.set_xlabel(xl, fontsize=fs)
    ax.set_ylabel(yl, fontsize=fs)

    ax.legend(handles=custom_legend, loc=legend_loc, fontsize=fs-2, framealpha=0.98)

    ax.tick_params(axis='x', labelsize=fs)
    ax.tick_params(axis='x', labelsize=fs)

    ax.set_xlim(limits['x'])
    ax.set_ylim(limits['y'])

    cbar_ax = g.fig.add_axes(cbar_rect)
    cbar = plt.colorbar(cax=cbar_ax)

    plt.tight_layout()

    if path:
        plt.savefig(path, dpi=dpi)
        print(f"Figure saved at {path}.")

    if show:
        plt.show()
