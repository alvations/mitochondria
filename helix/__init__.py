import random
import datetime
from bisect import bisect_left

class Chromosome:
    __slots__ = ['genes', 'fitness', 'age', 'strategy']
    def __init__(self, genes, fitness, age=None, strategy=None):
        self.genes = genes
        self.fitness = fitness
        self.strategy = strategy
        self.age = age


class Evolution:
    def __init__(self, gene_set, fitness_func, optimal_fitness):
        self.gene_set = gene_set
        self.fitness_func = fitness_func
        self.optimal_fitness = optimal_fitness

    def generate_parent(self, num_genes, age=None, *args, **kwargs):
        genes = []
        while len(genes) < num_genes:
            sample_size = min(num_genes-len(genes), len(self.gene_set))
            genes.extend(random.sample(self.gene_set, sample_size))
        return Chromosome(genes, self.fitness_func(genes, *args, **kwargs),
                          age, strategy='create')

    def mutate(self, parent, *args, **kwargs):
        """
        :param parent:
        :type parent: Chromosome
        :rtype: Chromosome
        """
        index = random.randrange(0, len(parent.genes))
        child_genes = list(parent.genes)
        new_gene, alternate = random.sample(self.gene_set, 2)
        child_genes[index] = alternate if new_gene == child_genes[index] else new_gene
        return Chromosome(child_genes, self.fitness_func(child_genes, *args, **kwargs))

    def crossover(self, child_fitness, fitness_history):
        index = bisect_left(fitness_history, child_fitness, 0, len(fitness_history))
        difference = len(fitness_history) - index
        similar_proportion = difference / len(difference)
        return random.random() < exp(-similar_proportion)

    def evolve(self, parent, max_age=None, *args, **kwargs):
        fitness_history = [parent.fitness]
        best_parent = parent
        while True:
            child = self.mutate(parent, *args, **kwargs)
            # parent > child
            if parent.fitness > child.fitness:
                continue
                """
                if max_age is None:
                    continue
                # Continue from parent.
                parent.age += 1
                if max_age > parent.age:
                    continue
                if crossover(child.fitness, fitness_history):
                    parent = child
                    continue
                best_parent.age = 0
                parent = best_parent
                continue
                """
            # child >= parent
            if child.fitness <= parent.fitness:
                ##child.age = parent.age + 1
                parent = child
                continue
            yield child
            child.age = 0
            parent = child

            # child > parent
            if child.fitness > best_parent.fitness:
                best_parent = child
                yield best_parent


    def find_fittest(self, num_genes, random_seed=0, max_age=None, *args, **kwargs):
        random.seed(random_seed)
        # Genesis: Create generation 0 parent.
        gen0 = self.generate_parent(num_genes, age=0, *args, **kwargs)
        # If somehow, we met the criteria after gen0, banzai!
        if gen0.fitness > self.optimal_fitness:
            return best_parent

        start_time = datetime.datetime.now()
        for child in self.evolve(gen0, max_age, *args, **kwargs):
            # Log time taken to reach better fitness.
            time_taken = datetime.datetime.now() - start_time
            print("{}\t{}\t{}".format(child.genes, child.fitness, time_taken))
            # Return child if fitness reached optimal.
            if self.optimal_fitness <= child.fitness:
                return child
