from voronoi import Polygon, Voronoi

points = [(3.45, 3.66), (6.0, 4.54), (7.82, 5.35), (5.65, 3.09), (1.99, 4.66)]
The_grid = Polygon([
    (0, 0),
    (0, 6),
    (9, 0),
    (9, 6)
])
v = Voronoi(The_grid)
matplotlib = True
v.create_diagram(points=points, vis_steps=False, verbose=True, vis_before_clipping=matplotlib, vis_result=matplotlib, vis_tree=True)
points = v.points
print(points[2].get_coordinates())