import numpy as np
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union


def signed_area(coords):
    x = coords[:, 0]
    y = coords[:, 1]
    return 0.5 * np.sum(x[:-1] * y[1:] - x[1:] * y[:-1])


def classify_winding(path_2d, area_threshold=0.1):
    raw_paths = path_2d.discrete
    if raw_paths is None:
        return []

    solids = []
    holes = []

    for loop in raw_paths:
        if len(loop) < 3:
            continue

        if not np.allclose(loop[0], loop[-1]):
            loop = np.vstack([loop, loop[0]])

        area = signed_area(loop)
        if abs(area) < area_threshold:
            continue

        poly = Polygon(loop)
        if not poly.is_valid:
            poly = poly.buffer(0)

        if area > 0:
            solids.append(poly)
        else:
            holes.append(poly)

    if not solids:
        return []

    solid_union = unary_union(solids)
    hole_union = unary_union(holes) if holes else None

    if hole_union:
        final_geom = solid_union.difference(hole_union)
    else:
        final_geom = solid_union

    return extract_islands(final_geom)


def extract_islands(geometry):
    results = []

    if isinstance(geometry, Polygon):
        geoms = [geometry]
    elif isinstance(geometry, MultiPolygon):
        geoms = list(geometry.geoms)
    else:
        return []

    for poly in geoms:
        results.append({
            "outer": list(poly.exterior.coords),
            "holes": [list(h.coords) for h in poly.interiors]
        })

    return results
