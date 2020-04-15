from tkinter import *
from PIL import ImageTk,Image, ImageDraw, ImageFont
import pandas
import numpy as np
from modify_poster import fill_poster

#----------------------------------------------------------------------

class MainWindow():

    #----------------
    def __init__(self, main, image_number=1, language="Marathi"):

        # canvas for image
        self.canvas = Canvas(main, width=726, height=1280)
        self.canvas.grid(row=0, column=0)

        # images
        self.my_image_number = image_number
        self.language = language
        self.my_images = ImageTk.PhotoImage(Image.open("Sample_images/%05d.jpg" % (self.my_image_number) ))

        # set first image on canvas
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor = NW, image = self.my_images)

        # Load csv file and placements file
        self.df = pandas.read_csv("Hoaxbuster.csv")
        try:
            self.df_pl = np.loadtxt("%s/placements.txt" % self.language)
        except:
            self.df_pl = np.loadtxt("English/placements.txt")

        # Load font config
        self.load_font_config()

        # Now we have to process a particular language, its placements, and fonts
        self.initialize_material()

        main.bind("<Key>", self.key_pressed) 
        main.bind("<Up>", self.up_key) 
        main.bind("<Down>", self.down_key) 

    def load_font_config(self):
        from yaml import load, Loader
        fin = open("Master_config.yaml", "r")
        self.config = load(fin, Loader=Loader)
        fin.close()

    def save_font_config(self):
        from yaml import dump
        with open('Master_config.yaml', 'w') as f:
            dump(self.config, f)

    def save_placements(self):
        from subprocess import call
        call ("mkdir -p %s" % (self.language), shell=True)
        np.savetxt("%s/placements.txt" % self.language, self.df_pl, fmt="%d")

    def render(self):
        a = fill_poster("Sample_images/%05d" % self.my_image_number)
        a.convert(self.my_image_number, self.strings, self.placements, self.language, self.fonts)

        self.my_images = ImageTk.PhotoImage(Image.open("Final/Sample_images/%05d_%s.jpg" % (self.my_image_number, self.language) ))

        # change image
        self.canvas.itemconfig(self.image_on_canvas, image = self.my_images)

    def initialize_material(self):
        idx = (self.df.Image==self.my_image_number)
        self.strings = self.df[idx][self.language].values

        # String placements
        self.placements = self.df_pl[self.my_image_number-1]
        print(self.placements)
        print(self.strings)

        self.update_fonts()

    def update_fonts(self):
        # Fonts
        self.fonts = {}
        self.fonts["1"] = ImageFont.truetype(self.config[self.language]["font1"], size=self.config[self.language]["size1"])
        self.fonts["2"] = ImageFont.truetype(self.config[self.language]["font2"], size=self.config[self.language]["size2"])
        self.fonts["3"] = ImageFont.truetype(self.config[self.language]["font1"], size=self.config[self.language]["size3"])
        self.fonts["4"] = ImageFont.truetype(self.config[self.language]["font2"], size=self.config[self.language]["size4"])
        print(self.config[self.language])

        self.render()

    def up_key(self, event):
        self.step_value = 5

        self.df_pl[self.my_image_number-1][self.modify_string] = self.df_pl[self.my_image_number-1][self.modify_string] - self.step_value
        self.initialize_material()

    def down_key(self, event):
        self.step_value = 5

        self.df_pl[self.my_image_number-1][self.modify_string] = self.df_pl[self.my_image_number-1][self.modify_string] + self.step_value
        self.initialize_material()

    #----------------
    def nextImage(self):

        # next image
        self.my_image_number += 1

        try:
            self.my_images = ImageTk.PhotoImage(Image.open("Sample_images/%05d.jpg" % (self.my_image_number) ))
        except:
            self.my_image_number = 1
            self.my_images = ImageTk.PhotoImage(Image.open("Sample_images/%05d.jpg" % (self.my_image_number) ))

        # change image
        self.canvas.itemconfig(self.image_on_canvas, image = self.my_images)

        self.initialize_material()

    def write_configs(self):

        # Start out with Master_config.yaml
        self.save_font_config()

        # Next the placements file
        self.save_placements()

    def key_pressed(self, event):

        if event.char == "n":
            print("pressed")
            self.nextImage()

        # Choose string
        if event.char == "1" or event.char == "2" or event.char == "3" or event.char == "4" :
            self.modify_string = int(event.char)-1
        
        # Increase font size
        if event.char == "i":
            self.config[self.language]["size%d" % (self.modify_string + 1)]  += 1
            self.update_fonts()

        if event.char == "d":
            self.config[self.language]["size%d" % (self.modify_string + 1)]  -= 1
            self.update_fonts()

        if event.char == "l":
            self.df_pl[self.my_image_number-1][self.modify_string + len(self.strings)] += 1
            self.render()

        if event.char == "s":
            self.df_pl[self.my_image_number-1][self.modify_string + len(self.strings)] -= 1
            self.render()

        if event.char == "w":
            self.write_configs()

        if event.char == "q":
            self.write_configs()
            root.quit()

        return

#----------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    try:
        language = sys.argv[1]
    except:
        language = "Marathi"

    root = Tk()
    MainWindow(root, language=language)
    root.mainloop()
