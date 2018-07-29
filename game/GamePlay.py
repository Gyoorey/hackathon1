import turtle
import numpy as np
import random
import numpy as np
import os

H = 600
W = 800
player_offset = 10
playerspeed = W / 40
player_y = -H / 2 + player_offset
playerwidth = 50

wn = turtle.Screen()
wn.setup(W + 20, H + 20)
wn.bgcolor("black")
wn.title("Hackathon Invaders")

wn.register_shape('ship.gif')
wn.register_shape('ghost.gif')

class GameArea():
    def __init__(self):
        self.border_pen = turtle.Turtle()
        self.border_pen.color('white')
        self.border_pen.speed(0)
        self.border_pen.penup()
        self.border_pen.setposition(-W / 2, H / 2)
        self.border_pen.pendown()
        self.border_pen.pensize(3)
        self.border_pen.fd(W)
        self.border_pen.rt(90)
        self.border_pen.fd(H)
        self.border_pen.rt(90)
        self.border_pen.fd(W)
        self.border_pen.rt(90)
        self.border_pen.fd(H)
        self.border_pen.hideturtle()


def exit():
    turtle.done()

class Asteroids(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.hideturtle()

    def drawAsteroids(self, a, b):
        self.hideturtle()
        self.color("red")
        self.shape("ghost.gif")
        self.penup()
        self.speed(0)
        # self.showturtle()
        self.setposition(a, b)
        self.showturtle()

# def move(turtle, a, b):

class Ship(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.x = 0
        self.hideturtle()
        self.asteroids = []
        self.ast_thresh = 0.95
        self.iter_cnt = 0
        self.ast_speed = 10
        random.seed = 0
        self.ended = False

    def drawShip(self):
        self.color("black")
        self.shape("ship.gif")
        self.penup()
        self.speed(0)
        self.setposition(self.x, player_y)
        self.showturtle()
        self.setheading(90)

    # def move(self):
        # self.setposition(self.x, player_y)

    def iterate(self, key):
        if (self.ended):
            return (self.iter_cnt, self.ended)
        if key == -1 and self.x > -W / 2 + playerspeed:
            self.x -= playerspeed
        if key == 1 and self.x < W / 2 - playerspeed:
            self.x += playerspeed
        # move asteroids
        for i in range(len(self.asteroids)):
            self.asteroids[i][1] = self.asteroids[i][1] - self.ast_speed
        # check collision
        for asteroid in self.asteroids:
            if abs(self.x - asteroid[0]) < playerwidth and asteroid[1] <= player_y + playerwidth:
                self.ended = True
                return (self.iter_cnt, self.ended)
                # kill the game
        # kill asteroids
        to_delete = []
        for i in range(len(self.asteroids)):
            if self.asteroids[i][1] < (-H / 2):
                to_delete = [i] + to_delete
        # print("New iter")
        # print(self.asteroids)
        # print(to_delete)
        if len(to_delete) > 0:
            for i in range(len(to_delete)):
                del self.asteroids[to_delete[i]]
        # print(self.asteroids)
        # generate asteroids
        if random.random() > self.ast_thresh:
            temp_x = random.random() * W
            temp_x = round(temp_x / 20) * 20
            temp_x -= W / 2
            self.asteroids.append([temp_x, H / 2])
        # change speed if needed
        if (self.iter_cnt % 50) == 0:
            self.ast_thresh -= 0.1
            self.ast_speed += 5
        # incr. iter_cnt
        self.iter_cnt += 1

        return (self.iter_cnt, self.ended)

    def generateOutput(self):
        out = np.ones((1, 42))
        for asteroid in self.asteroids:
            if (out[0][round((asteroid[0] + W / 2) / 20)] > (asteroid[1] + H / 2) / H):
                out[0][round((asteroid[0] + W / 2) / 20)] = (asteroid[1] + H / 2) / H
        out[0][41] = (self.x * 2) / W
        return out

def showState():
    ship.drawShip()
    asterlist = []
    for asteroid in ship.asteroids:
        aster = Asteroids()
        aster.hideturtle()
        aster.drawAsteroids(asteroid[0], asteroid[1])
        # time.sleep(1)
        asterlist.append(aster)
        # aster.reset()
        # aster.hideturtle()
        # move(aster, asteroid[0], asteroid[1])
    for a in asterlist:
        a.hideturtle()
        a.reset()
        a.hideturtle()

gameArea = GameArea()
ship = Ship()


tmpfile = os.path.join('.', 'tmp.svg')  # name of file to save SVG to

buffer = "./steps/gen%d.txt" % (6)
file = open(buffer, 'r')
a = file.read()
print(len(a))

for iter in range(len(a)):
    # print(iter)
    # aa = np.int(a.split(';')[iter])
    aa = a.split(';')[iter]
    # print(type(int(aa)))
    # print(aa)
    aaa = int(aa)
    # print(isinstance(aaa, int))
    # print(np.int(a.split(';')[iter]))
    (fitness, ended) = ship.iterate(aaa)
    # ship.move()
    showState()
    # canv = wn.getcanvas()
    # ts = wn.getscreen()
    # a = "teszt" + str(iter)
    # ts = turtle.getscreen()

    # img = Image.open('teszt0.eps')
    wn.update()
    # canvas = wn.getcanvas()
    # canvas.postscript(file = str(a) + '.eps')
    # img.show
    # wn.reset()
    # wn.update()
    # time.sleep(1)
    # img.save('ez.png')
    print("iteration %d" % iter)
    # print(ship.x)
    # print(ship.generateOutput())
    # game.show()
    # if ended:
    #     break

exit()
