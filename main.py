import data_point_generator
import math as maths
from evolver import evolve_functions


if __name__ == "__main__":
    input('''To use this program, edit "data_points.py". It should contain a list of tuples of input -> output pairs that the AI is trained on. By default, the AI is trained on the function exp(-x^2) on [-3, 3]''')
    generations = int(input("Enter the number of generations. Somewhere in the range of 100-500 is recommended: "))
    evolve_functions(generations)
