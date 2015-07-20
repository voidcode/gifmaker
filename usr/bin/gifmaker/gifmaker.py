#!/usr/bin/python3
from gi.repository import Gtk, Gdk, GdkPixbuf
from PIL import Image
import os, time, shutil
class Settings:
	global filename, folderPath
	def __init__(self):
		self.filename = "settings.conf"
		self.folderPath =  os.getenv("HOME") + "/.gifmaker/"
		if not os.path.exists(self.folderPath):
			os.mkdir(self.folderPath)
		if not os.path.exists(self.folderPath+self.filename):
			try:
				f = open(self.folderPath+self.filename, "w")
				f.write(os.getenv("HOME") + '/Pictures/')
				f.close()
			except os.error:
				pass
	def get(self):
		f = open(self.folderPath+self.filename)
		fdata = f.read()
		f.close()
		return fdata
	def set(self, newData):
		f = open(self.folderPath+self.filename, "w")
		f.write(newData)
		f.close()
class EventHandler:
	global builder, approot, sw, settings, lb, comboboxtextDelay, labelSaveFolderPath
	def __init__(self, builder):
		self.builder = builder
		self.settings = Settings()
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
	def onOpenAbortDialog(self, *widget):
		print "onOpenAbortDialog is clicked!"
		aboutdialog = Gtk.AboutDialog()
		aboutdialog.set_name("GifMaker")
		aboutdialog.set_version("0.1")
		aboutdialog.set_comments("This app make it easy to create .gif images.")
		aboutdialog.set_website("https://github.com/voidcode/gifmaker")
		aboutdialog.set_website_label("Get the code")
		aboutdialog.set_authors(["Terkel Sorensen"])
		#abortDialog.set_license_type("gpl-3-0")
		#abortDialog.set_logo(os.path.dirname(os.path.abspath(__file__)) + "/images/logo48.svg")
		aboutdialog.run()
		aboutdialog.destroy()
	def onConvertToGif(self, *widgets):
		print "Convert to gif is clciked"
		folderpath = self.labelSaveFolderPath.get_text()
		gifFilename = str(time.time())+'.gif'
		delay = str(self.comboboxtextDelay.get_active() + 1)
		self.resizeAllImageInFolder(folderpath)
		os.chdir(folderpath+"thumbails/")
		if not os.path.exists(folderpath+"gifs/"):
			os.mkdir(folderpath+"gifs/")
		print 'convert -delay '+delay+'x1 -loop 0 *.png ../gifs/'+gifFilename
		os.system('convert -delay '+delay+'x1 -loop 0 *.png ../gifs/'+gifFilename)
		os.system('xdg-open '+folderpath+"gifs/"+gifFilename)
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
			pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(savepath, width=230, height=230, preserve_aspect_ratio=False)
			fimg.set_from_pixbuf(pixbuf)
			lbr = Gtk.ListBoxRow()
			lbr.add(fimg)
			self.lb.insert(lbr, 0)
			self.sw.show_all()
			print "Adding new image to sw: (savepath) == " + savepath
	def resizeAllImageInFolder(self, pathToFolder):
		print "resizeAllImageInFolder is running..." +pathToFolder
		thumbailFolder = pathToFolder+"thumbails/"		
		if not os.path.exists(thumbailFolder):
			os.mkdir(thumbailFolder)
		else:
			allFilesInThumbailFolder = os.listdir(thumbailFolder)
			for filename in allFilesInThumbailFolder:
				os.remove(thumbailFolder+filename)	
		allImages = os.listdir(pathToFolder)
		for filename in allImages:
			fn, ext = os.path.splitext(filename)
			if ext == ".png":
				img = Image.open(pathToFolder+filename).resize( (500,500) )
				#img.thumbnail((300, 300), Image.ANTIALIAS)
				img.save(thumbailFolder+filename)
	def onOpenCurrentImagefolderClicked(self, *widget):
		os.system("gnome-open "+self.settings.get())
	def onChooseImagefolderClicked(self, *widgets):
		print "Choose image folder is clicked!"
		fcd = Gtk.FileChooserDialog("Please choose a folder", None, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Use this folder", Gtk.ResponseType.OK))
		if self.settings.get() == "":
			fcd.set_current_folder(os.getenv('HOME') + '/Pictures/')
		else:
			fcd.set_current_folder(self.settings.get())
		fcd.connect('current-folder-changed', self.onChooseFolderSelectedChanged)
		fcd.show_all()

		response = fcd.run()
		if response == Gtk.ResponseType.OK:
			#print "gifMakerRoot: " +gifMakerRoot
			print "Changes folder selected to: " + fcd.get_filename()
			self.gifMakerRoot = fcd.get_filename() + "/"
			self.settings.set(self.gifMakerRoot)
			self.removeAllImagesInSw()		
			self.fillImagesIntoSw()
		elif response == Gtk.ResponseType.CANCEL:
			fcd.hide()
		fcd.destroy()

	def removeAllImagesInSw(self, *args):
		#OMG there must be at better way to do this.. like self.lb.destroy or self.lb.removeAllItems() ...
		i = 0		
		while i < len(self.lb):
			self.lb.remove(self.lb.get_row_at_index(i))
			i+1
	def fillImagesIntoSw(self, *args):
		pathToFolder = self.settings.get()
		filesInGifMakerRoot = os.listdir(pathToFolder)
		self.labelSaveFolderPath.set_text(pathToFolder)
		if len(filesInGifMakerRoot) > 0:
			for filename in reversed(filesInGifMakerRoot):
				fn, ext = os.path.splitext(filename)
				if ext == '.png':
					print filename + '\n'
					fimg = Gtk.Image()
					fimg.set_from_file(self.gifMakerRoot + filename)
					pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(self.gifMakerRoot + filename, width=230, height=230, preserve_aspect_ratio=False)
					fimg.set_from_pixbuf(pixbuf)
					lbr = Gtk.ListBoxRow()
					lbr.add(fimg)
					self.lb.insert(lbr, 0)
				else:
					print 'This app only support the .png format... '+filename+' is not added to listbox!'
		self.sw.show_all()
	def onChooseFolderSelectedChanged(self, *widget):
		print "onChooseFolderSelectedChanged is clicked"
	def onQuit(self, *widget):
		print "Quit this app is clicked!"
		Gtk.main_quit()

class GifMakerWindow:
	global builder
	global approot
	global sw
	def __init__(self):
		self.approot = os.path.dirname(os.path.abspath(__file__))
		#self.bgColor = Gdk.RGBA.from_color(Gdk.color_parse('#272822'))

		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.approot + '/ui/main.glade')
		self.builder.connect_signals(EventHandler(self.builder))

		self.window = self.builder.get_object('mainWindow')
		self.window.set_icon_from_file(self.approot+'/images/logo48.png')
		#self.window.override_background_color(0, self.bgColor)
		self.window.set_title('GifMaker')
		#self.window.set_position(Gtk.WindowPosition.CENTER)

		self.window.show_all()
	def main(self):
		Gtk.main()

if __name__ == '__main__':
	mainWindow = GifMakerWindow()
	mainWindow.main()
