import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

class Pareto:
    def __init__(self, master, path, header):
        self.master = master
        self.path = path
        self.header = header
        self.master.title('Gráfico de Pareto')
        self.master.wm_iconbitmap('Imagens\Logo.ico')
        Labels_Title = tk.Label(self.master,
                                text='Selecione a coluna que contém\nos dados para plotagem do gráfico de Pareto:')
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

        Lab = tk.Label(self.master,text='Selecione a coluna que contém\na classe para plotagem do gráfico de Pareto:')
        Lab.grid(row=2)
        self.frame1 = tk.Frame(self.master)
        self.frame1.grid(row=3)
        self.CBcontents1 = {i: 0 for i in self.header}

        i = 0
        for h in self.CBcontents1:
            self.CBcontents1[h] = tk.IntVar()
            l = tk.Checkbutton(self.frame1, text=h, variable=self.CBcontents1[h], onvalue=1, offvalue=0,
                               activebackground='#ffffff', indicatoron='false').grid(row=0, column=i)
            i = i + 1


        Lab2 = tk.Label(self.master, text='Selecione o tipo de dado:').grid(row=4, column=0)
        self.frame2 = tk.Frame(self.master)
        self.frame2.grid(row=5)
        self.tipo1 = ["Contagem", "Porcentagem"]
        self.tkvar1 = tk.StringVar()
        self.tkvar1.set('Tipo de dado')  # set the default option

        self.PlotType1 = tk.OptionMenu(self.frame2, self.tkvar1, *self.tipo1).grid(row=0, column=0)

        b = tk.Button(self.master, text='Mostrar Resultados', command=lambda: self.Plot()).grid(row=6)

        self.master.mainloop()

    def Plot(self):
        plt.style.use('classic')
        try:
            dados = pd.read_csv(self.path)
        except:
            dados = pd.read_excel(self.path, engine='openpyxl')
            dados = dados.dropna(1, how='all')
            dados = dados.dropna(0, how='all')
        #criar novo dataframe
        classes=[]
        valores=[]
        for i in self.header:
            if self.CBcontents1[i].get() == 1:
                classes = dados[i].tolist()
        for i in self.header:
            if self.CBcontents[i].get() == 1:
                valores = dados[i].tolist()

        if self.tkvar1.get()=='Contagem':
            valores=[int(i) for i in valores]
            df = pd.DataFrame(columns=['Contagem'], index=classes)
            df['Contagem']=valores
            df = df.sort_values(by='Contagem', ascending=False)
            print(df)
            df["cumpercentage"] = df['Contagem'].cumsum() / df['Contagem'].sum() * 100
            fig, ax = plt.subplots()
            ax.bar(df.index, df['Contagem'], color="C0")
            plt.ylabel('Percentual', fontsize=14, color="blue")
            ax2 = ax.twinx()
            ax2.plot(df.index, df["cumpercentage"], color="C1", marker="D", ms=7)
            ax2.yaxis.set_major_formatter(PercentFormatter())
            ax.tick_params(axis="y", colors="C0")
            ax.tick_params(axis="x", labelrotation=-80)
            ax2.tick_params(axis="y", colors="C1")
            plt.ylabel('Percentual Acumulado', fontsize=14, color="green")
            plt.show()
        else:
            valores = [float(i) for i in valores]
            df = pd.DataFrame(columns=['Porcentagem'], index=classes)
            df['Porcentagem'] = valores
            df = df.sort_values(by='Porcentagem', ascending=False)
            print(df)
            df["cumpercentage"] = df['Porcentagem'].cumsum()
            fig, ax = plt.subplots()
            plt.title('Gráfico de Pareto', fontsize=14, fontweight="bold")
            ax.bar(df.index, df['Porcentagem'], color="C0")
            plt.ylabel('Percentual', fontsize=14, color="blue")
            ax2 = ax.twinx()
            ax2.plot(df.index, df["cumpercentage"], color="C1", marker="D", ms=7)
            ax2.yaxis.set_major_formatter(PercentFormatter())
            ax.tick_params(axis="y", colors="C0")
            ax.tick_params(axis="x", labelrotation=-80)
            ax2.tick_params(axis="y", colors="C1")
            plt.ylabel('Percentual Acumulado', fontsize=14, color="green")
            plt.show()

# root = tk.Tk()
# header = ["a","b"]
# path = "/"
# app=Histograma(root,path,header)