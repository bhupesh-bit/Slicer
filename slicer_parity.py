import numpy as np
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union


def classify_parity(path_2d, area_threshold=0.1):
    """
    Region classification using parity (even–odd rule)
    Returns list of islands:
    [
        {
            "outer": [(x,y), ...],
            "holes": [[(x,y), ...], ...]
        },
        ...
    ]
    """

    raw_paths = path_2d.discrete
    if raw_paths is None:
        return []

    polygons = []

    # Convert loops to shapely polygons
    for loop in raw_paths:
        if len(loop) < 3:
            continue

        if not np.allclose(loop[0], loop[-1]):
            loop = np.vstack([loop, loop[0]])

        poly = Polygon(loop)
        if not poly.is_valid:
            poly = poly.buffer(0)

        if poly.is_empty or poly.area < area_threshold:
            continue

        polygons.append(poly)

    if not polygons:
        return []

    # Parity classification
    filled = []

    for poly in polygons:
        p = poly.representative_point()
        count = 0
        for other in polygons:
            if other.contains(p):
                count += 1

        if count % 2 == 1:
            filled.append(poly)

    if not filled:
        return []

    final_geom = unary_union(filled)
    final_geom = final_geom.buffer(0)

    results = []

    if isinstance(final_geom, Polygon):
        geoms = [final_geom]
    elif isinstance(final_geom, MultiPolygon):
        geoms = list(final_geom.geoms)
    else:
        return []

    for poly in geoms:
        outer = list(poly.exterior.coords)

        holes = []
        for interior in poly.interiors:
            holes.append(list(interior.coords))

        results.append({
            "outer": outer,
            "holes": holes
        })

    return results
