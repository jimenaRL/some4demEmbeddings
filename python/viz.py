import os
from datetime import date

import seaborn as sns
import matplotlib.pyplot as plt


def viz2dEmb(
    sources_coord_ide,
    targets_coord_ide,
    sources_coord_att,
    targets_coord_att,
    groups_coord_att,
    dimensions,
    palette,
    output_folder,
    ide_path,
    att_path
):

    os.makedirs(output_folder, exist_ok=True)

    # visualize ideological embedding
    visualize_ide(
        sources_coord_ide,
        targets_coord_ide,
        palette,
        os.path.join(output_folder, ide_path)
    )

    # Visualize attitudinal embedding
    visualize_att(
        sources_coord_att,
        targets_coord_att,
        groups_coord_att,
        dict(zip(['x', 'y'], dimensions)),
        palette,
        os.path.join(output_folder, att_path)
    )


def visualize_ide(
    sources_coord_ide,
    targets_coord_ide,
    palette=None,
    path=None
):

    # plot sources embeddings
    g = sns.jointplot(
        data=sources_coord_ide.drop_duplicates(),
        x='latent_dimension_0',
        y='latent_dimension_1',
        kind="hex",
        height=8
    )

    # get unique groups and build color dictionary
    unique_groups = targets_coord_ide.group.unique().tolist()
    nunique_groups = targets_coord_ide.group.nunique()
    if palette is None:
        unique_groups.sort()
        palette = dict(zip(
            unique_groups,
            sns.color_palette("viridis", nunique_groups)
            )
        )

    # plot colored by groups target embeddings
    ax = g.ax_joint
    for p in unique_groups:
        sample = targets_coord_ide[targets_coord_ide.group == p] \
            .drop_duplicates()
        ax.scatter(
            sample['latent_dimension_0'],
            sample['latent_dimension_1'],
            marker='+',
            s=30,
            alpha=0.75,
            color=palette[p],
            label=p
        )
    plt.legend(loc='best', title='PARTY')

    if path:
        plt.savefig(path, dpi=150)
        print(f"Figure saved at {path}.")


def visualize_att(
    sources_coord_att,
    targets_coord_att,
    groups_coord_att,
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
    unique_groups = targets_coord_att.group.unique().tolist()
    nunique_groups = targets_coord_att.group.nunique()
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
        sample = targets_coord_att[targets_coord_att.group == p] \
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
        group_positions = groups_coord_att[groups_coord_att.group == p]
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
