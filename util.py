import copy
import pygame
import math
import random
import os

class Stack:
    def __init__(self):
        self.list = []
        self.list.append([])
        self.headIndex = 0
    
    def append(self, item):
        if self.headIndex < len(self.list) - 1:
            self.list = self.list[0:self.headIndex + 1]
        self.list.append(copy.deepcopy(item))
        self.headIndex += 1
        return self.list[self.headIndex]
    
    def peek(self):
        return self.list[self.headIndex]

    def pop(self):
        if self.headIndex > 0:
            self.headIndex -= 1
        return self.list[self.headIndex]
        
    def unpop(self):
        if self.headIndex < len(self.list) - 1:
            self.headIndex += 1
        return self.list[self.headIndex]
    
    def print(self):
        print("############# Stack Contents #################")
        for i in range(self.headIndex + 1):
            print(self.list[i])
        print("##############################################")

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def computeBezier(p1,c1,c2,p2):
    # Draw the Bezier curve as 100 tiny segments
    line_seg = []
    steps = 100
    for i in range(steps + 1):
        t = i/steps
        x = p1[0]*(1-t)**3 + 3*c1[0]*t*(1-t)**2 + 3*c2[0]*t*t*(1-t) + p2[0]*t**3
        y = p1[1]*(1-t)**3 + 3*c1[1]*t*(1-t)**2 + 3*c2[1]*t*t*(1-t) + p2[1]*t**3
        line_seg.append((x, y))
    return line_seg


def read_shape(filename):
    # Reads a shape from a file and returns it as a list
    # Every element is delimited by a newline
    # An element is either a pair of numbers delimted by a comma (Point)
    # Or a 4 numbers delimted by commas (Bezier Control Points)

    # Open the file
    file = open(filename, "r")
    # Read the file
    lines = file.readlines()
    # Close the file
    file.close()

    # Parse the file
    shape = []
    for line in lines:
        # Split the line into a list of strings
        line = line.split(",")
        # Convert the strings into numbers
        for i in range(len(line)):
            line[i] = float(line[i])
        if len(line) != 2 and len(line) != 4:
            print("Error: Invalid Line in Shape File")
            return None
        # Add the line to the shape
        shape.append(tuple(line))
    
    return shape   

def to_pygame_coords(coord, width, height):
        # Convert the point to pygame coordinates
        return (coord[0] + width/2, height/2 - coord[1])

def to_central_origin_coords(coord, width, height):
    # Convert the point to central origin coordinates
    return (coord[0] - width/2, height/2 - coord[1])

def convert_shape_to_central_origin_coords(shape, width, height):
    # Convert the shape to central origin coordinates
    for i in range(len(shape)):
        if len(shape[i]) == 2:
            shape[i] = to_central_origin_coords(shape[i], width, height)
        elif len(shape[i]) == 4:
            c1 = to_central_origin_coords(shape[i][0:2], width, height)
            c2 = to_central_origin_coords(shape[i][2:4], width, height)
            shape[i] = (c1[0], c1[1], c2[0], c2[1])
        else:
            print("Error: Invalid Shape")
            exit(-1)
    return shape

def convert_shape_to_pygame_coords(shape, width, height):
    # Convert the shape to pygame coordinates
    for i in range(len(shape)):
        if len(shape[i]) == 2:
            shape[i] = to_pygame_coords(shape[i], width, height)
        elif len(shape[i]) == 4:
            c1 = to_pygame_coords(shape[i][0:2], width, height)
            c2 = to_pygame_coords(shape[i][2:4], width, height)
            shape[i] = (c1[0], c1[1], c2[0], c2[1])
        else:
            print("Error: Invalid Shape")
            exit(-1)
    return shape