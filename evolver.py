import math as maths
from function_generator import generate_functions, random_expression, mutate_functions
from data_points import data_points

def find_difference(data_points, f):
    total_difference = 0
    for i in data_points:
        try:
            difference = (i[1] - f(i[0]))**2
            total_difference += difference
        except ZeroDivisionError:
            total_difference += 10000

    total_difference /= len(data_points)

    if total_difference <= 1e-4:
        return 0
    #elif total_difference <= 0.5:
    #    print(f"Strong contender found: {f}\nWith an error rate of {total_difference}")
    else:
        return total_difference

def test_functions(functions):
    global lowest_difference
    global best_function
    function_ranking = []
    for f in functions:
        difference = find_difference(data_points, lambda x : eval(str(f)))
        if difference < lowest_difference:
            print(f"Strong contender found: {f}\nWith an error rate of {difference}")
            lowest_difference = difference
            best_function = f
        function_ranking.append((f, difference))
    return sorted(function_ranking, key = lambda item : item[1])

def purge_functions(functions):
    surviving_functions = test_functions(functions)[:50]
    output = []
    for function in surviving_functions:
        output.append(function[0])
    return output

best_function = None
lowest_difference = 10000

def evolve_functions(generations = 1):
    population = []
    for i in range(500):
        population.append(random_expression(2))
    #print(initial_functions)
    for i in range(generations):
        population = purge_functions(population)
        population = mutate_functions(population)
        print(i)
    final_functions = population[:10]
    print(f"List of surviving functions found, in order of ascending error rate {final_functions}")
    print(f"The best function was {str(best_function)}")
    print(f"With an error rate of{lowest_difference}")
