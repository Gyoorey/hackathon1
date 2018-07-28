from game import Game

#def __main__():
game = Game()
for iter in range(100):
    (fitness, ended) = game.iterate(-1)
    print("iteration %d" % iter )
    print(game.generateOutput())
    #game.show()
    if ended:
        break
    #delay(100)
game.exit()