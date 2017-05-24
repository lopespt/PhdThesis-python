# -*- coding: utf-8 -*-
import unittest
from typing import List

import SunDatabaseReader
from ImageFeatures import area, hsv, angle
from SunDatabaseReader import SunImage

__author__ = 'wachs'


class TestSunReader(unittest.TestCase):
	def setUp(self):
		self.reader = SunDatabaseReader.SunDatabaseReader("./DatabaseFolder/")

	def test_files(self):
		self.assertEqual(len(list(self.reader)), 1)

	def test_imageOpen(self):
		for a in self.reader:
			self.assertIsNotNone(a.getImage().shape)

	def test_area(self):
		l: List[SunImage] = list(self.reader)
		a = area(l[0].getObjects()[0], 100)
		self.assertAlmostEqual(a, 0.02, delta=0.01)

	def test_hsv(self):
		l: List[SunImage] = list(self.reader)
		a = hsv(l[0].getObjects()[0], y=100)
		v = [0] * 162
		v[4] = 1
		for i, j in zip(a, v):
			self.assertAlmostEqual(i, j, delta=0.035)

		a = hsv(l[0].getObjects()[1], y=100)
		v = [0] * 162
		v[38] = 1
		for i, j in zip(a, v):
			self.assertAlmostEqual(i, j, delta=0.035)

	def test_angle(self):
		l: List[SunImage] = list(self.reader)
		a = angle(l[0].getObjects()[0], 50)
		#print(a)
		self.assertAlmostEqual(a, 0.22, delta=0.01)

	def test_obj_parse(self):
		objs = []
		for i in self.reader:
			objs = list([k.name for k in i.getObjects()])
			break

		self.assertListEqual(objs, ['obj 1', 'obj 2'], "Object Parser Error")
