import numpy as np
import neat
import os
from neat.reporting import ReporterSet
from neat.math_util import mean
from neat.six_util import iteritems, itervalues
from game import Game

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

for generation in range(1):
    genomes = list(iteritems(p.population));

    for genome_id, genome in genomes:
        #genome.fitness = 6.0  # random.uniform(0, 100)
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        g = Game()

        for iter in range(100):
            xi = g.generateOutput()
            xi = tuple(xi[0])
            #print(xi)
            output = net.activate(xi)

            action = np.argmax(output) - 1
            print(action, end=';')

            (fitness, ended) = g.iterate(action)
            #print("iteration %d" % iter )
            #print(game.generateOutput())
            #game.show()ss
            if ended:
                genome.fitness = fitness
                print(fitness)
                break
            #delay(100)
        #g.exit()

    #p.reproduce()
