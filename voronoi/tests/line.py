from voronoi import Point
from voronoi.graph.bounding_circle import BoundingCircle


bc = BoundingCircle(5,6,12)

p1 = Point(1,2)
p2 = Point(7.5, 21.4)
a = bc.get_line(p1, p2)
print(a)

p1 = Point(1,2)
p2 = Point(7.5, 2)
a = bc.get_line(p1, p2)
print(a)

p1 = Point(1,2)
p2 = Point(1, 11.2)
a = bc.get_line(p1, p2)
print(a)



pass
