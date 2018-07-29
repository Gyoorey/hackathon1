import turtle
import random
from random import Random
import os
import numpy as np
import math
import cv2

H = 600
W = 840
num_of_cols = int(21) #should be even
player_offset = 20
player_y = player_offset
playerwidth = W / num_of_cols
playerspeed = W / num_of_cols #one column
output_width = int(11) #should be even
half_out_width = int((output_width-1)/2)


class Game:
    def __init__(self):
        self.x = 0
        self.col = int(round((num_of_cols-1)/2))
        self.asteroids = []
        self.ast_thresh = 0.5
        self.iter_cnt = 0
        self.ast_speed = 40
        self.r = Random(0)
        self.ended = False
        self.col_available = np.zeros((1,num_of_cols))

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
    
    def processLogfile(self, genNum):
        log_filename = 'steps\gen%d.txt'%genNum
        print('Processing: %s'%log_filename)
        file = open(log_filename, "r")
        seqString = file.readline()
        #print(seqString)
        nums_as_strings = seqString.split(";")
        nums = [int(n) for n in nums_as_strings[:-1]]
        #print(nums)
        video_name = 'steps\gen%d.avi'%genNum
        self.animateSeq(nums,video_name)
    
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
        self.r = Random(self.iter_cnt)
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
            #if abs(self.col - asteroid[0])<3 and asteroid[1] <= player_y + playerwidth:
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
                if self.col_available[0][self.asteroids[to_delete[i]][0]] > 0:
                    self.col_available[0][self.asteroids[to_delete[i]][0]] -= 1
                del self.asteroids[to_delete[i]]
        # print(self.asteroids)
        # generate asteroids
        if self.r.uniform(0,1) >= self.ast_thresh:
            free_col = False
            col_cnt = 0
            while not free_col or col_cnt>num_of_cols:
                temp_col = self.r.randint(0,num_of_cols-1)
                if self.col_available[0][temp_col] < 2:
                    self.asteroids.append([temp_col, H])
                    self.col_available[0][temp_col] += 1
                    free_col = True
                else:
                    col_cnt +=1
        # change speed if needed
        if (self.iter_cnt % 100) == 0:
            self.ast_thresh -= 0.05
            #self.ast_speed += 5
        # incr. iter_cnt
        self.iter_cnt += 1
        return (self.iter_cnt, self.ended)
        

    def generateOutput(self):
        out = np.ones((1, num_of_cols))
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
            if self.col+i>num_of_cols-1:
                break
            out2[0][half_out_width+i] = out[0][self.col+i]
        #print(out2)
        return out2