# -*- coding: utf-8 -*-
import concurrent.futures
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor

import networkx as nx

from ImageFeatures import hsv, area, angle
from SunDatabaseReader import SunDatabaseReader, SunImage

__author__ = 'wachs'


class Network(nx.DiGraph):
	def __init__(self, data=None, **kwargs):
		super().__init__(data, **kwargs)


def features(image: SunImage):
	for obj in image.getObjects():
		yield (0, tuple(hsv(obj, y=10)))
		yield (1, area(obj, 10))
		yield (2, angle(obj, 10))


def featuresProc(image: SunImage):
	v = []
	for obj in image.getObjects():
		v.append((0, tuple(hsv(obj, y=10))))
		v.append((1, area(obj, 10)))
		v.append((2, angle(obj, 10)))
	return v


def buildNetwork(graph: Network, reader: SunDatabaseReader):
	with ThreadPoolExecutor(10) as ex:
		futs = {ex.submit(features, img): idx for idx, img in enumerate(list(reader))}

		for feat in concurrent.futures.as_completed(futs):
			allFeat = feat.result()
			idx = futs[feat]
			for ia, a in enumerate(allFeat):
				for ib, b in enumerate(allFeat):
					if ia != ib:
						if graph.has_edge(a, b):
							graph[a][b]['w'] += 1
						else:
							graph.add_edge(a, b, {"w": 1})
			print(graph.number_of_nodes(), graph.number_of_edges())
