import turtle
import random
from random import Random
import os
import numpy as np
import math
import cv2

H = 600
W = 820
num_of_cols = int(41) #should be even
player_offset = 50
player_y = player_offset
playerwidth = 30
playerspeed = W / num_of_cols #one column
output_width = int(num_of_cols) #should be even
half_out_width = int((output_width-1)/2)


class Game:
    def __init__(self):
        self.x = 0
        self.col = int(round((num_of_cols-1)/2))
        self.asteroids = []
        self.ast_thresh = 0.95
        self.iter_cnt = 0
        self.ast_speed = 10
        self.r = Random(0)
        self.ended = False

    def show(self):
        img = np.zeros((H,W,3), np.uint8)
        #draw ship
        self.x = self.col * int(W/num_of_cols) + int(playerwidth/2)
        #print(self.x)
        x_l = int(self.x-playerwidth/2)
        y_l = int(H-player_y-playerwidth/2)
        x_r = int(self.x+playerwidth/2)
        y_r = int(H-player_y+playerwidth/2)
        cv2.rectangle(img,(x_l,y_l),(x_r,y_r),(0,255,0),3)
        #draw asteroids
        for ast in self.asteroids:
            temp_x = ast[0] * int(W/num_of_cols) + int(playerwidth/2)
            x_l = int(temp_x-playerwidth/2)
            y_l = int(H-ast[1]-playerwidth/2)
            x_r = int(temp_x+playerwidth/2)
            y_r = int(H-ast[1]+playerwidth/2)
            cv2.rectangle(img,(x_l,y_l),(x_r,y_r),(255,0,0),3)
        #cv2.imshow('image',img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        return img
    
    def animateSeq(self, seq, filename):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(filename,fourcc, 10.0, (W,H))
        for i in seq:
            (fitness, ended) = self.iterate(i)
            img = self.show()
            out.write(img)
            if ended:
                break
        out.release()
        

    def iterate(self, key):
        if (self.ended):
            return (self.iter_cnt, self.ended)
        if key == -1 and self.col > 0:
            self.col -= 1
        if key == 1 and self.col < num_of_cols-1:
            self.col += 1
        # move asteroids
        for i in range(len(self.asteroids)):
            self.asteroids[i][1] = self.asteroids[i][1] - self.ast_speed
        # check collision
        for asteroid in self.asteroids:
            if self.col == asteroid[0] and asteroid[1] <= player_y + playerwidth:
                self.ended = True
                return (self.iter_cnt, self.ended)
                # kill the game
        # kill asteroids
        to_delete = []
        for i in range(len(self.asteroids)):
            if self.asteroids[i][1] < 0:
                to_delete = [i] + to_delete
        # print("New iter")
        # print(self.asteroids)
        # print(to_delete)
        if len(to_delete) > 0:
            for i in range(len(to_delete)):
                del self.asteroids[to_delete[i]]
        # print(self.asteroids)
        # generate asteroids
        if self.r.uniform(0,1) > self.ast_thresh:
            temp_col = self.r.randint(0,num_of_cols)
            self.asteroids.append([temp_col, H])
        # change speed if needed
        if (self.iter_cnt % 100) == 0:
            self.ast_thresh -= 0.05
            #self.ast_speed += 5
        # incr. iter_cnt
        self.iter_cnt += 1
        return (self.iter_cnt, self.ended)
        

    def generateOutput(self):
        out = np.ones((1, 41))
        for asteroid in self.asteroids:
            if (out[0][asteroid[0]] > asteroid[1] / H):
                out[0][asteroid[0]] = asteroid[1] / H
        out2 = np.ones((1,output_width))*-1
     
        out2[0][half_out_width] = out[0][self.col]
        #left side
        for i in range(1,half_out_width+1):
            if self.col-i<0:
                break
            out2[0][half_out_width-i] = out[0][self.col-i]
        #rigth side
        for i in range(1,half_out_width+1):
            if self.col+i>output_width-1:
                break
            out2[0][half_out_width+i] = out[0][self.col+i]
        #print(out2)
        return out2