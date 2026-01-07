import numpy as np
import trimesh


def load_mesh(mesh_path):
    return trimesh.load(mesh_path)


def get_bounding_box(mesh):
    return mesh.bounds[0], mesh.bounds[1]


def generate_z_levels(mesh, layer_height):
    z_min, z_max = mesh.bounds[:, 2]
    eps = 1e-6
    return np.arange(z_min, z_max + eps, layer_height)


def slice_at_z(mesh, z):
    section_3d = mesh.section(
        plane_origin=[0, 0, z],
        plane_normal=[0, 0, 1]
    )

    if section_3d is None:
        return None

    section_2d, _ = section_3d.to_2D()
    return section_2d
