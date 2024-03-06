import os
import tkinter as tk
from tkinter import scrolledtext as st
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import messagebox as ms

from environment.environment import Environment
from environment.ast import Ast
from parser.parser import Parser


class Frame(tk.Frame):

    def __init__(self, root=None):
        # Elementosde la app
        super().__init__(root, width=550, height=350)
        self.root = root
        self.pack()
        self.config(bg='black')

        # Functions
        self.actions()
        self.menu_bar()

        # Variables
        self.validate_open = False
        self.file_name = ""
        self.content = ''

    def actions(self):

        # self.boton_nuevo = tk.Button(self, text='Nuevo')
        # self.boton_nuevo.config(width=20, font=('Arial', 12, 'bold'), fg='#DAD5D6', bg='#138d75', cursor='hand2', activebackground='#3586df')
        # self.boton_nuevo.grid(row=0, column=0, padx=10, pady=10, columnspan=1)

        self.button_analyze = tk.Button(self, text='Analyze', command=self.action_analyze)
        self.button_analyze.config(width=12, font=('Arial', 12, 'bold'), fg='#DAD5D6', bg='#28b463', cursor='hand2', activebackground='#3586df')
        self.button_analyze.grid(row=0, column=0, padx=10, pady=10, columnspan=1)

        self.button_save = tk.Button(self, text='Save', command=self.save)
        self.button_save.config(width=12, font=('Arial', 12, 'bold'), fg='#DAD5D6', bg='#d4ac0d', cursor='hand2', activebackground='#35bd6f')
        self.button_save.grid(row=0, column=1, padx=10, pady=10, columnspan=1)

        self.button_errors = tk.Button(self, text='Errors', command=self.show_errors)
        self.button_errors.config(state='disabled', width=12, font=('Arial', 12, 'bold'), fg='#DAD5D6', bg='#cb4335', cursor='hand2', activebackground='#E15370')
        self.button_errors.grid(row=0, column=2, padx=10, pady=10, columnspan=1)

        self.button_symbols = tk.Button(self, text='Symbols', command=self.show_symbols)
        self.button_symbols.config(state='disabled', width=12, font=('Arial', 12, 'bold'), fg='#DAD5D6', bg='#ba4a00', cursor='hand2', activebackground='#E15370')
        self.button_symbols.grid(row=0, column=3, padx=10, pady=10, columnspan=1)

        # self.boton_nuevo.config(state='disabled')
        self.button_save.config(state='disabled')
        # self.boton_errores.config(state='disabled')

        self.title1 = tk.Label(self, text="EDITOR TEXT: ", font=('Arial', 12, 'bold'))
        self.title1.grid(row=1, column=0, columnspan=4)

        self.title2 = tk.Label(self, text="RESULTS: ", font=('Arial', 12, 'bold'))
        self.title2.grid(row=3, column=0, columnspan=4)

        self.scrolledtext1 = st.ScrolledText(self, width=80, height=20)
        self.scrolledtext1.grid(row=2, column=0, padx=10, pady=5, columnspan=5)

        self.scrolledtext2 = st.ScrolledText(self, width=80, height=20)
        self.scrolledtext2.grid(row=4, column=0, padx=10, pady=5, columnspan=5)

    def menu_bar(self):
        barra_menu = tk.Menu(self.root)
        self.root.config(menu=barra_menu, width=300, height=300)  # Anclando la barra de menu

        menu_inicio = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label='Archivo', menu=menu_inicio)

        menu_inicio.add_command(label='Abrir', command=self.open_file)
        menu_inicio.add_command(label='Nuevo', command=self.clean_editor)
        menu_inicio.add_command(label='Guardar Como...', command=self.save_as)
        menu_inicio.add_command(label='Salir', command=self.root.destroy)

        menu_ayuda = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label='Ayuda', menu=menu_ayuda)

        menu_ayuda.add_command(label='Info', command=self.help)

    def enabling(self):
        self.button_symbols.config(state='normal')
        self.button_errors.config(state='normal')
        self.button_save.config(state='normal')

    def save(self):
        archi1 = open(self.nombreArchivo, "w", encoding="utf-8")
        archi1.write(self.scrolledtext1.get("1.0", tk.END))
        self.content = self.scrolledtext1.get("1.0", tk.END)
        archi1.close()
        mb.showinfo("Información", "Los datos fueron guardados en el archivo")
        print(self.content)

    def open_file(self):
        nombrearch = fd.askopenfilename(initialdir="files_ocl/", title="Seleccione un archivo",filetypes=(("txt files","*.txt"),("todos los archivos","*.*")))
        self.file_name = nombrearch
        if nombrearch != '':
            archi1 = open(nombrearch, "r", encoding="utf-8")
            content = archi1.read() # Se lee de forma completa
            archi1.close()
            self.scrolledtext1.delete("1.0",tk.END)
            self.scrolledtext1.insert("1.0",content)
        self.validate_open = True
        self.enabling()
        self.scrolledtext2.delete("1.0", tk.END)

    def save_as(self):
        filename = fd.asksaveasfilename(initialdir="files_ocl/", title="Guardar como",filetypes=(("txt files","*.txt"),("todos los archivos","*.*")))
        if filename != '':
            archi1 = open(filename, "w", encoding="utf-8")
            archi1.write(self.scrolledtext1.get("1.0", tk.END))
            self.content = self.scrolledtext1.get("1.0", tk.END)
            archi1.close()
            mb.showinfo("Information","The data has been saved successfully.")
            print(self.content)
        self.scrolledtext2.delete("1.0", tk.END)

    def clean_editor(self):
        if self.validate_open:
            response = mb.askyesnocancel("Save Changes", "Do you want to save the changes before cleaning the editor?")
            if response is not None:
                if response:
                    self.save_as()
                self.scrolledtext1.delete("1.0", tk.END)
                self.content = ""
                self.validate_open = False
                self.file_name = ""
        else:
            self.scrolledtext1.delete("1.0", tk.END)
            self.content = ""
            self.file_name = ""
        self.scrolledtext2.delete("1.0", tk.END)

    def action_analyze(self):
        print('Analyze')
        input_data = self.scrolledtext1.get("1.0", tk.END)

        env_initial = Environment(None, 'GLOBAL')
        ast = Ast()
        parser = Parser()
        instructions_arr = parser.interpreter(input_data)
        for instruction in instructions_arr:
            instruction.execute(ast, env_initial)
        self.scrolledtext2.delete("1.0", tk.END)
        self.scrolledtext2.insert("1.0", ast.get_console())

    def show_symbols(self, console):
        print("Symbols")

        print(console)
        self.scrolledtext2.insert("1.0", console)


    def show_errors(self):
        print("Show Mongo xD")


    def help(self):
        ms.showinfo("Información del Programador",
                    "Nombre: Luis Eduardo De León Pacheco\nCarné: 202000959\nCurso: Lenguajes Formales y de Programación")