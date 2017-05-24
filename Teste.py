# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor

import cv2
import networkx as nx
import numpy as np
#import matplotlib.pyplot as plt

import ComplexNetwork
from ImageFeatures import area, hsv, angle
from SunDatabaseReader import SunDatabaseReader

__author__ = 'wachs'

a = SunDatabaseReader("/Users/wachs/Desktop/SUN2012")


def cl():
	img = np.zeros((50, 500, 3), np.uint8)

	cm = []
	for h in range(0, 180):
		for s in range(0, 256):
			for v in range(0, 256):
				cm.append([h, s, v])

	tot = 180 * 256 * 256

	for i in range(0, 50):
		for j in range(0, 500):
			img[i, j, :] = cm[int(j / 500. * tot)]

	cv2.cvtColor(img, cv2.COLOR_HSV2BGR, img)

	return img


def ab(k):
	i = k[1]
	idx = k[0]
	for j in i.getObjects():
		# print(idx,area(j))
		# print(idx,angle(j))
		# print(idx,hsv(j).size)
		area(j)
		angle(j)
		hsv(j)
	return "Processo %d terminado" % idx


def inicia():
	print("comecou")
	aa = []
	with ThreadPoolExecutor(20) as ex:
		aa = ex.map(ab, enumerate(a))
	for i in aa:
		print(i)
	print("terminou")


g = ComplexNetwork.Network()
ComplexNetwork.buildNetwork(g, a)
nx.write_graphml(g, "teste.txt")
#g = ComplexNetwork.Network(nx.read_graphml("teste.txt"))
# print(g.number_of_nodes())
# print(g.number_of_edges())
#cc = nx.degree_histogram(g)
#plt.plot(cc)
#plt.show()

# nx.write_multiline_adjlist(g, "teste.txt")
