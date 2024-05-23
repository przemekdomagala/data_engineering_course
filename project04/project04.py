# %% [markdown]
# # Loading Data

# %%
import json

with open("proj4_params.json") as f:
    data = json.load(f)

# %% [markdown]
# # Exercise 1

# %%
import geopandas as gpd

with open("proj4_points.geojson") as geofile:
    data1 = gpd.read_file(geofile)

# %%
data1_new_crs = data1.to_crs(epsg=2180)
buffer1 = data1_new_crs.geometry.buffer(100)
joined1 = gpd.sjoin(data1_new_crs, gpd.GeoDataFrame(geometry=buffer1))
count_lamps_within_distance = joined1.groupby('index_right').size()
data1_with_count = data1_new_crs.join(count_lamps_within_distance.rename('count'))
data1_with_count[["lamp_id", "count"]].to_csv('proj4_ex01_counts.csv', index=False)

# %% [markdown]
# # Exercise 1b

# %%
data1b = data1.to_crs(epsg=4326)
lst_x = []
lst_y = []

for i in data1b["geometry"]:
    lst_x.append(int(i.x*10000000)/10000000)
    lst_y.append(int(i.y*10000000)/10000000)

data1b["lat"] = lst_y
data1b["lon"] = lst_x
data1b[["lamp_id", "lat", "lon"]].to_csv("proj4_ex01_coords.csv", index=False)

# %% [markdown]
# # Exercise 2

# %%
from pyrosm import get_data
from pyrosm import OSM
from shapely.ops import linemerge

data2 = get_data(data["city"])
osm = OSM(data2)
drive_net = osm.get_network(network_type="driving")
drive_net = drive_net[drive_net.highway == "tertiary"]
drive_net["geometry"] = drive_net["geometry"].apply(lambda x: linemerge(x) if x.geom_type == "MultiLineString" else x)
drive_net["osm_id"] = drive_net["id"]
drive_net[["osm_id", "name", "geometry"]].to_file("proj4_ex02_roads.geojson", driver="GeoJSON")

# %% [markdown]
# # Exercise 3

# %%
data2 = drive_net[["osm_id", "name", "geometry"]]
data3 = data2.to_crs(epsg=2180)
buffer3 = data3.geometry.buffer(distance=50, cap_style=2)
joined3 = gpd.sjoin(data1_new_crs, gpd.GeoDataFrame(geometry=buffer3))
lamps_within_distance = joined3.groupby('index_right').size()
data3_with_count = data3.join(lamps_within_distance.rename('point_count'))
data3_final = data3_with_count.dropna(subset=["point_count"])
summed_data3 = data3_final.groupby('name')['point_count'].sum().reset_index()
summed_data3[["point_count"]] = summed_data3[["point_count"]].astype('int64')
summed_data3.to_csv("proj4_ex03_streets_points.csv", index=False)

# %% [markdown]
# # Exercise 4

# %%
with open("proj4_countries.geojson") as geofile:
    data4 = gpd.read_file(geofile)

data4["geometry"] = data4["geometry"].boundary
data4 = data4.to_crs("+proj=cea")
data4.to_pickle("proj4_ex04_gdf.pkl")

# %%
import contextily as cx
import matplotlib.pyplot as plt

for i in range(len(data4)):
    ax = data4[data4["name"]==data4.loc[i, "name"]].plot()
    cx.add_basemap(ax, crs=data4.crs, source=cx.providers.OpenStreetMap.Mapnik)
    name = str(data4.loc[i, "name"]).lower()
    file_ = "proj4_ex04_"+name+".png"
    plt.savefig(file_, dpi=300)


