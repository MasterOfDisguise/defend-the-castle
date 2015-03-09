__author__ = 'Simon'
import pygame
import sys
import json
import eztext
pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
running = 1
black = (0, 0, 0)
white = (255, 255, 255)
f = open('saved_data', 'r')
saved_data = json.load(f)
saved_money = saved_data[0]
