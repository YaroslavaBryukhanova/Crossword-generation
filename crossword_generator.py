import random
import os

POPULATION_SIZE = 100
GENERATIONS =  1000
GRID_SIZE = 20

ALL_WORDS_REWARD = 3000
MISSING_WORDS_PENALTY = 90000000

CROSSING_REWARD = 20000
CROSSING_PENALTY = 100000
NO_CROSSING_PENALTY = 10000

OVERLAPPING_PENALTY = 70000

NEIGHBOURS_PENALTY = 100

CONNECTIVITY_REWARD = 100000
CONNECTIVITY_PENALTY = 1000000

SUBSTRINGS_PENALTY = 90000
SUBSTRINGS_REWARD = 1000    


class Coordinates:
    def __init__(self, x, y, position) -> None:
        self.x = x
        self.y = y
        self.position = position


class Crossword:
    def __init__(self) -> None:
        self.data = []
        self.fitnes = 0
        self.coords = list(map(Coordinates, []))

    def initialise(self):
        for i in range(GRID_SIZE):
            self.data.append(["."]*GRID_SIZE)

    def add_coordinates(self, x, y, position):
        coordinates = Coordinates(x, y, position)
        self.coords.append(coordinates)

    def copy(self, crossword):
        for i in range(len(crossword.coords)):
            self.add_coordinates(
                crossword.coords[i].x, crossword.coords[i].y, crossword.coords[i].position)
        self.fitnes = crossword.fitnes


class CrosswordDFS:
    def __init__(self, data) -> None:
        self.data = data
        self.visited = [[False for _ in range(
            GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]

    def is_valid(self, row, col):
        return row >= 0 and row < GRID_SIZE and col >= 0 and col < GRID_SIZE and self.data[row][col] != '.'

    def dfs(self, row, col):
        self.visited[row][col] = True
        for direction in self.directions:
            new_row = row + direction[0]
            new_col = col + direction[1]
            if self.is_valid(new_row, new_col) and not self.visited[new_row][new_col]:
                self.dfs(new_row, new_col)

    def are_all_words_connected(self):
        count_of_words = 0
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.data[i][j] != '.' and not self.visited[i][j]:
                    count_of_words += 1
                    self.dfs(i, j)
        return count_of_words == 1


def read_words(i):
    """ Read the words from the input file.

    Args:
        i (int): The number of the input file.

    Returns:
        list: The list of the words.
    """
    words = []
    with open(f'inputs/input{i + 1}.txt', 'r') as f:
        for line in f:
            words.append(line.strip())
    return words


def main():

    input_files = len(os.listdir('inputs'))

    for i in range(input_files):
        words = []
        words = read_words(i)
        output = open(f'outputs/output{i + 1}.txt', 'w')
        population = []
        for i in range(POPULATION_SIZE):
            population.append(generate_individual(words))

        for generation in range(GENERATIONS):
            # 1. Calculate the fitness of each individual in the population
            # 2. Select the best-fit individuals for reproduction
            # 3. Breed new individuals through crossover and mutation operations to give birth to offspring
            # 4. Replace the least-fit individuals in the population with the new individuals
            # 5. Repeat the process until the termination criterion is satisfied (i.e. number of generations)

            for i in range(POPULATION_SIZE):
                calculate_fitness(
                    population[i], words)
            population.sort(key=lambda x: x.fitnes, reverse=True)

            new_population = []
            for i in range(POPULATION_SIZE//4):
                new_population.append(population[i])

            for i in range(POPULATION_SIZE//4 * 3):
                parent1 = random.choice(population[:POPULATION_SIZE//4])
                parent2 = random.choice(population[:POPULATION_SIZE//4])
                child = crossover(parent1, parent2, words)
                update_crossword(child, words)
                new_population.append(child)
            population = new_population

            for i in range(POPULATION_SIZE):
                calculate_fitness(
                    population[i], words)
            population.sort(key=lambda x: x.fitnes, reverse=True)
            
            

        population.sort(key=lambda x: x.fitnes, reverse=True)
        update_crossword(population[0], words)

        for coords in population[0].coords:
            if coords.position == 0:
                coords.position = 1
            else:
                coords.position = 0
            output.write(f"{coords.x} {coords.y} {coords.position}\n")

        calculate_fitness(population[0], words)


def update_crossword(individual, words):
    for i in range(len(words)):
        if individual.coords[i].position == 0:
            row = individual.coords[i].x
            col = individual.coords[i].y
            for j in range(len(words[i])):
                individual.data[row + j][col] = words[i][j]
        else:
            row = individual.coords[i].x
            col = individual.coords[i].y
            for j in range(len(words[i])):
                individual.data[row][col + j] = words[i][j]
    return individual


# Function to generate a random individual (crossword grid)
def generate_individual(word_sequence):

    grid = Crossword()
    grid.initialise()

    for word in word_sequence:
        # Choose a random direction (0: vertical, 1: horizontal)
        direction = random.randint(0, 1)
        placed = False
        while not (placed):
            if direction == 0:  # Vertical
                row = random.randint(0, 20 - len(word))
                col = random.randint(0, 19)
                flag = True
                for i in range(len(word)):
                    if grid.data[row + i][col] != '.':
                        flag = False
                        break

                if flag:
                    for i in range(len(word)):
                        grid.data[row + i][col] = word[i]
                    placed = True
                    grid.add_coordinates(row, col, 0)

            else:  # Horizontal
                row = random.randint(0, 19)
                col = random.randint(0, 20 - len(word))
                flag = True
                for i in range(len(word)):
                    if grid.data[row][col + i] != '.':
                        flag = False
                        break

                if flag:
                    for i in range(len(word)):
                        grid.data[row][col+i] = word[i]
                    placed = True
                    grid.add_coordinates(row, col, 1)
    return grid


# Function to calculate the fitness of an individual (crossword)
def calculate_fitness(individual: Crossword, words):
    fitnes = 0
    # 1. check if all words are placed
    vertical_substrings = [''.join([individual.data[i][j] for i in range(GRID_SIZE)]).split('.') for j in range(GRID_SIZE)]
    horizontal_substrings = [''.join([individual.data[i][j] for j in range(GRID_SIZE)]).split('.') for i in range(GRID_SIZE)]
    
    for word in words:
        if word not in vertical_substrings and word not in horizontal_substrings:
            fitnes -= MISSING_WORDS_PENALTY
        else:
            fitnes += ALL_WORDS_REWARD
    
    placed_words = []
    for word in words:
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if individual.data[i][j] == word[0]:
                    if j + len(word) <= GRID_SIZE:
                        flag = True
                        for k in range(len(word)):
                            if individual.data[i][j + k] != word[k]:
                                flag = False
                                break
                        if flag:
                            placed_words.append(word)
                    if i + len(word) <= GRID_SIZE:
                        flag = True
                        for k in range(len(word)):
                            if individual.data[i + k][j] != word[k]:
                                flag = False
                                break
                        if flag:
                            placed_words.append(word)
    if len(placed_words) == len(words):
        fitnes += ALL_WORDS_REWARD
    else:
        fitnes -= MISSING_WORDS_PENALTY * (len(words) - len(set(placed_words)))

    # 2. check if the words are connected
    dfs = CrosswordDFS(individual.data)
    if dfs.are_all_words_connected():
        fitnes += CONNECTIVITY_REWARD
    else:
        fitnes -= CONNECTIVITY_PENALTY

    # 3 check if the words are crossing correctly
    count = 0
    count_of_crossing = 0
    for i in range(len(words) - 1):
        for j in range(i+1, len(words)):
            row_i, col_i = individual.coords[i].x, individual.coords[i].y
            row_j, col_j = individual.coords[j].x, individual.coords[j].y
            if individual.coords[i].position == 0:
                if individual.coords[j].position == 1:
                    for letter1 in range(len(words[i])):
                        for letter2 in range(len(words[j])):
                            if row_i + letter1 == row_j and col_j + letter2 == col_i:
                                count_of_crossing += 1
                                if words[i][letter1] != words[j][letter2]:
                                    # fitnes -= CROSSING_PENALTY
                                    count += 1
                                else:
                                    fitnes += CROSSING_REWARD
            else:
                if individual.coords[j].position == 0:
                    for letter1 in range(len(words[i])):
                        for letter2 in range(len(words[j])):
                            if row_j + letter2 == row_i and col_i + letter1 == col_j:
                                count_of_crossing += 1
                                if words[i][letter1] != words[j][letter2]:
                                    fitnes -= CROSSING_PENALTY
                                    count += 1
                                else:
                                    fitnes += CROSSING_REWARD
            if individual.coords[i].position == 1 and individual.coords[j].position == 1:
                for letter1 in range(len(words[i])):
                    for letter2 in range(len(words[j])):
                        if row_i == row_j and col_i + letter1 == col_j + letter2:
                            fitnes -= OVERLAPPING_PENALTY
                            count += 1

            if individual.coords[i].position == 0 and individual.coords[j].position == 0:
                for letter1 in range(len(words[i])):
                    for letter2 in range(len(words[j])):
                        if row_i + letter1 == row_j + letter2 and col_i == col_j:
                            fitnes -= OVERLAPPING_PENALTY
                            count += 1
    if count_of_crossing == 0:
        fitnes -= NO_CROSSING_PENALTY

    # 4 check the substrings
    vertical_words = []
    horizontal_words = []
    for i in range(GRID_SIZE):
        vertical_word = ''
        for j in range(GRID_SIZE):
            if individual.data[i][j] != '.':
                vertical_word += individual.data[i][j]
            elif vertical_word != '':
                vertical_words.append(vertical_word)
                vertical_word = ''
        if vertical_word != '':
            vertical_words.append(vertical_word)
            vertical_word = ''

    for i in range(GRID_SIZE):
        horizontal_word = ''
        for j in range(GRID_SIZE):
            if individual.data[j][i] != '.':
                horizontal_word += individual.data[j][i]
            elif horizontal_word != '':
                horizontal_words.append(horizontal_word)
                horizontal_word = ''
        if horizontal_word != '':
            horizontal_words.append(horizontal_word)
            horizontal_word = ''

    for word in vertical_words:
        if word not in words and len(word) > 1:
            fitnes -= SUBSTRINGS_PENALTY
            count += 1
        else:
            fitnes += SUBSTRINGS_REWARD

    for word in horizontal_words:
        if word not in words and len(word) > 1:
            fitnes -= SUBSTRINGS_PENALTY
            count += 1
        else:
            fitnes += SUBSTRINGS_REWARD

    individual.fitnes = fitnes


def generate_grid(crossword: Crossword, words):
    grid = Crossword()
    grid.initialise()

    for i, word in enumerate(words):
        row = crossword.coords[i].x
        col = crossword.coords[i].y
        # vertical
        if crossword.coords[i].position == 0:
            for j in range(len(word)):
                if row + j < 20:
                    grid.data[row + j][col] = word[j]
        else:
            for j in range(len(word)):
                if col + j < 20:
                    grid.data[row][col + j] = word[j]

    return grid

# Function for crossover operation
def crossover(parent1: Crossword, parent2: Crossword, words):
    child = Crossword()
    child.initialise()
    # 1. Randomly select a crossover point
    # 2. Copy all the characters before the crossover point from the first parent to the child
    # 3. Copy all the characters after the crossover point from the second parent to the child
    # 4. Perform mutation on the child
    crossover_point = random.randint(0, len(words) - 1)
    for i in range(crossover_point):
        child.add_coordinates(
            parent1.coords[i].x, parent1.coords[i].y, parent1.coords[i].position)
    for i in range(crossover_point, len(words)):
        child.add_coordinates(
            parent2.coords[i].x, parent2.coords[i].y, parent2.coords[i].position)

    child = mutate(child, words)
    return child


def mutate(individual: Crossword, words):
    # 1. Randomly select a mutation point
    # 2. Randomly select a new position for the word
    # 3. Perform the mutation

    mutation_point = random.randint(0, len(words) - 1)
    direction = random.randint(0, 1)
    placed = False
    while not (placed):
        if direction == 0:  # Vertical
            row = random.randint(0, 20 - len(words[mutation_point]))
            col = random.randint(0, 19)
            flag = True
            for i in range(len(words[mutation_point])):
                if individual.data[row + i][col] != '.':
                    flag = False
                    break

            if flag:
                for i in range(len(words[mutation_point])):
                    individual.data[row + i][col] = words[mutation_point][i]
                placed = True
                individual.coords[mutation_point].x = row
                individual.coords[mutation_point].y = col
                individual.coords[mutation_point].position = 0

        else:  # Horizontal
            row = random.randint(0, 19)
            col = random.randint(0, 20 - len(words[mutation_point]))
            flag = True
            for i in range(len(words[mutation_point])):
                if individual.data[row][col + i] != '.':
                    flag = False
                    break

            if flag:
                for i in range(len(words[mutation_point])):
                    individual.data[row][col+i] = words[mutation_point][i]
                placed = True
                individual.coords[mutation_point].x = row
                individual.coords[mutation_point].y = col
                individual.coords[mutation_point].position = 1

    return individual


if __name__ == '__main__':
    main()
