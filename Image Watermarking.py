#!/usr/bin/env python

import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
Gdk.threads_init()
from gi.repository import GLib

from DWT2 import *
from PSNR import *
from embed import *
from WatermarkComparison import *

# print pygtk._get_available_versions()
# we can call it just about anything we want

def resizePixbuf(pixbuf,desired_width,desired_height):


    pixbuf_width  = (float) (pixbuf.get_width())
    pixbuf_height = (float) (pixbuf.get_height())
    if desired_width != pixbuf_width or desired_height != pixbuf_height:
        if pixbuf_height < pixbuf_width:
            target_scale  = desired_width/pixbuf_width
            target_width  = (int) (pixbuf_width * target_scale)
            target_height = (int) (pixbuf_height * target_scale)

        else:
            target_scale  = desired_height/pixbuf_height
            target_width  = (int) (pixbuf_width *  target_scale)
            target_height = (int) (pixbuf_height * target_scale)
        print "target width = " +  (str(pixbuf_width)+ " * (" +str(desired_width)+ "/"+str(pixbuf_width) + ")" )
        pixbuffed = pixbuf.scale_simple(target_width, target_height, GdkPixbuf.InterpType.BILINEAR)
        # pixbuf = pixbuf.scale(0,0,target_width, target_height,0,0,target_scale,target_scale, GdkPixbuf.InterpType.BILINEAR)
        return pixbuffed

def resizePixbuf2(pixbuf,gtkimage):

    widget = gtkimage
    allocation = widget.get_allocation()
    desired_width, desired_height = allocation.width, allocation.height
    print "desired_width 2 = ",desired_width
    pixbuf_width  = (float) (pixbuf.get_width())
    pixbuf_height = (float) (pixbuf.get_height())
    if desired_width != pixbuf_width or desired_height != pixbuf_height:
        if pixbuf_height > pixbuf_width:
            target_scale  = desired_height/pixbuf_height
            target_width  = (int) (pixbuf_width *  target_scale)
            target_height = (int) (pixbuf_height * target_scale)
        else:
            target_scale  = desired_width/pixbuf_width
            target_width  = (int) (pixbuf_width * target_scale)
            target_height = (int) (pixbuf_height * target_scale)
        print "target scale", target_scale
        print "resize2", (str(pixbuf_width)+ " * () " +str(desired_width)+ "/"+str(pixbuf_width) )
        pixbuffed = pixbuf.scale_simple(target_width, target_height, GdkPixbuf.InterpType.BILINEAR)
        # pixbuf = pixbuf.scale(0,0,target_width, target_height,0,0,target_scale,target_scale, GdkPixbuf.InterpType.BILINEAR)
        return pixbuffed

def resizePixbuf3(pixbuf,gtkimage):

    widget = gtkimage
    allocation = widget.get_allocation()
    desired_width, desired_height = allocation.width, allocation.height
    print "desired_width 2 = ",desired_width
    pixbuf_width  = (float) (pixbuf.get_width())
    pixbuf_height = (float) (pixbuf.get_height())
    if desired_width != pixbuf_width or desired_height != pixbuf_height:
        if pixbuf_height > pixbuf_width:
            target_scale  = desired_height/pixbuf_height
            target_width  = (int) (pixbuf_width *  target_scale)
            target_height = (int) (pixbuf_height * target_scale)
        else:
            target_scale  = desired_width/pixbuf_width
            target_width  = (int) (pixbuf_width * target_scale)
            target_height = (int) (pixbuf_height * target_scale)
        print "target scale", target_scale
        print "resize2", (str(pixbuf_width)+ " * () " +str(desired_width)+ "/"+str(pixbuf_width) )
        pixbuffed = pixbuf.scale_simple(target_width, target_height, GdkPixbuf.InterpType.BILINEAR)
        # pixbuf = pixbuf.scale(0,0,target_width, target_height,0,0,target_scale,target_scale, GdkPixbuf.InterpType.BILINEAR)
        return pixbuffed

class Watermark:

    # This first define is for our on_window1_destroy signal we created in the
    # Glade designer. The print message does just that and prints to the terminal
    # which can be useful for debugging. The 'object' if you remember is the signal
    # class we picked from GtkObject.
    def on_window1_destroy(self, object, data=None):
        print ("quit with cancel")
        Gtk.main_quit()

    # This is the same as above but for our menu item.
    def on_gtk_quit_activate(self, menuitem, data=None):
        print "quit from menu"
        Gtk.main_quit()

    def on_home_resize(self,widget):
        newheight=(float) (self.windowHome.get_allocation().height)
        scale=newheight/self.windowheight-0.1
        if (scale!=self.windowscale):
            print "new height, window height", newheight, " , ",self.windowheight
            print "scale" , scale
            self.builder.get_object("imageEmbedIcon").set_from_pixbuf(
                resizePixbuf(self.embedicon,200*scale,115*scale))
            self.builder.get_object("imageExtractIcon").set_from_pixbuf(
                resizePixbuf(self.extracticon,200*scale,115*scale))
            self.windowscale=scale
    # def on_embed_resize(self,widget):
    #     pixbuf=self.imgembedori.get_pixbuf()
    #     pixbuf_width,pixbuf_height= pixbuf.get_width(), pixbuf.get_height()
    #     newheight=(float) (self.windowEmbed.get_allocation().height)
    #     scale=newheight/self.embedheight
    #     print "RESIZE !","new height, window height", newheight, " , ",self.embedheight
    #     print "scale" , scale
    #     if (scale!=self.embedscale):
    #         self.builder.get_object("imageEmbedOriginal").set_from_pixbuf(
    #             resizePixbuf(self.embedicon,pixbuf_width*scale,pixbuf_height*scale))
    #         self.embedscale=scale;

    # This is our init part where we connect the signals
    def __init__(self):
        self.gladefile = "imk.glade"  # store the file name
        self.builder = Gtk.Builder()  # create an instance of the gtk.Builder
        # add the xml file to the Builder
        self.builder.add_from_file(self.gladefile)
        self.logo = GdkPixbuf.Pixbuf.new_from_file("data/media/icon.svg")
        self.embedicon = GdkPixbuf.Pixbuf.new_from_file("data/media/embed.svg")
        self.extracticon = GdkPixbuf.Pixbuf.new_from_file("data/media/extract.svg")
        self.inserticon = GdkPixbuf.Pixbuf.new_from_file("data/media/Insert.svg")
        self.progress1 = GdkPixbuf.Pixbuf.new_from_file("data/media/Progress1.svg")
        self.progress2 = GdkPixbuf.Pixbuf.new_from_file("data/media/Progress2.svg")
        self.progress3 = GdkPixbuf.Pixbuf.new_from_file("data/media/Progress3.svg")
        # This line does the magic of connecting the signals created in the Glade3
        # builder to our defines above. You must have one def for each signal if
        # you use this line to connect the signals.
        self.builder.connect_signals(self)
        #Home Window
        self.windowHome = self.builder.get_object(
            "windowHome")  # This gets the 'window1' object
        self.windowHome.connect("delete-event", self.on_gtk_quit_activate)
        self.windowHome.resize(100,100)

        self.windowheight = self.windowHome.get_allocation().height;
        self.builder.get_object("imageEmbedIcon").set_from_pixbuf(
            resizePixbuf(self.embedicon,200,115))
        self.builder.get_object("imageExtractIcon").set_from_pixbuf(
            resizePixbuf(self.extracticon,200,115))
        self.windowHome.show()  # this shows the 'window1' object
        self.windowheight = self.windowHome.get_allocation().height;
        self.windowscale  = 1
        self.builder.get_object("windowHome").connect("check-resize",self.on_home_resize)
        print "win width",self.windowheight;

        self.windowEmbed = self.builder.get_object("windowEmbed")
        self.ImageOriginal=None
        self.ImageWatermark=None
        #Connecting Buttons

        self.builder.get_object("buttonEmbed").connect("clicked",self.openEmbed )
        self.builder.get_object("buttonExtract").connect("clicked",self.openExtract )
        self.builder.get_object("buttonAbout").connect("clicked", self.openAbout)
        self.builder.get_object("buttonQuit").connect("clicked", Gtk.main_quit)
        # self.builder.get_object("BtnOriginal").connect(
        #     "clicked", self.loadOriginal)
        # self.BoxOriginal = self.builder.get_object("BoxOriginal")
        # self.ImageOriginal = self.builder.get_object("ImageOriginal")
        # self.EntryOriginal = self.builder.get_object("EntryOriginal")
        # self.ImageWatermark = self.builder.get_object("ImageWatermark")
        # self.EntryWatermark = self.builder.get_object("EntryWatermark")
        # self.builder.get_object("BtnWatermark").connect(
        # "clicked", self.loadWatermark)
        # self.builder.get_object("BtnEmbed").connect(
        #     "clicked", self.embedWatermark)

    def openAbout(self,widget):
        self.builder.add_from_file(self.gladefile)
        dialogAbout = self.builder.get_object(
            "aboutdialog")  # This gets the 'window1' object
        dialogAbout.set_logo(resizePixbuf(self.logo,128,128))
        response = dialogAbout.run()
        if response == -4:
            dialogAbout.hide()
        dialogAbout.destroy

    def openEmbed(self,widget):
        self.builder.add_from_file(self.gladefile)
        self.windowEmbed = self.builder.get_object("windowEmbed")
        self.windowHome.hide()
        self.windowEmbed.show()
        self.windowEmbed.connect("delete-event", Gtk.main_quit)
        self.notebookEmbed = self.builder.get_object("notebookEmbed")
        print "newpage",  self.notebookEmbed.append_page(self.builder.get_object("box17"),None)
        self.windowEmbed.resize(100,100)


        #page1

        self.builder.get_object("buttonHome").connect("clicked",self.goHome)
        self.builder.get_object("buttonEmbedOriginal").connect("clicked",self.loadOriginal)
        self.builder.get_object("buttonEmbedNext1").connect("clicked",self.nextEmbed1)
        self.builder.get_object("imageEmbedOriginal").set_from_pixbuf(
            resizePixbuf(self.inserticon,400,300))
        self.builder.get_object("progress1").set_from_pixbuf(
            resizePixbuf(self.progress1,400,50))

        #page2
        self.builder.get_object("buttonHome1").connect("clicked",self.goHome)
        self.builder.get_object("buttonEmbedWatermark").connect("clicked",self.loadWatermark)
        self.builder.get_object("buttonEmbedNext2").connect("clicked",self.nextEmbed2)
        self.builder.get_object("buttonEmbedBack").connect("clicked",self.backEmbed)
        self.builder.get_object("imageEmbedOriginal").set_from_pixbuf(
            resizePixbuf(self.inserticon,400,300))
        self.progressbarEmbed = self.builder.get_object("progressbar1")
        self.builder.get_object("progress2").set_from_pixbuf(
            resizePixbuf(self.progress2,400,50))

        #page3
        self.builder.get_object("buttonHome2").connect("clicked",self.goHome)
        self.builder.get_object("buttonEmbedBack1").connect("clicked",self.nextEmbed1)
        self.builder.get_object("buttonEmbedSave").connect("clicked",self.saveImage)
        self.builder.get_object("progress3").set_from_pixbuf(
            resizePixbuf(self.progress3,400,50))

        # self.windowEmbed.resize(50,50)
        # self.embedscale=1
        # self.builder.get_object("windowEmbed").connect("check-resize",self.on_embed_resize)
    def openExtract(self,widget):
        self.builder.add_from_file(self.gladefile)
        self.windowEmbed = self.builder.get_object("windowEmbed")
        self.windowHome.hide()
        self.windowEmbed.show()
        self.windowEmbed.connect("delete-event", Gtk.main_quit)
        self.windowEmbed.resize(100,100)
        self.notebookEmbed = self.builder.get_object("notebookEmbed")
        print "newpage",  self.notebookEmbed.append_page(self.builder.get_object("box17"),None)

        #page1

        self.builder.get_object("buttonHome").connect("clicked",self.goHome)
        self.builder.get_object("buttonEmbedOriginal").connect("clicked",self.loadOriginal)
        self.builder.get_object("buttonEmbedNext1").connect("clicked",self.nextEmbed1)
        self.builder.get_object("imageEmbedOriginal").set_from_pixbuf(
            resizePixbuf(self.inserticon,400,300))
        self.builder.get_object("progress1").set_from_pixbuf(
            resizePixbuf(self.progress1,400,50))
        self.builder.get_object("label6").set_text("Select Watermarked Image")
        #page2
        self.builder.get_object("buttonHome1").connect("clicked",self.goHome)
        self.builder.get_object("buttonEmbedWatermark").connect("clicked",self.loadWatermark)
        self.builder.get_object("buttonEmbedNext2").connect("clicked",self.nextExtract2)
        self.builder.get_object("buttonEmbedBack").connect("clicked",self.backEmbed)
        self.builder.get_object("imageEmbedOriginal").set_from_pixbuf(
            resizePixbuf(self.inserticon,400,300))
        self.progressbarEmbed = self.builder.get_object("progressbar1")
        self.builder.get_object("progress2").set_from_pixbuf(
            resizePixbuf(self.progress2,400,50))
        self.builder.get_object("label8").set_text("Select Original Image\n and Adjust Intensity")

        #page3
        self.builder.get_object("buttonHome3").connect("clicked",self.goHome)
        self.builder.get_object("buttonEmbedBack2").connect("clicked",self.nextEmbed1)
        self.builder.get_object("progress4").set_from_pixbuf(
            resizePixbuf(self.progress3,400,50))

        # self.windowEmbed.resize(50,50)
        # self.embedscale=1
        # self.builder.get_object("windowEmbed").connect("check-resize",self.on_embed_resize)

    def goHome(self,widget):
        self.notebookEmbed.set_current_page(0)
        self.ImageOriginal=None
        self.ImageWatermark=None
        try:
            self.ImageWatermark=None
        except:
            print "ok"
        self.windowEmbed.destroy()
        self.windowHome.show()

    def nextEmbed1(self,widget):
        if (self.ImageOriginal!=None):
            self.builder.get_object("grid1").hide()
            self.windowEmbed.resize(100,100)
            self.progressbarEmbed.hide()
            self.notebookEmbed.set_current_page(1)
            print type(self.ImageWatermark)
            try:
                if( type(self.ImageWatermark)!=np.ndarray):
                    self.builder.get_object("imageEmbedWatermark").set_from_pixbuf(
                        resizePixbuf(self.inserticon,400,300))
                else:
                    self.builder.get_object("imageEmbedWatermark").set_from_pixbuf(
                        resizePixbuf(GdkPixbuf.Pixbuf.new_from_file("tmp/Image2.jpeg"),400,300))
            except:
                self.builder.get_object("imageEmbedWatermark").set_from_pixbuf(
                    resizePixbuf(self.inserticon,400,300))
        else:
            md = Gtk.MessageDialog(self.windowEmbed, 0, Gtk.MessageType.ERROR, (Gtk.STOCK_CLOSE,Gtk.ResponseType.CLOSE), "Image not found ")
            md.run()
            md.destroy()

    def nextEmbed2(self,widget):
        if self.ImageWatermark!=None:
            print "cvcv", self.ImageOriginal
            self.progressbarEmbed.show()
            self.embedWatermark()

            pixbufOriginal = GdkPixbuf.Pixbuf.new_from_file("tmp/ImageOriginal.jpeg")
            pixbufOriginal = resizePixbuf(pixbufOriginal,200,150)
            self.builder.get_object("imageOrigin").set_from_pixbuf(pixbufOriginal)
            pixbufWatermarked = GdkPixbuf.Pixbuf.new_from_file("tmp/ImageWatermarked.jpeg")
            pixbufWatermarked = resizePixbuf(pixbufWatermarked,200,150)
            self.builder.get_object("imageWatermarked").set_from_pixbuf(pixbufWatermarked)
            pixbufWatermark = GdkPixbuf.Pixbuf.new_from_file("tmp/ImageWatermark.jpeg")
            pixbufWatermark = resizePixbuf(pixbufWatermark,200,150)
            self.builder.get_object("imageWatermark").set_from_pixbuf(pixbufWatermark)
            pixbufExtract = GdkPixbuf.Pixbuf.new_from_file("tmp/ImageExtract.jpeg")
            pixbufExtract = resizePixbuf(pixbufExtract,200,150)
            self.builder.get_object("imageExtract").set_from_pixbuf(pixbufExtract)
            self.builder.get_object("imageEmbedWatermark").set_from_stock("gtk-missing-image",4)
            self.windowEmbed.resize(100,100)
            self.builder.get_object("grid1").show()

            self.notebookEmbed.set_current_page(2)
        else:
            md = Gtk.MessageDialog(self.windowEmbed, 0, Gtk.MessageType.ERROR, (Gtk.STOCK_CLOSE,Gtk.ResponseType.CLOSE), "Image not found ")
            md.run()
            md.destroy()

    def nextExtract2(self,widget):
        if self.ImageWatermark !=None:
            self.progressbarEmbed.show()
            self.extractWatermark()
            self.windowEmbed.resize(100,100)
            pixbuf = GdkPixbuf.Pixbuf.new_from_file("tmp/ImageExtraction.jpeg")
            pixbuf = resizePixbuf(pixbuf,400,300)
            self.builder.get_object("imageOrigin1").set_from_pixbuf(pixbuf)
            self.builder.get_object("imageEmbedWatermark").set_from_stock("gtk-missing-image",4)
            self.notebookEmbed.set_current_page(3)
            self.windowEmbed.resize(100,100)
        else:
            md = Gtk.MessageDialog(self.windowEmbed, 0, Gtk.MessageType.ERROR, (Gtk.STOCK_CLOSE,Gtk.ResponseType.CLOSE), "Image not found ")
            md.run()
            md.destroy()


    def loadOriginal(self, widget):
        dialog = Gtk.FileChooserDialog("Pilih Gambar "
            , self.windowEmbed
            , Gtk.FileChooserAction.OPEN
            , (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.ImageOriginal=cv2.imread(dialog.get_filename())
            cv2.imwrite("tmp/Image1.jpeg",self.ImageOriginal)
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(dialog.get_filename())
            print pixbuf.get_width()
            pixbuf = resizePixbuf(pixbuf,400,300)
            print pixbuf.get_width()
            self.builder.get_object("imageEmbedOriginal").set_from_pixbuf(pixbuf)
            print("File Selected", dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def loadWatermark(self, widget):
        dialog = Gtk.FileChooserDialog("Pilih Gambar ", self.windowEmbed, Gtk.FileChooserAction.OPEN, (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.ImageWatermark=cv2.imread(dialog.get_filename())
            cv2.imwrite("tmp/Image2.jpeg",self.ImageWatermark)
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(dialog.get_filename())
            pixbuf = resizePixbuf(pixbuf,400,300)
            self.builder.get_object("imageEmbedWatermark").set_from_pixbuf(pixbuf)
            print("File Selected", dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def add_filters(self, dialog):
        filter_image = Gtk.FileFilter()
        filter_image.set_name("Image File")
        filter_image.add_mime_type("image/*")
        dialog.add_filter(filter_image)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def embedWatermark(self):
        self.progressbarEmbed.set_text("Unpacking Image")
        while Gtk.events_pending():
                Gtk.main_iteration()
        print "sedang DWT"
        ImageOriginalDWT = waveleteTransform(self.ImageOriginal)
        height, width = self.ImageOriginal.shape[:2]
        waterHeight, waterWidth = self.ImageWatermark.shape[:2]
        if width / 2 < waterWidth or height / 2 < waterHeight:
            if waterHeight > waterWidth:
                print waterHeight / (height / 2)
                ImageWatermark = cv2.resize(ImageWatermark, (0, 0), fx=float(
                    height) / 2 / waterHeight, fy=float(height) / 2 / waterHeight)
            else:
                # print  str(w) + "/" + str(waterWidth) +" = "+
                # str(float(w)/waterWidth)
                self.ImageWatermark = cv2.resize(self.ImageWatermark, (0, 0), fx=float(width) / 2 / waterWidth, fy = float(width) / 2 / waterWidth)
        waterHeight, waterWidth=self.ImageWatermark.shape[:2]
        self.progressbarEmbed.set_text("Embedding Watermark into image")
        self.progressbarEmbed.set_fraction(1.0/5)
        while Gtk.events_pending():
                Gtk.main_iteration()
        print "sedang embedding"
        # alpha=float(self.builder.get_object("EntryIntensity").get_text())
        alpha=0.004
        print alpha
        ImageWatermarkedDWT=embed(ImageOriginalDWT, self.ImageWatermark, 0, 0, waterWidth, waterHeight, alpha)
        self.progressbarEmbed.set_fraction(2.0/5)
        self.progressbarEmbed.set_text("Packing Image with Watermark")
        while Gtk.events_pending():
                Gtk.main_iteration()
        print "sedang embedding2"
        ImageWatermarked=inverseWaveleteTransform(ImageWatermarkedDWT)
        self.progressbarEmbed.set_fraction(3.0/5)
        self.progressbarEmbed.set_text("Unpack Watermarked Image")
        while Gtk.events_pending():
                Gtk.main_iteration()
        print "sedang ekstrak1"
        imageWatermarkedDDWT=waveleteTransform(ImageWatermarked)
        self.progressbarEmbed.set_fraction(4.0/5)
        self.progressbarEmbed.set_text("Extracting Watermark")
        while Gtk.events_pending():
                Gtk.main_iteration()
        print "sedang Ekstrak2"
        ImageExtract=extract(imageWatermarkedDDWT[0:waterHeight, 0:waterWidth],
                            ImageOriginalDWT[0:waterHeight, 0:waterWidth], alpha)
        self.progressbarEmbed.set_fraction(5.0/5)
        self.progressbarEmbed.set_text("Rendering Image")
        self.ImageWatermarked= ImageWatermarked
        while Gtk.events_pending():
                Gtk.main_iteration()
        print "sedang nyetak"
        cv2.imwrite("tmp/ImageOriginal.jpeg",self.ImageOriginal)
        cv2.imwrite("tmp/ImageWatermarked.jpeg",ImageWatermarked)
        cv2.imwrite("tmp/ImageWatermark.jpeg",self.ImageWatermark)
        cv2.imwrite("tmp/ImageExtract.jpeg",ImageExtract)
        # compare = WatermarkCompare("/tmp/ImageOriginal.jpeg","/tmp/ImageWatermarked.jpeg","/tmp/ImageWatermark.jpeg","/tmp/ImageExtract.jpeg")

    def extractWatermark(self):
        while Gtk.events_pending():
            Gtk.main_iteration()
        alpha =0.004
        ImageWatermarked=self.ImageOriginal
        waterHeight,waterWidth = self.ImageOriginal.shape[:2]
        print "height, width", waterHeight,waterWidth
        self.progressbarEmbed.set_fraction(3.0/5)
        self.progressbarEmbed.set_text("Unpack Watermarked Image")
        while Gtk.events_pending():
                Gtk.main_iteration()
        print "sedang ekstrak1"
        imageWatermarkedDDWT=waveleteTransform(self.ImageOriginal)
        self.progressbarEmbed.set_fraction(4.0/5)
        self.progressbarEmbed.set_text("Extracting Watermark")
        while Gtk.events_pending():
                Gtk.main_iteration()
        print "sedang Ekstrak2"
        ImageExtract=extract(imageWatermarkedDDWT[0:waterHeight/2, 0:waterWidth/2],
                            waveleteTransform(self.ImageWatermark)[0:waterHeight/2, 0:waterWidth/2], alpha)
        self.progressbarEmbed.set_fraction(5.0/5)
        self.progressbarEmbed.set_text("Rendering Image")
        self.ImageExtracted= extract
        while Gtk.events_pending():
                Gtk.main_iteration()
        print "sedang nyetak"
        cv2.imwrite("tmp/ImageExtraction.jpeg",ImageExtract)
        # compare = WatermarkCompare("/tmp/ImageOriginal.jpeg","/tmp/ImageWatermarked.jpeg","/tmp/ImageWatermark.jpeg","/tmp/ImageExtract.jpeg")

    def saveImage(self,widget):
        dialog = Gtk.FileChooserDialog("Pilih Gambar ", self.windowEmbed, Gtk.FileChooserAction.SAVE, (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))
        dialog.set_do_overwrite_confirmation(True)
        response = dialog.run()
        if response == Gtk.ResponseType.ACCEPT:
            filename=str(dialog.get_filename())
            print("File Selected", filename)
            cv2.imwrite(filename,self.ImageWatermarked)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def backEmbed(self,widget):
        self.windowEmbed.resize(100,100)
        self.notebookEmbed.set_current_page(0)
        self.builder.get_object("imageEmbedWatermark").set_from_stock("gtk-missing-image",4)


if __name__ == '__main__':
    # win = MyWindow()
    # win.connect("delete-event", Gtk.main_quit)
    # win.show_all()
    wtm=Watermark()
    Gtk.main()
