#!/usr/bin/python3
from gi.repository import Gtk, Gdk
import os

class EventHandler:
	def __init__(self):
		self.currentGifFolder = '~/Desktop/gif/'
		print "init"

	def onConvertToGif(self, *widgets):
		print "Convert to gif is clciked"
	def onAddNewImage(self, *widgets):
		print str(self.currentGifFolder)
	def onQuit(self, *widget):
		print "quit is clicked"
		Gtk.main_quit()

class GifMakerWindow:
	global approot
	global sw
	def __init__(self):
		self.gifMakerRoot = os.getenv('HOME') + '/.gifmaker/'
		print str(self.gifMakerRoot)
		#mkdir if ~/.gifmaker/ do not exists
		if not os.path.exists(self.gifMakerRoot):
			os.makedirs(self.gifMakerRoot)

		self.approot = os.path.dirname(os.path.abspath(__file__))
		self.bgColor = Gdk.RGBA.from_color(Gdk.color_parse('#272822'))

		builder = Gtk.Builder()
		builder.add_from_file(self.approot + '/ui/main.glade')
		builder.connect_signals(EventHandler())

		self.window = builder.get_object('mainWindow')
		self.window.override_background_color(0, self.bgColor)
		self.window.set_title('GifMaker')

		self.sw = builder.get_object('sw')
		self.fillImagesIntoSw()

		self.window.show_all()
	def fillImagesIntoSw(self, *args):
		filesInGifMakerRoot = os.listdir(self.gifMakerRoot)
		lb = Gtk.ListBox()
		print os.listdir(self.gifMakerRoot) 
		for filename in filesInGifMakerRoot:
			print filename + '\n'
			fimg = Gtk.Image()
			fimg.set_pixel_size(1)
			fimg.set_from_file(self.gifMakerRoot + filename)
			lbr = Gtk.ListBoxRow()
			lbr.add(fimg)
			lb.add(lbr)
		self.sw.add(lb)
		self.sw.show_all()

if __name__ == '__main__':
	mainWindow = GifMakerWindow()
	#mainWindow.connect('destroy', Gtk.main_quit())
	#mainWindow.connect('delete-event', lambda widget: Gtk.main_quit)
	#mainWindow.connect('destroy', lambda widget: Gtk.main_quit)
	Gtk.main()