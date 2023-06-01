from docplex.mp.model import Model
from scipy.spatial import distance_matrix

def tsp_solver(pharmacies):
    num_pharmacies = len(pharmacies)

    # Calculate distance matrix
    distances = distance_matrix(pharmacies, pharmacies)

    # Create a CPLEX model
    model = Model(name='TSP')

    # Create binary variables
    x = {(i, j): model.binary_var(name='x_{0}_{1}'.format(i, j)) for i in range(num_pharmacies) for j in range(num_pharmacies)}

    # Objective function
    model.minimize(model.sum(distances[i][j] * x[i, j] for i in range(num_pharmacies) for j in range(num_pharmacies)))

    # Constraints
    for i in range(num_pharmacies):
        model.add_constraint(model.sum(x[i, j] for j in range(num_pharmacies) if j != i) == 1)
        model.add_constraint(model.sum(x[j, i] for j in range(num_pharmacies) if j != i) == 1)

    # Solve the model
    solution = model.solve()

    # Extract the optimal trajectory
    optimal_trajectory = [i for i in range(num_pharmacies)]
    visited = [False] * num_pharmacies
    current = 0
    visited[current] = True

    for _ in range(num_pharmacies - 1):
        for j in range(1, num_pharmacies):
            if not visited[j] and solution.get_value(x[current, j]) == 1:
                optimal_trajectory.append(j)
                visited[j] = True
                current = j
                break

    return optimal_trajectory