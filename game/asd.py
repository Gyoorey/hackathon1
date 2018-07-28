import turtle
import random
from random import Random
import os
import numpy as np

H = 600
W = 820
player_offset = 10
player_y = -H / 2 + player_offset
playerwidth = 30
playerspeed = W / 41

class GameArea():
    def __init__(self):
        wn = turtle.Screen()
        # wn.setup(W + 20, H + 20)
        wn.bgcolor("pink")
        wn.title("Hackathon Invaders")

        self.border_pen = turtle.Turtle()
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

        self.player = turtle.Turtle()
        self.player.color("black")
        self.player.shape("triangle")
        self.player.penup()
        self.player.speed(0)
        self.player.setposition(self.x, player_y)
        self.player.setheading(90)



class Game:
    def __init__(self):
        self.x = 0
        self.screen = None
        self.player = None
        self.asteroids = []
        self.ast_thresh = 0.95
        self.iter_cnt = 0
        self.ast_speed = 10
        self.r = Random(0)
        self.ended = False

    def exit(self):
        turtle.done()

    def show(self):
        self.screen = turtle.Screen()
        self.screen.setup(W + 20, H + 20)
        self.screen.bgcolor("pink")
        self.screen.title("Hackathon Invaders")
        # draw border
        border_pen = turtle.Turtle()
        border_pen.speed(0)
        border_pen.penup()
        border_pen.setposition(-W / 2, H / 2)
        border_pen.pendown()
        border_pen.pensize(3)
        border_pen.fd(W)
        border_pen.rt(90)
        border_pen.fd(H)
        border_pen.rt(90)
        border_pen.fd(W)
        border_pen.rt(90)
        border_pen.fd(H)
        border_pen.hideturtle()
        # draw player
        self.player = turtle.Turtle()
        self.player.color("black")
        self.player.shape("triangle")
        self.player.penup()
        self.player.speed(0)
        self.player.setposition(self.x, player_y)
        self.player.setheading(90)
        # draw asteroids

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
        if self.r.random() > self.ast_thresh:
            temp_x = self.r.random() * W
            temp_x = round(temp_x / 20) * 20
            temp_x -= W / 2
            self.asteroids.append([temp_x, H / 2])
            # self.asteroids[-1].color("red")
            # self.asteroids[-1].shape("circle")
            # self.asteroids[-1].penup()
            # self.asteroids[-1].speed(0)
            # self.asteroids[-1].setheading(270)
            # self.asteroids[-1].setposition(temp_x, H/2)
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


a = GameArea()
game = Game()
for iter in range(100):
    (fitness, ended) = game.iterate(-1)
    print("iteration %d" % iter )
    print(game.generateOutput())
    # game.show()
    if ended:
        break
    #delay(100)
game.exit()