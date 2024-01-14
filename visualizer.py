import json
import matplotlib.pyplot as plt
import numpy as np
import time


class Visualizer:
  def __init__(self):
    self.data = {}
    self.fig = plt.figure()
    self.ax = plt.axes(projection="3d")
    self.graph = self.ax.scatter([], [], [], c="r", marker="o")

  def update(self, message : json):
    self.data = json.loads(message)

    self.visualize()

  # Data is a dictionary of the form:
  #   {"landmarks":[[
  #   {"x":0.0,"y":0.0,"z":0.0},
  #   ]], "worldLandmarks":[], "handednesses":[], "handedness":[]}

  # Visualize the data in a 3D plot
  #
  def visualize(self):
    landmarks = self.data["landmarks"]
    if landmarks == []:
      return

    x = []
    y = []
    z = []
    for landmark in landmarks[0]:
      x.append(landmark["x"])
      y.append(landmark["y"])
      z.append(landmark["z"])
    self.graph._offsets3d = (x, y, z)
    plt.draw()
    plt.pause(0.001)

