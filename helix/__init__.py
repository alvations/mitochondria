import random

class Chromosome:
    __slots__ = ['genes', 'fitness', 'age', 'strategy']
    def __init__(self, genes, fitness, age=None, strategy=None):
        self.genes = genes
        self.fitness = fitness
        self.strategy = strategy
        self.age = age


def generate_parent(target_length, gene_set, fitness_func, target, age=None):
    genes = []
    while len(genes) < target_length:
        sample_size = min(target_length-len(genes), len(gene_set))
        genes.extend(random.sample(gene_set, sample_size))
    return Chromosome(genes, fitness_func(genes, target), age, strategy='create')


def mutate(parent, gene_set, fitness_func, target):
    """
    :param parent:
    :type parent: Chromosome
    :rtype: Chromosome
    """
    index = random.randrange(0, len(parent.genes))
    child_genes = list(parent.genes)
    new_genes, alternate = random.sample(gene_set, 2)
    child_genes[index] = alternate if new_genes == child_genes[index] else new_genes
    return Chromosome(child_genes, fitness_func(child_genes, target))

def display(genes, start_time):
    timeDiff = datetime.datetime.now() - startTime
    print("{}\t{}\t{}".format(
        candidate.Genes, candidate.Fitness, timeDiff))

def find_fittest(target_length, optimal_fitness=float('inf'), gene_set, fitness_func, random_seed=0):
    random.seed()
    best_parent = generate_parent(target_length, gene_set)
    best_fitness = best_parent.fitness

    if best_fitness >= optimal_fitness:
        return best_parent
