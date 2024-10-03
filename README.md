This code implements a genetic algorithm to generate crossword puzzles, aiming to place a set of words on a grid in a way that maximizes a fitness score. 
The algorithm evolves a population of potential solutions (crosswords) over generations through fitness evaluation, selection, crossover, and mutation. 

* Main Flow:

Reads input words from files, applies the genetic algorithm, and outputs the best crossword solution for each input set.

* Crossword Structure:

The Crossword class represents a 20x20 grid where words are placed either vertically or horizontally. Each crossword has fitness (fitnes) and coordinates for word placement.

* Fitness Calculation:

The fitness score is calculated based on criteria such as whether all words are placed, word connectivity, crossing of words, penalties for missing or overlapping words, and substring checks (non-listed words appearing due to placement).

* Genetic Algorithm:

A population of random crosswords is generated, and fitness is calculated for each.
In each generation, individuals are selected based on fitness, undergo crossover (to mix traits of two parents), and mutations (random adjustments to word placements).
The process repeats for a specified number of generations.

Input folder contains examples of words that you can use to generate a crossword.
Output folder contains the solution.

Recommenadation: do not use more than 10 words for one crossword.