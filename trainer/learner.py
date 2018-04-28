from pygep.chromosome import Chromosome
from pygep.population import Population
from pygep.functions.mathematical.arithmetic import add_op
from pygep.functions.mathematical.arithmetic import subtract_op
from pygep.functions.mathematical.arithmetic import multiply_op
from pygep.functions.mathematical.arithmetic import divide_op
from pygep.functions.mathematical.arithmetic import modulus_op
from pygep.functions.mathematical.comparison import COMPARISON_ARITY_2
from pygep.functions.linkers import sig_sum_linker
from pygep.functions.logical import and_op
from pygep.functions.logical import or_op
import pickle
import math


# The Learner class contains the code that uses the PyGEP library to evolve a population of GEP chromosomes. It contains
# functionality for measuring fitness, setting up populations, and training/validation of a GEP population.


class Learner:
    # The precision used for the number of hits fitness function
    noh_precision = 2

    def __init__(self, n_chrom, h_len, n_gene, data, fit=0):
        self.n_chrom = n_chrom
        self.h_len = h_len
        self.n_gene = n_gene
        self.best_pop = self.setup_pop(data)
        self.max_fit = -math.inf
        self.max_fit, err = self.measure_fit(self.best_pop, data)
        self.fit_func = Learner.number_of_hits if fit == 0 else \
            Learner.mean_squared_error

    def learn(self, max_cycles, pop=None, val=None):
        MovieChromosome.fit_func = self.fit_func
        if pop is None:
            pop = self.best_pop

        for i in range(max_cycles):
            pop.cycle()

        fit, err = self.measure_fit(pop, val) if val is not None else \
            self.measure_fit(pop, MovieChromosome.data)
        if fit > self.max_fit:
            self.best_pop = pop
            self.max_fit = fit

    def measure_fit(self, pop, val_set):
        val_pred = list(map(pop.best, val_set))
        val_targ = list(map(lambda x: x.score, val_set))
        fit = Learner.validate(val_targ, val_pred)
        err = Learner.error(val_targ, val_pred)
        if fit > self.max_fit:
            self.best_pop = pop
            self.max_fit = fit
        return fit, err

    def k_fold_validation(self, in_data, cycles=500, k=10):
        set_size = len(in_data) // k
        for i in range(set_size, len(in_data), set_size):
            val_set = in_data[i-set_size:i]
            train_set = in_data[:i-set_size] + in_data[i:]
            pop = self.setup_pop(train_set)
            self.learn(cycles, pop=pop, val=val_set)
            fit, err = self.measure_fit(pop, val_set)
            print("Fold {} fitness: {} error: {}%".format(
                i // set_size, fit, err))

    def set_params(self, params):
        self.fit_func = Learner.number_of_hits if \
            params[0] == 0 else Learner.mean_squared_error
        Learner.noh_precision = params[1]
        self.n_chrom = params[2]
        self.h_len = params[3]
        self.n_gene = params[4]
        self.best_pop.mutation_rate = params[5]
        self.best_pop.inversion_rate = params[6]
        self.best_pop.is_transposition_rate = params[7]
        self.best_pop.ris_transposition_rate = params[8]
        self.best_pop.gene_transposition_rate = params[9]
        self.best_pop.crossover_one_point_rate = params[10]
        self.best_pop.crossover_two_point_rate = params[11]
        self.best_pop.crossover_gene_rate = params[12]

    def setup_pop(self, in_data):
        MovieChromosome.data = in_data
        return Population(MovieChromosome, self.n_chrom, self.h_len,
                          self.n_gene, linker=sig_sum_linker)

    def evaluate(self, x):
        return self.best_pop.best(x)

    def save(self, f_name, data):
        with open(f_name, "wb") as out:
            pickle.dump(out, data)

    def load_pop(self):
        with open("saved_pop.p", "rb") as inp:
            return pickle.load(inp)

    def load_pop_data(self):
        with open("saved_pop_data.p", "rb") as inp:
            return pickle.load(inp)

    @staticmethod
    def validate(target, predict):
        return MovieChromosome.fit_func(target, predict)

    @staticmethod
    def error(x, y):
        return sum(list(map(lambda p: abs(p[0] - p[1]), zip(x, y)))) / len(y)

    @staticmethod
    def number_of_hits(x, y):
        hits = list(map(lambda p: 1 if abs(p[0] - p[1]) <=
                                       Learner.noh_precision else 0, zip(x, y)))
        return sum(hits) * 1000 / len(y)

    @staticmethod
    def mean_squared_error(x, y):
        error_sum = sum(list(map(lambda p: pow(p[0] - p[1], 2), zip(x, y))))\
                    / (len(y) * 100.0)
        return 1000 / (1 + error_sum)

    @staticmethod
    def r_square(x, y):
        n = len(y)
        sum_prod = sum(list(map(lambda p: p[0]*p[1], zip(x, y))))
        sum_targ = sum(y)
        sum_pred = sum(x)
        num = (n * sum_prod) - (sum_targ * sum_pred)

        sum_sq_targ = sum(list(map(lambda p: math.pow(p, 2), y)))
        sum_sq_pred = sum(list(map(lambda p: math.pow(p, 2), x)))

        left = (n * sum_sq_targ) - pow(sum_targ, 2)
        right = (n * sum_sq_pred) - pow(sum_pred, 2)

        try:
            return pow(num / math.sqrt(left * right), 2) * 1000
        except ZeroDivisionError:
            return 0


# The MovieChromosome class is the class of all individuals in the GEP population. It names the function and terminal
# symbols used for constructing Karva genes.


class MovieChromosome(Chromosome):
    fit_func = Learner.number_of_hits
    data = []

    # Class variables defined in chromosome superclass
    functions = add_op, subtract_op, multiply_op, divide_op, modulus_op,\
        and_op, or_op, *COMPARISON_ARITY_2
    terminals = "director_score", "writer_score", "actor_score",\
                "rating", "act_adv", "drama", "sci_fant", "anim", "comedy",\
                "kids", "artsy", "mystery", "romance", "doc", "horror"

    def _fitness(self):
        return MovieChromosome.fit_func(list(map(self, MovieChromosome.data)),
                                        list(map(lambda x: x.score,
                                                 MovieChromosome.data)))

    def _solved(self):
        return False

    def __call__(self, obj):
        return 100.0 * super().__call__(obj)

    def __gt__(self, other):
        return self.fitness > other.fitness

if __name__ == "__main__":
    x_test = [99, 100, 92, 100, 97, 92, 45]
    y_test = [100, 100, 92, 99, 96, 90, 47]

    print("Error: {}".format(Learner.error(x_test, y_test)))
    print("Number of Hits: {}".format(Learner.number_of_hits(x_test, y_test)))
    print("Mean Squared Error: {}".format(Learner.mean_squared_error(x_test, y_test)))
    print("R-Squared: {}".format(Learner.r_square(x_test, y_test)))
