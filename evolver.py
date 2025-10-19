import math as maths
from function_generator import generate_functions, random_expression, mutate_functions
from data_points import data_points
from standard_functions import log

def find_difference(data_points, f):
    total_difference = 0
    for i in data_points:
        try:
            difference = (i[1] - f(i[0]))**2
            if type(difference) == complex:
                total_difference += 100000
            else:
                total_difference += difference
        except ZeroDivisionError:
            total_difference += 100000
        except OverflowError:
            total_difference += 100000

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
        if f[1]:
            function_ranking.append(f)
        else:
            difference = find_difference(data_points, lambda x : eval(str(f[0])))
            if difference == 0:
                print("########## Expression found ############")
                print(str(f[0]))
                input()
                exit()
            if difference < lowest_difference:
                print(f"Strong contender found: {f[0]}\nWith an error rate of {difference}")
                lowest_difference = difference
                best_function = f[0]
            function_ranking.append((f[0], difference))
    return sorted(function_ranking, key = lambda item : item[1])

def purge_functions(functions, num_population):
    surviving_functions = test_functions(functions)[:num_population//2]
    output = []
    #for function in surviving_functions:
    #    output.append(function[0])
    return surviving_functions

best_function = None
lowest_difference = 10000

def evolve_functions(generations = 1, num_population = 500, migration = 0.1):
    population = []
    for i in range(num_population):
        population.append((random_expression(2), None))
    #print(initial_functions)
    for i in range(generations):
        population = purge_functions(population, num_population)
        #print(population[:10], end = "\n\n\n\n\n")
        population = mutate_functions(population)
        print(i)
        if i%100 == 0:
            print(f"Best function is {best_function}\nWith an error rate of {lowest_difference}")
    final_functions = population[:10]
    print(f"List of surviving functions found, in order of ascending error rate {final_functions}")
    print(f"The best function was {str(best_function)}")
    print(f"With an error rate of{lowest_difference}")
