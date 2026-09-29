import random

# Distance matrix between cities
distance = [
    [0, 10, 15, 20, 25],
    [10, 0, 35, 25, 30],
    [15, 35, 0, 30, 20],
    [20, 25, 30, 0, 15],
    [25, 30, 20, 15, 0]
]

num_cities = len(distance)

# Calculate total distance of a route
def calculate_distance(route):
    total = 0

    for i in range(num_cities - 1):
        total += distance[route[i]][route[i + 1]]

    # Return to starting city
    total += distance[route[-1]][route[0]]

    return total


# Create initial population
def create_population(size):
    population = []

    for i in range(size):
        route = list(range(num_cities))
        random.shuffle(route)
        population.append(route)

    return population


# Select two best routes
def selection(population):
    population.sort(key=calculate_distance)
    return population[:2]


# Crossover
def crossover(parent1, parent2):
    start = random.randint(0, num_cities - 2)
    end = random.randint(start + 1, num_cities - 1)

    child = [None] * num_cities

    # Copy part of parent1
    child[start:end] = parent1[start:end]

    # Fill remaining cities from parent2
    index = 0

    for city in parent2:
        if city not in child:
            while child[index] is not None:
                index += 1

            child[index] = city

    return child


# Mutation
def mutation(route):
    i, j = random.sample(range(num_cities), 2)

    route[i], route[j] = route[j], route[i]

    return route


# Genetic Algorithm
def genetic_algorithm(population_size=20, generations=100):
    population = create_population(population_size)

    for generation in range(generations):

        # Select the best two routes
        parents = selection(population)

        new_population = parents.copy()

        # Create new population
        while len(new_population) < population_size:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)

            child = crossover(parent1, parent2)

            # Mutation
            if random.random() < 0.1:
                child = mutation(child)

            new_population.append(child)

        population = new_population

    # Find best route
    best_route = min(population, key=calculate_distance)
    best_distance = calculate_distance(best_route)

    return best_route, best_distance


# Run the Genetic Algorithm
best_route, best_distance = genetic_algorithm()

print("Best Route:", best_route)
print("Shortest Distance:", best_distance)
print("Complete Tour:", best_route + [best_route[0]])
