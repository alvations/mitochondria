import random

from mitochondria import Chromosome

class Mutation:
    def __init__(self, mutation_type, *args, **kwargs):
        """
        The `Mutation` object controls the mutation functions in the genetic process.

        :param mutation_type: string option to toggle mutation function.
        :type mutation_type: str
        """
        # Select the mutation strategy.
        self.mutate = {'pick': self.pick, 'swap': self.swap}[mutation_type]

    def pick(self, parent, gene_set, fitness_func, *args, **kwargs):
        """
        The `pick` mutation randomly selects a single gene from the genome and
        replace one of the parent's to create a child.

        :param parent: The parent chromosome.
        :type parent: Chromosome
        :param gene_set: The fixed set of gene.
        :type gene_set: list
        :param fitness_func: The fitness function used to optimize mutation.
        :type fitness_func: module
        :rtype: Chromosome
        """
        child_genes = list(parent.genes)
        index = random.randrange(0, len(parent.genes))
        new_gene, alternate = random.sample(gene_set, 2)
        child_genes[index] = alternate if new_gene == child_genes[index] else new_gene
        return Chromosome(child_genes, fitness_func(child_genes, *args, **kwargs), age=parent.age)

    def swap(self, parent, gene_set, fitness_func, *args, **kwargs):
        """
        The `swap` mutation randomly selects a two positions of the genes and
        swap them to create a child.

        :param parent: The parent chromosome.
        :type parent: Chromosome
        :param gene_set: The fixed set of gene.
        :type gene_set: list
        :param fitness_func: The fitness function used to optimize mutation.
        :type fitness_func: module
        :rtype: Chromosome
        """
        gene_indices = list(range(len(gene_set)))
        child_genes = list(parent.genes)
        index_a, index_b = random.sample(gene_indices, 2)
        child_genes[index_a],  child_genes[index_b] = child_genes[index_b], child_genes[index_a]
        return Chromosome(child_genes, fitness_func(child_genes, *args, **kwargs), age=parent.age)
