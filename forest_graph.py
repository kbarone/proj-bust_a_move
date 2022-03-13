#CHANGES



import geopandas

shp_file = geopandas.read_file('/Users/katybarone/Documents/uchicago/forest2.dbf')
shp_file.to_file('forest.geojson', driver='GeoJSON')

import shapefile
from json import dumps

pat = "/Users/katybarone/Documents/uchicago/forest.shp"
assert os.path.exists(pat), "Input file does not exist."
# read the shapefile
reader = shapefile.Reader("/Users/katybarone/Documents/uchicago/forest2.dbf")
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    geom = sr.shape.__geo_interface__
    buffer.append(dict(type="Feature", \
    geometry=geom, properties=atr)) 
   
    # write the GeoJSON file
   
geojson = open("forest.json", "w")
geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
geojson.close()

import json
from urllib.request import urlopen
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import math

forest = open("forest.json")
forest = json.load(forest)

fig = go.Figure(go.Choroplethmapbox(geojson=forest, locations=  
                                    colorscale="Jet", zmin=-17, zmax=58, 
                                    marker_opacity=0.5, marker_line_width=0))
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()