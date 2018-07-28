import numpy as np
import neat
import os
from neat.reporting import ReporterSet
from neat.math_util import mean
from neat.six_util import iteritems, itervalues
from game import Game

class CompleteExtinctionException(Exception):
    pass

#def __main__():
local_dir = os.path.dirname("..\\AI\\")
config_path = os.path.join(local_dir, 'config-feedforward')
print('debug')
# Load configuration.
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)
#print('debug')
# Create the population, which is the top-level object for a NEAT run.
p = neat.Population(config)

for generation in range(1000):
    max_fit = 0;

    genomes = list(iteritems(p.population));
    #counter = 1
    for genome_id, genome in genomes:
        #genome.fitness = 6.0  # random.uniform(0, 100)
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        g = Game()
        genome.fitness = 10000
        for iter in range(10000):
            xi = g.generateOutput()
            xi = tuple(xi[0])
            #print(xi)
            output = net.activate(xi)

            action = np.argmax(output) - 1
            #print(action, end=';')

            (fitness, ended) = g.iterate(action)
            #print("iteration %d" % iter )
            #print(game.generateOutput())
            #game.show()ss
            if ended:
                #p.population[genome_id].fitness = fitness
                genome.fitness = fitness
                #print(fitness)
                if fitness > max_fit:
                    max_fit = fitness
                break
            #delay(100)
        #g.exit()

    print("generation: %d " % generation)
    print("max fitness: %f " % max_fit)

    #genomes = list(iteritems(p.population));
    #for genome_id, genome in genomes:
    #    print(genome.fitness)
    #selection:
    p.population = p.reproduction.reproduce(p.config, p.species, p.config.pop_size, p.generation)
    #p.reproduce()

    # Check for complete extinction.
    if not p.species.species:
        p.reporters.complete_extinction()

        # If requested by the user, create a completely new population,
        # otherwise raise an exception.
        if p.config.reset_on_extinction:
            p.population = p.reproduction.create_new(p.config.genome_type,
                                                           p.config.genome_config,
                                                           p.config.pop_size)
        else:
            raise CompleteExtinctionException()

    # Divide the new population into species.
    p.species.speciate(p.config, p.population, p.generation)

    p.reporters.end_generation(p.config, p.population, p.species)

    p.generation += 1
