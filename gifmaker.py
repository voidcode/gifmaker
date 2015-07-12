#!/usr/bin/python3
from gi.repository import Gtk, Gdk
import os, time
from random import randint
global gifMakerRoot

class Settings:
	global filename, folderPath
	def __init__(self):
		self.filename = "settings.conf"
		self.folderPath =  os.getenv("HOME") + "/.gifmaker/"
		if not os.path.exists(self.folderPath):
			os.makefile()
	def get(self):
		f = open(self.folderPath+self.filename)
		return f.read()
	def set(self, newData):
		f = open(self.folderPath+self.filename, "w")
		f.write(newData)

class EventHandler:
	global builder, approot, sw, settings, lb, comboboxtextDelay, labelSaveFolderPath
	def __init__(self, builder):
		self.settings = Settings()
		self.builder = builder
		self.sw = self.builder.get_object('sw')
		self.lb = Gtk.ListBox()
		self.sw.add(self.lb)
		self.sw.show_all()
		self.gifMakerRoot = self.settings.get()
		self.comboboxtextDelay = self.builder.get_object('comboboxtextDelay')
		self.labelSaveFolderPath = self.builder.get_object('labelSaveFolderPath')
		self.labelSaveFolderPath.set_text(self.settings.get())
		self.fillImagesIntoSw()
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
		if self.gifMakerRoot=="":
			self.onChooseImagefolderClicked()
		else:
			savepath = self.gifMakerRoot + str(time.time())+'.png'
			os.system('gnome-screenshot -a -f '+ savepath)
			print 'gnome-screenshot -a -file="' + savepath + '"'
			fimg = Gtk.Image()
			fimg.set_from_file(savepath)
			lbr = Gtk.ListBoxRow()
			lbr.add(fimg)
			self.lb.insert(lbr, 0)
			self.sw.show_all()
			print "Adding new image to sw: (savepath) == " + savepath
	def onChooseImagefolderClicked(self, *widgets):
		print "Choose image folder is clicked!"
		fcd = Gtk.FileChooserDialog("Please choose a folder", None, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Use this folder", Gtk.ResponseType.OK))
		if self.settings.get() == "":
			fcd.set_current_folder(os.getenv('HOME') + '/Pictures/')
		else:
			fcd.set_current_folder(self.settings.get())
		#fcd.connect('current-folder-changed', self.onChooseFolderSelectedChanged)
		fcd.show_all()

		response = fcd.run()
		if response == Gtk.ResponseType.OK:
			#print "gifMakerRoot: " +gifMakerRoot
			print "Changes folder selected to: " + fcd.get_filename()
			self.gifMakerRoot = fcd.get_filename() + "/"
			self.settings.set(self.gifMakerRoot)
			self.fillImagesIntoSw()
		elif response == Gtk.ResponseType.CANCEL:
			fcd.hide()
		fcd.destroy()

	def fillImagesIntoSw(self, *args):
		filesInGifMakerRoot = os.listdir(self.gifMakerRoot)
		self.labelSaveFolderPath.set_text(self.gifMakerRoot)
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
					self.lb.insert(lbr, 0)
				else:
					print 'This app only support the .png format... '+filename+' is not added to sw!'
			self.sw.show_all()
		else:
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
