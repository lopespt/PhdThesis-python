# -*- coding: utf-8 -*-
from math import sqrt, pi, atan2

import cv2
import numpy as np

from SunDatabaseReader import SunImageObject

__author__ = 'wachs'


def normalize(x, min, max, steps, nmin=0, nmax=1):
	steps = steps
	width = (max - min) / steps
	bin = None
	if (type(x) == np.ndarray):
		bin = ((x - min - width / 2) / width).astype(np.uint8)
	else:
		bin = int((x - min - width / 2) / width)

	nbin = bin / steps

	return nbin * (nmax - nmin) + nmin


def area(obj: SunImageObject, disc=10):
	c = cv2.countNonZero(obj.getMaskImage()[:, :, 1])
	c = c / obj.getMaskImage()[:, :, 1].size
	return normalize(c, 0, 1, disc)


def hsv(obj: SunImageObject, h=18, s=3, v=3, y=10):
	imgHsv = cv2.cvtColor(obj.getSunImage().getImage(), cv2.COLOR_BGR2HSV)
	mk = obj.getMaskImage()[:, :, 1].squeeze()

	h: np.ndarray = cv2.calcHist([imgHsv], [0, 1, 2], mk, [h, s, v], [0, 180, 0, 256, 0, 256])
	imgHsv = None
	h = h.flatten() / h.sum()
	h = normalize(h, 0, 1, y)
	return h


def angle(obj: SunImageObject, disc=10):
	def dist(p1, p2):
		return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

	first = True
	dmax = 0
	p1 = None
	p2 = None
	for i in obj.polygon:
		for j in obj.polygon:
			d = dist(i, j)
			if first or d > dmax:
				dmax = d
				p1 = i
				p2 = j
			first = False

	ang = 0
	if p2[0] == p1[0]:
		ang = pi
	else:
		p2, p1 = (p2, p1) if p2[1] > p1[1] else (p1, p2)
		ang = atan2(p2[1] - p1[1], p2[0] - p1[0])
	assert (ang >= 0)
	return normalize(ang, 0, pi, disc)
