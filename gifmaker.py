#!/usr/bin/python3
from gi.repository import Gtk, Gdk
import os, time
from random import randint
global gifMakerRoot

class settings:
	def __init__(self):
		print "setting init---"
		self.filePath =  os.getenv("HOME") + "/settings.conf"
		if not os.path.exists(self.filePath):
			os.makefile()
	def get():
		f = open(self.filePath)
		return f.read()
	def set(newData):
		f = open(self.filePath, "+w")
		f.write(newData)

class EventHandler:
	global builder
	global approot
	global sw
	global lb, comboboxtextDelay, labelSaveFolderPath
	def __init__(self, builder):
		self.builder = builder
		self.gifMakerRoot = None
		self.comboboxtextDelay = self.builder.get_object('comboboxtextDelay')
		self.labelSaveFolderPath = self.builder.get_object('labelSaveFolderPath')
		print "EventHanlder() init END"
	def onConvertToGif(self, *widgets):
		folderpath = self.labelSaveFolderPath.get_text()
		gifFilename = str(time.time())+'.gif'
		delay = str(self.comboboxtextDelay.get_active() + 1)
		print folderpath+'*.png'
		print '-delay set to: '+ delay
		os.chdir(folderpath)
		os.system('convert -delay '+delay+'x1 -loop 0 *.png '+gifFilename)
		os.system('xdg-open '+folderpath+gifFilename)
		print "Convert to gif is clciked"
		print folderpath
	def onAddNewImage(self, *widgets):
		if self.gifMakerRoot is None:
			self.onChooseImagefolderClicked()
		else:
			savepath = self.gifMakerRoot + str(time.time())+'.png'
			os.system('import -screen '+ savepath)
			print 'import -screen root -resize 100x200 "' + savepath + '"'
			fimg = Gtk.Image()
			fimg.set_from_file(savepath)
			lbr = Gtk.ListBoxRow()
			lbr.add(fimg)
			self.lb.insert(lbr, 0)
			self.sw.show_all()
			print "Adding new image to sw: (savepath) == " + savepath
	def onChooseImagefolderClicked(self, *widgets):
		print "Choose image folder is clicked!"
		fcd = Gtk.FileChooserDialog("Please choose a folder", None, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))
		fcd.set_current_folder(os.getenv('HOME') + '/Pictures/')
		#fcd.connect('current-folder-changed', self.onChooseFolderSelectedChanged)
		fcd.show_all()

		response = fcd.run()
		if response == Gtk.ResponseType.OK:
			print "OK"
			#print "gifMakerRoot: " +gifMakerRoot
			print "Changes folder selected to: " + fcd.get_filename()
			self.gifMakerRoot = fcd.get_filename() + "/"
			self.fillImagesIntoSw()
		elif response == Gtk.ResponseType.CANCEL:
			print "CANCEL: hide FileChooserDialog!"
			fcd.hide()
		fcd.destroy()

	def fillImagesIntoSw(self, *args):
		filesInGifMakerRoot = os.listdir(self.gifMakerRoot)
		self.sw = self.builder.get_object('sw')
		self.labelSaveFolderPath.set_text(self.gifMakerRoot)
		self.lb = Gtk.ListBox()
		if len(filesInGifMakerRoot) > 0:
			print os.listdir(self.gifMakerRoot) 
			for filename in reversed(filesInGifMakerRoot):
				fn, ext = os.path.splitext(filename)
				if ext == '.png':
					print filename + '\n'
					fimg = Gtk.Image()
					fimg.set_from_file(self.gifMakerRoot + filename)
					lbr = Gtk.ListBoxRow()
					lbr.add(fimg)
					self.lb.add(lbr)
				else:
					print 'This app only support the .png format... '+filename+' is not added to sw!'
			self.sw.add(self.lb)
			self.sw.show_all()
		else:
			self.lb.destroy()
			self.sw.show_all()
			print "This folder has no files in this folder"
	def onQuit(self, *widget):
		print "quit is clicked"
		Gtk.main_quit()

class GifMakerWindow:
	global builder
	global approot
	global sw
	def __init__(self):
		self.approot = os.path.dirname(os.path.abspath(__file__))
		self.bgColor = Gdk.RGBA.from_color(Gdk.color_parse('#272822'))

		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.approot + '/ui/main.glade')
		self.builder.connect_signals(EventHandler(self.builder))

		self.window = self.builder.get_object('mainWindow')
		self.window.override_background_color(0, self.bgColor)
		self.window.set_title('GifMaker')
		self.window.set_position(Gtk.WindowPosition.MOUSE)

		self.window.show_all()
	def main(self):
		Gtk.main()

if __name__ == '__main__':
	mainWindow = GifMakerWindow()
	mainWindow.main()