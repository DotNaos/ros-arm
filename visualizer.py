import json
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np



class Visualizer:
  def __init__(self):
    # Create a empty array in shape:
    # [
    #   [0. 0. 0.]
    #   [0. 0. 0.]
    #   ...
    # ]
    self.vertecies = np.zeros((21, 3))

    #Init hand / fingers
    self.fingers = np.array([
       [0, 1, 2, 3, 4],
       [0, 5, 6, 7, 8],
       [9, 9, 10, 11, 12],
       [13, 13, 14, 15, 16],
       [0, 17, 18, 19, 20],
       [2, 5, 9, 13, 17]
    ])

    print(self.vertecies)
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -5)
    glScalef(2, -2, 2)

  def run(self):
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              quit()

      # glRotatef(1, 3, 1, 1)
      glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
      self.render()
      pygame.display.flip()
      pygame.time.wait(10)

  def update(self, message : json):
    self.data = json.loads(message)

    # Data is a dictionary of the form:
    #   {"landmarks":[[
    #   {"x":0.0,"y":0.0,"z":0.0},
    #   ]], "worldLandmarks":[], "handednesses":[], "handedness":[]}

    if (self.data["landmarks"] == []):
      return

    for i in range(len(self.data["landmarks"][0])):
      for j in range(3):
        key = 'x' if j == 0 else 'y' if j == 1 else 'z'
        self.vertecies[i][j] = self.data["landmarks"][0][i][key]

    print(self.vertecies)



  def render(self):
    # Draw hand-knuckles

    glBegin(GL_POINTS)
    for vertex in self.vertecies:
        glVertex3fv(vertex)
    glEnd()

    # Draw fingers
    glBegin(GL_LINES)
    for finger in self.fingers:
       temp = 0
       for knuckle in finger:
          glVertex3fv(self.vertecies[temp])
          glVertex3fv(self.vertecies[knuckle])
          temp = knuckle
    glEnd()



