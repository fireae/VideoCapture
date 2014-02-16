#!/usr/bin/python
#videocapture.py
# --author-- fireae

import sys
import cv2
from PyQt4 import QtGui, QtCore
import time
import numpy as np


class VideoWin(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent);
		
		self.resize(640, 480);
		self.setWindowTitle('VideoCapture');
		
		# start menu
		self.start = QtGui.QAction(QtGui.QIcon(''), 'Start', self);
		self.start.setShortcut('Ctrl+S');
		self.start.setStatusTip('Start capture.');
		
		# stop menu
		self.stop = QtGui.QAction(QtGui.QIcon(''), 'Stop', self);
		self.stop.setShortcut('Ctrl+E');
		self.stop.setStatusTip('Stop capture.');
	
		self.menubar = self.menuBar();
		self.video = self.menubar.addMenu('&Video');
		self.video.addAction(self.start);
		self.video.addAction(self.stop);

		# self.image display image
		self.image = QtGui.QImage()
	
		# timer used for capture video
		self.timer = Timer();
		
		# camera with cv2
		self.capture = cv2.VideoCapture(0);
		if self.capture is None or not self.capture.isOpened():
			self.statusBar().showMessage('can not open video.');
		
		# signal and slot
		self.connect(self.timer, QtCore.SIGNAL('updateTime()'), self.captureVideo);
		self.start.connect(self.start, QtCore.SIGNAL('triggered()'), self.startCapture);
		self.stop.connect(self.stop, QtCore.SIGNAL('triggered()'), self.stopCapture);	


	def startCapture(self):
		self.timer.start();
		
	def captureVideo(self):
		ret, frame = self.capture.read();
		self.showImage(frame);
		self.update();

	def stopCapture(self):
		self.timer.stop();

	# rewrite paintEvent, display image;
	def paintEvent(self, event):
		painter = QtGui.QPainter(self);
		painter.drawImage(self.rect(), self.image, self.image.rect());

	# convert cv2.capture.read() image to QImage(), to display
	def showImage(self, img):
		h, w, cn = img.shape
		step = w*cn;
		self.image = QtGui.QImage(img, w, h, step, QtGui.QImage.Format_RGB888).rgbSwapped();

class Timer(QtCore.QThread):
	def __init__(self, signal='updateTime()', parent=None):
		super(Timer, self).__init__(parent);
		self.stopped = False
		self.signal = signal;
		self.mutex = QtCore.QMutex();
	
	def run(self):
		with QtCore.QMutexLocker(self.mutex):
			self.stopped = False;
		while True:
			if self.stopped:
				return;
			# every 0.2 seconds emit a signal	
			self.emit(QtCore.SIGNAL(self.signal));
			time.sleep(0.2);

	def stop(self):
		with QtCore.QMutexLocker(self.mutex):
			self.stopped = True;
	def isStopped(self):
		with QtCore.QMutexLocker(self.mutex):
			return self.stopped;


if __name__ == '__main__':
		
	app = QtGui.QApplication(sys.argv)
	win= VideoWin();
	win.show();
	sys.exit(app.exec_());

