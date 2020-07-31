# -*- coding: utf-8 -*-
import random
from queue import Queue
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animtion
import numpy as np
import BeeAndHive
from PIL import Image


speedlost = 5
side = 350
CountPick = 10
class Field:
	def __init__(self):
		self.ind = 0
		self.IND = 0
		self.AllVersionMatrix = []
		global side, CountPick
		self.matrix = [[0 for i in range(side)] for i in range(side)]
		self.PositionPicks = []
		for n in range(CountPick):
			self.PositionPicks.append(
				[random.randint(0, side-1),
				 random.randint(0, side-1)])
		self.step = [
			[1, 0], [-1, 0],
			[0, 1], [0, -1],
			[1, 1], [-1, -1],
			[1, -1], [-1, 1]
		]

		q = Queue()
		speedlost = 5

		# node = [[x, y], weight, speed_delete]
		for i in self.PositionPicks:
			self.matrix[i[0]][i[1]] = 255 - random.randint(0, 5) * 10
			tmp = random.randint(speedlost, speedlost*3)
			print([i, 255 - q.qsize() * 10, tmp])
			q.put([i, 255 - q.qsize() * 10, tmp])

		while not q.empty():
			node = q.get()

			# if node[1] - speedlost <= 0:
			# 	continue
			for i in self.step:
				if 0 <= node[0][0] + i[0] <= side - 1 and 0 <= node[0][1] + i[1] <= side - 1 \
						and self.matrix[node[0][0] + i[0]][node[0][1] + i[1]] < node[1] - node[2] - max(0, (
						math.sqrt(i[0] ** 2 + i[1] ** 2) - 1)) * node[2]:
					self.matrix[node[0][0] + i[0]][node[0][1] + i[1]] = node[1] - node[2] - max(0, (
							math.sqrt(i[0] ** 2 + i[1] ** 2) - 1)) * node[2]
					q.put([[node[0][0] + i[0], node[0][1] + i[1]],
						   self.matrix[node[0][0] + i[0]][node[0][1] + i[1]], node[2]])

		self.AllVersionMatrix.append(self.matrix)
		self.fig, self.ax = plt.subplots()
		self.DrawPicture(self.matrix)
	# self.DrawPlot()

	def DrawPlot(self):
		# plt.clf()
		# self.ax.clear()
		# plt.clf()
		# self.fig, self.ax = plt.subplots()
		# self.ax.

		self.ax.clear()
		self.ax.set_facecolor('#f5deb3')
		ColorField = [245 / 255, 222 / 255, 179 / 255]
		x, y, color = [], [], []
		for i in range(len(self.matrix)):
			for j in range(len(self.matrix[i])):
				if self.matrix[i][j] != 0:
					# tmp = 255 - self.matrix[i][j]
					# tmp /= 255
					tmp = 1 - self.matrix[i][j] / 255
					color.append([ColorField[0] * tmp, ColorField[1] * tmp, ColorField[2] * tmp])
					# color.append(str(tmp))
					x.append(i)
					y.append(j)

		self.ax.scatter(0, 0, c=['#f5deb3'])
		self.ax.scatter(side - 1, side - 1, c=['#f5deb3'])
		self.ax.scatter(x, y, c=color)

		print('kek')
		# fig.set_figwidth(8)     #  ширина и
		# fig.set_figheight(8)    #  высота "Figure"
		plt.draw()
	# plt.show()

	def KillPick(self, a):
		speedlost = 5
		q = Queue()
		q.put(a)
		self.matrix[a[0]][a[1]] = 0
		while not q.empty():
			node = q.get()

			for i in self.step:
				if 0 <= node[0] + i[0] <= side - 1 and 0 <= node[1] + i[1] <= side - 1 \
						and self.matrix[node[0] + i[0]][node[1] + i[1]] > random.randint(speedlost, speedlost*2):
					self.matrix[node[0] + i[0]][node[1] + i[1]] = 0
					q.put([node[0] + i[0], node[1] + i[1]])
		# self.AllVersionMatrix.append(self.matrix)
	# self.ax.clear()
	# self.DrawPlot()
		self.DrawPicture(self.matrix)

	def DrawPicture(self,matrix):
		w, h = side, side
		a = np.zeros((h, w, 3), dtype=np.uint8)
		for i in range(len(matrix)):
			for j in range(len(matrix[i])):
				ColorField = [245, 222, 179]
				tmp = 1-matrix[len(matrix)-i-1][j]/255
				a[i][j] = ColorField
				for k in range(3):
					a[i][j][k] = int(a[i][j][k]*tmp)
			# # print(-tmp + 255, end=' ')
			# a[i][j] = [tmp, tmp, tmp]

		img = Image.fromarray(a, 'RGB')
		img.save("pic/"+str(self.IND)+'.png')
		self.IND += 1
		# img.show()

	def animate(self, qwe):
		if self.ind >= len(self.AllVersionMatrix):
			self.ind = len(self.AllVersionMatrix)-1
		matrix = self.AllVersionMatrix[self.ind]
		self.ax.clear()
		self.ax.set_facecolor('#f5deb3')

		ColorField = [245 / 255, 222 / 255, 179 / 255]
		x, y, color = [], [], []
		for i in range(len(matrix)):
			for j in range(len(matrix[i])):
				if matrix[i][j] != 0:
					tmp = 1 - matrix[i][j] / 255

					color.append([ColorField[0] * tmp, ColorField[1] * tmp, ColorField[2] * tmp])
					x.append(i)
					y.append(j)

		self.ax.scatter(0, 0, c=['#f5deb3'])
		self.ax.scatter(side - 1, side - 1, c=['#f5deb3'])
		self.ax.scatter(x, y, c=color)
		self.ind += 1


	def WatchProcces(self):
		cnt = 0
		for i in self.AllVersionMatrix:
			self.DrawPicture(i)
			cnt += 1
	# ani = animtion.FuncAnimation(self.fig, self.animate, init_func=lambda a: a, frame=len(self.AllVersionMatrix), interval=5000)
	# plt.show()

f = Field()


class MapGoodOrBadField(BeeAndHive.FloatBee):
	Count = 2

	@staticmethod
	def GetStartRange():
		return [200] * MapGoodOrBadField.Count

	@staticmethod
	def GetRangeKoeff():
		return [1] * MapGoodOrBadField.Count

	def __init__(self):
		BeeAndHive.FloatBee.__init__(self)
		self.MinVal = [0] * MapGoodOrBadField.Count
		self.MaxVal = [side - 1] * MapGoodOrBadField.Count
		# self.position = [random.uniform(self.MinVal[n], self.MaxVal[n] for n in range(MapGoodOrBadField.Count)]
		self.position = [random.randint(self.MinVal[n], self.MaxVal[n]) for n in range(MapGoodOrBadField.Count)]
		self.CalcFitness()

	def CalcFitness(self):
		"""Расчет целевой функции. Этот метод необходимо перегрузить в производном классе.
		Функция не возвращает значение целевой функции, а только устанавливает член self.fitness
		Эту функцию необходимо вызывать после каждого изменения координат пчелы"""
		self.fitness = 0
		# for val in self.position:
		#     self.fitness -= val**2
		global f
		self.fitness = f.matrix[self.position[0]][self.position[1]]
