# -*- coding: utf-8 -*-
from tkinter import Label

import cv2
import numpy as np
from PIL import ImageTk, Image

__author__ = 'wachs'


class CvWidget(Label):
	def __init__(self, root, timg: np.ndarray, **kw):
		img = cv2.cvtColor(timg, cv2.COLOR_BGR2RGB)
		iimg = Image.fromarray(img)
		self.pimg = ImageTk.PhotoImage(iimg)
		self.root = root
		super().__init__(root, image=self.pimg, **kw)

	def changeImage(self, timg: np.ndarray):
		img = cv2.cvtColor(timg, cv2.COLOR_BGR2RGB)
		iimg = Image.fromarray(img)
		self.pimg = ImageTk.PhotoImage(iimg)
		self.configure(image=self.pimg)
