import data_point_generator
import math as maths
from data_points import data_points

def find_difference(data_points, f):
    total_difference = 0
    for x in data_points:
        difference = (x[1] - f(x[0]))**2
        total_difference += difference

    total_difference /= len(data_points)

    if total_difference <= 1e-4:
        print(0)
    else:
        print(total_difference)

if __name__ == "__main__":
    data_point_type = input("1. Standard function\n2. Custom dataset")
    if data_point_type == "1":
        function = input("Function > ")
        find_difference(data_point_generator.generate_data_points(function), lambda x : x**2)
    elif data_point_type == "2":
        find_difference(data_points, lambda x : (x**5)/120 - (x**4)/8 + 17*(x**3)/24 - 15*(x**2)/8 + 197*x/60 - 1 )