import math as maths

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

standard_function = {
    "sin(x)" : maths.sin,
    "cos(x)" : maths.cos,
    "x**2" : lambda x : x*x,
    "x**3" : lambda x : x*x*x,
    "sqrt(x)" : lambda x : x**0.5
}

def generate_data_points(function):
    data_points = []
    function = standard_function[function]
    for i in range(-100, 101, 1):
        data_points.append((float(truncate(i/10, 5)), float(truncate(function(i/10), 5))))
    return data_points
