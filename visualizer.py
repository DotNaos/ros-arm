import numpy as np
import json
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
class Visualizer:
    def __init__(self):
        # Create an empty array in shape:
        # [
        #   [0. 0. 0.]
        #   [0. 0. 0.]
        #   ...
        # ]

        self.max_hands = 2
        self.vertecies = np.zeros((self.max_hands, 21, 3))

        # Init hand / fingers
        self.fingers = np.array([
            [0, 1, 2, 3, 4],
            [0, 5, 6, 7, 8],
            [9, 9, 10, 11, 12],
            [13, 13, 14, 15, 16],
            [0, 17, 18, 19, 20],
            [2, 5, 9, 13, 17]
        ])

        self.colors = np.array([
        [1,0,0],
        [0,1,0],
        [0,0,1],
        [0,1,0],
        [1,1,1],
        [0,1,1],
        [1,0,0],
        [0,1,0],
        [0,0,1],
        [1,0,0],
        [1,1,1],
        [0,1,1],
        ])

        print(self.vertecies)
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

        glTranslatef(0.0, 0.0, -5)
        glScalef(2, -2, 2)

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.render()
        pygame.display.flip()
        pygame.time.wait(10)

    def update(self, message: json):
        self.data = json.loads(message)

        # Data is a dictionary of the form:
        #   {"landmarks":[[
        #   {"x":0.0,"y":0.0,"z":0.0},
        #   ]], "worldLandmarks":[], "handednesses":[], "handedness":[]}
        # if 1 :
        #     return

        if (self.data["landmarks"] == []):
            return

        handcount = min(self.max_hands, len(self.data["landmarks"]))

        for n in range(handcount):
          for i in range(len(self.data["landmarks"][n])):
              for j in range(3):
                  key = 'x' if j == 0 else 'y' if j == 1 else 'z'
                  self.vertecies[n][i][j] = self.data["landmarks"][n][i][key]

        print(self.vertecies)

    def render(self):
        # Draw hand-knuckles
        for vertecies in self.vertecies:
          print(vertecies)

          glColor3f(1.0, 0.0, 0.0)  # Set color to red
          for vertex in vertecies:
              glPushMatrix()
              glTranslatef(vertex[0], vertex[1], vertex[2])
              glScalef(0.2, 0.2, 0.2)
              gluSphere(gluNewQuadric(), 0.1, 4, 4)
              glPopMatrix()

          glColor3f(0.0, 0.0, 0.0)
          # Draw fingers
          glBegin(GL_LINES)
          i = 0
          for finger in self.fingers:
              temp = 0
              glColor3fv(self.colors[-i])
              i += 1
              for knuckle in finger:
                  glVertex3fv(vertecies[temp])
                  glVertex3fv(vertecies[knuckle])
                  temp = knuckle
          glEnd()



