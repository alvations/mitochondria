import random

from helix import Chromosome

class Mutation:
    def __init__(self, mutation_type):
        # Select the mutation strategy.
        self.mutate = {'pick': self.pick, 'swap': self.swap}[mutation_type]

    def pick(self, parent, gene_set, fitness_func, *args, **kwargs):
        """
        :param parent:
        :type parent: Chromosome
        :rtype: Chromosome
        """
        child_genes = list(parent.genes)
        index = random.randrange(0, len(parent.genes))
        new_gene, alternate = random.sample(gene_set, 2)
        child_genes[index] = alternate if new_gene == child_genes[index] else new_gene
        return Chromosome(child_genes, fitness_func(child_genes, *args, **kwargs), age=parent.age)

    def swap(self, parent, gene_set, fitness_func, *args, **kwargs):
        """
        :param parent:
        :type parent: Chromosome
        :rtype: Chromosome
        """
        gene_indices = list(range(len(gene_set)))
        child_genes = list(parent.genes)
        index_a, index_b = random.sample(gene_indices, 2)
        child_genes[index_a],  child_genes[index_b] = child_genes[index_b], child_genes[index_a]
        return Chromosome(child_genes, fitness_func(child_genes, *args, **kwargs), age=parent.age)
