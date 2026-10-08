from io import BytesIO
import tkinter as tk

from matplotlib import cm
import numpy as np
from PIL import Image, ImageDraw, ImageTk


def _create_gif(memory):
    floors = memory[0].shape[0]
    columns = min(floors, 3)
    rows = (floors + columns - 1) // columns
    cell_size = max(1, min(5, 360 // max(memory.shape[2:])))
    margin = 12
    title_height = 34
    floor_title_height = 22
    floor_width = memory.shape[3] * cell_size
    floor_height = memory.shape[2] * cell_size
    width = margin + columns * (floor_width + margin)
    height = title_height + margin + rows * (
        floor_height + floor_title_height + margin
    )
    colormap = cm.get_cmap("jet")
    colors = (colormap(np.linspace(0, 1, 254))[:, :3] * 255).astype(np.uint8)
    palette = [0, 0, 0, 255, 255, 255] + colors.ravel().tolist()

    def make_frame(t):
        frame = Image.new("P", (width, height), 1)
        frame.putpalette(palette)
        draw = ImageDraw.Draw(frame)
        draw.text((margin, 8), f"Time {t}", fill=0)

        for z in range(floors):
            row, column = divmod(z, columns)
            x = margin + column * (floor_width + margin)
            y = title_height + margin + row * (
                floor_height + floor_title_height + margin
            )
            draw.text((x, y), f"Floor {z}", fill="black")

            values = np.flipud(memory[t, z])
            normalized = np.clip((values + 1.5) / 3, 0, 1)
            indices = 2 + np.rint(normalized * 253).astype(np.uint8)
            floor_image = Image.frombytes(
                "P", (values.shape[1], values.shape[0]), indices.tobytes()
            )
            floor_image.putpalette(palette)
            floor_image = floor_image.resize(
                (floor_width, floor_height),
                resample=Image.Resampling.NEAREST,
            )
            frame.paste(floor_image, (x, y + floor_title_height))

        return frame

    gif = BytesIO()
    first_frame = make_frame(0)
    first_frame.save(
        gif,
        format="GIF",
        save_all=True,
        append_images=(make_frame(t) for t in range(1, len(memory))),
        duration=100,
        loop=0,
    )
    gif.seek(0)
    return gif


def animate(memory):
    gif = Image.open(_create_gif(memory))
    window = tk.Tk()
    window.title("Building Fire Propagation")
    label = tk.Label(window)
    label.pack()

    def show_frame(index=0):
        gif.seek(index)
        frame = ImageTk.PhotoImage(gif.copy())
        label.configure(image=frame)
        label.image = frame
        window.after(
            gif.info.get("duration", 100),
            show_frame,
            (index + 1) % gif.n_frames,
        )

    show_frame()
    window.mainloop()
