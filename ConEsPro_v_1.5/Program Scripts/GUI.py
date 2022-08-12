import tkinter as tk
from tkinter import messagebox
import Functions as func

class Menu_Principal:
    def __init__(self, master):
        self.master = master
        self.function = func.GUIFunctions('/')

        # File Name Label Update Var
        self.txt = tk.StringVar()
        self.txt.set("Nenhum arquivo selecionado")

        self.menubar = tk.Menu(master)
        self.master.config(menu= self.menubar)
        self.master.title('ConEsPro V_1.5')
        self.master.wm_iconbitmap('Imagens\Logo.ico')
        self.master.geometry('600x400')

        self.menu = tk.Menu(self.menubar)
        self.menu2 = tk.Menu(self.menubar)
        self.menu3 = tk.Menu(self.menubar)
        self.menu4 = tk.Menu(self.menubar)
        self.menu5 = tk.Menu(self.menubar)
        self.submenuTestNorm = tk.Menu(self.menubar)
        self.submenuCartVar = tk.Menu(self.menubar)
        self.submenuCartAtr = tk.Menu(self.menubar)
        self.submenuCartEsp = tk.Menu(self.menubar)

        self.menubar.add_cascade(label='Arquivo', menu=self.menu)
        self.menubar.add_cascade(label='Estatística Básica', menu=self.menu2)
        self.menu2.add_cascade(label='Testes de Normalidade',menu=self.submenuTestNorm)
        self.menubar.add_cascade(label='Ferramentas Gráficas', menu=self.menu3)
        self.menubar.add_cascade(label='Cartas de Controle', menu=self.menu4)
        self.menu4.add_cascade(label='Variáveis', menu=self.submenuCartVar)
        self.menu4.add_cascade(label='Atributos', menu=self.submenuCartAtr)
        self.menu4.add_cascade(label='Especiais', menu=self.submenuCartEsp)
        self.menubar.add_cascade(label='Ajuda', menu=self.menu5)

        self.menu.add_command(label='Abrir...', command=lambda:[self.frame.destroy(),self.function.Fileopen(self.txt)])
        self.menu.add_separator()
        self.menu.add_command(label='Sair', command=lambda:self.master.quit())
        self.menu3.add_command(label='Histograma', command=lambda:self.new_window(10))
        self.menu2.add_command(label='Diagrama de Pareto', command=lambda: self.new_window(11))
        self.menu2.add_command(label='Diagrama de Dispersão', command=lambda: self.new_window(12))
        self.submenuTestNorm.add_command(label='Anderson Darling', command=lambda:self.new_window(3))
        self.submenuTestNorm.add_command(label='Kolmogorov Smirnov', command=lambda: self.new_window(4))
        self.submenuTestNorm.add_command(label='Shapiro Wilk', command=lambda: self.new_window(5))
        self.menu3.add_command(label='Gráfico CUSUM', command=lambda: self.new_window(6))
        self.submenuCartAtr.add_command(label='Carta p', command=lambda: self.new_window(13))
        self.submenuCartAtr.add_command(label='Carta np', command=lambda: self.new_window(14))
        self.submenuCartAtr.add_command(label='Carta C', command=lambda:self.new_window(0))
        self.submenuCartAtr.add_command(label='Carta U', command=lambda: self.new_window(8))
        self.submenuCartVar.add_command(label=('Carta X\u0304'), command=lambda:self.new_window(1))
        self.submenuCartVar.add_command(label='Carta R', command=lambda:self.new_window(2))
        self.submenuCartEsp.add_command(label='Carta CUSUM Tabular', command=lambda: self.new_window(7))
        self.submenuCartEsp.add_command(label='Carta MMEP', command=lambda: self.new_window(9))
        self.menu5.add_command(label='Sobre', command=lambda:self.new_window(-1))

        # Labels
        self.Labels_FileName = tk.Label(self.master, textvariable=self.txt)
        self.Labels_FileName.pack()

        self.showbutton = tk.Button(self.master,text='Mostrar dados',command=self.ShowData)
        self.showbutton.pack()

        self.canvas = tk.Canvas(self.master, borderwidth=0)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)


    def ShowData(self):
        if not self.function.path == '/':
            self.frame = tk.Frame(self.canvas)
            self.frame.grid(row=2, column=0)
            self.vsb.pack(side="right", fill="y")
            self.canvas.pack(side="left", fill="both", expand=True)
            self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                      tags="self.frame")
            self.frame.bind("<Configure>", self.onFrameConfigure)

            columns = [str(a) for a in self.function.header]
            for i in range(len(self.function.lista)):
                for j in range(len(self.function.lista[i])):
                    columns[j] = columns[j] + '\n' + str(self.function.lista[i][j])

            for i in range(len(columns)):
                tk.Label(self.frame, text=columns[i]).grid(row=1, column=i)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def new_window(self, tipo):
        if self.function.path == "/" or self.function.path == "":
            messagebox.showwarning(title="Erro", message="Nenhum arquivo selecionado")
        else:
            self.newWindow = tk.Toplevel(self.master)
            self.function.runPlotMenu(tipo,self.newWindow)

    def close_windows(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    app = Menu_Principal(root)
    root.mainloop()

if __name__ == '__main__':
    main()