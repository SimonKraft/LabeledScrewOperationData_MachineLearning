from pathlib import Path
import os
import shutil
import time
import xmltodict
import json as js
import tkinter as tk
from tkinter import ttk
import time
from tkinter import *
import tkinter.font as tkFont
import tkinter.messagebox
import sys
from tkinter import filedialog
from tkinter.messagebox import showinfo
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from datetime import date
from os.path import join
import pyperclip as pc
import cv2 as cv
import matplotlib.image as mpimg
from PIL import Image, ImageTk


############################ FUNKTIONER ##################################

running = False
file_counter = 1

main_bg_color = "gray56"
stop_color = "red2"
start_color = "green1"

src_folder = ""
destination1 = ""

proces_type = ["N", "O", "U", "M", "MA", "MU", "L", "NA"]


def save_user_data():
    global src_folder
    global destination1
    if src_folder and destination1 != "":
        saved_userdata_folder = open("SavedUserdataFolder.txt", "w")
        saved_userdata_folder.write(f"{src_folder}\n")
        saved_userdata_folder.write(destination1)
        saved_userdata_folder.close()


def load_user_data():
    global src_folder
    global destination1
    if os.path.isfile("SavedUserdataFolder.txt"):
        with open("SavedUserdataFolder.txt") as saved_file:
            file_data = saved_file.readlines()
            src_folder = file_data[0].replace("\n", "")
            src_folder_label.config(text=src_folder)
            destination1 = file_data[1]
            destination1_label.config(text=destination1)
            saved_file.close()


def select_src_folder():
    global src_folder
    Chosen_folder = filedialog.askdirectory()
    if Chosen_folder != "":
        src_folder = Chosen_folder
        src_folder_label.config(text=src_folder)
    else:
        src_folder_label.config(text="you didnt click a search folder :(")


def converter():
    global file_counter
    global src_folder
    wood_number = wood_number_entry.get()
    screwing_type = screwing_type_entry.get()

    file_counter_label.config(text=f"Current Screw nr: {file_counter-1}")

    if running:
        # definerer mappen vi søger efter filer i
        # src_folder
        # definerer destinations mappen, som de konveterede filer skal ligge i
        # Tjekker om mapper til json- og kxml filerne er lavet. Hvis ikke laver den dem.
        check_dst_folder_json = os.path.isdir(
            destination1 + "/data_collection_json")
        check_dst_folder_kxml = os.path.isdir(
            destination1 + "/data_collection_kxml")

        check_dst_folder_pictures = os.path.isdir(destination1 + "/pictures/")  #Tjekker for mappen til billeder


        if check_dst_folder_json:
            dst_folder_json = destination1 + "/data_collection_json/"
        else:
            dst_folder_json = os.makedirs(
                destination1 + "/data_collection_json/")
            dst_folder_json = destination1 + "/data_collection_json/"

        if check_dst_folder_kxml:
            dst_folder_kxml = destination1 + "/data_collection_kxml/"
        else:
            dst_folder_kxml = os.makedirs(
                destination1 + "/data_collection_kxml/")
            dst_folder_kxml = destination1 + "/data_collection_kxml/"
        
        if check_dst_folder_pictures:                                       #Bruger mappen eller laver en mappe til billeder
            dst_folder_pictures = destination1 + "/pictures/"
        else:
            dst_folder_pictures = os.makedirs(
                destination1 + "/pictures/")
            dst_folder_pictures = destination1 + "/pictures/"

        # Tjekker om der er undermapper til de forskellige skruetyper.
        check_type_folder_json = os.path.isdir(dst_folder_json + screwing_type)
        check_type_folder_kxml = os.path.isdir(dst_folder_kxml + screwing_type)
        check_type_folder_pictures = os.path.isdir(dst_folder_pictures + screwing_type)

        if check_type_folder_json:
            sub_folder_json = dst_folder_json + screwing_type + "/"
        else:
            sub_folder_json = os.makedirs(
                dst_folder_json + screwing_type + "/")
            sub_folder_json = dst_folder_json + screwing_type + "/"

        if check_type_folder_kxml:
            sub_folder_kxml = dst_folder_kxml + screwing_type + "/"
        else:
            sub_folder_kxml = os.makedirs(
                dst_folder_kxml + screwing_type + "/")
            sub_folder_kxml = dst_folder_kxml + screwing_type + "/"

        if check_type_folder_pictures:
            sub_folder_pictures = dst_folder_pictures + screwing_type + "/"
        else:
            sub_folder_pictures = os.makedirs(
                dst_folder_pictures + screwing_type + "/")
            sub_folder_pictures = dst_folder_pictures + screwing_type + "/"


        # venter på at der kommer en fil ind som data som skal konverteres. Hvis ikke der er en fil, så venter den bare.
        if not os.listdir(src_folder):
            time.sleep(0.8)

        else:
            time.sleep(1)
            #Opretter en mappe hvor billederne til hver skrue skal gemmes
            folder_for_screw_pictures = os.makedirs(sub_folder_pictures + "/" + wood_number + "_" + str(file_counter) + "_" + str(date.today()) + "/")
            folder_for_screw_pictures = sub_folder_pictures + "/" + wood_number + "_" + str(file_counter) + "_" + str(date.today()) + "/"
            
            #Tager et billede så snart der er modtages en fil i search folderen
            cap1 = cv.VideoCapture(1, cv.CAP_DSHOW)
            cap2 = cv.VideoCapture(2, cv.CAP_DSHOW)
            path_picture1 = f"{folder_for_screw_pictures}picture_1.jpg"
            path_picture2 = f"{folder_for_screw_pictures}picture_2.jpg"
            ret, frame1 = cap1.read()
            ret, frame2 = cap2.read()
            cv.imwrite(path_picture1, frame1)
            cv.imwrite(path_picture2, frame2)
            cap1.release()
            cap2.release()


            #dst_folder_kxml = r"C:\Users\tobia\OneDrive - Aalborg Universitet\Aalborg Universitet\3. Semester\P3\test_for_app\data_collection_kxml\\"
            # laver en liste med fil navne i mappen, og en string med den første indgang i listen
            list = os.listdir(src_folder)
            file_name = str(list[0])
            #xmlpath = src_folder + "/" + file_name
            # HVIS DET UNDER GIVER FEJL, BRUG OVENSTÅENDE
            xmlpath = (src_folder + "/" + file_name)

            jsonpath = sub_folder_json + \
                f"{wood_number}_{file_counter}_{date.today()}"

            # Åbner xml filen og lagrer elementerne i et pythonobjekt
            with open(xmlpath, "r") as myfile:
                python_fil_objekt = xmltodict.parse(myfile.read())
                myfile.close()
            # Åbner en JSON fil og ligger den gemte data der i.
            with open(jsonpath + ".json", "w") as jsonfil:
                jsonfil.write(js.dumps(python_fil_objekt))
                jsonfil.close()
            # Flytter xml filen til en seperat mappe for at holde søge mappen tom

            new_name_kxml = wood_number + f"_{file_counter}_{date.today()}"
            file_counter += 1
            shutil.move(src_folder + "/" + file_name,
                        sub_folder_kxml + new_name_kxml)

    root.after(10, converter)


def stop_converter():
    global running
    running = False


def start_converter():
    global running

    wood_number = wood_number_entry.get()
    # måske slet, vi bruger vel drop down menu nu?
    screwing_type = screwing_type_entry.get().upper()

    if wood_number != "" and screwing_type != "":
        running = True
    
    else:
        running = False
        tkinter.messagebox.showinfo(
            title="Missing Values!", message="Input values are missing! Add 'Wood Number' and 'Screwing Type'")


def Status():
    if running:
        text_status = "Program Running"
        color_status = start_color
    else:
        text_status = "Program Off"
        color_status = stop_color
    status_label = tk.Label(collect_data, text=text_status, font=(
        "Arial", 15, "bold"), height=3, width=14, bg=color_status)
    status_label.place(x=1725, y=690)


def destination_selection():
    global destination1
    Chosen_folder = filedialog.askdirectory()
    if Chosen_folder != "":
        destination1 = Chosen_folder
        destination1_label.config(text=destination1)
    else:
        destination1_label.config(
            text="You didnt click a destination folder :(")


def sys_exit():
    sys.exit()


def check_password():
    password = '123'
    input = login_window_canvas_entry.get()

    if input == password:
        login_window.destroy()
    else:
        # laver en label der fortæller man har skrevet forkert password
        login_window_canvas_label = tk.Label(
            login_window, text="Wrong password, try again")
        login_window_canvas.create_window(
            login_width/2, 300, window=login_window_canvas_label)
        # sletter label efter 2 sek
        login_window_canvas_label.after(
            2000, login_window_canvas_label.destroy)


def clear_input():
    wood_number_entry.delete(0, END)
    screwing_type_entry.delete(0, END)
    start_offset_entry.delete(0, END)
    global file_counter
    file_counter = 1


def add_offset():
    global file_counter

    if start_offset_entry.get() != "" and int(start_offset_entry.get()) > 0:
        file_counter = int(start_offset_entry.get())
    else:
        file_counter = file_counter


def move_file():
    location_change = to_entry.get().upper()
    type_change = type_change_entry.get().upper()
    wood_number_change = wood_number_change_entry.get()
    screw_number_change = screw_number_change_entry.get()

    if location_change != "" and wood_number_change != "" and screw_number_change != "" and type_change != "":
        file_to_change_json = destination1 + \
            f"/data_collection_json/{type_change}/{wood_number_change}_{screw_number_change}_{date.today()}.json"
        dst_location_json = destination1 + \
            f"/data_collection_json/{location_change}/"
        file_to_change_kxml = destination1 + \
            f"/data_collection_kxml/{type_change}/{wood_number_change}_{screw_number_change}_{date.today()}"
        dst_location_kxml = destination1 + \
            f"/data_collection_kxml/{location_change}/"
        folder_to_change_pictures = destination1 + \
            f"/pictures/{type_change}/{wood_number_change}_{screw_number_change}_{date.today()}/"
        dst_location_pictures = destination1 + \
            f"/pictures/{location_change}/"

        check_file_to_change_json = os.path.isfile(file_to_change_json)

        if check_file_to_change_json:
            check_dst_location_json = os.path.isdir(
                destination1 + f"/data_collection_json/{location_change}/")
            check_dst_location_kxml = os.path.isdir(
                destination1 + f"/data_collection_kxml/{location_change}/")
            check_dst_location_pictures = os.path.isdir(destination1 + f"/pictures/{location_change}/")

            if check_dst_location_json:
                shutil.move(file_to_change_json, dst_location_json)
            else:
                os.makedirs(destination1 +
                            f"/data_collection_json/{location_change}/")
                #dst_location_json = destination1 + f"/data_collection_json/{location_change}/"
                shutil.move(file_to_change_json, dst_location_json)

            if check_dst_location_kxml:
                shutil.move(file_to_change_kxml, dst_location_kxml)
            else:
                os.makedirs(destination1 +
                            f"/data_collection_kxml/{location_change}/")
                #dst_location_kxml = destination1 + f"/data_collection_kxml/{location_change}/"
                shutil.move(file_to_change_kxml, dst_location_kxml)

            if check_dst_location_pictures:
                shutil.move(folder_to_change_pictures, dst_location_pictures)
            else:
                os.makedirs(destination1 + f"/pictures/{location_change}")
                shutil.move(folder_to_change_pictures, dst_location_pictures)

            to_entry.delete(0, END)
            type_change_entry.delete(0, END)
            wood_number_change_entry.delete(0, END)
            screw_number_change_entry.delete(0, END)
        else:
            tkinter.messagebox.showinfo(
                title="Missing file!", message="The file doesn't exist!")

    else:
        tkinter.messagebox.showinfo(
            title="Missing information!", message="All information about the file and location must be insert")


#Denne funktion kører når knappen for at vise billederne trykkes. 
def show_picture():
    selected_ting = vores_listebox.curselection()
    selected_fil = ",".join([vores_listebox.get(i) for i in selected_ting])

    if path_us == "" or selected_fil == "":
        tkinter.messagebox.showinfo(
                    title="Missing File!", message="A file must be selected!")
    else:  
        
        #Deler den valgte path ind i en liste med hver del som et element
        p = Path(path_us).parts

        #Bruger dette til at kunne bestemme hvilken mappe som er valgt ved at tage det sidste element i listen
        selected_folder = p[-1]

        #Tager den valgte json fil og fjerner .json for at få navnet på filen
        name_for_selected_file = os.path.splitext(selected_fil)[0]

        im1 = cv.imread(f"{destination1}/pictures/{selected_folder}/{name_for_selected_file}/picture_1.jpg")
        im2 = cv.imread(f"{destination1}/pictures/{selected_folder}/{name_for_selected_file}/picture_2.jpg")

        #Tilføjer en cirkel som sættes omkring skruen. 
        center_coordinates = (315,170)
        radius = 30
        color = (0, 0, 255)
        thickness = 3

        im1 = cv.circle(im1, center_coordinates, radius, color, thickness)
        im2 = cv.circle(im2, center_coordinates, radius, color, thickness)

        pictures = np.concatenate((im1, im2), axis=1)
        cv.imshow(f'{name_for_selected_file}', pictures)
        

   


############################TKINTER SETUP##################################
login_window = tk.Tk()
login_window.title("AWESOME DATA COLLECTOR PROGRAM")

login_width = 500
login_height = 500

login_window_canvas = tk.Canvas(
    login_window, width=login_width, height=login_height)
login_window_canvas.pack()

# Input felt på login skærm
login_window_canvas_entry = tk.Entry(login_window)
login_window_canvas.create_window(
    login_width/2, 200, window=login_window_canvas_entry)

# Knap på login skærm
login_window_canvas_button = tk.Button(text="LOGIN", command=check_password)
login_window_canvas.create_window(
    login_width/2, 250, window=login_window_canvas_button)
login_window.bind('<Return>', lambda event: check_password())

# gør så at luk knappen i login viduet lukker hele programmet
login_window.protocol("WM_DELETE_WINDOW", sys_exit)

login_window.mainloop()


# Hvis koden er godkedt lukker login-menuen og hovedmenuen for programmet starter.

##################### NOTEBOOK 1 ############################

root = tk.Tk()
root.title("AWESOME DATA COLLECTOR PROGRAM")
root.geometry("1920x1080")

my_notebook = ttk.Notebook(root)
my_notebook.pack()

collect_data = Frame(my_notebook, width=1920, height=1080, bg=main_bg_color)
inspect_data = Frame(my_notebook, width=1920, height=1080, bg=main_bg_color)


collect_data.pack(fill="both", expand=1)
inspect_data.pack(fill="both", expand=1)

# Her tilføjes de til notebooken med .add
my_notebook.add(collect_data, text="Collect Data")
my_notebook.add(inspect_data, text="Inspect Data")

# Start knap collect data
start_button = Button(collect_data, text="Start Collecting", bg=start_color, font=(
    "Arial", 15, "bold"), height=3, width=14, command=lambda: [start_converter(), Status(), add_offset(), save_user_data()])
start_button.place(x=1725, y=887)

# Luk knap gemmer data i fil inden luk
#root.protocol("WM_DELETE_WINDOW", command=lambda:[save_user_data(), sys_exit()])

stop_button = Button(collect_data, text="Stop Collecting", bg=stop_color, font=(
    "Arial", 15, "bold"), height=3, width=14, command=lambda: [stop_converter(), Status()])
stop_button.place(x=1725, y=787)

status_label = tk.Label(collect_data, text="Program off", font=(
    "Arial", 15, "bold"), height=3, width=14, bg=stop_color)
status_label.place(x=1725, y=690)

# Knap til at vælge destination folder
select_folder = Button(collect_data, text="Select \n destination folder", font=(
    "Arial", 15, "bold"), height=3, width=14, command=destination_selection)
select_folder.place(x=65, y=625)

destination1_label = tk.Label(collect_data, text="Missing destination folder", font=(
    "Arial", 10, "bold"), height=3, width=100,)
destination1_label.place(x=265, y=640)


# Stop knap collect data
# Titlen laves
title_data_converter = tk.Label(collect_data, text="Data Collector", font=(
    "Arial", 50), height=2, width=14, bg=main_bg_color)
title_data_converter.place(x=700, y=0)


# Wood number label + underline font
wood_number_label = tk.Label(collect_data, text="Wood number:", font=(
    "Arial", 18, "bold"), height=3, width=14, bg=main_bg_color)
wood_number_label.place(x=40, y=200)
font_underline = tkFont.Font(wood_number_label, wood_number_label.cget("font"))
font_underline.configure(underline=True)
wood_number_label.configure(font=font_underline)
# Wood number entry
wood_number_entry = tk.Entry(collect_data, width=20)
wood_number_entry.place(x=250, y=240)

# Screwing type label + underline font
screwing_type_label = tk.Label(collect_data, text="Screwing type:", font=(
    "Arial", 18, "bold"), height=3, width=14, bg=main_bg_color)
screwing_type_label.place(x=40, y=300)
screwing_type_label.configure(font=font_underline)
# Screwing type entry

screwing_type_entry = ttk.Combobox(
    collect_data, state="readonly", values=proces_type, width=17)
screwing_type_entry.place(x=250, y=340)

# screwing_type_entry = tk.Entry(collect_data, width=20)
# screwing_type_entry.place(x=250, y=340)

# Start offset label. Dette er til at starte ved en skrue som ikke er nr. 1
start_offset_label = tk.Label(collect_data, text="Start offset:", font=(
    "Arial", 18, "bold"), height=3, width=14, bg=main_bg_color)
start_offset_label.place(x=25, y=400)
start_offset_label.configure(font=font_underline)
# Start offset entry
start_offset_entry = tk.Entry(collect_data, width=20)
start_offset_entry.place(x=250, y=440)
# File counter text
file_counter_label = tk.Label(collect_data, text=f"Current Screw nr: {file_counter-1}", font=(
    "Arial", 12, "bold"), height=3, width=16, bg=main_bg_color)
file_counter_label.place(x=230, y=470)


# Laver reset knap til at nulstille input værdierne
reset_button = Button(collect_data, text="Reset values", font=(
    "Arial", 15, "bold"), height=3, width=14, command=clear_input)
reset_button.place(x=450, y=300)

# Knap til at vælge search folder:
src_folder_button = Button(collect_data, text="Select \n search folder", font=(
    "Arial", 15, "bold"), height=3, width=14, command=select_src_folder)
src_folder_button.place(x=65, y=725)
src_folder_label = tk.Label(collect_data, text="Missing search folder", font=(
    "Arial", 10, "bold"), height=3, width=100,)
src_folder_label.place(x=265, y=740)

load_user_data()
# Laver del som gør at en fil kan flyttes. Vi kulle lave alt tekst som clases!
# From label

from_label = tk.Label(collect_data, text="From:", font=(
    "Arial", 12, "bold"), height=3, width=14, bg=main_bg_color)
from_label.place(x=1200, y=217)
type_change_label = tk.Label(collect_data, text="Type:", font=(
    "Arial", 12, "bold"), height=3, width=15, bg=main_bg_color)
type_change_label.place(x=1300, y=195)
wood_number_change_label = tk.Label(collect_data, text="Wood nr:", font=(
    "Arial", 12, "bold"), height=3, width=15, bg=main_bg_color)
wood_number_change_label.place(x=1450, y=195)
screw_number_change_label = tk.Label(collect_data, text="Screw nr:", font=(
    "Arial", 12, "bold"), height=3, width=15, bg=main_bg_color)
screw_number_change_label.place(x=1600, y=195)

# type change entry
type_change_entry = ttk.Combobox(
    collect_data, state="readonly", values=proces_type, width=17)
type_change_entry.place(x=1325, y=240)


# wood number change entry
wood_number_change_entry = tk.Entry(collect_data, width=20)
wood_number_change_entry.place(x=1475, y=240)
# screw number change entry
screw_number_change_entry = tk.Entry(collect_data, width=20)
screw_number_change_entry.place(x=1625, y=240)

# To label
to_label = tk.Label(collect_data, text="To (location):", font=(
    "Arial", 12, "bold"), height=3, width=18, bg=main_bg_color)
to_label.place(x=1152, y=275)

# To entry
to_entry = ttk.Combobox(collect_data, state="readonly",
                        values=proces_type, width=17)
to_entry.place(x=1325, y=295)
# Laver reset knap til at flytte et datasæt værdierne
change_button = Button(collect_data, text="Move file", font=(
    "Arial", 15, "bold"), height=3, width=14, command=move_file)
change_button.place(x=1525, y=295)





######################################################### NOTEBOOK 2 ##########################################################
####### GUI program for graphs ###########

#### Scrollbar for the listbox #####
Myframe = Frame(inspect_data)
Myframe.pack(side=tk.LEFT, fill=Y)
#####Listbox#####
vores_listebox = Listbox(Myframe, width=22, height=40)
vores_listebox.pack(side=LEFT, expand=True)
Myframe.pack()


###### Button functions ######
path_us = ""


def vis_NS():
    vores_listebox.delete(0, END)
    # Husk at ændre mapper##
    global path_us
    path_us = destination1 + "/data_collection_json/N/"
    if os.path.isdir(path_us):
        for x in os.listdir(path_us):
            if x.endswith(".json"):
                vores_listebox.insert(END, x)
    else:
        vores_listebox.insert(END, "Files not found")
    if vores_listebox.size() == 0:
        vores_listebox.insert(END, "Folder is empty")



def vis_OS():
    vores_listebox.delete(0, END)
    global path_us
    path_us = destination1 + "/data_collection_json/O/"
    if os.path.isdir(path_us):
        for x in os.listdir(path_us):
            if x.endswith(".json"):
                vores_listebox.insert(END, x)
    # De NS;OS,US,MS skal ligge i hver sin mappe#
    else:
        vores_listebox.insert(END, "Files not found")
    if vores_listebox.size() == 0:
        vores_listebox.insert(END, "Folder is empty")


def vis_US():
    vores_listebox.delete(0, END)
    global path_us
    path_us = destination1 + "/data_collection_json/U/"
    if os.path.isdir(path_us):
        for x in os.listdir(path_us):
            if x.endswith(".json"):
                vores_listebox.insert(END, x)
    else:
        vores_listebox.insert(END, "Files not found")
    if vores_listebox.size() == 0:
        vores_listebox.insert(END, "Folder is empty")


def vis_MS():
    vores_listebox.delete(0, END)
    global path_us
    path_us = destination1 + "/data_collection_json/M/"
    if os.path.isdir(path_us):
        for x in os.listdir(path_us):
            if x.endswith(".json"):
                vores_listebox.insert(END, x)
    else:
        vores_listebox.insert(END, "Files not found")
    if vores_listebox.size() == 0:
        vores_listebox.insert(END, "Folder is empty")

def vis_LS():
    vores_listebox.delete(0, END)
    global path_us
    path_us = destination1 + "/data_collection_json/L/"
    if os.path.isdir(path_us):
        for x in os.listdir(path_us):
            if x.endswith(".json"):
                vores_listebox.insert(END, x)
    else:
        vores_listebox.insert(END, "Files not found")
    if vores_listebox.size() == 0:
        vores_listebox.insert(END, "Folder is empty")

def vis_MA():
    vores_listebox.delete(0, END)
    global path_us
    path_us = destination1 + "/data_collection_json/MA/"
    if os.path.isdir(path_us):
        for x in os.listdir(path_us):
            if x.endswith(".json"):
                vores_listebox.insert(END, x)
    else:
        vores_listebox.insert(END, "Files not found")
    if vores_listebox.size() == 0:
        vores_listebox.insert(END, "Folder is empty")

def vis_MU():
    vores_listebox.delete(0, END)
    global path_us
    path_us = destination1 + "/data_collection_json/MU/"
    if os.path.isdir(path_us):
        for x in os.listdir(path_us):
            if x.endswith(".json"):
                vores_listebox.insert(END, x)
    else:
        vores_listebox.insert(END, "Files not found")
    if vores_listebox.size() == 0:
        vores_listebox.insert(END, "Folder is empty")

def vis_NA():
    vores_listebox.delete(0, END)
    global path_us
    path_us = destination1 + "/data_collection_json/NA/"
    if os.path.isdir(path_us):
        for x in os.listdir(path_us):
            if x.endswith(".json"):
                vores_listebox.insert(END, x)
    else:
        vores_listebox.insert(END, "Files not found")
    if vores_listebox.size() == 0:
        vores_listebox.insert(END, "Folder is empty")

#### Buttons #####
button1 = Button(inspect_data,
                 text="N",
                 width=8,
                 height=2,
                 bg="white",
                 fg="black",
                 command=vis_NS
                 )
button1.place(x=5, y=10)

button2 = Button(inspect_data,
                 text="O",
                 width=8,
                 height=2,
                 bg="white",
                 fg="black",
                 command=vis_OS
                 )
button2.place(x=70, y=10)

button3 = Button(inspect_data,
                 text="U",
                 width=8,
                 height=2,
                 bg="white",
                 fg="black",
                 command=vis_US
                 )
button3.place(x=5, y=50)

button4 = Button(inspect_data,
                 text="M",
                 width=8,
                 height=2,
                 bg="white",
                 fg="black",
                 command=vis_MS
                 )
button4.place(x=70, y=50)

button5 = Button(inspect_data,
                 text="L",
                 width=8,
                 height=2,
                 bg="white",
                 fg="black",
                 command=vis_LS
                 )
button5.place(x=5, y=90)

button6 = Button(inspect_data,
                 text="MA",
                 width=8,
                 height=2,
                 bg="white",
                 fg="black",
                 command=vis_MA
                 )
button6.place(x=70, y=90)

button7 = Button(inspect_data,
                 text="MU",
                 width=8,
                 height=2,
                 bg="white",
                 fg="black",
                 command=vis_MU
                 )
button7.place(x=5, y=130)

button8 = Button(inspect_data,
                 text="NA",
                 width=8,
                 height=2,
                 bg="white",
                 fg="black",
                 command=vis_NA
                 )
button8.place(x=70, y=130)

##### Canvas ####
figure = plt.figure()
canvas = FigureCanvasTkAgg(figure, master=inspect_data)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


###### En fil bliver trykket #####


def items_selected(d):
    plt.clf()
    selected_indices = vores_listebox.curselection()                            #Der er noget kode her som kan fejle. Ved ikke hvorfor
    selected_json = ",".join([vores_listebox.get(i) for i in selected_indices]) #Fejlkode: open_json = js.load(open(full_file_path, "r"))
    full_file_path = path_us + selected_json                                    #PermissionError: [Errno 13] Permission denied: 'C:/Users/tobia/OneDrive - Aalborg Universitet/Aalborg Universitet/3. Semester/P3/test_for_app/data_collection_json/U/'
    if full_file_path.find("'") == True:
        full_file_path = full_file_path.replace("'", "")
    else:
        full_file_path = full_file_path
    
    open_json = js.load(open(full_file_path, "r"))                                  
    time = [open_json['XML_Data']
            ['Wsk3Vectors']['X_Axis']['Values']['float']]
    rpm = [open_json['XML_Data']['Wsk3Vectors']
           ['Y_AxesList']['AxisData'][0]['Values']['float']]
    torque = [open_json['XML_Data']['Wsk3Vectors']
              ['Y_AxesList']['AxisData'][1]['Values']['float']]
    current = [open_json['XML_Data']['Wsk3Vectors']
               ['Y_AxesList']['AxisData'][2]['Values']['float']]
    angle = [open_json['XML_Data']['Wsk3Vectors']
             ['Y_AxesList']['AxisData'][3]['Values']['float']]
    depth = [open_json['XML_Data']['Wsk3Vectors']
             ['Y_AxesList']['AxisData'][4]['Values']['float']]


####### Using Matlib.pyplot to plot 5 graphs ######
    plt.rcParams["figure.figsize"] = (7, 10)

    plt.subplot(5, 1, 1)
    plt.scatter(time, rpm, c="b", linewidths=2,
                marker=",", edgecolor="b", s=1, alpha=0.5)
    plt.title(selected_json)
    plt.gca().axes.xaxis.set_ticklabels([])
    plt.ylabel("RPM")
    plt.grid()

    plt.subplot(5, 1, 2)
    plt.scatter(time, torque, c="g", linewidths=1,
                marker=",", edgecolor="g", s=1, alpha=0.3)
    plt.gca().axes.xaxis.set_ticklabels([])
    plt.ylabel("Torque [Nm]")
    plt.grid()

    plt.subplot(5, 1, 3)
    plt.scatter(time, current, c="r", linewidths=2,
                marker=",", edgecolor="r", s=1, alpha=0.5)
    plt.gca().axes.xaxis.set_ticklabels([])
    plt.ylabel("Current [Amps]")
    plt.grid()

    plt.subplot(5, 1, 4)
    plt.scatter(time, angle, c="m", linewidths=2,
                marker=",", edgecolor="m", s=1, alpha=0.5)
    plt.gca().axes.xaxis.set_ticklabels([])
    plt.ylabel("Angle [RAD]")
    plt.grid()

    plt.subplot(5, 1, 5)
    plt.scatter(time, depth, c="c", linewidths=2,
                marker=",", edgecolor="c", s=1, alpha=0.5)
    plt.xlabel("Time [ms]")
    plt.ylabel("Depth [mm]")
    plt.grid()
    canvas.draw()
    root.geometry(f'{root.winfo_width()}x{root.winfo_height()}')

# Copy datapoints to clipboard


def CopyTorque():
    selected_indices = vores_listebox.curselection()
    selected_json = ",".join([vores_listebox.get(i) for i in selected_indices])
    full_file_path = path_us + selected_json
    if path_us == "" or selected_json == "":
        tkinter.messagebox.showinfo(
                    title="Missing File!", message="A file must be selected!")
    else:
        open_json = js.load(open(full_file_path, "r"))
        torque = [open_json['XML_Data']['Wsk3Vectors']
                ['Y_AxesList']['AxisData'][1]['Values']['float']]
        torque_string = "".join(str(e) for e in torque)
        pc.copy(torque_string)


def CopyRPM():
    selected_indices = vores_listebox.curselection()
    selected_json = ",".join([vores_listebox.get(i) for i in selected_indices])
    full_file_path = path_us + selected_json
    if path_us == "" or selected_json == "":
        tkinter.messagebox.showinfo(
                    title="Missing File!", message="A file must be selected!")
    else:
        open_json = js.load(open(full_file_path, "r"))
        rpm = [open_json['XML_Data']['Wsk3Vectors']
            ['Y_AxesList']['AxisData'][0]['Values']['float']]
        RPM_string = "".join(str(e) for e in rpm)
        pc.copy(RPM_string)


def CopyCurrent():
    selected_indices = vores_listebox.curselection()
    selected_json = ",".join([vores_listebox.get(i) for i in selected_indices])
    full_file_path = path_us + selected_json
    if path_us == "" or selected_json == "":
        tkinter.messagebox.showinfo(
                    title="Missing File!", message="A file must be selected!")
    else:
        open_json = js.load(open(full_file_path, "r"))
        current = [open_json['XML_Data']['Wsk3Vectors']
                ['Y_AxesList']['AxisData'][2]['Values']['float']]
        Current_string = "".join(str(e) for e in current)
        pc.copy(Current_string)


def CopyAngle():
    selected_indices = vores_listebox.curselection()
    selected_json = ",".join([vores_listebox.get(i) for i in selected_indices])
    full_file_path = path_us + selected_json
    if path_us == "" or selected_json == "":
        tkinter.messagebox.showinfo(
                    title="Missing File!", message="A file must be selected!")
    else:
        open_json = js.load(open(full_file_path, "r"))
        angle = [open_json['XML_Data']['Wsk3Vectors']
                ['Y_AxesList']['AxisData'][3]['Values']['float']]
        Angle_string = "".join(str(e) for e in angle)
        pc.copy(Angle_string)


def CopyDepth():
    selected_indices = vores_listebox.curselection()
    selected_json = ",".join([vores_listebox.get(i) for i in selected_indices])
    full_file_path = path_us + selected_json
    if path_us == "" or selected_json == "":
        tkinter.messagebox.showinfo(
                    title="Missing File!", message="A file must be selected!")
    else:
        open_json = js.load(open(full_file_path, "r"))
        depth = [open_json['XML_Data']['Wsk3Vectors']
                ['Y_AxesList']['AxisData'][4]['Values']['float']]
        Depth_string = "".join(str(e) for e in depth)
        pc.copy(Depth_string)
# knap til at kopiere


CopyRPMButton = Button(inspect_data,
                       text="Copy RPM data",
                       width=15,
                       height=2,
                       bg="white",
                       fg="black",
                       command=CopyRPM
                       )
CopyRPMButton.place(x=1750, y=175)

CopyTorqueButton = Button(inspect_data,
                          text="Copy torque data",
                          width=15,
                          height=2,
                          bg="white",
                          fg="black",
                          command=CopyTorque
                          )
CopyTorqueButton.place(x=1750, y=340)

CopyCurrentButton = Button(inspect_data,
                           text="Copy current data",
                           width=15,
                           height=2,
                           bg="white",
                           fg="black",
                           command=CopyCurrent
                           )
CopyCurrentButton.place(x=1750, y=505)

CopyAngleButton = Button(inspect_data,
                         text="Copy angle data",
                         width=15,
                         height=2,
                         bg="white",
                         fg="black",
                         command=CopyAngle
                         )
CopyAngleButton.place(x=1750, y=670)

CopyDepthButton = Button(inspect_data,
                         text="Copy depth data",
                         width=15,
                         height=2,
                         bg="white",
                         fg="black",
                         command=CopyDepth
                         )
CopyDepthButton.place(x=1750, y=835)

FileFormatLabel = Label(
    inspect_data, text="The format of the JSON files is: Woodnumber_Screwnumber_Date", font=("Arial", 12, "bold"), height=3, bg=main_bg_color)
FileFormatLabel.place(x=800, y=25)

#Laver knappen til at vise billederne fra skrueningen
show_pictures_button = Button(inspect_data,
                       text="Show Pictures",
                       width=15,
                       height=2,
                       bg="white",
                       fg="black",
                       command=show_picture
                       )
show_pictures_button.place(x=1750, y=50)


vores_listebox.bind('<<ListboxSelect>>', items_selected)

root.protocol("WM_DELETE_WINDOW", sys_exit)

root.after(1000, converter)
root.mainloop()
