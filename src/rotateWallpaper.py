#! /usr/bin/env python

import os
import time
import random
import sys
from ConfigParser import *

class RotateWallpapers:
	wallpapers = list()
	current_index = 0;
	#delay = 600
	delay = 10
	random_order = False

	def __init__(self, pic_uri_list, delay, index, random_order):
		self.wallpapers = pic_uri_list
		self.delay = delay
		self.random_order = random_order
		self.current_index = index
				
	def get_next_wallpaper(self):
		self.current_index += 1
		self.current_index %= len(self.wallpapers)
	
	def get_prev_wallpaper(self):
		self.current_index -= 1
		self.current_index %= len(self.wallpapers)

	def get_random_wallpaper(self):
		self.current_index = random.randint(0, len(self.wallpapers) - 1)

	def set_wallpaper(self):
		print('running gsettings set org.gnome.desktop.background picture-uri file://'
				+ self.wallpapers[self.current_index])
		os.system('gsettings set org.gnome.desktop.background picture-uri "file://'
				+ self.wallpapers[self.current_index] + '"')
	
	def add_wallpaper(uri):
		self.wallpapers.append(uri)

	def remove_wallpaper(uri):
		self.wallpapers.remove(uri)

	def start(self):
		while True:
			if self.random_order:
				self.get_random_wallpaper()
			else:
				self.get_next_wallpaper()
			self.set_wallpaper()
			time.sleep(self.delay)
			c = ConfigParser()
			c.add_section('conf')
			c.set('conf', 'index', self.current_index)
			c.write(open('/home/ljones/Desktop/Pictures/rotator.config', 'wb'))
		
if __name__ == '__main__':
	PIC_DIR = '/home/ljones/Desktop/Pictures/Wallpapers/'
	pic_uris = []
	

	c = ConfigParser()
	c.read('/home/ljones/Desktop/Pictures/rotator.config')
	
	for p in sorted(os.listdir(PIC_DIR)):
		pic_uris.append(PIC_DIR + p)
	RotateWallpapers(pic_uris, 300, c.getint('conf', 'index'), False).start()
