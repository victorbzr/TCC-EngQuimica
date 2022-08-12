import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt

class Histograma:
    def __init__(self, master, path, header):
        self.master = master
        self.path = path
        self.header = header
        self.master.title('Histograma')
        self.master.wm_iconbitmap('Imagens\Logo.ico')
        Labels_Title = tk.Label(self.master,
                                text='Selecione as colunas que contenham\nos dados para plotagem do histograma')
        Labels_Title.grid(row=0)
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=1)
        self.CBcontents = {i: 0 for i in self.header}

        i = 0
        for h in self.CBcontents:
            self.CBcontents[h] = tk.IntVar()
            l = tk.Checkbutton(self.frame, text=h, variable=self.CBcontents[h], onvalue=1, offvalue=0,
                               activebackground='#ffffff', indicatoron='false').grid(row=0, column=i)
            i = i + 1

        lopt = tk.Label(self.master, text='Selecione os parâmetros:').grid(row=6)

        self.frame2 = tk.Frame(self.master)
        self.frame2.grid(row=7)

        l1 = tk.Label(self.frame2, text='Número de grupos:').grid(row=1, column=0)
        self.var = tk.IntVar()
        self.var.set("0")
        self.e1 = tk.Entry(self.frame2, textvariable=self.var)
        self.e1.grid(row=1, column=1)

        l2 = tk.Label(self.frame2, text='Título eixo X:').grid(row=2, column=0)
        self.var1 = tk.StringVar()
        self.var1.set("")
        self.e2 = tk.Entry(self.frame2, textvariable=self.var1)
        self.e2.grid(row=2, column=1)

        l2 = tk.Label(self.frame2, text='Título eixo Y:').grid(row=3, column=0)
        self.var2 = tk.StringVar()
        self.var2.set("")
        self.e3 = tk.Entry(self.frame2, textvariable=self.var2)
        self.e3.grid(row=3, column=1)

        b = tk.Button(self.master, text='Mostrar Resultados', command=lambda: self.Plot(0)).grid(row=8)

        self.master.mainloop()

    def Plot(self,a):
        # import seaborn as sns
        #plt.style.use("seaborn-whitegrid") #https://matplotlib.org/3.2.2/tutorials/introductory/customizing.html
        #plt.style.use('ggplot') #veja qual estilo vc gosta mais.. a lista completa está no link acima
        plt.style.use('classic')
        import matplotlib.patches as mpatches
        # import numpy as np
        try:
            dados = pd.read_csv(self.path)
        except:
            dados = pd.read_excel(self.path, engine='openpyxl')
            dados = dados.dropna(1, how='all')
            dados = dados.dropna(0, how='all')
        #criar novo dataframe
        droplist = []
        for i in self.header:
            if not self.CBcontents[i].get() == 1:
                print(self.CBcontents[i].get())
                droplist.append(i)
        replicas = dados.drop(droplist, axis=1).copy()
        #transferir dados para coluna única no caso de dataframe com várias colunas
        aux = replicas.values.tolist()
        flat_list = pd.DataFrame([item for sublist in aux for item in sublist],columns=['Valores'])
        print(aux)
        print(flat_list)
        #calcular estatísticas
        MediaGlob = flat_list.mean()
        SigmaGlob = flat_list.std()
        MedianGlob = flat_list.median()
        #receber dados do usuário
        n_bins = self.var.get()
        xlabel = self.var1.get()
        ylabel = self.var2.get()
        #plotar histograma
        fig, ax = plt.subplots()
        x_max = flat_list["Valores"].max()
        x_min = flat_list["Valores"].min()
        delta = x_max - x_min
        ax.set_xlim(x_min - 0.1 * delta, x_max + 0.1 * delta)  # o delta é para o gráfico não ficar "grudado" nas barras
        plt.ylabel(ylabel, fontsize=14)
        plt.xlabel(xlabel, fontsize=14)
        plt.title('Histograma', fontsize=14, fontweight="bold")
        ax.hist(flat_list["Valores"], bins=n_bins, label='Valor Alvo', color="blue")
        # Tutorial em https://matplotlib.org/gallery/recipes/placing_text_boxes.html#sphx-glr-gallery-recipes-placing-text-boxes-py
        textstr = '\n'.join((
            r'$\mu=%.2f$' % (MediaGlob,),
            r'$\mathrm{Mediana}=%.2f$' % (MedianGlob,),
            r'$\sigma=%.2f$' % (SigmaGlob,)))
        # Propriedades da matplotlib.patch.Patch
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        # Coloca uma caixa de texto no topo esquerdo das coordenadas do gráfico
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
                verticalalignment='top', bbox=props)
        plt.show()

# root = tk.Tk()
# header = ["a","b"]
# path = "/"
# app=Histograma(root,path,header)