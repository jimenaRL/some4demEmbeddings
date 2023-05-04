import os

import seaborn as sns

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patheffects as PathEffects

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


def visualize_ide(
    sources_coord_ide,
    targets_coord_ide,
    targets_groups,
    latent_dim_x=0,
    latent_dim_y=1,
    palette=None,
    output_folder=None
):

    # preprocessing
    colrename = {
        f'latent_dimension_{latent_dim_x}': 'x',
        f'latent_dimension_{latent_dim_y}': 'y'
    }
    sources_coord_ide = sources_coord_ide \
        .rename(columns=colrename) \
        .drop_duplicates()
    targets_coord_ide = targets_coord_ide \
        .rename(columns=colrename) \
        .drop_duplicates()

    targets_groups = targets_groups \
        .rename(columns=colrename) \
        .drop_duplicates()

    # plot sources embeddings
    g = sns.jointplot(
        data=sources_coord_ide.drop_duplicates(),
        x='x',
        y='y',
        kind="hex",
        height=8
    )

    # get unique groups and build color dictionary
    unique_groups = targets_groups.party_acronym.unique().tolist()
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
    for p in unique_groups:
        sample = targets_coord_ide[targets_coord_ide.party_acronym == p]

        ax.scatter(
            sample['x'],
            sample['y'],
            marker='+',
            s=30,
            alpha=0.75,
            color=palette[p],
            label=p
        )

        # plot estimated groups mean
        mean_group_estimated = sample[['x', 'y']].mean()
        ax.plot(
            mean_group_estimated['x'],
            mean_group_estimated['y'],
            marker='o',
            mec='k',
            color=palette[p],
            ms=7
        )

    plt.legend(loc='best', title='PARTY')

    ax.set_xlabel(
        fr'{latent_dim_x}th latent dimension $\delta_{latent_dim_x}$',
        fontsize=fs)
    ax.set_ylabel(
        fr'{latent_dim_y}th latent dimension $\delta_{latent_dim_y}$',
        fontsize=fs)

    ax.legend(handles=custom_legend, loc='lower right', fontsize=fs-2)
    ax.tick_params(axis='x', labelsize=fs)
    ax.tick_params(axis='x', labelsize=fs)

    # ax.set_aspect('equal')
    plt.tight_layout()

    if output_folder:
        figname = f"latent_dims_{latent_dim_x}_vs_{latent_dim_y}.png"
        path = os.path.join(output_folder, figname)
        plt.savefig(path, dpi=300)
        print(f"Figure saved at {path}.")


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
    unique_groups = targets_coord_att.party_acronym.unique().tolist()
    nunique_groups = targets_coord_att.party_acronym.nunique()
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
        sample = targets_coord_att[targets_coord_att.party_acronym == p] \
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
