# machine-learning-using-expression-trees
Uses a genetic algorithm to find a function matching a set of data points

WIP - very incomplete. Full version should feature a UI, ability to upload a dataset in the form of a JSON or CSV file, and should graph the final function against the data points to demonstrate its success (or failure)

Edit the file "data_points.py" to upload your own data points in the form of a list of tuples. "main.py" features a function that finds the average difference between the proposed function and the training data.
You can also automatically generate data points for the program. Input "sin(x)", "cos(x)", "x**2", "x**3", or "sqrt(x)" when prompted to generate a set of data points for that function.
Features a non-implemented function generator that creates valid algebraic expressions and mutates them. This is the basis of the genetic algorithm in the future
