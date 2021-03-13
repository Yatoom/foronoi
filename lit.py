import streamlit as st
import numpy as np
import pandas as pd
from graphviz import Digraph

from voronoi import Voronoi, Polygon
from voronoi.beta.debug_observer import DebugObserver
from voronoi.beta.tree_observer import TreeObserver
from voronoi.beta.voronoi_observer import VoronoiObserver

points = [
    (2.5, 2.5),
    (4, 7.5),
    (7.5, 2.5),
    (6, 7.5),
    (4, 4),
    (3, 3),
    (6, 3),
]

# Define a bounding box
polygon = Polygon([
    (2.5, 10),
    (5, 10),
    (10, 5),
    (10, 2.5),
    (5, 0),
    (2.5, 0),
    (0, 2.5),
    (0, 5),
])

st.write("hello world")

def callback(visualization):
    st.pyplot(visualization)

# Initialize the algorithm
v = Voronoi(polygon)
v.attach(VoronoiObserver(visualize_result=True, visualize_before_clipping=True, visualize_steps=True, callback=callback))
v.attach(DebugObserver())
v.attach(TreeObserver())
v.create_diagram(
    points=points,
)
