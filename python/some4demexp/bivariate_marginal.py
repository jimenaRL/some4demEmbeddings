import os
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patheffects as PathEffects
from adjustText import adjust_text

mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['mathtext.rm'] = 'serif'
mpl.rcParams['text.latex.preamble'] = r"\usepackage{amsmath}"
plt.rc('text', usetex=True)
plt.rc('font', family='sans-serif', size=12)
mpl.rcParams['mathtext.fontset'] = 'custom'
mpl.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
mpl.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
mpl.rcParams['mathtext.bf'] = 'Bitstream Vera Sans:bold'
mpl.rcParams.update(mpl.rcParamsDefault)

fs = 12

legend_mps = Line2D(
    [0],
    [0],
    color='black',
    marker='+',
    lw=0,
    alpha=1.0,
    label='MPs'
)
legend_parties = Line2D(
    [0],
    [0],
    color='gray',
    marker='o',
    mec='k',
    lw=0,
    alpha=1,
    label='Parties'
)
legend_followers = Line2D(
    [0],
    [0],
    color='deepskyblue',
    marker='s',
    alpha=0.8,
    linestyle='None',
    label='Followers'
)
custom_legend = [legend_mps, legend_parties, legend_followers]


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
    targets_groups,
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
    targets_groups = targets_groups.rename(columns=colrename)

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

    # plot sources and targets embeddings
    g = sns.jointplot(**kwargs)

    # get unique groups and build color dictionary
    unique_groups = targets_groups.party.unique().tolist()
    nunique_groups = len(set(unique_groups))

    if palette is None:
        unique_groups.sort()
        palette = dict(zip(
            unique_groups,
            sns.color_palette("viridis", nunique_groups)
            )
        )

    targets_coord_ide = targets_coord_ide.merge(
            targets_groups,
            left_on="entity",
            right_on="mp_pseudo_id",
            how="inner"
        ) \
        .drop(columns="mp_pseudo_id")

    # plot colored by groups target embeddings
    ax = g.ax_joint
    texts = []
    for party in unique_groups:

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

        # plot estimated groups mean
        mean_group_estimated = sample[['x', 'y']].mean()
        ax.plot(
            mean_group_estimated['x'],
            mean_group_estimated['y'],
            marker='o',
            mec='k',
            mew=1.0,
            ms=5,
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

    ax.legend(handles=custom_legend, loc=legend_loc, fontsize=fs-2)
    ax.tick_params(axis='x', labelsize=fs)
    ax.tick_params(axis='x', labelsize=fs)

    ax.set_xlim(limits['x'])
    ax.set_ylim(limits['y'])

    cbar_ax = g.fig.add_axes(cbar_rect)
    plt.colorbar(cax=cbar_ax)

    plt.tight_layout()

    if output_folder:
        figname = f"latent_dims_{latent_dim_x}_vs_{latent_dim_y}.png"
        path = os.path.join(output_folder, figname)
        plt.savefig(path, dpi=300)
        print(f"Figure saved at {path}.")

    if show:
        plt.show()


def visualize_att(
    sources_coord_att,
    targets_coord_att,
    groups_coord_att,
    targets_groups,
    dims,
    palette=None,
    path=None
):

    # plot sources embeddings
    g = sns.jointplot(
        data=sources_coord_att,
        x=dims['x'],
        y=dims['y'],
        kind="hex",
        height=8
    )

    # get unique groups and build color dictionary
    unique_groups = targets_coord_att.party.unique().tolist()
    nunique_groups = targets_coord_att.party.nunique()
    if palette is None:
        unique_groups.sort()
        palette = dict(zip(
            unique_groups,
            sns.color_palette("viridis", nunique_groups)
            )
        )

    ax = g.ax_joint

    # plot groups target

    for p in unique_groups:

        # plot colored by groups target embeddings
        sample = targets_coord_att[targets_coord_att.party == p] \
            .drop_duplicates()

        ax.scatter(
            sample[dims['x']],
            sample[dims['y']],
            marker='+',
            s=30,
            alpha=0.75,
            color=palette[p]
        )

        # plot estimated groups mean
        mean_group_estimated = sample[[dims['x'], dims['y']]].mean()
        ax.plot(
            mean_group_estimated[dims['x']],
            mean_group_estimated[dims['y']],
            marker='o',
            mec='k',
            color=palette[p],
            ms=7
        )

        # plot groups attitudinal_positions
        group_positions = groups_coord_att[groups_coord_att.party == p]
        if len(group_positions) > 1:
            raise ValueError("Bizarre")
        if len(group_positions) == 1:
            ax.plot(
                group_positions.iloc[0][dims['x']],
                group_positions.iloc[0][dims['y']],
                marker='^',
                mec='k',
                color=palette[p],
                ms=7,
                label=p
            )

        plt.legend(loc='best', title='PARTY')

    if path:
        plt.savefig(path, dpi=150)
        print(f"Figure saved at {path}.")
