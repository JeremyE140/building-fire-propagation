from io import BytesIO
import logging
import queue
import threading
import tkinter as tk

from matplotlib import colormaps
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageTk


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
    colormap = colormaps["jet"]
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
            draw.text((x, y), f"Floor {z}", fill=0)

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


def _fit_frame(frame, size):
    return ImageOps.contain(
        frame.convert("RGB"),
        size,
        method=Image.Resampling.LANCZOS,
    )


def animate(memory):
    window = tk.Tk()
    window.title("Building Fire Propagation")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    loading_width = 360
    loading_height = 100
    window.geometry(
        f"{loading_width}x{loading_height}+"
        f"{(screen_width - loading_width) // 2}+"
        f"{(screen_height - loading_height) // 2}"
    )
    window_width = int(window.winfo_screenwidth() * 0.9)
    window_height = int(window.winfo_screenheight() * 0.85)
    status = tk.Label(window, text="Préparation de l’animation…")
    status.pack(padx=20, pady=20)
    label = tk.Label(window)

    result = queue.Queue(maxsize=1)

    def prepare_gif():
        try:
            result.put(("ready", _create_gif(memory).getvalue()))
        except Exception as error:
            logging.exception("Could not generate the simulation GIF")
            result.put(("error", str(error)))

    def show_frame(gif, index=0):
        gif.seek(index)
        frame = ImageTk.PhotoImage(
            _fit_frame(
                gif.copy(),
                (max(1, label.winfo_width()), max(1, label.winfo_height())),
            )
        )
        label.configure(image=frame)
        label.image = frame
        window.after(
            gif.info.get("duration", 100),
            show_frame,
            gif,
            (index + 1) % gif.n_frames,
        )

    def check_ready():
        try:
            result_type, content = result.get_nowait()
        except queue.Empty:
            window.after(100, check_ready)
            return

        if result_type == "error":
            status.configure(text=f"Erreur lors de la préparation du GIF :\n{content}")
            return

        status.destroy()
        window.geometry(
            f"{window_width}x{window_height}+"
            f"{(screen_width - window_width) // 2}+"
            f"{(screen_height - window_height) // 2}"
        )
        label.pack(fill=tk.BOTH, expand=True)
        window.update_idletasks()
        show_frame(Image.open(BytesIO(content)))

    threading.Thread(target=prepare_gif, daemon=True).start()
    window.after(100, check_ready)
    window.mainloop()
