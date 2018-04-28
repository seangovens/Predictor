from pyeasyga.pyeasyga import GeneticAlgorithm
from trainer.learner import Learner
from trainer.file_data import FileData
import random
import math
import pickle


# The MetaLearner class is used by the meta-evolutionary system provided with the program. It runs a genetic algorithm
# with GEP subsystems as parameters.


class MetaLearner:
    # The maximum number of cycles performed to train a GEP individual
    MAX_CYCLES = 800
    # The maximum training set size of a GEP individual
    MAX_DATA = 800

    # The following variables are the indices of parameters in each chromosome, whose values are used to construct new
    # instances of the Learner class (GEP individuals)
    FIT_FUNC = 0
    PRECISION = 1
    N_CHROM = 2
    HEAD_LEN = 3
    N_GENE = 4
    MUT_RATE = 5
    INV_RATE = 6
    IST_RATE = 7
    RIST_RATE = 8
    GENET_RATE = 9
    OPX_RATE = 10
    TPX_RATE = 11
    GENEX_RATE = 12

    data = []

    def __init__(self, nlearn: int, ngen: int, in_data):
        self.num_learners = nlearn
        self.num_gen = ngen
        MetaLearner.data = in_data

    def run(self):
        setup_data = [0,    # Fitness function, 0 = NOH, 1 = MSE
                      2,    # Precision for NOH
                      30,   # Number of chromosomes
                      7,    # Head length
                      4,    # Number of genes per chromosome
                      0.05,  # Mutation rate
                      0.1,  # Inversion rate
                      0.1,  # IS Transposition rate
                      0.1,  # RIS Transposition rate
                      0.1,  # Gene Transposition rate
                      0.3,  # One-point crossover rate
                      0.3,  # Two-point crossover rate
                      0.1   # Gene crossover rate
                      ]

        ga = GeneticAlgorithm(setup_data, population_size=self.num_learners,
                              generations=self.num_gen,
                              elitism=True,
                              maximise_fitness=False)
        ga.create_individual = MetaLearner.create_individual
        ga.crossover_function = MetaLearner.crossover
        ga.mutate_function = MetaLearner.mutate
        ga.fitness_function = MetaLearner.fitness
        ga.run()

        print("Best model: {}".format(ga.best_individual()))

        with open("best_model.p", "wb") as file:
            pickle.dump(ga.best_individual()[1], file)

    @staticmethod
    def create_individual(data):
        individual = data[:]
        for i in range(len(individual)):
            if random.random() >= 0.5:
                MetaLearner.perturb_index(individual, i)
        return individual

    @staticmethod
    def crossover(p1, p2):
        cross_index = random.randrange(1, len(p1))
        return p1[:cross_index] + p2[cross_index:], \
            p2[:cross_index] + p1[cross_index:]

    @staticmethod
    def gen_signed(start, low, high, clamp_l, clamp_h, div=1.0):
        offset = random.randrange(low, high+1) / div
        if random.random() >= 0.5:
            offset *= -1.0
        return min(clamp_h, max(clamp_l, start + offset))

    @staticmethod
    def perturb_index(individual, index):
        if index == 0:
            individual[index] = 1 - individual[index]
        elif index == 1:
            individual[index] = MetaLearner.gen_signed(individual[index],
                                                       0, 2, 0.1, 50, div=2.0)
        elif index == 2:
            individual[index] = MetaLearner.gen_signed(individual[index],
                                                       0, 3, 1, 500)
        elif index == 3:
            individual[index] = MetaLearner.gen_signed(individual[index],
                                                       0, 2, 2, 50)
        elif index == 4:
            individual[index] = MetaLearner.gen_signed(individual[index],
                                                       0, 2, 2, 30)
        else:
            individual[index] = MetaLearner.gen_signed(individual[index],
                                                       0, 10000, 0.0, 1.0,
                                                       div=500000)

    @staticmethod
    def mutate(individual):
        index = random.randrange(len(individual))
        MetaLearner.perturb_index(individual, index)


    @staticmethod
    def fitness(individual, data):
        print(individual)
        learn = Learner(math.floor(individual[MetaLearner.N_CHROM]),
                        math.floor(individual[MetaLearner.HEAD_LEN]),
                        math.floor(individual[MetaLearner.N_GENE]),
                        MetaLearner.data, fit=individual[MetaLearner.FIT_FUNC])
        learn.noh_precision = individual[MetaLearner.PRECISION]
        learn.best_pop.mutation_rate = individual[MetaLearner.MUT_RATE]
        learn.best_pop.inversion_rate = individual[MetaLearner.INV_RATE]
        learn.best_pop.is_transposition_rate = individual[MetaLearner.IST_RATE]
        learn.best_pop.ris_transposition_rate = \
            individual[MetaLearner.RIST_RATE]
        learn.best_pop.gene_transposition_rate = \
            individual[MetaLearner.GENET_RATE]
        learn.best_pop.crossover_one_point_rate = \
            individual[MetaLearner.OPX_RATE]
        learn.best_pop.crossover_two_point_rate = \
            individual[MetaLearner.TPX_RATE]
        learn.best_pop.crossover_gene_rate = individual[MetaLearner.GENEX_RATE]

        learn.learn(MetaLearner.MAX_CYCLES)
        fit, err = learn.measure_fit(learn.best_pop, MetaLearner.data)
        print("Meta fitness: {}, Error: {}".format(fit, err))
        return err
