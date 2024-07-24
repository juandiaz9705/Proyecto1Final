
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk, font, filedialog, Entry
from tkinter.messagebox import askokcancel, showinfo, WARNING
import getpass
from PIL import ImageTk, Image
import csv
import pyautogui
import tkcap
import img2pdf
import numpy as np
# -----------------------------
#   OWN SCRIPTS
import IN_1
import integrator


class App():
    def __init__(self):
        self.root = Tk()
        self.root.title("Herramienta para la detección rápida de neumonía")

        #   BOLD FONT
        fonti = font.Font(weight='bold')

        self.root.geometry("815x560")        
        self.root.resizable(0,0)

        #   LABELS
        self.lab1 = ttk.Label(self.root, text="Imagen Radiográfica", font=fonti)
        self.lab2 = ttk.Label(self.root, text="Imagen con Heatmap", font=fonti)
        self.lab3 = ttk.Label(self.root, text="Resultado:", font=fonti)
        self.lab4 = ttk.Label(self.root, text="Paciente ID:", font=fonti)

        #   TWO STRING VARIABLES TO CONTAIN ID AND RESULT
        self.ID = StringVar()
        self.result = StringVar()

        #   TWO INPUT BOXES
        self.text1 = ttk.Entry(self.root, textvariable=self.ID, width=10)
        self.text2 = ttk.Entry(self.root, textvariable=self.result)

        #   GET ID
        self.ID_content = self.text1.get()
        print(self.ID_content)

        #   TWO IMAGE INPUT BOXES
        self.text_img1 = Text(self.root, width=31, height=15)
        self.text_img2 = Text(self.root, width=31, height=15)
        self.separator = ttk.Separator(self.root, orient=HORIZONTAL)

        #   BUTTONS
        self.button1 = ttk.Button(self.root, text="Predecir", command=self.run_model)
        self.button2 = ttk.Button(self.root, text="Cargar Imagen", command=self.load_img_file)
        self.button3 = ttk.Button(self.root, text="Limpiar", command=self.clean_up)
        self.button4 = ttk.Button(self.root, text="Imprimir", command=self.create_pdf)
        self.button6 = ttk.Button(self.root, text="Guardar", command=self.save_results_csv)

        #   WIDGETS POSITIONS   
        self.lab1.place(x=110, y=40)
        self.lab2.place(x=545, y=40)        
        self.lab3.place(x=500, y=350)
        self.lab4.place(x=65, y=350)
        self.button1.place(x=220, y=460)
        self.button2.place(x=70, y=460)
        self.button3.place(x=220, y=500)
        self.button4.place(x=70, y=500)
        self.button6.place(x=370, y=460)
        self.text1.place(x=200, y=350)
        self.text2.place(x=500, y=375, width=250, height=75)
        self.text_img1.place(x=65, y=80)
        self.text_img2.place(x=500, y=80)

        #   FOCUS ON PATIENT ID
        self.text1.focus_set()

        #  se reconoce como un elemento de la clase
        self.array = None 
        #self.proba = None

        #   MESSAGES
        #self.message1 = "El paciente " + str(self.ID_content) + "probabilidad de {:.2f}".format(self.proba)
        #self.message2 =

        #   RUN LOOP
        self.root.mainloop()  
        
    #   METHODS
    def load_img_file(self):
        filepath = filedialog.askopenfilename(initialdir="/", title="Select image", filetypes=(('DICOM','*.dcm'),('jpg files','*.jpg'),('png files','*.png')))
        if filepath:            
            self.array, img2show = IN_1.read_xray(filepath)
            self.img1 = img2show.resize((250,250), Image.ANTIALIAS)
            self.img1 = ImageTk.PhotoImage(self.img1)
            self.text_img1.image_create(END, image=self.img1)
            print(self.array.shape) #1024,1024
            print(self.array[0])

    def run_model(self):
        self.label, self.proba, self.heatmap = integrator.predict(self.array) 
        self.img2 = Image.fromarray(self.heatmap)#*255).astype(np.uint8))
        self.img2 = ImageTk.PhotoImage(self.img2)
        print('lo logro')
        self.text_img2.image_create(END, image=self.img2)
        if self.label == 'normal':
            self.message2 = "El paciente no presenta signos de neumonía con una probabilidad de {:.2f}".format(self.proba)+"%."
            self.text2.insert(END, self.message2)
        else:
            self.message1 = "El paciente ".format(self.ID) + "presenta neumonía " + self.label + " con una probabilidad de {:.2f}".format(self.proba)+"%."
            self.text2.insert(END, self.message1)
        #self.text2.insert(END, self.message2)
        print(self.label, self.proba) 
    
    def save_results_csv(self):
        with open('historial.csv', 'a') as f:
            w=csv.writer(f)
            w.writerow([self.text1.get(),self.text2.get()])
            showinfo(title='Guardar', message='Los datos se guardaron con éxito')

    def create_pdf(self):
        cap = tkcap.CAP(self.root)
        img = cap.capture('test2.jpg')
        img = Image.open('test2.jpg')
        img = img.convert('RGB')
        pdf_path = r'patient1.pdf'
        img.save(pdf_path)

    def clean_up(self):
        answer = askokcancel(title='Confirmación', message='Se borrarán todos los datos.', icon=WARNING)
        if answer:
            self.text1.delete(0, 'end')
            self.text2.delete(0, 'end')
            self.text_img1.delete(self.img1, 'end')
            self.text_img2.delete(self.img2, 'end')
            showinfo(title='Cancelar', message='Los datos se borraron con éxito')           

def main():
    my_app = App()
    return 0

if __name__ == '__main__':
    main()

