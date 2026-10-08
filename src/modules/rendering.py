# rendering.py

import matplotlib.pyplot as plt
import numpy as np


def animate(memory):

    floors = memory[0].shape[0]

    for t, state in enumerate(memory):

        fig, axs = plt.subplots(
            floors // 3,
            3,
            constrained_layout=True
        )

        for z in range(floors):

            ax = axs[z // 3, z % 3]

            im = ax.pcolormesh(
                np.flipud(state[z]),
                cmap="jet",
                vmin=-1.5,
                vmax=1.5
            )

            ax.set_title(f"Floor {z}")
            ax.set_aspect("equal")

        fig.suptitle(f"Time {t}")

        plt.colorbar(im, ax=axs.ravel().tolist())

        plt.show()