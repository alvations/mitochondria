#!/usr/bin/env python
#-*- coding: utf-8 -*-

import random
import datetime
from bisect import bisect_left
from math import exp


class Chromosome:
    __slots__ = ['genes', 'fitness', 'age', 'strategy']
    def __init__(self, genes, fitness, age=None, strategy=None):
        """
        The `Chromosome` class is a container object to store the variables
        used in genetic evolution process. Think of it like an organism.

        :param genes: The genome of this organism
        :type genes: list
        :param fitness: The fitness object from helix.fitness
        :type fitness: Fitness
        :param age: The age from which the organism has descended.
        :type age: int
        :param strategy: Specify how is the organism created.
        :type strategy: str
        """
        self.genes = genes
        self.fitness = fitness
        self.strategy = strategy
        self.age = age


class Evolution:
    def __init__(self, gene_set, fitness_func, mutation,
                 *args, **kwargs):
        """
        The `Evolution` class is the main object that controls the evolution
        process.

        :param gene_set: The no. of unique genes of the organism's genome.
        :type gene_set: list
        :param fitness_func: The fitness function to optimize evolution.
        :type fitness_func: module
        :param mutation: The mutation object from helix.mutation
        :type mutation: Mutation
        """
        self.gene_set = gene_set
        self.fitness_func = fitness_func
        # Select the mutation strategy.
        self.mutation = mutation
        # Currently *gene_indices* are only used for swap mutation


    def generate_parent(self, num_genes, age=None, *args, **kwargs):
        """
        The function to emulate the genesis of the ancestor's gene.

        :param num_genes: The length of the genes for the Chromosome object.
        :param num_genes: int
        :param age: The age from which the organism has descended.
        :type age: int
        """
        genes = []
        while len(genes) < num_genes:
            sample_size = min(num_genes-len(genes), len(self.gene_set))
            genes.extend(random.sample(self.gene_set, sample_size))
        return Chromosome(genes, self.fitness_func(genes, *args, **kwargs),
                          age, strategy='create')

    def child_becomes_parent(self, child_fitness, fitness_history):
        """
        The stimulated annealing condition function.

        :param child_fitness: The child's fitness object.
        :type child_fitness: Fitness
        :param fitness_history: The history of fitness objects through the evolution.
        :type fitness_history: list(Fitness)
        """
        # Determine how far away is the child_fitness from best_fitness.
        # Find the  position of the child's fitness.
        index = bisect_left(fitness_history, child_fitness, 0, len(fitness_history))
        # Find the proxmity to the best fitness (last on the *fitness_history*)
        difference = len(fitness_history) - index
        # Convert it to a proportion.
        similar_proportion = difference / len(fitness_history)
        # Pick a random number, check if random number is smaller than
        # `exp(-similar_proportion)`, then child becomes parent.
        return random.random() < exp(-similar_proportion)

    def evolve(self, parent, max_age=None, *args, **kwargs):
        """
        The evolve functions that:
         1. Mutate the child from the parent

         2. Check if the parent's fitness is > child's fitness
           2a.  Continue the evolution if no max_age is required
           2b.1.  If yes, let the parent die out if max_age is reached
           2b.2.  Check the condition for stimulated annealing
           2b.2.1.  If condition, parent genes passed on to child fully
           2b.2.2   Else, reset the parent's age and make it the best_parent

         3. Check if the childn's fitness == parent's fitness.
           3a.  If yes, update the child's age to be parent's age + 1
               and the child becomes the new parent, process on the branch.

         4. Set the child's age to 0 and the child becomes the new parent to
            start a new branch.

         5. Check if the child's fitness is better than the best_parent's fitness
           5a.  if yes, the child becomes the best_parent and append its fitness
                to the fitness_history.

        :param parent: The parent chromosome.
        :type parent: Chromosome
        :param max_age: The hyperparameter that affects the rate of stimulated annealing.
        :type max_age: int
        :rtype: Chromosome
        """
        fitness_history = [parent.fitness]
        best_parent = parent
        while True:
            child = self.mutation.mutate(parent, self.gene_set, self.fitness_func,
                                         *args, **kwargs)
            # parent's fitness > child's fitness
            if parent.fitness > child.fitness:
                if max_age is None:
                    continue
                # Let the parent die out if max_age is reached.
                parent.age += 1
                if max_age > parent.age:
                    continue
                # Simulated annealing.
                # If child is to become the new parent.
                if self.child_becomes_parent(child.fitness, fitness_history):
                    parent = child
                else: # Otherwise reset parent's age.
                    best_parent.age = 0
                    parent = best_parent
                continue

            # parent's fitness == child's fitness
            if child.fitness == parent.fitness:
                child.age = parent.age + 1
                parent = child
                continue

            # parent's fitness < child's fitness:
            child.age = 0
            parent = child

            # best_parent's fitness < child's fitness:
            if child.fitness > best_parent.fitness:
                best_parent = child
                yield best_parent
                fitness_history.append(child.fitness)

    def generate(self, num_genes, optimal_fitness, random_seed=0, max_age=None, *args, **kwargs):
        """
        The main function to start the evolution process.

        First the generation 0 parent will be generated and then the evolution
        starts with self.evolve().

        This function will print the best child in each evolution process and
        return the final child that matches the target based on the fitness.

        :param num_genes: The length of the genes for the Chromosome object.
        :param num_genes: int
        :param optimal_fitness: The optimal fitness that evolution should head towards.
        :type optimal_fitness: Fitness
        :param random_seed: The random seed.
        :type random_seed: int
        :param max_age: The hyperparameter that affects the rate of stimulated annealing.
        :type max_age: int
        :rtype: Chromosome
        """
        random.seed(random_seed)
        generations_best = []
        # Genesis: Create generation 0 parent.
        gen0 = self.generate_parent(num_genes, age=0, *args, **kwargs)
        generations_best.append(gen0)

        # If somehow, we met the criteria after gen0, banzai!
        if gen0.fitness > optimal_fitness:
            return generations_best

        start_time = datetime.datetime.now()
        for child in self.evolve(gen0, max_age, *args, **kwargs):
            # Log time taken to reach better fitness.
            time_taken = datetime.datetime.now() - start_time
            print("{}\t{}\t{}".format(child.genes, child.fitness, time_taken))
            generations_best.append(child)
            # Return child if fitness reached optimal.
            if optimal_fitness <= child.fitness:
                break
        return generations_best
