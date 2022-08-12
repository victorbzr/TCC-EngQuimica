import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class SalvarDados:
    def __init__(self,Resultados):
        files = [('Comma Separated Values', '*.csv'),
                 ('Excel', '*.xlsx')]
        path = tk.filedialog.asksaveasfilename(filetypes=files, defaultextension=files)
        if path[-3:] == "csv":
            Resultados.to_csv(path)
            tk.messagebox.showinfo(title=None, message='Resultados salvos em:\n' + path)
        elif path[-4:] == "xlsx":
            Resultados.to_excel(path, index=False, sheet_name="Resultados")
            tk.messagebox.showinfo(title=None, message='Resultados salvos em:\n' + path)
        else:
            tk.messagebox.showerror(title='Erro', message='Diretório não encontrado')