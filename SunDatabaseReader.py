# -*- coding: utf-8 -*-
import datetime as dt
import os
from datetime import datetime
from typing import Union, List, Iterable, Tuple
from xml.etree import ElementTree
from xml.etree.ElementTree import ParseError

import cv2
import numpy as np

__author__ = 'wachs'


class SunImageObject:
	def __init__(self, img: "SunImage", id: int, name: str, deleted: bool, verified: bool, date: datetime,
	             polygon: List[Tuple[int, int]]):
		self.id = id
		self.name = name
		self.deleted = deleted
		self.verified = verified
		self.date = date
		self.polygon = polygon
		self.img = img
		self.maskedOriginal = None
		self.maskImage = None

	def getMaskImage(self) -> Union[np.ndarray, None]:
		if self.maskImage is None:
			self.maskImage = np.zeros(self.img.getImage().shape,dtype=np.uint8)
			cv2.fillPoly(self.maskImage, np.array([self.polygon]), (255, 255, 255))

		return self.maskImage

	def getMaskedOriginal(self):
		if self.maskedOriginal is None:
			self.maskedOriginal = ((self.getMaskImage() / 255.0) * self.img.getImage()).astype(np.uint8)
		return self.maskedOriginal

	def getSunImage(self):
		return self.img


class SunImage(object):
	def __init__(self, imagePath, annotationsPath):
		self.image = None
		self.annotationsXml = None
		self.annotations = None
		self.imagePath = imagePath
		self.annotationsPath = annotationsPath
		self.objects = None

	def getImage(self) -> Union[np.ndarray, None]:
		if self.image is None:
			self.image = cv2.imread(self.imagePath)
		return self.image

	def getAnnotationsXml(self) -> Union[ElementTree.ElementTree, None]:
		try:
			if self.annotationsXml is None:
				self.annotationsXml = ElementTree.parse(self.annotationsPath)
			return self.annotationsXml
		except ParseError:
			print("Error while parsing ", self.annotationsPath)

	def getObjects(self):
		def parseOneObj(xmlElem: ElementTree.Element):
			name = xmlElem.find('name').text.strip()
			deleted = xmlElem.find('deleted').text.strip() == '1'
			verified = xmlElem.find('verified').text.strip() == '1'
			date = dt.datetime.strptime(xmlElem.find('date').text.strip(), "%d-%b-%Y %H:%M:%S")
			id = xmlElem.find('id')
			if id is not None:
				id = id.text.strip()
			polygon = [[int(el.find("x").text.strip()), int(el.find("y").text.strip())] for el in
			           xmlElem.find("polygon").findall("pt")]
			return SunImageObject(self, id, name, deleted, verified, date, polygon)

		self.objects = [parseOneObj(xml) for xml in self.getAnnotationsXml().findall("object")]
		return self.objects


class SunDatabaseReader(Iterable[SunImage]):
	def __init__(self, basePath: str) -> None:
		self.basePath = basePath
		self.imagesIt = os.walk(os.path.join(self.basePath, "Images"))
		self.annotationsIt = os.walk(os.path.join(self.basePath, "annotations"))

	def __iter__(self):
		try:
			while True:
				r1, _, f1 = next(self.imagesIt)
				r2, _, f2 = next(self.annotationsIt)

				f1 = filter(lambda x: not x.endswith(".swp"), f1)
				f2 = filter(lambda x: not x.endswith(".swp"), f2)

				for ff1, ff2 in zip(f1, f2):
					assert (os.path.basename(ff1)[:-3] == os.path.basename(ff2)[:-3])
					yield SunImage(os.path.join(r1, ff1), os.path.join(r2, ff2))
		except StopIteration:
			pass
