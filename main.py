from math import sin, cos, radians
from numpy import dot
import time
import os

foco = 40
angle_x = -5
angle_y = -10
angle_z = 5
resolution = 40

delay = 0.01
y_distorter = 1.1
up_down = 0.5
left_right = 1.5


CUBE_CORNERS = [[-10, -10, -10],  # Point 0
[10, -10, -10],  # Point 1
[-10, -10, 10],  # Point 2
[-10, 10, -10],  # Point 3
[10, -10, 10],  # Point 4
[10, 10, -10],  # Point 5
[-10, 10, 10],  # Point 6
[10, 10, 10]]  # Point 7


def rotator(cube):
    x_rotator = [[1, 0, 0],
                 [0, cos(radians(angle_x)), sin(radians(angle_x))],
                 [0, -sin(radians(angle_x)), cos(radians(angle_x))]]
    y_rotator = [[cos(radians(angle_y)), 0, -sin(radians(angle_y))],
                 [0, 1, 0],
                 [sin(radians(angle_y)), 0, cos(radians(angle_y))]]
    z_rotator = [[cos(radians(angle_z)), sin(radians(angle_z)), 0],
                 [-sin(radians(angle_z)), cos(radians(angle_z)), 0],
                 [0, 0, 1]]
    return [dot((dot((dot(point, x_rotator)), y_rotator)), z_rotator) for point in cube]


def projection(cube):
    return [(round(2 * point[0] * foco / (foco + point[2])), round(point[1] * foco / ((foco + point[2]) * y_distorter))) for point in cube]


def lines(proj):
    connected_points = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 4), (2, 6), (3, 5), (3, 6), (7, 6), (7, 5), (7, 4)]
    return [interpolate(proj[point0][0], proj[point0][1], proj[point1][0], proj[point1][1]) for point0, point1 in connected_points]


def interpolate(x0, y0, x1, y1):
    alpha = (y1 - y0 + 0.001) / (x1 - x0 + 0.001)
    beta = y0 - (alpha * x0)
    if alpha > 1 or alpha < -1:
        return [((round((y - beta) / (alpha + 0.001))), y) for y in range(int(min(y1, y0)), int(max(y1, y0) + 1))]
    else:
        return [(x, (round(x * alpha + beta))) for x in range(int(min(x1, x0)), int(max(x1, x0)) + 1)]


def printer(proj, lins):
    for j in range(resolution):
        for i in range(resolution * 3):
            if (i - resolution * left_right, j - resolution * up_down) in proj:
                print("#", end="")
            elif any((i - resolution * left_right, j - resolution * up_down) in lin for lin in lins):
                print("*", end="")
            else:
                print(" ", end="")
        # print("")
        print("|")
    print("-" * resolution * 3)


if __name__ == "__main__":
    cube = CUBE_CORNERS
    try:
        while 1:
            os.system('cls')
            printer(projection(cube), lines(projection(cube)))
            cube = rotator(cube)
            time.sleep(delay)
    except KeyboardInterrupt:
        pass
