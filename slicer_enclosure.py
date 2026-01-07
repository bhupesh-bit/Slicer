from shapely.ops import unary_union
import trimesh


def classify_enclosure(path_2d, area_threshold=0.1):
    raw_polygons = path_2d.polygons_closed
    if raw_polygons is None:
        return []

    graph = path_2d.enclosure_directed
    roots = path_2d.root

    solids = []
    holes = []

    for i, poly in enumerate(raw_polygons):
        if poly.area < area_threshold:
            continue

        if not poly.is_valid:
            poly = poly.buffer(0)

        level = 0
        try:
            for root in roots:
                if i == root:
                    level = 0
                    break
                if trimesh.graph.nx.has_path(graph, root, i):
                    path = trimesh.graph.nx.shortest_path(graph, root, i)
                    level = len(path) - 1
                    break
        except:
            level = 0

        if level % 2 == 0:
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

    if geometry.geom_type == "Polygon":
        geoms = [geometry]
    else:
        geoms = list(geometry.geoms)

    for poly in geoms:
        results.append({
            "outer": list(poly.exterior.coords),
            "holes": [list(h.coords) for h in poly.interiors]
        })

    return results
