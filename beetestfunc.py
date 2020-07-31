#-*- coding: utf-8 -*-

import matplotlib.pylab as pylab

def plotswarm (hive_inst, x_index, y_index):
	"""Нарисовать рой с помощью PyLab"""
	x = []
	y = []

	x_best = []
	y_best = []
	
	x_sel = []
	y_sel = []
	
	for curr_bee in  hive_inst.swarm:
		if curr_bee in hive_inst.bestsites:
			x_best.append (curr_bee.position[x_index])
			y_best.append (curr_bee.position[y_index])
		
		elif curr_bee in hive_inst.selsites:
			x_sel.append (curr_bee.position[x_index])
			y_sel.append (curr_bee.position[y_index])
		
		else:		
			x.append (curr_bee.position[x_index])
			y.append (curr_bee.position[y_index])		

	pylab.clf()

	pylab.scatter (x, y, c = 'k', s=1, marker='o')
	
	if len (x_sel) != 0:
		pylab.scatter (x_sel, y_sel, c = 'y', s=20, marker='o')
	
	pylab.scatter (x_best, y_best, c = 'r', s=30, marker='o')
		
	pylab.draw()

def plotfitness (stat, runnumber):
	"""Вывести значение целевой функции в зависимости от номера итерации"""
	x = range (len (stat.fitness[runnumber]) )
	y = stat.fitness[runnumber]
	
	pylab.plot (x, y)
	pylab.xlabel ("Iteration")
	pylab.ylabel ("Fitness")
	pylab.grid (True)
	
def plotaveragefitness (stat):
	"""Вывести усредненное по всем запускам значение целевой функции в зависимости от номера итерации"""
	x = range (len (stat.fitness[0]) )
	y = [val for val in stat.fitness[0] ]
	
	for runnumber in range(1, len (stat.fitness)):
		for iter in range(len(stat.fitness[runnumber])):
			y[iter] += stat.fitness[runnumber][iter]
	
	y = [val / len (stat.fitness) for val in y]
	
	pylab.plot (x, y)
	pylab.xlabel ("Iteration")
	pylab.ylabel ("Fitness")
	pylab.grid (True)
	

def plotpositions (stat, runnumber, posindex):
	"""Вывести график сходимости искомых величин"""
	x = range (len (stat.positions[runnumber] ) )
	vallist = []

	for positions in stat.positions[runnumber]:					
		vallist.append (positions[posindex] )
			
	pylab.plot (x, vallist)
	pylab.xlabel ("Iteration")
	pylab.ylabel ("Position %d" % posindex)
	pylab.grid (True)


def plotrange (stat, runnumber, posindex):
	"""Вывести график уменьшения областей"""
	x = range (len (stat.range[runnumber] ) )
	vallist = []

	for currange in stat.range[runnumber]:					
		vallist.append (currange[posindex] )
			
	pylab.plot (x, vallist)
	pylab.xlabel ("Iteration")
	pylab.ylabel ("Range %d" % posindex)
	pylab.grid (True)	
	
def plotstat (stat):
	"""Нарисовать статистику"""
	pylab.ioff()
	
	# Вывести изменение целевой функции в зависимости от номера итерации
	# pylab.figure()
	# plotfitness(stat, 0)

	# Вывести усредненное по всем запускам изменение целевой функции в зависимости от номера итерации
	# pylab.figure()
	# plotaveragefitness (stat)
	
	# Вывести сходимость положений лучшей точки в зависимости от номера итерации
	# pylab.figure ()
	# poscount = len (stat.positions[0][0])

	# for n in range(poscount):
	# 	pylab.subplot (poscount, 1, n + 1)
	# 	plotpositions (stat, 0, n)

	# Вывести изменение размеров областей в зависимости от номера итерации
	# pylab.figure ()
	# rangecount = len (stat.range[0][0])
	#
	# for n in range (rangecount):
	# 	pylab.subplot (rangecount, 1, n + 1)
	# 	plotrange (stat, 0, n)

	
	pylab.show ()