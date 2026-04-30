# https://city2graphy.net/index.html
!pip install city2graph
!pip install osmnx
!pip install geopandas
!pip install matplotlib
!pip install contextily
!pip install shapely

import osmnx as ox
import city2graph
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from matplotlib.lines import Line2D
from shapely.geometry import box

city2graph.__version__


city_name = "Budapest"
admin = ox.geocode_to_gdf(city_name)
admin.plot()

poi_gdf = ox.features_from_place(city_name,{"leisure":["gym","sports_centre"]}).to_crs(3857)
poi_gdf ["geometry"] = poi_gdf.geometry.centroid
poi_gdf = poi_gdf.dropna(subset=["geometry"]).reset_index(drop=True)
poi_gdf.head()

# start using and exploring the city
dir(city2graph)

#waxman graph = take the poi as an input and using various underlying logics and networks.
#network concepts will reconstruct the graph of these POIs

#a function to plot a single connectivity graph
def plot_pub_graph(edges_gdf, nodes_gdf, admin_gdf, title, color="#00FFFF", alpha=0.5, linewidth=0.75):

  fig, ax = plt.subplots(figsize=(5,5))

  admin_gdf.to_crs(epsg=3857).boundary.plot(ax=ax, alpha=0.1, color="white",linewidth=1.0)
  edges_gdf.plot(ax=ax, color=color, alpha=alpha, linewidth=linewidth)

  ctx.add_basemap(ax, source=ctx.providers.CartoDB.DarkMatter)

  ax.set_axis_off()
  ax.set_title(title, fontsize=14, color="white", pad=12)
  plt.tight_layout()
  plt.show()

#define the radius 1000m
radius = 2500
#fixed radius proximity graph
fixed_nodes, fixed_edges = city2graph.fixed_radius_graph(poi_gdf, radius=radius) #this graph will connect all the pups that lie within a fixed uclidean distance of 1000m from eachother, its a simple geometry thresholding based on networks
##and easy way to capture clusters and studying various local densities, but it's not based on actual walkable distance, so its better to used in agricultural case where we dont know the exact roads

plot_pub_graph(fixed_edges, poi_gdf, admin, "Fixed-radius Graph", color="#00FFFF")

wax_l1_nodes, wax_l1_edges = city2graph.waxman_graph(
    poi_gdf,
    distance_metric="manhattan",
    r0=radius,
    beta=0.5
)

plot_pub_graph(wax_l1_edges, poi_gdf, admin, "Waxman (Manhattan Distance)", color="#FF6EFF")

#waxman but the euclidean matrix
wac_l2_nodes, wax_l2_edges = city2graph.waxman_graph(
    poi_gdf,
    distance_metric="euclidean",
    r0=radius,
    beta=0.5
)

plot_pub_graph(wax_l2_edges, poi_gdf, admin, "Waxman (Euclidean Distance)", color="#00FF9F")

##real street network
segments_gdf = ox.graph_to_gdfs(ox.graph_from_place(city_name, network_type="drive"))[1].to_crs(3857)
segments_gdf = segments_gdf.to_crs(3857)
len(segments_gdf)

wax_net_nodes, wax_net_edges = city2graph.waxman_graph(
    poi_gdf,
    distance_metric="network",
    r0=radius,
    beta=0.5,
    network_gdf=segments_gdf
)

plot_pub_graph(wax_net_edges, poi_gdf, admin, "Waxman (Network Distance)", color="#FFA500")

from networkx.algorithms.bipartite.basic import color
## reaching essential services

city_name = "budapest"
admin = ox.geocode_to_gdf(city_name).to_crs(3857)
sg = ox.graph_from_place(city_name, network_type="drive")
segments_gdf = ox.graph_to_gdfs(sg)[1].to_crs(3857)

poi_queries = {
    "active_life": {"leisure":["gym", "sports_centre"]},
    "daily_needs": {"shop":["supermarket","convenience"]},
    "social_life": {"amenity":["restaurant"]},
    "health_services": {"amenity":["clinic","hospital", "pharmacy"]}
}

poi_layers = {}
for label, query in poi_queries.items():
  poi = ox.features_from_place(city_name,query).to_crs(3857)
  # Convert all geometries to their centroids
  poi["geometry"] = poi.geometry.centroid
  # Drop any rows where centroid conversion might have failed (resulting in NaN geometry)
  poi = poi.dropna(subset=["geometry"]).reset_index(drop=True)
  # Now filter for 'Point' geometry type explicitly (with capital 'P')
  poi_layers[label] = poi[poi.geometry.type == "Point"]
  print(label, len(poi))


##wax graph for every single category
wax_graphs = {}
radius = 1000
for label, gdf in poi_layers.items():
  if len (gdf) > 1 :
    nodes, edges = city2graph.waxman_graph(
        gdf,
        distance_metric="network",
        r0=radius,
        beta=0.5,
        network_gdf=segments_gdf
    )
    wax_graphs[label]=edges

len(wax_graphs)
4

layer_colors = {
    "active_life": "#00e5ff", #neon
    "daily_needs": "#ffea00", #bright yellow
    "social_life": "#ff4081", #neon pink
    "health_services": "#76ff03" #lime green
}

fig, ax = plt.subplots(figsize=(10,10))

admin.to_crs(3857).boundary.plot(ax=ax, color="white", linewidth=0.8, zorder=5)

# Removed crs=3875 as it was causing the InvalidLatitudeError
ctx.add_basemap(ax, source=ctx.providers.CartoDB.DarkMatter, zoom=12)

# Corrected wax-graphs to wax_graphs and linewidht to linewidth
for label, edges in wax_graphs.items():
  for _, row in edges.iterrows():
    x, y = row.geometry.xy
    ax.plot(x, y, color=layer_colors[label], linewidth=0.6, alpha=0.3, label=label, zorder=6)

for label, pois in poi_layers.items():
  pois.to_crs(3857).plot(ax=ax, markersize=5, color=layer_colors[label], alpha=0.8, zorder=7)


ax.set_title(
    "waxman (Network Distance) - Daily Life Connectivity in Budapest",
    fontsize=14,
    color="white",
    pad=12
)


ax.set_axis_off()
plt.tight_layout()
plt.show()