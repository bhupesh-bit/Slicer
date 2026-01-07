import os
import matplotlib.pyplot as plt

from common import load_mesh, generate_z_levels, slice_at_z
from slicer_parity import classify_parity
from slicer_winding import classify_winding
from slicer_enclosure import classify_enclosure

METHOD = "parity"   # options: "parity", "winding", "enclosure"
MODEL_NAME = "cluster.stl"   # or "carburetor.stl"
LAYER_HEIGHT = 0.5
AREA_THRESHOLD = 0.5
OUTPUT_DIR = "winding_cluster_output"
def plot_outer(islands, path):
    fig, ax = plt.subplots(figsize=(6, 6))
    for island in islands:
        ox, oy = zip(*island["outer"])
        ax.plot(ox, oy, color="green", linewidth=2)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.savefig(path, bbox_inches="tight")
    plt.close()


def plot_holes(islands, path):
    fig, ax = plt.subplots(figsize=(6, 6))
    for island in islands:
        for hole in island["holes"]:
            hx, hy = zip(*hole)
            ax.plot(hx, hy, color="red", linewidth=2)
            ax.fill(hx, hy, color="red", alpha=0.3)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.savefig(path, bbox_inches="tight")
    plt.close()


def main():
    mesh_path = os.path.join("models", MODEL_NAME)
    mesh = load_mesh(mesh_path)
    z_levels = generate_z_levels(mesh, LAYER_HEIGHT)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"Using method: {METHOD}")
    print(f"Slicing {len(z_levels)} layers")

    for z in z_levels:
        section_2d = slice_at_z(mesh, z)
        if section_2d is None:
            continue

        if METHOD == "parity":
            islands = classify_parity(section_2d, AREA_THRESHOLD)
        elif METHOD == "winding":
            islands = classify_winding(section_2d, AREA_THRESHOLD)
        elif METHOD == "enclosure":
            islands = classify_enclosure(section_2d, AREA_THRESHOLD)
        else:
            raise ValueError("Invalid METHOD selected.")

        if not islands:
            continue

        layer_folder = os.path.join(OUTPUT_DIR, f"{z:.2f}")
        os.makedirs(layer_folder, exist_ok=True)

        plot_outer(islands, os.path.join(layer_folder, "outer.png"))
        plot_holes(islands, os.path.join(layer_folder, "holes.png"))

        print(f"Z={z:.2f}")

    print("Finished")


if __name__ == "__main__":
    main()
