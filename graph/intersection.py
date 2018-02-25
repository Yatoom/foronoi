import numpy as np

from graph import Point


def magnitude(vector):
    return np.sqrt(np.dot(np.array(vector), np.array(vector)))


def norm(vector):
    return np.array(vector) / magnitude(np.array(vector))


def line_ray_intersection_point(ray_orig, ray_end, point_1, point_2):
    # Convert to numpy arrays
    orig = np.array(ray_orig, dtype=np.float)
    end = np.array(ray_end)
    direction = np.array(norm(end - orig), dtype=np.float)
    point_1 = np.array(point_1, dtype=np.float)
    point_2 = np.array(point_2, dtype=np.float)

    # Ray-Line Segment Intersection Test in 2D
    # http://bit.ly/1CoxdrG
    v1 = orig - point_1
    v2 = point_2 - point_1
    v3 = np.array([-direction[1], direction[0]])

    if np.dot(v2, v3) == 0:
        return []

    t1 = np.cross(v2, v1) / np.dot(v2, v3)
    t2 = np.dot(v1, v3) / np.dot(v2, v3)
    if t1 >= 0.0 and 0.0 <= t2 <= 1.0:
        return [orig + t1 * direction]
    return []


def get_intersection(orig: Point, end: Point, p1: Point, p2: Point):
    point = line_ray_intersection_point([orig.x, orig.y], [end.x, end.y], [p1.x, p1.y], [p2.x, p2.y])

    if len(point) == 0:
        return None

    return Point(point[0][0], point[0][1])


if __name__ == "__main__":
    line_ray_intersection_point([5, 0.5], [38, 33], [10, 5], [7.5, 10])
    line_ray_intersection_point([5, 0.5], [-28, 33], [0, 5], [2.5, 10])
