import matplotlib.pyplot as plt
import contextily as ctx
import folium
from folium.plugins import MarkerCluster
import networkx as nx
import geopandas as gpd

def plot_graph_and_path(G, tsp_path, positions, nodes, total_cost, p, map=True, name = None):

    """ A function to plot the graph and the path, overlayed on a map (optional). """
    
    priority_names = ['time', 'distance', 'cost']
    priority_units = ['hours', 'km', 'local currency']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

    # --- Shared preparation ---
    node_coords = [(lon, lat) for _, (lat, lon) in positions.items()]
    if map:
        gdf_nodes = gpd.GeoDataFrame(geometry=gpd.points_from_xy(*zip(*node_coords)), crs='EPSG:4326')
        gdf_nodes = gdf_nodes.to_crs(epsg=3857)
        projected_positions = {
            node: (point.x, point.y)
            for node, point in zip(positions.keys(), gdf_nodes.geometry)
        }
        pos = projected_positions
    else:
        pos = {n: (lon, lat) for n, (lat, lon) in positions.items()}

    # --- Graph View (Left Plot) ---
    labels = {i: nodes[i] for i in G.nodes()}
    node_colors = ['skyblue' for _ in G.nodes()]

    nx.draw(G, pos=pos, ax=ax1, node_color=node_colors, node_size=800, edge_color='grey', with_labels=False)
    nx.draw_networkx_labels(G, pos=pos, labels=labels, ax=ax1, font_size=12)
    
    if not map:
        edge_labels = {(u, v): f"{d['weight']:.1f}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels, ax=ax1)

    ax1.set_title("Full Graph")
    ax1.axis("off")
    if map:
        ctx.add_basemap(ax1, source=ctx.providers.OpenStreetMap.Mapnik)

    # --- TSP Path View (Right Plot) ---
    if len(tsp_path) == len(G.nodes()):
        ordered_labels = {node: f"{i}" for i, node in enumerate(tsp_path)}
    else:
        ordered_labels = {node: f"{i}" for i, node in enumerate(tsp_path[:-1])}

    tsp_edges = list(zip(tsp_path[:-1], tsp_path[1:]))
    start_node = tsp_path[0]
    node_colors = ['red' if node == start_node else 'skyblue' for node in G.nodes()]

    nx.draw(G, pos=pos, ax=ax2, node_color=node_colors, node_size=800, edge_color='lightgray', with_labels=False)
    nx.draw_networkx_labels(G, pos=pos, labels=ordered_labels, ax=ax2, font_size=14, font_weight='bold')
    nx.draw_networkx_edges(G, pos=pos, edgelist=tsp_edges, edge_color='red', width=3, ax=ax2)

    if map:
        ctx.add_basemap(ax2, source=ctx.providers.OpenStreetMap.Mapnik)

    # Legend (right)
    label_mapping_legend = [f"{label}: {nodes[node]}" for node, label in ordered_labels.items()]
    legend_text = "\n".join(label_mapping_legend)
    props = dict(boxstyle='round', facecolor='white', alpha=0.8)
    ax2.text(1.02, 0.5, legend_text, transform=ax2.transAxes, fontsize=12,
             verticalalignment='center', bbox=props)

    if isinstance(total_cost, float):
        ax2.set_title(f"TSP Path Total {priority_names[p]}: {total_cost:.2f} {priority_units[p]}")
    ax2.axis("off")

    plt.tight_layout()
    plt.show()

    if name:
        fig.savefig(name)
    return 


def plot_route_folium(tsp_path, positions, nodes, total_cost, p = 0):
    priority_names = ['time', 'distance', 'cost']
    priority_units = ['hours', 'km', 'local currency']

    # Route coordinates for the full path
    route_coords = [positions[node] for node in tsp_path]

    # Center map on the first location
    start_lat, start_lon = route_coords[0]
    m = folium.Map(location=[start_lat, start_lon], zoom_start=6)

    # Add numbered markers: red for start, blue for all others
    for i, node in enumerate(tsp_path):
        lat, lon = positions[node]
        label = f"{i}: {nodes[node]}"
        icon_color = "red" if i == 0 else "blue"

        folium.Marker(
            location=[lat, lon],
            popup=label,
            tooltip=label,
            icon=folium.Icon(color=icon_color)
        ).add_to(m)

    # Draw the full route path
    folium.PolyLine(
        locations=route_coords,
        color="red",
        weight=5,
        opacity=0.8
    ).add_to(m)

    # Add floating total cost box
    if not isinstance(total_cost, list):
        title_html = f"""
            <h4 style="position:fixed;top:10px;left:10px;z-index:9999;
            background:white;padding:10px;border-radius:8px;box-shadow:2px 2px 10px rgba(0,0,0,0.1);">
            Total {priority_names[p]}: {total_cost:.2f} {priority_units[p]}
            </h4>
        """
        m.get_root().html.add_child(folium.Element(title_html))
    
    else: 
        title_html = f"""
        <h4 style="position:fixed;top:10px;left:10px;z-index:9999;
        background:white;padding:10px;border-radius:8px;box-shadow:2px 2px 10px rgba(0,0,0,0.1);">
        Time: {total_cost[0]:.2f} {priority_units[p]}, 
        Distance: {total_cost[1]:.2f} km, 
        Cost: {total_cost[2]:.2f} local_currency
        </h4>
        """
        m.get_root().html.add_child(folium.Element(title_html))
    return m
