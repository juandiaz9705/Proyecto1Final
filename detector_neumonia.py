#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk, font, filedialog
from tkinter.messagebox import askokcancel, showinfo, WARNING
from PIL import ImageTk, Image
import csv
import tkcap
import time
import numpy as np
import os
import tensorflow as tf

# Definir la ruta relativa del modelo
model_path = os.path.join(os.getcwd(), "WilhemNet_86.h5")

# Cargar el modelo
try:
    model = tf.keras.models.load_model(model_path)
    print(f"Modelo cargado desde {model_path}")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    model = None

# -----------------------------
#   OWN SCRIPTS
import read_img
import integrator


class App():
    def __init__(self):
        self.root = Tk()
        self.root.title("Herramienta para la detección rápida de neumonía")

        # Setting up the style
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")

        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 12))
        self.style.configure('TButton', font=('Helvetica', 10, 'bold'), foreground='white', background='#007ACC')
        self.style.map('TButton', background=[('active', '#005f9e')])
        self.style.configure('TEntry', font=('Helvetica', 12))

        # Adjusting window size and position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 900
        window_height = 650
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)

        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.resizable(False, False)

        # Main Frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Title Label
        title_label = ttk.Label(main_frame, text="Software para el Apoyo al Diagnóstico Médico de Neumonía", font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Image Frames
        image_frame = ttk.Frame(main_frame)
        image_frame.grid(row=1, column=0, columnspan=2, pady=10)

        img1_frame = ttk.Frame(image_frame)
        img1_frame.grid(row=0, column=0, padx=20)
        self.lab1 = ttk.Label(img1_frame, text="Imagen Radiográfica")
        self.lab1.grid(row=0, column=0, pady=5)
        self.text_img1 = Text(img1_frame, width=40, height=15)
        self.text_img1.grid(row=1, column=0)

        img2_frame = ttk.Frame(image_frame)
        img2_frame.grid(row=0, column=1, padx=20)
        self.lab2 = ttk.Label(img2_frame, text="Imagen con Heatmap")
        self.lab2.grid(row=0, column=0, pady=5)
        self.text_img2 = Text(img2_frame, width=40, height=15)
        self.text_img2.grid(row=1, column=0)

        # Input and Result Frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.lab4 = ttk.Label(input_frame, text="Cédula Paciente:")
        self.lab4.grid(row=0, column=0, padx=5, pady=5, sticky=E)
        self.text1 = ttk.Entry(input_frame, width=20)
        self.text1.grid(row=0, column=1, padx=5, pady=5)

        self.lab3 = ttk.Label(input_frame, text="Resultado:")
        self.lab3.grid(row=1, column=0, padx=5, pady=5, sticky=E)
        self.text2 = Text(input_frame, width=20, height=1)
        self.text2.grid(row=1, column=1, padx=5, pady=5)

        self.lab6 = ttk.Label(input_frame, text="Probabilidad:")
        self.lab6.grid(row=2, column=0, padx=5, pady=5, sticky=E)
        self.text3 = Text(input_frame, width=20, height=1)
        self.text3.grid(row=2, column=1, padx=5, pady=5)

        # Buttons Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.button1 = ttk.Button(button_frame, text="Predecir", state='disabled', command=self.run_model)
        self.button1.grid(row=0, column=0, padx=10, pady=10)
        self.button2 = ttk.Button(button_frame, text="Cargar Imagen", command=self.load_img_file)
        self.button2.grid(row=0, column=1, padx=10, pady=10)
        self.button3 = ttk.Button(button_frame, text="Borrar", command=self.delete)
        self.button3.grid(row=0, column=2, padx=10, pady=10)
        self.button4 = ttk.Button(button_frame, text="PDF", command=self.create_pdf)
        self.button4.grid(row=0, column=3, padx=10, pady=10)
        self.button6 = ttk.Button(button_frame, text="Guardar", command=self.save_results_csv)
        self.button6.grid(row=0, column=4, padx=10, pady=10)

        # FOCUS ON PATIENT ID
        self.text1.focus_set()

        #  se reconoce como un elemento de la clase
        self.array = None

        # RUN LOOP
        self.root.mainloop()

    # METHODS
    def load_img_file(self):
        filepath = filedialog.askopenfilename(
            initialdir="/", 
            title="Select image", 
            filetypes=(('DICOM', '*.dcm'), ('JPEG', '*.jpeg'), ('JPG', '*.jpg'), ('PNG', '*.png'))
        )
        if filepath:
            file_ext = os.path.splitext(filepath)[1].lower()
            if file_ext == '.dcm':
                try:
                    self.array, img2show = read_img.read_dicom_file(filepath)
                    self.img1 = img2show.resize((250, 250), Image.LANCZOS)
                    self.img1 = ImageTk.PhotoImage(self.img1)
                    self.text_img1.image_create(END, image=self.img1)
                    self.button1['state'] = 'enabled'
                except pydicom.errors.InvalidDicomError:
                    showinfo(title='Error', message='El archivo DICOM no es válido.')
            elif file_ext in ['.jpeg', '.jpg', '.png']:
                img2show = Image.open(filepath)
                self.img1 = img2show.resize((250, 250), Image.LANCZOS)
                self.img1 = ImageTk.PhotoImage(self.img1)
                self.text_img1.image_create(END, image=self.img1)
                self.array = np.array(img2show)
                self.button1['state'] = 'enabled'
            else:
                showinfo(title='Error', message='Formato de archivo no soportado.')

    def run_model(self):
        self.label, self.proba, self.heatmap = integrator.predict(self.array)
        self.img2 = Image.fromarray(self.heatmap)
        self.img2 = self.img2.resize((250, 250), Image.LANCZOS)
        self.img2 = ImageTk.PhotoImage(self.img2)
        self.text_img2.image_create(END, image=self.img2)
        self.text2.insert(END, self.label)
        self.text3.insert(END, '{:.2f}'.format(self.proba) + '%')

    def save_results_csv(self):
        with open('historial.csv', 'a') as csvfile:
            w = csv.writer(csvfile, delimiter='-')
            w.writerow([self.text1.get(), self.label, '{:.2f}'.format(self.proba) + '%'])
            showinfo(title='Guardar', message='Los datos se guardaron con éxito.')

    def create_pdf(self):
        timestamp = int(time.time())
        ID = f'Reporte_{timestamp}.jpg'
        cap = tkcap.CAP(self.root)
        img = cap.capture(ID)
        img = Image.open(ID)
        img = img.convert('RGB')
        pdf_path = f'Reporte_{timestamp}.pdf'
        img.save(pdf_path)
        showinfo(title='PDF', message='El PDF fue generado con éxito.')

    def delete(self):
        answer = askokcancel(title='Confirmación', message='Se borrarán todos los datos.', icon=WARNING)
        if answer:
            self.text1.delete(0, 'end')
            self.text2.delete(1.0, 'end')
            self.text3.delete(1.0, 'end')
            self.text_img1.delete(1.0, 'end')
            self.text_img2.delete(1.0, 'end')
            self.button1['state'] = 'disabled'


if __name__ == "__main__":
    app = App()
